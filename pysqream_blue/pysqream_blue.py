#!/usr/bin/env python3

# import os
# os.environ['GRPC_TRACE'] = 'all'
# os.environ['GRPC_VERBOSITY'] = 'DEBUG'
import time
from datetime import datetime, date, time as t
from pysqream_blue.connection import Connection
from pysqream_blue.logger import Logs, log_level_str_to_enum

logs = Logs(__name__)


def connect(host:      str,
            port:      str =  '443',
            use_ssl:   bool = True,
            use_logs:  bool = False,
            database:  str =  'master',
            username:  str =  'sqream',
            password:  str =  'sqream',
            tenant_id: str =  'tenant',
            service:   str =  'sqream',
            access_token: str = None,
            reconnect_attempts : int = 10,
            reconnect_interval : int = 3,
            query_timeout      : int = 0,
            pool_name: str = None,
            log_level: str = 'INFO',
            source_type: str = "EXTERNAL"
            ) -> Connection:
    ''' Connect to SQream database '''

    if use_logs:
        if logs.log_path is None:
            raise ValueError("Please set log path to save the log using pysqream_blue.set_log_path('PATH') before "
                             "connecting to DB")

        if log_level.upper() not in log_level_str_to_enum.keys():
            raise ValueError(f"Please choose the correct log level = [{log_level_str_to_enum.keys()}]")

        logs.set_level(log_level_str_to_enum[log_level.upper()])

    conn = Connection(host, port, logs, use_ssl=use_ssl, is_base_connection=True, reconnect_attempts=reconnect_attempts,
                      reconnect_interval=reconnect_interval, query_timeout=query_timeout, pool_name=pool_name,
                      use_logs=use_logs, source_type=source_type)
    conn.connect_database(database, username, password, tenant_id, service, access_token)

    return conn


def set_log_path(log_path):
    logs.set_log_path(log_path)


## DBapi compatibility
#  -------------------
''' To fully comply to Python's DB-API 2.0 database standard. Ignore when using internally '''

# Type objects and constructors required by the DB-API 2.0 standard
Binary = memoryview
Date = date
Time = t
Timestamp = datetime


class _DBAPITypeObject:
    """DB-API type object which compares equal to all values passed to the constructor.
        https://www.python.org/dev/peps/pep-0249/#implementation-hints-for-module-authors
    """
    def __init__(self, *values):
        self.values = values

    def __eq__(self, other):
        return other in self.values


STRING = "STRING"
BINARY = _DBAPITypeObject("BYTES", "RECORD", "STRUCT")
NUMBER = _DBAPITypeObject("INTEGER", "INT64", "FLOAT", "FLOAT64", "NUMERIC",
                          "BOOLEAN", "BOOL")
DATETIME = _DBAPITypeObject("TIMESTAMP", "DATE", "TIME", "DATETIME")
ROWID = "ROWID"


def DateFromTicks(ticks):
    return Date.fromtimestamp(ticks)


def TimeFromTicks(ticks):
    return Time(
        *time.localtime(ticks)[3:6]
    )  # localtime() returns a namedtuple, fields 3-5 are hr/min/sec


def TimestampFromTicks(ticks):
    return Timestamp.fromtimestamp(ticks)


# DB-API global parameters
apilevel = '2.0' 

threadsafety = 1 # Threads can share the module but not a connection

paramstyle = 'qmark'
