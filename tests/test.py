import time
from datetime import datetime, date, timezone
from numpy.random import randint, uniform
from queue import Queue
from time import sleep
import threading, sys, os
import socket
import pytest
from tests.logger import Logger
import pysqream_blue


q = Queue()
varchar_length = 10
nvarchar_length = 10
max_bigint = sys.maxsize if sys.platform not in ('win32', 'cygwin') else 2147483647
_access_token="Z2hZaDdyMmhEWHFkdGJBN3c4em9SSndjcVBXQjI5a05XZjRHSHU4X1B0R1RmbzYzYm53NENGaUVIMGlSX0lLRjVhMUQ3c3JfbHQyVGtfRk1md3U5T1M3aXNlZlcwS2l4"

def generate_varchar(length):
    return ''.join(chr(num) for num in randint(32, 128, length))


col_types = {'bool', 'tinyint', 'smallint', 'int', 'bigint', 'real', 'double', 'date', 'datetime', 'nvarchar({})'.format(varchar_length)}#, 'varchar({})'.format(varchar_length)}


pos_test_vals = {'bool': (0, 1, True, False, 2),
                 'tinyint': (randint(0, 255), randint(0, 255), 0, 255, True, False),
                 'smallint': (randint(-32768, 32767), 0, -32768, 32767, True, False),
                 'int': (randint(-2147483648, 2147483647), 0, -2147483648, 2147483647, True, False),
                 'bigint': (randint(1-max_bigint, max_bigint), 0, 1-max_bigint, max_bigint, True, False),
                 'real': (round(uniform(1e-6, 1e6), 5), 837326.52428, True, False),   # float('nan')
                 'double': (uniform(1e-6, 1e6), True, False),  # float('nan')
                 'date': (date(1998, 9, 24), date(2020, 12, 1), date(1997, 5, 9), date(1993, 7, 13)),
                 'datetime': (datetime(1001, 1, 1, 10, 10, 10), datetime(1997, 11, 30, 10, 10, 10), datetime(1987, 7, 27, 20, 15, 45), datetime(1993, 12, 20, 17, 25, 46)),
                #  'varchar': (generate_varchar(varchar_length), generate_varchar(varchar_length), generate_varchar(varchar_length), 'b   '),
                 'nvarchar': ('א', 'א  ', '', 'ab א')}

