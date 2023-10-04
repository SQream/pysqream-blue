import logging
from enum import Enum
import sys
from pysqream_blue.utils import NotSupportedError, ProgrammingError, InternalError, IntegrityError, OperationalError, DataError, \
    DatabaseError, InterfaceError, Warning, Error


class LogLevel(Enum):
    INFO = logging.INFO
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    CRITICAL = logging.CRITICAL


log_level_str_to_enum = {
    'INFO': LogLevel.INFO,
    'ERROR': LogLevel.ERROR,
    'DEBUG': LogLevel.DEBUG,
    'WARNING': LogLevel.WARNING,
    'CRITICAL': LogLevel.CRITICAL
}


class Logs:

    def __init__(self, module_name):
        self.logger = logging.getLogger(module_name)
        self.log_path = None
        self.logger.disabled = True
        self.level = None
        self.info = logging.INFO
        self.error = logging.ERROR
        self.debug = logging.DEBUG
        self.warning = logging.WARNING
        self.critical = logging.CRITICAL
        self.start = False
        self.file_handler = None

    def __del__(self):
        if self.start:
            self.stop_logging()

    def set_level(self, level):
        self.level = level

    def set_log_path(self, log_path=None):
        self.log_path = log_path if log_path else self.log_path
        try:
            self.file_handler = logging.FileHandler(self.log_path)
        except Exception as e:
            raise Exception(
                f"Bad log path was given, please verify path is valid and no forbidden characters were used {e}")

    def start_logging(self, module_name):
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(self.level.value)
        self.logger.disabled = False
        logging.addLevelName(self.level.value, self.level.name)
        self.file_handler.setLevel(self.level.value)
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))
        self.logger.addHandler(self.file_handler)
        self.start = True
        return self.logger

    def stop_logging(self):
        self.logger.disabled = True
        self.logger.handlers = []
        if self.file_handler:
            self.file_handler.close()

    def log_and_raise(self, exception_type: [NotSupportedError, ProgrammingError, InternalError,
                                       IntegrityError, OperationalError, DataError,
                                       DatabaseError, InterfaceError, Warning, Error], error_msg: str):
        if self.logger.isEnabledFor(logging.ERROR):
            self.logger.error(error_msg, exc_info=True)

        raise exception_type(error_msg)

    def message(self, message: str, level: [logging.INFO, logging.DEBUG, logging.WARNING, logging.ERROR,
                                            logging.CRITICAL]):
        if self.logger.isEnabledFor(level):
            self.logger.log(level, message)