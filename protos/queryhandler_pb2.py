# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/queryhandler.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos import error_pb2 as protos_dot_error__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19protos/queryhandler.proto\x12\x1d\x63om.sqream.cloud.generated.v1\x1a\x12protos/error.proto\"Z\n\x0e\x43ompileRequest\x12\x12\n\ncontext_id\x18\x01 \x01(\t\x12\x0b\n\x03sql\x18\x02 \x01(\x0c\x12\x10\n\x08\x65ncoding\x18\x03 \x01(\t\x12\x15\n\rquery_timeout\x18\x04 \x01(\x03\"\xd8\x01\n\x0f\x43ompileResponse\x12\x12\n\ncontext_id\x18\x01 \x01(\t\x12>\n\x07\x63olumns\x18\x02 \x03(\x0b\x32-.com.sqream.cloud.generated.v1.ColumnMetadata\x12<\n\nquery_type\x18\x03 \x01(\x0e\x32(.com.sqream.cloud.generated.v1.QueryType\x12\x33\n\x05\x65rror\x18\x04 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error\"#\n\rStatusRequest\x12\x12\n\ncontext_id\x18\x01 \x01(\t\"\x8a\x01\n\x0eStatusResponse\x12\x43\n\x06status\x18\x01 \x01(\x0e\x32\x33.com.sqream.cloud.generated.v1.QueryExecutionStatus\x12\x33\n\x05\x65rror\x18\x02 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error\"$\n\x0e\x45xecuteRequest\x12\x12\n\ncontext_id\x18\x01 \x01(\t\"Z\n\x0f\x45xecuteResponse\x12\x12\n\ncontext_id\x18\x01 \x01(\t\x12\x33\n\x05\x65rror\x18\x02 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error\"\xf1\x01\n\x0e\x43olumnMetadata\x12\x37\n\x04type\x18\x01 \x01(\x0e\x32).com.sqream.cloud.generated.v1.ColumnType\x12\x10\n\x08nullable\x18\x02 \x01(\x08\x12\x13\n\x0btru_varchar\x18\x03 \x01(\x08\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x12\n\nvalue_size\x18\x05 \x01(\x03\x12\r\n\x05scale\x18\x06 \x01(\x05\x12\x11\n\tprecision\x18\x07 \x01(\x05\x12;\n\x08sub_type\x18\x08 \x01(\x0e\x32).com.sqream.cloud.generated.v1.ColumnType\"\"\n\x0c\x46\x65tchRequest\x12\x12\n\ncontext_id\x18\x01 \x01(\t\"o\n\rFetchResponse\x12\x14\n\x0cquery_result\x18\x01 \x01(\x0c\x12\x33\n\x05\x65rror\x18\x02 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error\x12\x13\n\x0bretry_fetch\x18\x03 \x01(\x08\"[\n\x15\x43loseStatementRequest\x12\x42\n\rclose_request\x18\x01 \x01(\x0b\x32+.com.sqream.cloud.generated.v1.CloseRequest\"^\n\x16\x43loseStatementResponse\x12\x44\n\x0e\x63lose_response\x18\x01 \x01(\x0b\x32,.com.sqream.cloud.generated.v1.CloseResponse\"Y\n\x13\x43loseSessionRequest\x12\x42\n\rclose_request\x18\x01 \x01(\x0b\x32+.com.sqream.cloud.generated.v1.CloseRequest\"\\\n\x14\x43loseSessionResponse\x12\x44\n\x0e\x63lose_response\x18\x01 \x01(\x0b\x32,.com.sqream.cloud.generated.v1.CloseResponse\"\"\n\x0c\x43loseRequest\x12\x12\n\ncontext_id\x18\x01 \x01(\t\"T\n\rCloseResponse\x12\x0e\n\x06\x63losed\x18\x01 \x01(\x08\x12\x33\n\x05\x65rror\x18\x02 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error\"#\n\rCancelRequest\x12\x12\n\ncontext_id\x18\x01 \x01(\t\"W\n\x0e\x43\x61ncelResponse\x12\x10\n\x08\x63\x61nceled\x18\x01 \x01(\x08\x12\x33\n\x05\x65rror\x18\x02 \x01(\x0b\x32$.com.sqream.cloud.generated.v1.Error*\xb9\x03\n\nColumnType\x12\x1b\n\x17\x43OLUMN_TYPE_UNSPECIFIED\x10\x00\x12\x18\n\x14\x43OLUMN_TYPE_LONG_INT\x10\x01\x12\x19\n\x15\x43OLUMN_TYPE_ULONG_INT\x10\x02\x12\x13\n\x0f\x43OLUMN_TYPE_INT\x10\x04\x12\x14\n\x10\x43OLUMN_TYPE_UINT\x10\x05\x12\x17\n\x13\x43OLUMN_TYPE_VARCHAR\x10\x06\x12\x16\n\x12\x43OLUMN_TYPE_DOUBLE\x10\x07\x12\x14\n\x10\x43OLUMN_TYPE_BYTE\x10\x08\x12\x15\n\x11\x43OLUMN_TYPE_UBYTE\x10\t\x12\x15\n\x11\x43OLUMN_TYPE_SHORT\x10\n\x12\x16\n\x12\x43OLUMN_TYPE_USHORT\x10\x0b\x12\x15\n\x11\x43OLUMN_TYPE_FLOAT\x10\x0c\x12\x14\n\x10\x43OLUMN_TYPE_DATE\x10\r\x12\x18\n\x14\x43OLUMN_TYPE_DATETIME\x10\x0e\x12\x14\n\x10\x43OLUMN_TYPE_BOOL\x10\x0f\x12\x14\n\x10\x43OLUMN_TYPE_BLOB\x10\x10\x12\x17\n\x13\x43OLUMN_TYPE_NUMERIC\x10\x11\x12\x15\n\x11\x43OLUMN_TYPE_ARRAY\x10\x12*W\n\tQueryType\x12\x1a\n\x16QUERY_TYPE_UNSPECIFIED\x10\x00\x12\x14\n\x10QUERY_TYPE_QUERY\x10\x01\x12\x18\n\x14QUERY_TYPE_NON_QUERY\x10\x02*\xf4\x02\n\x14QueryExecutionStatus\x12&\n\"QUERY_EXECUTION_STATUS_UNSPECIFIED\x10\x00\x12\"\n\x1eQUERY_EXECUTION_STATUS_RUNNING\x10\x01\x12$\n QUERY_EXECUTION_STATUS_SUCCEEDED\x10\x02\x12!\n\x1dQUERY_EXECUTION_STATUS_FAILED\x10\x03\x12$\n QUERY_EXECUTION_STATUS_CANCELLED\x10\x04\x12\"\n\x1eQUERY_EXECUTION_STATUS_ABORTED\x10\x05\x12!\n\x1dQUERY_EXECUTION_STATUS_QUEUED\x10\x06\x12(\n$QUERY_EXECUTION_STATUS_QUEUE_TIMEOUT\x10\x07\x12\x30\n,QUERY_EXECUTION_STATUS_QUERY_RUNTIME_TIMEOUT\x10\x08\x32\x93\x06\n\x13QueryHandlerService\x12h\n\x07\x43ompile\x12-.com.sqream.cloud.generated.v1.CompileRequest\x1a..com.sqream.cloud.generated.v1.CompileResponse\x12h\n\x07\x45xecute\x12-.com.sqream.cloud.generated.v1.ExecuteRequest\x1a..com.sqream.cloud.generated.v1.ExecuteResponse\x12\x65\n\x06Status\x12,.com.sqream.cloud.generated.v1.StatusRequest\x1a-.com.sqream.cloud.generated.v1.StatusResponse\x12\x62\n\x05\x46\x65tch\x12+.com.sqream.cloud.generated.v1.FetchRequest\x1a,.com.sqream.cloud.generated.v1.FetchResponse\x12}\n\x0e\x43loseStatement\x12\x34.com.sqream.cloud.generated.v1.CloseStatementRequest\x1a\x35.com.sqream.cloud.generated.v1.CloseStatementResponse\x12\x65\n\x06\x43\x61ncel\x12,.com.sqream.cloud.generated.v1.CancelRequest\x1a-.com.sqream.cloud.generated.v1.CancelResponse\x12w\n\x0c\x43loseSession\x12\x32.com.sqream.cloud.generated.v1.CloseSessionRequest\x1a\x33.com.sqream.cloud.generated.v1.CloseSessionResponseB\x02P\x01\x62\x06proto3')