neg_test_vals = {'tinyint': (258, 3.6, 'test',  (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'smallint': (40000, 3.6, 'test', (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'int': (9999999999, 3.6, 'test',  (1997, 5, 9), (1997, 12, 12, 10, 10, 10)),
                 'bigint': (92233720368547758070, 3.6, 'test', (1997, 12, 12, 10, 10, 10)),
                 'real': ('test', (1997, 12, 12, 10, 10, 10)),
                 'double': ('test', (1997, 12, 12, 10, 10, 10)),
                 'date': (5, 3.6, (-8, 9, 1), (2012, 15, 6), (2012, 9, 45), 'test', False, True),
                 'datetime': (5, 3.6, (-8, 9, 1, 0, 0, 0), (2012, 15, 6, 0, 0, 0), (2012, 9, 45, 0, 0, 0), (2012, 9, 14, 26, 0, 0), (2012, 9, 14, 13, 89, 0), 'test', False, True),
                #  'varchar': (5, 3.6, (1, 2), (1997, 12, 12, 10, 10, 10), False, True),
                 'nvarchar': (5, 3.6, (1, 2), (1997, 12, 12, 10, 10, 10), False, True)}


def connect_pysqream_blue(domain, use_ssl=True):
    return pysqream_blue.connect(host=domain, use_ssl=use_ssl,
                                 access_token=_access_token, database="developer_regression_query3")


class Query():

    def __init__(self, con):
        self.con = con

    def fetch(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        return res

    def execute(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        cur.close()

    def fetchmany(self, query, number):
        cur = self.con.cursor()
        cur.execute(query)
        res = cur.fetchmany(number)
        cur.close()
        return res

    def fetchone(self, query):
        cur = self.con.cursor()
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        return res


class TestBase():

    @pytest.fixture()
    def domain(self, pytestconfig):
        return pytestconfig.getoption("domain")

    @pytest.fixture(autouse=True)
    def Test_setup_teardown(self, domain):
        self.domain = domain
        Logger().info("Before Scenario")
        Logger().info(f"Connect to server with domain {domain}")
        self.con = connect_pysqream_blue(domain)
        self.query = Query(self.con)
        yield
        Logger().info("After Scenario")
        self.con.close()
        Logger().info(f"Close Session to server {domain}")

    def fetch(self, query):
        return self.query.fetch(query)

    def execute(self, query):
        self.query.execute(query)

    def fetchmany(self, query, number):
        return self.query.fetchmany(query, number)

    def fetchone(self, query):
        return self.query.fetchone(query)

class TestBaseWithoutBeforeAfter():
    @pytest.fixture()
    def domain(self, pytestconfig):
        return pytestconfig.getoption("domain")

    @pytest.fixture(autouse=True)
    def Test_setup_teardown(self, domain):
        self.domain = domain
        yield


class TestConnection(TestBaseWithoutBeforeAfter):

    def test_connection(self):

        Logger().info("connect and run select 1")
        con = connect_pysqream_blue(self.domain, use_ssl=False)
        cur = con.cursor()
        try:
            cur.execute("select 1")
        except Exception as e:
            if "SQreamd connection interrupted" not in repr(e):
                raise Exception("bad error message")
        cur.close()
        Logger().info("Connection tests - wrong ip")
        try:
            pysqream_blue.connect(host='123.4.5.6', port='443', database='master', username='sqream',
                                  password='sqream',use_ssl=False, access_token=_access_token)
        except Exception as e:
            if "Error from grpc while attempting to open database connection" not in repr(e):
                raise Exception("bad error message")

        Logger().info("Connection tests - wrong port")
        try:
            pysqream_blue.connect(host=self.domain, port='6000', database='master', username='sqream',
                                  password='sqream', use_ssl=False, access_token=_access_token)
        except Exception as e:
            if "Error from grpc while attempting to open database connection" not in repr(e):
                raise Exception("bad error message")

        Logger().info("Connection tests - wrong database")
        try:
            pysqream_blue.connect(host=self.domain, port='443', database='wrong_db', username='sqream',
                                  password='sqream', use_ssl=False, access_token=_access_token)
        except Exception as e:
            if "Database \'wrong_db\' does not exist" not in repr(e).replace("""\\""", ''):
                raise Exception("bad error message")

        Logger().info("Connection tests - wrong username")
        try:
            pysqream_blue.connect(host=self.domain, port='443', database='master', username='wrong_username',
                                  password='sqream', use_ssl=False, access_token=_access_token)
        except Exception as e:
            if "role \'wrong_username\' doesn't exist" not in repr(e).replace("""\\""", ''):
                raise Exception("bad error message")

        Logger().info("Connection tests - wrong password")
        try:
            pysqream_blue.connect(host=self.domain, port='443', database='master', username='sqream',
                                  password='wrong_pw', use_ssl=False, access_token=_access_token)
        except Exception as e:
            if "wrong password for role 'sqream'" not in repr(e).replace("""\\""", ''):
                raise Exception("bad error message")

        Logger().info("Connection tests - close() function")
        con = connect_pysqream_blue(self.domain)
        cur = con.cursor()
        cur.close()
        try:
            cur.execute('select 1')
        except Exception as e:
          if "Session has been closed" not in repr(e):
              raise Exception("bad error message")

        Logger().info("Connection tests - Trying to close a connection that is already closed with close()")
        con = connect_pysqream_blue(self.domain)
        con.close()
        try:
            con.close()
        except Exception as e:
            if "Trying to close a connection that's already closed" not in repr(e):
                raise Exception("bad error message")

        # ssl not supported
        # Logger().info("Connection tests - negative test for use_ssl=True")
        # try:
        #     pysqream_blue.connect(self.domain, 5000, 'master', 'sqream', 'sqream', False, True)
        # except Exception as e:
        #     if "Using use_ssl=True but connected to non ssl sqreamd port" not in repr(e):
        #         raise Exception("bad error message")

        # Logger().info("Connection tests - positive test for use_ssl=True")
        # con = connect_pysqream_blue(False, True)
        # res = con.execute('select 1').fetchall()[0][0]
        # if res != 1:
        #     if f'expected to get 1, instead got {res}' not in repr(e):
        #         raise Exception("bad error message")


class TestPositive(TestBase):

    def test_positive(self):

        for col_type in col_types:
            trimmed_col_type = col_type.split('(')[0]

            Logger().info(f'Positive tests - Inserted values test for column type {col_type}')
            Logger().info(f"create or replace table test (t_{trimmed_col_type} {col_type})")
            self.execute(f"create or replace table test (t_{trimmed_col_type} {col_type})")
            for val in pos_test_vals[trimmed_col_type]:
                # cur.execute('truncate table test')
                self.execute('truncate table test')
                if type(val) in [date, datetime, str]:
                    Logger().info(f"insert into test values (\'{val}\')")
                    self.execute(f"insert into test values (\'{val}\')")
                else:
                    Logger().info(f"insert into test values ({val})")
                    self.execute(f"insert into test values ({val})")
                Logger().info("select * from test")
                res = self.fetch("select * from test")[0][0]
                # Compare
                if val != res:
                    if trimmed_col_type not in ('bool', 'varchar', 'date', 'datetime', 'real'):
                        Logger().info((repr(val), type(val), repr(res), type(res)))
                        raise Exception("TEST ERROR: No match between the expected result to the returned result. expected to get {}, instead got {} on datatype {}".format(repr(val), repr(res), trimmed_col_type))
                    elif trimmed_col_type == 'bool' and val != 0:
                        if res is not True:
                            raise Exception("TEST ERROR: No match between the expected result to the returned result. expected to get 'True', instead got {} on datatype {}".format(repr(res), trimmed_col_type))
                    elif trimmed_col_type == 'varchar' and val.strip() != res:
                        raise Exception("TEST ERROR: No match between the expected result to the returned result. expected to get {}, instead got {} on datatype {}".format(repr(val), repr(res), trimmed_col_type))
                    elif trimmed_col_type in ('date', 'datetime') and datetime(*val) != res and date(*val) != res:
                        raise Exception("TEST ERROR: No match between the expected result to the returned result. expected to get {}, instead got {} on datatype {}".format(repr(val), repr(res), trimmed_col_type))
                    elif trimmed_col_type == 'real' and abs(res-val) > 0.1:
                        # Single precision packing and unpacking is inaccurate:
                        # unpack('f', pack('f', 255759.83335))[0] == 255759.828125
                        raise Exception("TEST ERROR: No match between the expected result to the returned result. expected to get {}, instead got {} on datatype {}".format(repr(val), repr(res), trimmed_col_type))

            # Network insert not supported
            # Logger().info(f'Positive tests - Null test for column type: {col_type}')
            # self.con.execute("create or replace table test (t_{} {})".format(trimmed_col_type, col_type))
            # self.con.executemany('insert into test values (?)', [(None,)])
            # status = self.con.execute('select * from test')
            # res = self.con.fetchall()[0][0]
            # if res not in (None,):
            #     raise Exception("TEST ERROR: Error setting null on column type: {}\nGot: {}, {}".format(trimmed_col_type, res, type(res)))

        # Network insert not supported
        # Logger().info("Positive tests - Case statement with nulls")
        # self.con.execute("create or replace table test (xint int)")
        # self.con.executemany('insert into test values (?)', [(5,), (None,), (6,), (7,), (None,), (8,), (None,)])
        # self.con.executemany("select case when xint is null then 1 else 0 end from test")
        # expected_list = [0, 1, 0, 0, 1, 0, 1]
        # res_list = []
        # res_list += [x[0] for x in self.con.fetchall()]
        # if expected_list != res_list:
        #     raise Exception("expected to get {}, instead got {}".format(expected_list, res_list))
        Logger().info("Positive tests - Testing select true/false")
        res = self.fetch("select false")[0][0]
        if res != 0:
            raise Exception("Expected to get result 0, instead got {}".format(res))
        res = self.fetch("select true")[0][0]
        if res != 1:
            raise Exception("Expected to get result 1, instead got {}".format(res))

        Logger().info("Positive tests - Running a statement when there is an open statement")
        self.execute("select 1")
        sleep(10)
        res = self.fetch("select 1")[0][0]
        if res != 1:
            raise Exception(f'expected to get result 1, instead got {res}')


class TestNegative(TestBase):

    def test_negative(self):
        ''' Negative Set/Get tests '''

        # not supported network insert
        # for col_type in col_types:
        #     if col_type == 'bool':
        #         continue
        #     Logger().info("Negative tests for column type: {}".format(col_type))
        #     trimmed_col_type = col_type.split('(')[0]
        #     Logger().info("prepare a table")
        #     self.con.execute("create or replace table test (t_{} {})".format(trimmed_col_type, col_type))
        #     for val in neg_test_vals[trimmed_col_type]:
        #         Logger().info("Insert value {} into data type {}".format(repr(val), repr(trimmed_col_type)))
        #         rows = [(val,)]
        #         try:
        #             self.con.executemany("insert into test values (?)", rows)
        #         except Exception as e:
        #             if "Error packing columns. Check that all types match the respective column types" not in repr(e):
        #                 raise Exception(f'bad error message')

        # Logger().info("Negative tests - Inconsistent sizes test")
        # self.con.execute("create or replace table test (xint int, yint int)")
        # try:
        #     self.con.executemany('insert into test values (?, ?)', [(5,), (6, 9), (7, 8)])
        # except Exception as e:
        #     if "Incosistent data sequences passed for inserting. Please use rows/columns of consistent length" not in repr(e):
        #         raise Exception(f'bad error message')

        Logger().info("Negative tests - Varchar - Conversion of a varchar to a smaller length")
        self.execute("create or replace table test (test varchar(10))")
        try:
            self.execute("insert into test values ('aa12345678910')")
        except Exception as e:
            if "Conversion of a varchar to a smaller length is not supported" not in repr(e):
                            raise Exception(f'bad error message')

        Logger().info("Negative tests - Nvarchar - Conversion of a varchar to a smaller length")
        self.execute("create or replace table test (test nvarchar(10))")
        try:
            self.execute("insert into test values ('aa12345678910')")
        except Exception as e:
            if "value \'aa12345678910\' is too long for column \'test\' of type TEXT(10)" not in repr(e).replace("""\\""", ''):
                raise Exception(f'bad error message')

        Logger().info("Negative tests - Incorrect usage of fetchmany - fetch without a statement")
        self.execute("create or replace table test (xint int)")
        cur = self.con.cursor()
        try:
            cur.fetchmany(2)
        except Exception as e:
            if "No open statement while attempting fetch operation" not in repr(e):
                raise Exception(f'bad error message')
        cur.close()

        Logger().info("Negative tests - Incorrect usage of fetchall")
        self.execute("create or replace table test (xint int)")
        cur = self.con.cursor()
        cur.execute("select * from test")
        try:
            cur.fetchall(5)
        except Exception as e:
            if "Bad argument to fetchall" not in repr(e):
                raise Exception(f'bad error message')
        cur.close()

        Logger().info("Negative tests - Incorrect usage of fetchone")
        self.execute("create or replace table test (xint int)")
        cur = self.con.cursor()
        cur.execute("select * from test")
        try:
            cur.fetchone(5)
        except Exception as e:
            if "Bad argument to fetchone" not in repr(e):
                raise Exception(f'bad error message')
        cur.close()

        Logger().info("Negative tests - Multi statements test")
        cur = self.con.cursor()
        try:
            cur.execute("select 1; select 1;")
        except Exception as e:
            if "expected one statement, got " not in repr(e):
                raise Exception(f'bad error message')
        cur.close()

        # not supported network insert
        # Logger().info("Negative tests - Parametered query tests")
        # params = 6
        # self.con.execute("create or replace table test (xint int)")
        # self.con.executemany('insert into test values (?)', [(5,), (6,), (7,)])
        # try:
        #     self.con.execute('select * from test where xint > ?', str(params))
        # except Exception as e:
        #     if "Parametered queries not supported" not in repr(e):
        #         raise Exception(f'bad error message')
        Logger().info("Negative tests - running execute on a closed cursor")
        cur = self.con.cursor()
        cur.close()
        try:
            cur.execute("select 1")
        except Exception as e:
            if "Session has been closed" not in repr(e):
                raise Exception(f'bad error message')


# Network insert not supported
# def parametered_test():
#     ''' Parametered query tests '''
#
#     global TESTS_PASS
#
#     print ('\nParametered Tests')
#     print ('-----------------')
#
#     params = 6,
#     con.execute(f'create or replace table test (t_int int)')
#     con.executemany('insert into test values (?)', [(5,), (6,), (7,)])
#     con.execute('select * from test where t_int > ?', params)
#     res = con.fetchall()
#
#     if res[0][0] != 7:
#         print (f"parametered test fail, expected value {params} but got {res[0][0]}")
#         TESTS_PASS = False


class TestFetch(TestBase):

    def test_fetch(self):

        Logger().info("Fetch tests - positive fetch tests")
        self.execute("create or replace table test (xint int)")
        # network insert not supported
        # self.con.executemany('insert into test values (?)', [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)])
        for i in range(1, 10):
            self.execute(f'insert into test values ({i})')

        # fetchmany(1) vs fetchone()
        res = self.fetchmany("select * from test", 1)[0][0]
        res2 = self.fetchone("select * from test")[0][0]
        if res != res2:
            raise Exception(f"fetchmany(1) and fetchone() didn't return the same value. fetchmany(1) is {res} and fetchone() is {res2}")
        # fetchmany(-1) vs fetchall()
        res3 = self.fetchmany("select * from test", -1)[0][0]
        res4 = self.fetch("select * from test")[0][0]
        if res3 != res4:
            raise Exception("fetchmany(-1) and fetchall() didn't return the same value. fetchmany(-1) is {} and fetchall() is {}".format(res3, res4))
        # fetchone() loop
        cur = self.con.cursor()
        cur.execute("select * from test")
        for i in range(1, 10):
            x = cur.fetchone()[0][0]
            if x != i:
                raise Exception("fetchone() returned {} instead of {}".format(x, i))
        cur.close()

        Logger().info("Fetch tests - combined fetch functions")
        self.execute("create or replace table test (xint int)")
        # network insert not supported
        # self.con.executemany('insert into test values (?)', [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)])
        for i in range(1, 10):
            self.execute(f'insert into test values ({i})')
        cur = self.con.cursor()
        cur.execute("select * from test")
        expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        res_list = []
        res_list.append(cur.fetchone()[0][0])
        res_list += [x[0] for x in cur.fetchmany(2)]
        res_list.append(cur.fetchone()[0][0])
        res_list += [x[0] for x in cur.fetchall()]
        if expected_list != res_list:
            raise Exception("expected to get {}, instead got {}".format(expected_list, res_list))
        cur.close()

        Logger().info("Fetch tests - fetch functions after all the data has already been read")
        self.execute("create or replace table test (xint int)")
        # network insert not supported
        # self.con.executemany('insert into test values (?)', [(1,)])
        self.execute('insert into test values (1)')
        cur = self.con.cursor()
        cur.execute("select * from test")
        x = cur.fetchone()[0]
        res = cur.fetchone()
        if res is not None:
            raise Exception(f"expected to get an empty result from fetchone, instead got {res}")
        try:
            cur.fetchall()
        except Exception as e:
            if "No open statement while attempting fetch operation" not in repr(e):
                raise Exception(f'bad error message')

        try:
            cur.fetchmany(1)
        except Exception as e:
            if "No open statement while attempting fetch operation" not in repr(e):
                raise Exception(f'bad error message')

        cur.close()


class TestCursor(TestBase):

    def test_cursor(self):

        Logger().info("Cursor tests - running two statements on the same cursor connection")
        vals = [1]
        cur = self.con.cursor()
        cur.execute("select 1")
        res1 = cur.fetchall()[0][0]
        cur.close()
        vals.append(res1)
        cur = self.con.cursor()
        cur.execute("select 1")
        res2 = cur.fetchall()[0][0]
        vals.append(res2)
        if not all(x == vals[0] for x in vals):
            raise Exception(f"expected to get result 1, instead got {res1} and {res2}")
        cur.close()
        # todo - need to check
        # Logger().info("Cursor tests - running a statement through cursor when there is an open statement")
        # cur = self.con.cursor()
        # cur.execute("select 1")
        # sleep(10)
        # cur.execute("select 1")
        # res = cur.fetchall()[0][0]
        # if res != 1:
        #     raise Exception(f"expected to get result 1, instead got {res}")

        Logger().info("Cursor tests - fetch functions after all the data has already been read through cursor")
        self.execute("create or replace table test (xint int)")
        # network insert not supported
        # cur.executemany('insert into test values (?)', [(1,)])
        self.execute('insert into test values (1)')
        cur = self.con.cursor()
        cur.execute("select * from test")
        x = cur.fetchone()[0]
        res = cur.fetchone()
        if res is not None:
            raise Exception("expected to get an empty result from fetchone, instead got {}".format(res))
        try:
            cur.fetchall()
        except Exception as e:
            if "No open statement while attempting fetch operation" not in repr(e):
                raise Exception(f'bad error message')

        try:
            cur.fetchmany(1)
        except Exception as e:
            if "No open statement while attempting fetch operation" not in repr(e):
                raise Exception(f'bad error message')
        cur.close()

        Logger().info("Cursor tests - run a query through a cursor and close the connection directly")
        cur = self.con.cursor()
        cur.execute("select 1")
        self.con.close()
        if not self.con.connected:
            raise Exception(f'Closed a connection after running a query through a cursor, but cursor is still open')


class TestString(TestBase):

    def test_string(self):

        # network insert not supported
        # Logger().info("String tests - insert and return UTF-8")
        # self.con.execute("create or replace table test (xvarchar varchar(20))")
        # self.con.executemany('insert into test values (?)', [(u"hello world",), ("hello world",)])
        # self.con.execute("select * from test")
        # res = self.con.fetchall()
        # if res[0][0] != res[1][0]:
        #     raise Exception("expected to get identical strings from select statement. instead got {} and {}".format(res[0][0], res[1][0]))

        Logger().info("String tests - strings with escaped characters")
        self.execute("create or replace table test (xvarchar varchar(20))")
        values = [("\t",), ("\n",), ("\\n",), ("\\\n",), (" \\",), ("\\\\",), (" \nt",), ("'abd''ef'",), ("abd""ef",), ("abd\"ef",)]
        # network insert not supported
        # self.con.executemany('insert into test values (?)', values)
        for val in values:
            self.execute(f"insert into test values ($${val[0]}$$)")
        cur = self.con.cursor()
        cur.execute("select * from test")
        expected_list = ['', '', '\\n', '\\', ' \\', '\\\\', ' \nt', "'abd''ef'", 'abdef', 'abd"ef']
        res_list = []
        res_list += [x[0] for x in cur.fetchall()]
        if expected_list != res_list:
            raise Exception("expected to get {}, instead got {}".format(expected_list, res_list))
        cur.close()


class TestDatetime(TestBase):

    def test_datetime(self):
        Logger().info("Datetime tests - insert different timezones datetime")
        t1 = datetime.strptime(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
        t2 = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M')
        self.execute("create or replace table test (xdatetime datetime)")
        # network insert not supported
        # self.concon.executemany('insert into test values (?)', [(t1,), (t2,)])
        self.execute(f'insert into test values ($${t1}$$)')
        self.execute(f'insert into test values ($${t2}$$)')
        res = self.fetch("select * from test")
        if res[0][0] == res[1][0]:
            raise Exception("expected to get different datetimes")

        Logger().info("Datetime tests - insert datetime with microseconds")
        t1 = datetime(1997, 5, 9, 4, 30, 10, 123456)
        t2 = datetime(1997, 5, 9, 4, 30, 10, 987654)
        self.execute("create or replace table test (xdatetime datetime)")
        # network insert not supported
        # self.con.executemany('insert into test values (?)', [(t1,), (t2,)])
        self.execute(f'insert into test values ($${t1}$$)')
        self.execute(f'insert into test values ($${t2}$$)')
        res = self.fetch("select * from test")
        if res[0][0] == res[1][0]:
            raise Exception("expected to get different datetimes")


class TestTimeout(TestBaseWithoutBeforeAfter):
    def test_timeout(self):
        con = None
        try:
            Logger().info("test_timeout after 120 seconds")
            con = pysqream_blue.connect(host=self.domain, use_ssl=False, query_timeout=120, access_token=_access_token)
            cur = con.cursor()
            cur.execute("select sleep(200)")
        except Exception as e:
            if "Connection timeout expired" not in repr(e):
                raise Exception(f'bad error message')
        finally:
            if con is not None:
                con.close()


class TestNoTimeout(TestBaseWithoutBeforeAfter):

    def test_no_timeout(self):
        con = None
        try:
            Logger().info("test_no_timeout")
            start_time = datetime.now()
            Logger().info(start_time)
            con = pysqream_blue.connect(host=self.domain, use_ssl=False, access_token=_access_token)
            cur = con.cursor()
            cur.execute("select sleep(200)")
            end_time = datetime.now()
            Logger().info(end_time)
            delta = end_time - start_time
            if delta.seconds < 200:
                raise ValueError("TimeOut occurs without reason!")
        except Exception as e:
            Logger().error(f"An error occurred {e}")
            raise Exception(f"An error occurred {e}")
        finally:
            if con is not None:
                con.close()


class TestAbort(TestBase):

    def test_abort(self):
        cur = self.con.cursor()
        try:
            Logger().info("Abort test - Prepare data before testing")
            create_query = "create or replace table big_text (x text)"
            insert_query1 = "insert into big_text values ('abcdef')"
            insert_query2 = "insert into big_text values ('eflmg')"
            insert_as_select_query = "insert into big_text select * from big_text"
            Logger().info(create_query)
            self.execute(create_query)
            Logger().info(insert_query1)
            self.execute(insert_query1)
            Logger().info(insert_query2)
            self.execute(insert_query2)
            for i in range(15):
                Logger().info(insert_as_select_query)
                self.execute(insert_as_select_query)

            Logger().info("Abort test - Abort Query on fetch test")
            select_fetch_query = "select * from big_text where x like '%ef%'"
            Logger().info(select_fetch_query)

            cur.execute(select_fetch_query)
            t = threading.Thread(target=cur.fetchall)
            t.start()
            time.sleep(5)
            cancel_response = cur.cancel()
            if not cancel_response:
                raise ValueError("Can't abort query on fetch")
        except Exception as e:
            Logger().error(f"An error occurred {e}")
        finally:
            cur.close()
            drop_query = "drop table big_text"
            Logger().info(drop_query)
            self.execute(drop_query)

        # Logger().info("Abort test - Abort Query on execute test")
        # select_sleep = "select sleep(200)"
        # Logger().info(select_sleep)
        # t1 = threading.Thread(target=cur.execute, args=(select_sleep,))
        # t1.start()
        # time.sleep(5)
        # cancel_response = cur.cancel()
        # if not cancel_response:
        #     raise ValueError("Can't abort query on execute")

        Logger().info("Abort test - Abort Query on close statement")
        select_1 = "select 1"
        Logger().info(select_1)
        cur = self.con.cursor()
        cur.execute(select_1)
        cur.fetchall()
        try:
            cur.cancel()
        except Exception as e:
            expected_error = "Query [{}] already closed"
            if expected_error not in repr(e):
                raise ValueError(f"expected to get {expected_error}, instead got {e}")
        finally:
            cur.close()

        Logger().info("Abort test - Abort Query on close session test")

        self.con.close()
        try:
            cur.cancel()
        except Exception as e:
            expected_error = "Query [{}] already closed"
            if expected_error not in repr(e):
                raise ValueError(f"expected to get {expected_error}, instead got {e}")

        # TODO - add test for two queries on parallel on the same session and abort one of them after refactor


class TestThreads(TestBase):

    def _execute(self, num):

        cur = self.con.cursor()
        cur.execute("select {}".format(num))
        res = cur.fetchall()
        q.put(res)
        cur.close()

    def test_threads(self):

        Logger().info("Thread tests - concurrent inserts with multiple threads through cursor")
        t1 = threading.Thread(target=self._execute, args=(3, ))
        t2 = threading.Thread(target=self._execute, args=(3, ))
        t1.start()
        t2.start()
        res1 = q.get()[0][0]
        res2 = q.get()[0][0]
        if res1 != res2:
            raise Exception("expected to get equal values. instead got res1 {} and res2 {}".format(res1, res2))

_queries = [
        'with cte0 as (select * from t_a) select count( * ) from cte0',
        'with cte0 as (select * from t_a), cte1 as (select * from cte0) select count( * ) from cte1',
        'with cte0 as (select xint from t_a where xint % 4=0) select * from cte0 t0 inner join cte0 t1 on t0.xint=t1.xint',
        'with cte0(x) as (select xint from t_a) select count(x) from cte0 where x % 2=0',
        'with t_a as (select * from t_b where xint % 2=0) select count( * ) from t_a',
        'with cte0(x) as (select xvarchar40 from t_a) select x from cte0 where len(x) % 4=0',
        'with cte0(x) as (select xnvarchar40 from t_a) select x from cte0 where len(x) % 4=0',
        'with cte0 as (select * from (values (1)) t(x)) select * from cte0',
        'with cte0(x) as (select * from (values (1)) t(x)) select * from cte0',
        'with cte0(x) as (select 1) select * from cte0',
        'select distinct xtext6 from t_e',
        'select distinct xtextnull6 from t_e',
        'select substring(xvarchar40, 2, 2) from t_a',
        'select xvarchar40,isnull(ascii(rtrim(xvarchar40)),0) from t_a',
        'select cast(substring(xnvarchar40,2,2) as nvarchar(40)) from t_a',
        'select reverse(xnvarchar40) from t_a',
        'select datepart(hour,xdatetime) from t_a',
        'select datepart(day,xdate) from t_a',
        'select xint,xint2 from t_a where xint2 is null',
        'select xint,xint2 from t_a where xint2 is not null',
        'select xint,xkey from t_a where xkey in (1,10)',
        """select 1 + len('data') - 1""",
        """select (3 * len('data')) / 3""",
        """select substring('data',len('data')-2+1,2)""",
        """select t_a.xint, t_b.xint from t_a join t_b on t_a.xint = t_b.xint where t_a.xint=5""",
        """select t_a.xint, t_b.xint from t_a left join t_b on t_a.xint = t_b.xint where t_a.xint=5""",
        """select top 5 t_a.xint, t_b.xint from t_a inner join t_b on t_a.xint = t_b.xint where t_a.xint=5""",
        """select distinct t_a.xint, t_b.xint from t_a inner join t_b on t_a.xint = t_b.xint where t_a.xint=5""",
        """select * from t_a join t_b on t_a.xint = t_b.xkey where t_a.xint=5""",
        """select * from t_a join t_b on t_a.xkey = t_b.xint where t_a.xkey=5""",
        """select t_a.xint, t_b.xint from t_a left join t_b on t_a.xint = t_b.xint and t_a.xint = t_b.xkey""",
        """select * from t_a left join t_b on t_a.xint = t_b.xint and t_a.xint2 = t_b.xint""",
        """select t_a.xint,t_b.xint from t_a right join t_b on t_a.xint = t_b.xint where t_a.xint < 100 and t_b.xint < 101 and t_a.xint2 = t_b.xint""",
        """select xint + 1 from t_a where high_selectivity(xint*4>20)""",
        """select xint from t_a where high_selectivity(xint%2=0)""",
        """select xsmallint , xreal , xint from t_a where high_selectivity(xint - 100 > 84)""",
        """select xreal , xint from t_a where high_selectivity(xint*2 > 50 and xreal*2 > 2)""",
        """select t_b.xvarchar40 , t_b.xbit from t_b where high_selectivity(t_b.xbit = 0 and t_b.xvarchar40 like '%t')""",
        """select count(*) as c2 from (select count(*) as c1 from t_a inner join t_b on t_a.xkey = t_b.xkey) as t1""",
        """select 1 from t_a having count(1) > 0""",
        """select 1 from t_a having count(1) > 0 and count(3) > 0""",
        """select avg(32) from t_a having count(1) > 0 and count(3) > 0""",
        """select min(1) as ans from t_a having count(1) > 0 and count(3) > 0 order by ans""",
        """select 'a'||'a',cast(min(1) as varchar(2)) ||'2' as ans from t_a having count(1) > 0 and count(3) > 2 order by ans""",
        """select t_a.xkey from t_a group by xkey having count(3) > 0 and count(5) > 0""",
        """select sum(xkey) from t_a having count(3) > 0 and count(5) > 0""",
        """select avg(xkey)+1 from t_a having count(3) > 0 and count(5) > 0 and count(3) > 0""",
        """select cast(min(xkey) as varchar(2)) || cast(min(xkey) as varchar(2)), cast(min(1) as varchar(2)) ||'2' as ans from t_a having count(1) > 0 and count(3) > 2 order by ans""",
        """select * from t_a order by xnvarchar40""",
        """select xnvarchar40 from t_a order by xnvarchar40""",
        """select xint, xnvarchar40 from t_a order by xnvarchar40""",
        """select xnvarchar40 from t_a order by xnvarchar40 desc""",
        """select xint, xnvarchar40 from t_a order by xnvarchar40 desc""",
        """select top 1 xnvarchar40 from t_a order by xnvarchar40""",
        """select top 1 xnvarchar40 from t_a order by xnvarchar40 desc""",
        """select top 1 xint, xnvarchar40 from t_a order by xnvarchar40""",
        """select top 1 xint, xnvarchar40 from t_a order by xnvarchar40 desc""",
        """select top 5 xnvarchar40, len (xnvarchar40 ) from t_a order by xnvarchar40""",
        """select top 5 xnvarchar40, len (xnvarchar40 ) from t_a where len(xnvarchar40) < 15 order by xnvarchar40""",
        """select top 5 xnvarchar40, lower (xnvarchar40 ) from t_a order by xnvarchar40""",
        """select xnvarchar40 from t_a group by xnvarchar40""",
        """select xnvarchar40,count(xint) from t_a group by xnvarchar40""",
        """select xnvarchar40,count(*) from t_a group by xnvarchar40""",
        """select count(*),t_a.xvarchar40 from t_a,t_b where t_a.xvarchar40 = t_b.xvarchar40 group by t_a.xvarchar40""",
        """select count(*),t_a.xvarchar40 from t_a where t_a.xvarchar40 not between '10050' and '10100' group by t_a.xvarchar40""",
        """select xint2,xfloat,min(xnvarchar40) from t_a group by xint2,xfloat,xnvarchar40""",
        """select distinct xvarchar40 from t_a where t_a.xint < 10""",
        """select distinct xnvarchar40 from t_a""",
        """select distinct xint,xtinyint,xsmallint,xbigint,xreal,xfloat,xnvarchar40,xdate,xdatetime,xbit from t_a where t_a.xint < 10""",
        """select distinct xnvarchar40 from t_a where xvarchar40 > 'm'""",
        """select top 5 xnvarchar40_not_null, len (xnvarchar40_not_null ) from t_g where len(xnvarchar40_not_null) < 15 order by xnvarchar40_not_null""",
        """select t_a.xint - subquery.new_num from t_a, (select xint,min(xint) as new_num from t_b group by xint) as subquery where t_a.xint = subquery.xint""",
        """select count(*) from (select count(*) as counts from t_a inner join t_b on t_a.xint=t_b.xint) as res"""
            ]





from time import sleep
import concurrent.futures


class ParallelJob:
    """
    parallel job interface
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        # self.results_dict = {"data": None, "column_names": None, "column_types": None, "errors": None,
        #                      "statementId": None, "execution_time": None, "compilation_time": None}
        # self.result = None
        self.result = None

    def execute(self):
        raise NotImplementedError

    def fetch(self):
        return self.result


class ExecuteQuery(ParallelJob, TestBase):
    """
    parallel object of execute_query
    """

    def execute(self):

        # self.results_dict["errors"], self.results_dict["statementId"], self.results_dict["execution_time"], \
        #     self.results_dict["compilation_time"] = sq.execute_query(*self.args, **self.kwargs)
        con = self.args[1]
        cur = con.cursor()
        cur.execute(*self.args)
        cur.close()
        return self


class FetchQuery(ParallelJob):
    """
    parallel object of fetch_query
    """

    def execute(self):
        query = self.args[0]
        con = self.args[1]
        cur = con.cursor()
        cur.execute(query)
        self.result = cur.fetchall()
        cur.close()
        # self.results_dict = sq.fetch_query(*self.args, **self.kwargs)
        return self


class CompileQuery(ParallelJob):

    def execute(self):
        client = self.args[0]
        query = self.args[1]
        context_id = self.args[2]
        query_timeout = self.args[3]
        use_ssl = self.args[4]
        call_credentialds = self.args[5]
        try:
            response_compile = client.Compile(
                qh_messages.CompileRequest(context_id=context_id, sql=query.encode('utf8'),
                                           encoding='utf8',
                                           query_timeout=query_timeout),
                credentials=call_credentialds if use_ssl else None)
        except grpc.RpcError as rpc_error:
            Logger().info(f'Query: {query}. Error from grpc while attempting to compile the query.\n{rpc_error}')
            try:
                if "expired" in str(rpc_error):
                    auth_response = client.auth_access_token()
                    token = auth_response.token
                    call_credentialds = grpc.access_token_call_credentials(token)
                    response_compile = client.Compile(
                        qh_messages.CompileRequest(context_id=context_id, sql=query.encode('utf8'),
                                                   encoding='utf8',
                                                   query_timeout=query_timeout),
                        credentials=call_credentialds if use_ssl else None)
            except grpc.RpcError as rpc_error:
                raise ValueError(f'Query: {query}. Error from grpc while attempting to compile the query.\n{rpc_error}')

        if response_compile.HasField('error'):
            raise OperationalError(
                    f'Query: {query}. Error while attempting to compile the query.\n{response_compile.error}')

        self.result = response_compile.context_id
        return self


class ParallelHandler:

    requested_jobs = []
    future_results = []
    executor = None

    @staticmethod
    def execute(interval: int = 0):
        # run the queries and fill future_results
        ParallelHandler.future_results = []
        ParallelHandler.executor = concurrent.futures.ThreadPoolExecutor()

        for parallel_job in ParallelHandler.requested_jobs:
            ParallelHandler.future_results.append(ParallelHandler.executor.submit(parallel_job.execute))
            if interval:
                sleep(interval)

        # flush queries list
        ParallelHandler.requested_jobs.clear()

    @staticmethod
    def wait():
        concurrent.futures.wait(ParallelHandler.future_results, return_when=concurrent.futures.ALL_COMPLETED)
        if ParallelHandler.executor:
            ParallelHandler.executor.shutdown()
            ParallelHandler.executor = None

    @staticmethod
    def register(parallel_job: ParallelJob):
        ParallelHandler.requested_jobs.append(parallel_job)

    @staticmethod
    def fetch_results(index: int):
        ParallelHandler.wait()
        return ParallelHandler.future_results[index].result().fetch()

    @staticmethod
    def fetch_all_results():
        ParallelHandler.wait()
        results = []
        for i in range(len(ParallelHandler.future_results)):
            results.append(ParallelHandler.fetch_results(i))

        return results


def register_request(parallel_job: ParallelJob):
    """
    adds a parallel job request to the parallel requests pool
    """

    ParallelHandler.register(parallel_job)


def execute(interval: int = 0):
    """
    executes all parallel jobs in parallel requests pool async
    :param interval: sleep time between every query
    """

    ParallelHandler.execute(interval=interval)


def wait():
    """
    wait for all futures (parallel jobs that were executed) to be done
    """

    ParallelHandler.wait()


def fetch_results(index: int):
    """
    waits for all futures to be done and return the result of parallel_job[index]
    """

    return ParallelHandler.fetch_results(index)


def fetch_all_results():
    """
    iterates all future results and return a list of results.
    each element in the list represents the returned value of the future.
    """

    return ParallelHandler.fetch_all_results()


class TestBug(TestBase):

    def test_rep(self):

        multiple_queries = _queries[:10]
        Logger().info(f"going to execute {len(multiple_queries)} queries")
        len_fetch_expected = len(multiple_queries)
        fetch_res_list = []
        for index, query in enumerate(multiple_queries):
            Logger().info(f"execute query number {index}")
            register_request(FetchQuery(query, self.con))
            execute()
            time.sleep(0.2)
            res = fetch_results(0)
            fetch_res_list.append(res)

        self.con.close()
        assert len_fetch_expected == len(fetch_res_list), f"count of results is not valid, expected to {len_fetch_expected} get {len(fetch_res_list)}"


import grpc
from pysqream_blue.globals import auth_services, auth_messages, qh_services, qh_messages, cl_messages, auth_type_messages
from pysqream_blue.utils import OperationalError

class TestGrpc:

    def _check_error(self, response, stmt_id, request_status):
        if response.HasField('error'):
            raise OperationalError(f'Query: {stmt_id}. Error while attempting to {request_status} the query.\n{response.error}')

    def _request_status(self, client, stmt_id, use_ssl, call_credentialds, query):
        while True:
            response_status = client.Status(
                qh_messages.StatusRequest(context_id=stmt_id),
                credentials=call_credentialds if use_ssl else None)

            self._check_error(response_status, query, "status")

            if response_status.status == qh_messages.QUERY_EXECUTION_STATUS_ABORTED:
                Logger().info(f"Query id {stmt_id} is aborted")
                return

            if response_status.status != qh_messages.QUERY_EXECUTION_STATUS_SUCCEEDED:
                raise OperationalError(
                    f"Query id: {stmt_id}. "
                    f"Query execution failed with status: "
                    f"{qh_messages.QueryExecutionStatus.Name(response_status.status)}.")

            if response_status.status != qh_messages.QUERY_EXECUTION_STATUS_RUNNING and \
                    response_status.status != qh_messages.QUERY_EXECUTION_STATUS_QUEUED:
                Logger().info(f'Query id: {stmt_id}. '
                              f'status: {qh_messages.QueryExecutionStatus.Name(response_status.status)}.')
                return

    def _request_channel(self):
        options = [('grpc.max_message_length', 1024 ** 3), ('grpc.max_receive_message_length', 1024 ** 3),
                   ('grpc.keepalive_time_ms', 1000), ('grpc.keepalive_timeout_ms', 2000),
                   ('grpc.keepalive_permit_without_calls', True), ('grpc.keepalive_without_calls', True),
                   ("grpc.enable_http_proxy", 0)]
        channel = grpc.secure_channel('danielg.isqream.com:443', grpc.ssl_channel_credentials(), options=options)
        return channel

    def _request_auth(self, access_token, auth_stub):
        auth_response = auth_stub.Auth(auth_messages.AuthRequest(
            auth_type=auth_type_messages.AUTHENTICATION_TYPE_IDP,
            access_token=access_token
        ))
        token = auth_response.token
        call_credentialds = grpc.access_token_call_credentials(token)
        return token, call_credentialds

    def _request_session(self, auth_stub, tenant_id, database, pool_name, call_credentialds):
        return auth_stub.Session(auth_messages.SessionRequest(
            tenant_id=tenant_id,
            database=database,
            source_ip=socket.gethostbyname("192.168.4.4"),
            client_info=cl_messages.ClientInfo(version='PySQream2_V_111'),
            pool_name=pool_name
        ), credentials=call_credentialds)

    def _request_compile(self, client, query, context_id, query_timeout, use_ssl, call_credentialds):
        response_compile = client.Compile(
            qh_messages.CompileRequest(context_id=context_id, sql=query.encode('utf8'),
                                       encoding='utf8',
                                       query_timeout=query_timeout),
            credentials=call_credentialds if use_ssl else None)

        self._check_error(response_compile, query, "compile")
        return response_compile.context_id

    def _request_execute(self, client, stmt_id, query, use_ssl, call_credentialds):
        response_execute = client.Execute(
            qh_messages.ExecuteRequest(context_id=stmt_id),
            credentials=call_credentialds if use_ssl else None)

        self._check_error(response_execute, query, "execute")

    def test(self):
        query_timeout = 0
        access_token = _access_token
        tenant_id = "tenant"
        pool_name = None
        use_ssl = False
        database = "developer_regression_query3"

        # open channel
        channel = self._request_channel()

        # open stub
        auth_stub = auth_services.AuthenticationServiceStub(channel)
        client = qh_services.QueryHandlerServiceStub(channel)

        # Auth Request
        token, call_credentialds = self._request_auth(access_token, auth_stub)

        # Session Request
        session_response = self._request_session(auth_stub, tenant_id, database, pool_name, call_credentialds)
        context_id = session_response.context_id
        number = 200
        for query in _queries * number:
        # Compile Request
        # stmt_id = self._request_compile(client, query, session_response.context_id, query_timeout, use_ssl, call_credentialds)
            register_request(CompileQuery(client, query, context_id, query_timeout, use_ssl, call_credentialds))
        try:
            execute()
            stmt_id_list = fetch_all_results()
        except grpc.RpcError as rpc_error:
            close_response = client.CloseSession(
                qh_messages.CloseSessionRequest(close_request=qh_messages.CloseRequest(context_id=context_id)),
                credentials=call_credentialds if use_ssl else None
            ).close_response

            self._check_error(close_response, context_id, "close session")
            raise ValueError(f'Error from grpc while attempting to compile the query.\n{rpc_error}')
        # Execute Request
        # self._request_execute(client, stmt_id, query, use_ssl, call_credentialds)

        # # Status Request
        # self._request_status(client, stmt_id, use_ssl, call_credentialds, query)

        # Close Request
        for stmt_id in stmt_id_list:
            try:
                response_close: qh_messages.CloseResponse = client.CloseStatement(
                        qh_messages.CloseStatementRequest(close_request=qh_messages.CloseRequest(context_id=stmt_id)),
                        credentials=call_credentialds if use_ssl else None).close_response

                self._check_error(response_close, stmt_id, "close")
            except grpc.RpcError as rpc_error:
                Logger().info(f'Query id: {stmt_id}. Error from grpc while attempting to close the query.\n{rpc_error}')

        time.sleep(5)
        try:
            close_response = client.CloseSession(
                qh_messages.CloseSessionRequest(close_request=qh_messages.CloseRequest(context_id=context_id)),
                credentials=call_credentialds if use_ssl else None
            ).close_response
        except grpc.RpcError as rpc_error:
            raise ValueError(f'context_id id: {context_id}. Error from grpc while attempting to close the session.\n{rpc_error}')
        self._check_error(close_response, context_id, "close session")

        channel.close()
        assert len(stmt_id_list) == len(
            _queries * number), f"count of results is not valid, expected to {len(stmt_id_list)} get {len(_queries*number)}"