# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import queryhandler_pb2 as protos_dot_queryhandler__pb2


class QueryHandlerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Compile = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/Compile',
                request_serializer=protos_dot_queryhandler__pb2.CompileRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.CompileResponse.FromString,
                )
        self.Execute = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/Execute',
                request_serializer=protos_dot_queryhandler__pb2.ExecuteRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.ExecuteResponse.FromString,
                )
        self.Status = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/Status',
                request_serializer=protos_dot_queryhandler__pb2.StatusRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.StatusResponse.FromString,
                )
        self.Fetch = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/Fetch',
                request_serializer=protos_dot_queryhandler__pb2.FetchRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.FetchResponse.FromString,
                )
        self.CloseStatement = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/CloseStatement',
                request_serializer=protos_dot_queryhandler__pb2.CloseStatementRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.CloseStatementResponse.FromString,
                )
        self.Cancel = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/Cancel',
                request_serializer=protos_dot_queryhandler__pb2.CancelRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.CancelResponse.FromString,
                )
        self.CloseSession = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.QueryHandlerService/CloseSession',
                request_serializer=protos_dot_queryhandler__pb2.CloseSessionRequest.SerializeToString,
                response_deserializer=protos_dot_queryhandler__pb2.CloseSessionResponse.FromString,
                )


class QueryHandlerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Compile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Execute(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Fetch(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CloseStatement(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Cancel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CloseSession(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryHandlerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Compile': grpc.unary_unary_rpc_method_handler(
                    servicer.Compile,
                    request_deserializer=protos_dot_queryhandler__pb2.CompileRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.CompileResponse.SerializeToString,
            ),
            'Execute': grpc.unary_unary_rpc_method_handler(
                    servicer.Execute,
                    request_deserializer=protos_dot_queryhandler__pb2.ExecuteRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.ExecuteResponse.SerializeToString,
            ),
            'Status': grpc.unary_unary_rpc_method_handler(
                    servicer.Status,
                    request_deserializer=protos_dot_queryhandler__pb2.StatusRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.StatusResponse.SerializeToString,
            ),
            'Fetch': grpc.unary_unary_rpc_method_handler(
                    servicer.Fetch,
                    request_deserializer=protos_dot_queryhandler__pb2.FetchRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.FetchResponse.SerializeToString,
            ),
            'CloseStatement': grpc.unary_unary_rpc_method_handler(
                    servicer.CloseStatement,
                    request_deserializer=protos_dot_queryhandler__pb2.CloseStatementRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.CloseStatementResponse.SerializeToString,
            ),
            'Cancel': grpc.unary_unary_rpc_method_handler(
                    servicer.Cancel,
                    request_deserializer=protos_dot_queryhandler__pb2.CancelRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.CancelResponse.SerializeToString,
            ),
            'CloseSession': grpc.unary_unary_rpc_method_handler(
                    servicer.CloseSession,
                    request_deserializer=protos_dot_queryhandler__pb2.CloseSessionRequest.FromString,
                    response_serializer=protos_dot_queryhandler__pb2.CloseSessionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.sqream.cloud.generated.v1.QueryHandlerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QueryHandlerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Compile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/Compile',
            protos_dot_queryhandler__pb2.CompileRequest.SerializeToString,
            protos_dot_queryhandler__pb2.CompileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Execute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/Execute',
            protos_dot_queryhandler__pb2.ExecuteRequest.SerializeToString,
            protos_dot_queryhandler__pb2.ExecuteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/Status',
            protos_dot_queryhandler__pb2.StatusRequest.SerializeToString,
            protos_dot_queryhandler__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Fetch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/Fetch',
            protos_dot_queryhandler__pb2.FetchRequest.SerializeToString,
            protos_dot_queryhandler__pb2.FetchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CloseStatement(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/CloseStatement',
            protos_dot_queryhandler__pb2.CloseStatementRequest.SerializeToString,
            protos_dot_queryhandler__pb2.CloseStatementResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Cancel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/Cancel',
            protos_dot_queryhandler__pb2.CancelRequest.SerializeToString,
            protos_dot_queryhandler__pb2.CancelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CloseSession(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.QueryHandlerService/CloseSession',
            protos_dot_queryhandler__pb2.CloseSessionRequest.SerializeToString,
            protos_dot_queryhandler__pb2.CloseSessionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)