_COLUMNTYPE = DESCRIPTOR.enum_types_by_name['ColumnType']
ColumnType = enum_type_wrapper.EnumTypeWrapper(_COLUMNTYPE)
_QUERYTYPE = DESCRIPTOR.enum_types_by_name['QueryType']
QueryType = enum_type_wrapper.EnumTypeWrapper(_QUERYTYPE)
_QUERYEXECUTIONSTATUS = DESCRIPTOR.enum_types_by_name['QueryExecutionStatus']
QueryExecutionStatus = enum_type_wrapper.EnumTypeWrapper(_QUERYEXECUTIONSTATUS)
COLUMN_TYPE_UNSPECIFIED = 0
COLUMN_TYPE_LONG_INT = 1
COLUMN_TYPE_ULONG_INT = 2
COLUMN_TYPE_INT = 4
COLUMN_TYPE_UINT = 5
COLUMN_TYPE_VARCHAR = 6
COLUMN_TYPE_DOUBLE = 7
COLUMN_TYPE_BYTE = 8
COLUMN_TYPE_UBYTE = 9
COLUMN_TYPE_SHORT = 10
COLUMN_TYPE_USHORT = 11
COLUMN_TYPE_FLOAT = 12
COLUMN_TYPE_DATE = 13
COLUMN_TYPE_DATETIME = 14
COLUMN_TYPE_BOOL = 15
COLUMN_TYPE_BLOB = 16
COLUMN_TYPE_NUMERIC = 17
COLUMN_TYPE_ARRAY = 18
QUERY_TYPE_UNSPECIFIED = 0
QUERY_TYPE_QUERY = 1
QUERY_TYPE_NON_QUERY = 2
QUERY_EXECUTION_STATUS_UNSPECIFIED = 0
QUERY_EXECUTION_STATUS_RUNNING = 1
QUERY_EXECUTION_STATUS_SUCCEEDED = 2
QUERY_EXECUTION_STATUS_FAILED = 3
QUERY_EXECUTION_STATUS_CANCELLED = 4
QUERY_EXECUTION_STATUS_ABORTED = 5
QUERY_EXECUTION_STATUS_QUEUED = 6
QUERY_EXECUTION_STATUS_QUEUE_TIMEOUT = 7
QUERY_EXECUTION_STATUS_QUERY_RUNTIME_TIMEOUT = 8


