import logging
from pysqream_blue.utils import NotSupportedError, ProgrammingError, InternalError, IntegrityError, OperationalError, DataError, \
    DatabaseError, InterfaceError, Warning, Error

logger = logging.getLogger("dbapi_logger")
logger.setLevel(logging.DEBUG)
logger.disabled = True


def start_logging(log_path=None):
    log_path = log_path or '/tmp/sqream_dbapi.log'
    logger.disabled = False
    try:
        handler = logging.FileHandler(log_path)
    except Exception as e:
        raise Exception("Bad log path was given, please verify path is valid and no forbidden characters were used")

    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    return logger


def stop_logging():
    logger.handlers = []
    logger.disabled = True


def log_and_raise(exception_type: [NotSupportedError, ProgrammingError, InternalError,
                                   IntegrityError, OperationalError, DataError,
                                   DatabaseError, InterfaceError, Warning, Error], error_msg: str):
    if logger.isEnabledFor(logging.ERROR):
        logger.error(error_msg, exc_info=True)

    raise exception_type(error_msg)


def log_info(message: str):
    if logger.isEnabledFor(logging.INFO):
        logger.info(message)


def log_error(message: str):
    if logger.isEnabledFor(logging.ERROR):
        logger.error(message)


def log_warning(message: str):
    if logger.isEnabledFor(logging.WARNING):
        logger.warning(message)