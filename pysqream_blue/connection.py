from pysqream_blue.logger import *
import grpc
from pysqream_blue.globals import auth_services, auth_messages, qh_services, qh_messages, cl_messages, auth_type_messages
import time
import socket
from pysqream_blue.utils import is_token_expired
from pysqream_blue.cursor import Cursor


class Connection:
    ''' Connection class used to interact with SQream '''

    def __init__(self, host: str, port: str, use_ssl: bool = True, log = False, is_base_connection: bool = True,
                 reconnect_attempts : int = 10, reconnect_interval : int = 3, query_timeout: int = 0):
        self.host, self.port, self.use_ssl = host, port, use_ssl
        # Product want to connect with SSL
        self.use_ssl = True
        self.is_base_connection = is_base_connection
        self.reconnect_attempts, self.reconnect_interval = reconnect_attempts, reconnect_interval
        self.connected = False
        self.session_opened = False
        self.statement_opened = False
        self.query_timeout = query_timeout

        self.is_base_connection = is_base_connection
        if is_base_connection:
            self.cursors = []
            self._connect_to_server()

        if log is not False:
            start_logging(None if log is True else log)

    def __del__(self):
        self._disconnect_server()

    def _connect_to_server(self):
        ''' open grpc chanel and stubs '''
        if self.connected:
            log_and_raise(ProgrammingError, "Trying to connect to a server that's already connected")

        try_connect_num = 0
        while True:
            try:
                options = [('grpc.max_message_length', 1024 ** 3), ('grpc.max_receive_message_length', 1024 ** 3)]
                if self.use_ssl:
                    options.append(("grpc.enable_http_proxy", 0))
                    self.channel = grpc.secure_channel(f'{self.host}:{self.port}', grpc.ssl_channel_credentials(), options=options)
                else:
                    self.channel = grpc.insecure_channel(f'{self.host}:{self.port}', options=options)
                self.auth_stub = auth_services.AuthenticationServiceStub(self.channel)
                self.client    = qh_services.QueryHandlerServiceStub(self.channel)
                break
            except grpc.RpcError as rpc_error:
                try_connect_num += 1
                if try_connect_num < self.reconnect_attempts:
                    log_error \
                        (f'Error from grpc while attempting to connect to server.\n{rpc_error}\ntrying to reconnect.')
                    time.sleep(self.reconnect_interval)
                else:
                    log_and_raise(ProgrammingError, f'Error from grpc while attempting to connect to server.\n{rpc_error}')

        self.connected = True
        log_info(f'Connection opened to the server at: {self.host}:{self.port}.')

    def _disconnect_server(self):
        """close grpc chanel and stubs"""
        if not self.connected:
            log_warning("Trying to close a connection that's already closed")
            return
        if self.session_opened:
            self.close()
        try:
            if self.is_base_connection:
                """close channel only in the base connection because cursors use the same channel from base"""
                self.channel.close()
        except grpc.RpcError as rpc_error:
            log_error(f'Error from grpc while attempting to disconnect from server.\n{rpc_error}')
            return

        self.connected = False
        log_info(f'Connection closed to the server at: {self.host}:{self.port}.')

    def connect_database(self, database: str, username: str, password: str, tenant_id: str, service: str,
                         access_token: str):
        """Authentication and token receipt"""

        self.database, self.username, self.password, self.tenant_id, self.service, self.access_token = \
            database, username, password, tenant_id, service, access_token

        if self.session_opened:
            ''' user should not reconnect before closing the previous connection'''
            log_and_raise(ProgrammingError, "Trying to connect to a database that's already connected")
        if not self.connected:
            self._connect_to_server()

        auth_response: auth_messages.AuthResponse = None
        session_response: auth_messages.SessionResponse = None
        try:
            print(self.access_token)
            if self.access_token is None:
                auth_response = self.auth_user_password()
            else:
                auth_response = self.auth_access_token()
        except grpc.RpcError as rpc_error:
            log_and_raise(ProgrammingError,
                          f'Error from grpc while attempting to open database connection.\n{rpc_error}')

        if auth_response.HasField('error'):
            log_and_raise(OperationalError,
                          f'Error while attempting to open database connection.\n{auth_response.error}')

        try:
            self.token = auth_response.token
            session_response = self.open_session()
        except grpc.RpcError as rpc_error:
            log_and_raise(ProgrammingError,
                          f'Error from grpc while attempting to open database connection.\n{rpc_error}')

            if is_token_expired(str(rpc_error)):
                auth_response = self.auth_access_token()
                self.token = auth_response.token
                session_response = self.open_session()

        if session_response.HasField('error'):
            log_and_raise(OperationalError,
                          f'Error while attempting to open database connection.\n{session_response.error}')

        self.context_id, self.sqream_version = session_response.context_id, session_response.sqream_version
        # hour = 1 * 60 * 60 * 1000
        # self.expiration_time = hour + time.time() * 1000
        self.call_credentialds = grpc.access_token_call_credentials(self.token)
        self.session_opened = True
        log_info(f'''Connection opened to database {database}. username: {self.username}.''')

    def open_session(self):
        session_response: auth_messages.SessionResponse = self.auth_stub.Session(auth_messages.SessionRequest(
            tenant_id=self.tenant_id,
            database=self.database,
            source_ip=socket.gethostbyname(socket.gethostname()),
            client_info=cl_messages.ClientInfo(version='PySQream2_V_111')
        ), credentials=grpc.access_token_call_credentials(self.token))
        return session_response

    def auth_user_password(self) -> auth_messages.AuthResponse:
        return self.auth_stub.Auth(auth_messages.AuthRequest(
            auth_type=auth_type_messages.AUTHENTICATION_TYPE_INTERNAL,
            user=self.username,
            password=self.password
        ))

    def auth_access_token(self) -> auth_messages.AuthResponse:
        return self.auth_stub.Auth(auth_messages.AuthRequest(
            auth_type=auth_type_messages.AUTHENTICATION_TYPE_IDP,
            access_token=self.access_token
        ))

    def close_connection(self):
        self.close()

    def close(self):
        """Disconnect from database. the connection to the server remains open."""
        if not self.session_opened:
            log_warning("Trying to close a session that's already closed")
            return

        if self.is_base_connection:
            for cursor in self.cursors:
                if cursor.statement_opened:
                    cursor.close()

        close_response: qh_messages.CloseResponse = None
        try:
            close_response: qh_messages.CloseResponse = self._close()
        except grpc.RpcError as rpc_error:
            log_error(f'Error from grpc while attempting to close database connection.\n{rpc_error}')

            if is_token_expired(str(rpc_error)):
                auth_response = self.auth_access_token()
                self.token = auth_response.token
                close_response: qh_messages.CloseResponse = self._close()

        if close_response.HasField('error'):
            log_error(f'Error while attempting to close database connection.\n{close_response.error}')

        self.session_opened = False
        log_info(f'Connection closed to database {self.database}.')

    def _close(self):
        return self.client.CloseSession(
                qh_messages.CloseSessionRequest(close_request=qh_messages.CloseRequest(context_id=self.context_id)),
                credentials=self.call_credentialds if self.use_ssl else None
            ).close_response

    def _verify_open(self):
        """Verify that connection still open, reconnect if not."""
        if not self.connected:
            log_and_raise(ProgrammingError, 'The connection to the server has been closed')
        # TODO if channel or stub are not connected (how to check that?) reconnect

        if not self.session_opened:
            log_and_raise(ProgrammingError, 'Session has been closed')
        # if self.expiration_time - time.time() * 1000 < 10000:
        #     self.session_opened = False
        #     self.connect_database(self.database, self.username, self.password, self.tenant_id, self.service, self.access_token)

    def commit(self):
        return None
        # self._verify_open()

    def rollback(self):
        return None

    def cursor(self):
        """Return a new connection with the same parameters.
            We use a connection as the equivalent of a 'cursor'
            The cursor uses the same grpc chuannel and stubs
            but different session (authentication / token)"""

        self._verify_open()
        cur = Cursor(self.client, self.context_id, self.query_timeout, self.call_credentialds, self.use_ssl)
        self.cursors.append(cur)
        return cur