_COMPILEREQUEST = DESCRIPTOR.message_types_by_name['CompileRequest']
_COMPILERESPONSE = DESCRIPTOR.message_types_by_name['CompileResponse']
_STATUSREQUEST = DESCRIPTOR.message_types_by_name['StatusRequest']
_STATUSRESPONSE = DESCRIPTOR.message_types_by_name['StatusResponse']
_EXECUTEREQUEST = DESCRIPTOR.message_types_by_name['ExecuteRequest']
_EXECUTERESPONSE = DESCRIPTOR.message_types_by_name['ExecuteResponse']
_COLUMNMETADATA = DESCRIPTOR.message_types_by_name['ColumnMetadata']
_FETCHREQUEST = DESCRIPTOR.message_types_by_name['FetchRequest']
_FETCHRESPONSE = DESCRIPTOR.message_types_by_name['FetchResponse']
_CLOSESTATEMENTREQUEST = DESCRIPTOR.message_types_by_name['CloseStatementRequest']
_CLOSESTATEMENTRESPONSE = DESCRIPTOR.message_types_by_name['CloseStatementResponse']
_CLOSESESSIONREQUEST = DESCRIPTOR.message_types_by_name['CloseSessionRequest']
_CLOSESESSIONRESPONSE = DESCRIPTOR.message_types_by_name['CloseSessionResponse']
_CLOSEREQUEST = DESCRIPTOR.message_types_by_name['CloseRequest']
_CLOSERESPONSE = DESCRIPTOR.message_types_by_name['CloseResponse']
_CANCELREQUEST = DESCRIPTOR.message_types_by_name['CancelRequest']
_CANCELRESPONSE = DESCRIPTOR.message_types_by_name['CancelResponse']
CompileRequest = _reflection.GeneratedProtocolMessageType('CompileRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMPILEREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CompileRequest)
  })
_sym_db.RegisterMessage(CompileRequest)

CompileResponse = _reflection.GeneratedProtocolMessageType('CompileResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMPILERESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CompileResponse)
  })
_sym_db.RegisterMessage(CompileResponse)

StatusRequest = _reflection.GeneratedProtocolMessageType('StatusRequest', (_message.Message,), {
  'DESCRIPTOR' : _STATUSREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.StatusRequest)
  })
_sym_db.RegisterMessage(StatusRequest)

StatusResponse = _reflection.GeneratedProtocolMessageType('StatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _STATUSRESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.StatusResponse)
  })
_sym_db.RegisterMessage(StatusResponse)

ExecuteRequest = _reflection.GeneratedProtocolMessageType('ExecuteRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTEREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.ExecuteRequest)
  })
_sym_db.RegisterMessage(ExecuteRequest)

ExecuteResponse = _reflection.GeneratedProtocolMessageType('ExecuteResponse', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTERESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.ExecuteResponse)
  })
_sym_db.RegisterMessage(ExecuteResponse)

ColumnMetadata = _reflection.GeneratedProtocolMessageType('ColumnMetadata', (_message.Message,), {
  'DESCRIPTOR' : _COLUMNMETADATA,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.ColumnMetadata)
  })
_sym_db.RegisterMessage(ColumnMetadata)

FetchRequest = _reflection.GeneratedProtocolMessageType('FetchRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.FetchRequest)
  })
_sym_db.RegisterMessage(FetchRequest)

