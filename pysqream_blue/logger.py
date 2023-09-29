import logging
from pysqream_blue.utils import NotSupportedError, ProgrammingError, InternalError, IntegrityError, OperationalError, DataError, \
    DatabaseError, InterfaceError, Warning, Error


class Logs:

    def __init__(self):
        self.logger = logging.getLogger("dbapi_logger")
        self.log_path = '/var/log/sqream_dbapi.log'
        # self.log_path = '/Users/danielg/sqream_dbapi.log'
        self.logger.disabled = True
        self.level = None
        self.info = logging.INFO
        self.error = logging.ERROR
        self.debug = logging.DEBUG
        self.warning = logging.WARNING
        self.start = False

    def __del__(self):
        self.stop_logging()

    def set_level(self, level):
        self.level = level

    def set_log_path(self, log_path=None):
        log_path = log_path if log_path else self.log_path
        try:
            self.handler = logging.FileHandler(log_path)
        except Exception as e:
            raise Exception(
                f"Bad log path was given, please verify path is valid and no forbidden characters were used {e}")

    def start_logging(self):
        self.logger.disabled = False
        self.handler.setLevel(self.level)
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.handler)
        self.start = True
        return self.logger

    def stop_logging(self):
        self.logger.handlers = []
        self.logger.disabled = True
        self.handler.close()

    def log_and_raise(self, exception_type: [NotSupportedError, ProgrammingError, InternalError,
                                       IntegrityError, OperationalError, DataError,
                                       DatabaseError, InterfaceError, Warning, Error], error_msg: str):
        if self.logger.isEnabledFor(logging.ERROR):
            self.logger.error(error_msg, exc_info=True)

        raise exception_type(error_msg)

    def message(self, message: str, level: [logging.INFO, logging.DEBUG, logging.WARNING, logging.ERROR]):
        if self.logger.isEnabledFor(level):
            self.logger.info(message)

    # def log_info(self, message: str):
    #     if self.logger.isEnabledFor(logging.INFO):
    #         self.logger.info(message)
    #
    # def log_error(self, message: str):
    #     if self.logger.isEnabledFor(logging.ERROR):
    #         self.logger.error(message)
    #
    # def log_warning(self, message: str):
    #     if self.logger.isEnabledFor(logging.WARNING):
    #         self.logger.warning(message)