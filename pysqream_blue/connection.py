from pysqream_blue.logger import *
import grpc
from pysqream_blue.globals import auth_services, auth_messages, qh_services, qh_messages, cl_messages
import time
import socket
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

    def connect_database(self, database: str, username: str, password: str, tenant_id: str, service: str):
        """Authentication and token receipt"""

        self.database, self.username, self.password, self.tenant_id, self.service = database, username, password, tenant_id, service

        if self.session_opened:
            ''' user should not reconnect before closing the previous connection'''
            log_and_raise(ProgrammingError, "Trying to connect to a database that's already connected")
        if not self.connected:
            self._connect_to_server()

        try:
            auth_response: auth_messages.AuthResponse = self.auth_stub.Auth(auth_messages.AuthRequest(
                user=self.username,
                password=self.password,
                tenant_id=self.tenant_id,
                database=self.database,
                source_ip=socket.gethostbyname(socket.gethostname()),
                client_info = cl_messages.ClientInfo(version='PySQream2_V_111')))
            self.token, self.token_type, self.context_id = auth_response.token, auth_response.token_type, auth_response.context_id
            self.expiration_time = auth_response.exp_time + time.time() * 1000
            self.call_credentialds = grpc.access_token_call_credentials(self.token)
        except grpc.RpcError as rpc_error:
            log_and_raise(ProgrammingError, f'Error from grpc while attempting to open database connection.\n{rpc_error}')
        if auth_response.HasField('error'):
            log_and_raise(OperationalError, f'Error while attempting to open database connection.\n{auth_response.error}')

        self.session_opened = True
        log_info(f'''Connection opened to database {database}. username: {self.username}.
                    The connection will be valid for {auth_response.exp_time / 1000} seconds.''')

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

        try:
            close_response: qh_messages.CloseResponse = self.client.CloseSession(
                qh_messages.CloseSessionRequest(close_request=qh_messages.CloseRequest(context_id=self.context_id)),
                credentials=self.call_credentialds if self.use_ssl else None
            ).close_response
        except grpc.RpcError as rpc_error:
            log_error(f'Error from grpc while attempting to close database connection.\n{rpc_error}')
            return
        if close_response.HasField('error'):
            log_error(f'Error while attempting to close database connection.\n{close_response.error}')
            return

        self.session_opened = False
        log_info(f'Connection closed to database {self.database}.')

    def _verify_open(self):
        """Verify that connection still open, reconnect if not."""
        if not self.connected:
            log_and_raise(ProgrammingError, 'The connection to the server has been closed')
        # TODO if channel or stub are not connected (how to check that?) reconnect

        if not self.session_opened:
            log_and_raise(ProgrammingError, 'Session has been closed')
        if self.expiration_time - time.time() * 1000 < 10000:
            self.session_opened = False
            self.connect_database(self.database, self.username, self.password, self.tenant_id, self.service)

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