FetchResponse = _reflection.GeneratedProtocolMessageType('FetchResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHRESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.FetchResponse)
  })
_sym_db.RegisterMessage(FetchResponse)

CloseStatementRequest = _reflection.GeneratedProtocolMessageType('CloseStatementRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLOSESTATEMENTREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CloseStatementRequest)
  })
_sym_db.RegisterMessage(CloseStatementRequest)

CloseStatementResponse = _reflection.GeneratedProtocolMessageType('CloseStatementResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLOSESTATEMENTRESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CloseStatementResponse)
  })
_sym_db.RegisterMessage(CloseStatementResponse)

CloseSessionRequest = _reflection.GeneratedProtocolMessageType('CloseSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLOSESESSIONREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CloseSessionRequest)
  })
_sym_db.RegisterMessage(CloseSessionRequest)

CloseSessionResponse = _reflection.GeneratedProtocolMessageType('CloseSessionResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLOSESESSIONRESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CloseSessionResponse)
  })
_sym_db.RegisterMessage(CloseSessionResponse)

CloseRequest = _reflection.GeneratedProtocolMessageType('CloseRequest', (_message.Message,), {
  'DESCRIPTOR' : _CLOSEREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CloseRequest)
  })
_sym_db.RegisterMessage(CloseRequest)

CloseResponse = _reflection.GeneratedProtocolMessageType('CloseResponse', (_message.Message,), {
  'DESCRIPTOR' : _CLOSERESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CloseResponse)
  })
_sym_db.RegisterMessage(CloseResponse)

CancelRequest = _reflection.GeneratedProtocolMessageType('CancelRequest', (_message.Message,), {
  'DESCRIPTOR' : _CANCELREQUEST,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CancelRequest)
  })
_sym_db.RegisterMessage(CancelRequest)

CancelResponse = _reflection.GeneratedProtocolMessageType('CancelResponse', (_message.Message,), {
  'DESCRIPTOR' : _CANCELRESPONSE,
  '__module__' : 'protos.queryhandler_pb2'
  # @@protoc_insertion_point(class_scope:com.sqream.cloud.generated.v1.CancelResponse)
  })
_sym_db.RegisterMessage(CancelResponse)

_QUERYHANDLERSERVICE = DESCRIPTOR.services_by_name['QueryHandlerService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _COLUMNTYPE._serialized_start=1715
  _COLUMNTYPE._serialized_end=2156
  _QUERYTYPE._serialized_start=2158
  _QUERYTYPE._serialized_end=2245
  _QUERYEXECUTIONSTATUS._serialized_start=2248
  _QUERYEXECUTIONSTATUS._serialized_end=2620
  _COMPILEREQUEST._serialized_start=80
  _COMPILEREQUEST._serialized_end=170
  _COMPILERESPONSE._serialized_start=173
  _COMPILERESPONSE._serialized_end=389
  _STATUSREQUEST._serialized_start=391
  _STATUSREQUEST._serialized_end=426
  _STATUSRESPONSE._serialized_start=429
  _STATUSRESPONSE._serialized_end=567
  _EXECUTEREQUEST._serialized_start=569
  _EXECUTEREQUEST._serialized_end=605
  _EXECUTERESPONSE._serialized_start=607
  _EXECUTERESPONSE._serialized_end=697
  _COLUMNMETADATA._serialized_start=700
  _COLUMNMETADATA._serialized_end=941
  _FETCHREQUEST._serialized_start=943
  _FETCHREQUEST._serialized_end=977
  _FETCHRESPONSE._serialized_start=979
  _FETCHRESPONSE._serialized_end=1090
  _CLOSESTATEMENTREQUEST._serialized_start=1092
  _CLOSESTATEMENTREQUEST._serialized_end=1183
  _CLOSESTATEMENTRESPONSE._serialized_start=1185
  _CLOSESTATEMENTRESPONSE._serialized_end=1279
  _CLOSESESSIONREQUEST._serialized_start=1281
  _CLOSESESSIONREQUEST._serialized_end=1370
  _CLOSESESSIONRESPONSE._serialized_start=1372
  _CLOSESESSIONRESPONSE._serialized_end=1464
  _CLOSEREQUEST._serialized_start=1466
  _CLOSEREQUEST._serialized_end=1500
  _CLOSERESPONSE._serialized_start=1502
  _CLOSERESPONSE._serialized_end=1586
  _CANCELREQUEST._serialized_start=1588
  _CANCELREQUEST._serialized_end=1623
  _CANCELRESPONSE._serialized_start=1625
  _CANCELRESPONSE._serialized_end=1712
  _QUERYHANDLERSERVICE._serialized_start=2623
  _QUERYHANDLERSERVICE._serialized_end=3410
# @@protoc_insertion_point(module_scope)
