#!/usr/bin/env python3

import time
from datetime import datetime, date, time as t
from pysqream_blue.connection import Connection
import os
from pysqream_blue.logger import *
# from pysqream_blue.connection import qh_messages

# os.environ['export GRPC_POLL_STRATEGY'] = 'poll'

def connect(host:      str,
            port:      str =  '443',
            use_ssl:   bool = True,
            log              = False,
            database:  str =  'master',
            username:  str =  'sqream',
            password:  str =  'sqream',
            tenant_id: str =  'tenant',
            service:   str =  'sqream',
            access_token: str = None,
            reconnect_attempts : int = 10,
            reconnect_interval : int = 3,
            query_timeout      : int = 0,
            pool_name: str = None
            ) -> Connection:
    ''' Connect to SQream database '''

    if log is not False:
        start_logging(None if log is True else log)

    conn = Connection(host, port, use_ssl, log=log, is_base_connection=True, reconnect_attempts=reconnect_attempts,
                      reconnect_interval=reconnect_interval, query_timeout=query_timeout, pool_name=pool_name)
    conn.connect_database(database, username, password, tenant_id, service, access_token)

    return conn



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


# if __name__ == '__main__':
#     con = connect(host='4_52.isqream.com', database='master')
#     query = None
#     while (True):
#         cursor = con.cursor()
#         query = input(f'{con.database}=> ')
#         if '\q' == query:
#             break
#         try:
#             cursor.execute(query)
#             if cursor.query_type == qh_messages.QUERY_TYPE_QUERY:
#                 print(*(desc[0] for desc in cursor.description), sep=', ')
#                 print(*cursor.fetchall() or [], sep="\n")
#                 print(f'{cursor.rowcount} rows')
#                 cursor.close()
#         except Exception as e:
#             print(e)
#     con.close()
