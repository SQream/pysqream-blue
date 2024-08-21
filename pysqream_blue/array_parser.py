import struct
from typing import List, Any

from pysqream_blue.globals import qh_messages, type_to_letter, dbapi_typecodes
import casting
from pysqream_blue.logger import Logs
from pysqream_blue.utils import NotSupportedError

#TODO- CHECK ABOUT LOGS!!
def _convert_fixed_size_buffer_to_array(buffer: memoryview, buffer_len: int, sub_type: qh_messages, scale: int) -> List[
    Any]:
    """Extract array with data of fixed size

     convert binary data to an array with fixed
    size (BOOL, TINYINT, SMALLINT, INT, BIGINT, REAL, DOUBLE,
    NUMERIC, DATE, DATETIME) objects (not with TEXT)

    Raw data contains binary data of data separated by optional padding (trailing zeros at the
    end for portions of data whose lengths are not dividable by 8)

    Example for binary data of boolean array[true, null,
    false]:
    `010 00000 100` -> replace paddings with _ `010_____100` where
    `010` are flag of null data inside array. Then `00000` is a
    padding to make lengths of data about nulls to be dividable by 8
    in case of array of length 8, 16, 24, 32 ... there won't be a
    padding, then `100` is a binary representation of 3 boolean
    values itself

    Returns:
        A list with fixed size data. Array represented as python
        lists also.

        [true, null, false]
    """
    data_fixed_size = struct.calcsize(type_to_letter[sub_type])
    array_size = _get_array_size(data_fixed_size, buffer_len)

    data = buffer[array_size + padding(array_size):buffer_len]
    nulls = buffer[0:array_size]

    transform = _get_trasform_func(sub_type, scale)
    return [
        transform(data[i * data_fixed_size:(i + 1) * data_fixed_size], nulls[i])
        for i in range(array_size)
    ]


def _get_array_size(data_size: int, buffer_length: int) -> int:
    """Get the SQream ARRAY size by inner data size and buffer length

    Args:
        data_size: integer with the size of data (fixed size data) inside ARRAY, for
          example for INT is 4, for BOOL is 1, etc.
        buffer_length: length of a chunk of buffer connected with one
          array

    Returns:
        An integer representing number of elements of an ARRAY with fixed sized data
    """
    aligned_block_size = (data_size + 1) * 8  # data + 1 byte for null
    div, mod = divmod(buffer_length, aligned_block_size)
    size = div * 8
    if mod:
        size += int((mod - 8) / data_size)
    return size


def _arr_lengths_to_pairs(text_lengths: List[int]):
    """Generator for parsing ARRAY TEXT columns' data"""
    start = 0
    for length in text_lengths:
        yield start, length
        start = length + padding(length)


def padding(number: int):
    return (8 - number % 8) % 8


def _get_unfixed_size_array(data: memoryview, nulls: List[bool], dlen: List[int]):
    """Construct one single array from data with dlen right bounds"""
    arr = []
    # lengths_to_pairs is not appropriate due to differences
    # in lengths representation
    for is_null, (start, end) in zip(nulls, _arr_lengths_to_pairs(dlen)):
        if is_null:
            arr.append(None)
        else:
            arr.append(data[start:end].tobytes().decode('utf8'))
    return arr


def _convert_unfixed_size_buffer_to_array(buffer: memoryview, buffer_len: int) -> List[List[Any]]:
    """Extract array with data of unfixed size

     Extract array from binary data of an Array with types of TEXT
     - unfixed size

     Contains 8 bytes (long) that contains length of elements in
     array, binary data of nulls at each index in array
     and data separated by optional padding. Data here represents
     chunked info of each element inside array

     At the beginning, the data contains **cumulative** lengths
     (however is better to say indexes of their ends at data buffer)
     of all data strings (+ their paddings) of array as integers.
     The number of those int lengths is equal to the array length
     (those was in 8 bytes above) and because int take 4 bytes it all
     takes N * 4 bytes. Then if it is not divisible by 8 -> + padding
     Then the strings data also separated by optional padding

     Example for binary data for 1 row of text array['ABC','ABCDEF',null]:
     (padding zeros replaced with _)
     Whole buffer data: `3000000 001_____ 3000 14000 16000 ____ `
                        `65 66 67 _____ 65 66 67 68 69 70 __`
     Length of array: `3000000` -> long 3
     Nulls: `001_____`
     Length of strings: `3000 14000 16000 ____` -> 3,14,16 + padding
     Strings: `65, 66, 67, _____ 65, 66, 67, 68, 69, 70, __`
     L1 = 3, so [0 - 3) is string `65 66 67` -> ABC, padding P1=5
     L2 = 14 (which is L1 + padding + current_length), so
     current_length = L2 - (L1 + P1) = 14 - (5 + 3) = 6, P2=2
     => [5 + 3, 14) is string `65, 66, 67, 68, 69, 70` -> ABCDEF
     L3 = 16 => current_length = L3 - (L2 + P2) = 16 - (14 + 2) = 0
     thus string is empty, and considering Nulls -> it is a null

     Args:
         buffer: memoryview (bytes represenation) of data of
           column
         buffer_len: the size of the chunk

     Returns:
         A list with Strings. Array represented as python
         lists also.

         ["ABC", "ABCDEF", None]
     """
    if len(buffer) == 0:
        return []

    num_of_elements = buffer[:8].cast('q')[0]  # Long
    cur = 8 + num_of_elements + padding(num_of_elements)
    # data lengths
    d_len = buffer[cur:cur + num_of_elements * 4].cast('i')
    cur += (num_of_elements + num_of_elements % 2) * 4
    data = buffer[cur: buffer_len]
    nulls = buffer[8: 8 + num_of_elements]
    return _get_unfixed_size_array(data, nulls, d_len)


def _get_trasform_func(type: qh_messages, scale: int) -> callable:
    """Provide function for casting bytes data to real data

    Args:
        type: type of an object
        scale: this parameter is relevant just for numeric type

    Returns:
        A function that cast simple portion of data to appropriate
        value.
    """
    data_format = type_to_letter[type]
    wrappers = {
        qh_messages.COLUMN_TYPE_DATE: casting.sq_date_to_py_date,
        qh_messages.COLUMN_TYPE_DATETIME: casting.sq_datetime_to_py_datetime
    }

    if type == qh_messages.COLUMN_TYPE_NUMERIC:
        def cast(data):
            return casting.sq_numeric_to_decimal(data, scale)
    elif type in wrappers:
        def cast(data):
            return wrappers[type](data.cast(data_format)[0])
    else:
        def cast(data):
            return data.cast(data_format)[0]

    def transform(mem: memoryview, is_null: bool = False):
        return None if is_null else cast(mem)

    return transform


def convert_buffer_to_array(buffer: memoryview, buffer_len: int, sub_type: qh_messages, scale: int) -> List[List[Any]]:
    sub_type_code = dbapi_typecodes.get(sub_type)
    if sub_type_code == "STRING":
        return _convert_unfixed_size_buffer_to_array(buffer, buffer_len)
    if sub_type_code not in ("NUMBER", "DATETIME"):
        logs.log_and_raise(
            NotSupportedError,
            f'Array of "{sub_type}" is not supported')
    return _convert_fixed_size_buffer_to_array(buffer, buffer_len, sub_type, scale)
