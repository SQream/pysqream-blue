from datetime import datetime, date, time as t
from decimal import Decimal, getcontext
from math import pow


def sq_date_to_py_date(sqream_date: int, date_convert_func=date) -> date:
    if sqream_date is None or sqream_date == 0:
        return None

    year = (10000 * sqream_date + 14780) // 3652425
    intermed_1 = 365 * year + year // 4 - year // 100 + year // 400
    intermed_2 = sqream_date - intermed_1
    if intermed_2 < 0:
        year = year - 1
        intermed_2 = sqream_date - (365 * year + year // 4 - year // 100 +
                                    year // 400)
    intermed_3 = (100 * intermed_2 + 52) // 3060

    year = year + (intermed_3 + 2) // 12
    month = int((intermed_3 + 2) % 12) + 1
    day = int(intermed_2 - (intermed_3 * 306 + 5) // 10 + 1)

    return date_convert_func(year, month, day)


def sq_datetime_to_py_datetime(sqream_datetime: int, dt_convert_func=datetime) -> datetime:
    ''' Getting the datetime items involves breaking the long into the date int and time it holds
        The date is extracted in the above, while the time is extracted here  '''

    if sqream_datetime is None or sqream_datetime == 0:
        return None

    date_part = sqream_datetime >> 32
    time_part = sqream_datetime & 0xffffffff
    date_part = sq_date_to_py_date(date_part)

    if date_part is None:
        return None

    msec = time_part % 1000
    sec = (time_part // 1000) % 60
    mins = (time_part // 1000 // 60) % 60
    hour = time_part // 1000 // 60 // 60

    return dt_convert_func(date_part.year, date_part.month, date_part.day,
                           hour, mins, sec, msec * int(pow(10, 3))) # Python expects to get 6 digit on
                                                                     # miliseconds while SQream returns 3.


tenth = Decimal("0.1")
if getcontext().prec < 38:
    getcontext().prec = 38


def sq_numeric_to_decimal(bigint_as_bytes: bytes, scale: int) -> Decimal:
    getcontext().prec = 38
    c = memoryview(bigint_as_bytes).cast('i')
    bigint = ((c[3] << 96) + ((c[2] & 0xffffffff) << 64) + ((c[1] & 0xffffffff) << 32) + (c[0] & 0xffffffff))

    return Decimal(bigint) * (tenth ** scale)