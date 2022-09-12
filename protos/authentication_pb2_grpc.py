# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import authentication_pb2 as protos_dot_authentication__pb2


class AuthenticationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Auth = channel.unary_unary(
                '/com.sqream.cloud.generated.v1.AuthenticationService/Auth',
                request_serializer=protos_dot_authentication__pb2.AuthRequest.SerializeToString,
                response_deserializer=protos_dot_authentication__pb2.AuthResponse.FromString,
                )


class AuthenticationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Auth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthenticationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Auth': grpc.unary_unary_rpc_method_handler(
                    servicer.Auth,
                    request_deserializer=protos_dot_authentication__pb2.AuthRequest.FromString,
                    response_serializer=protos_dot_authentication__pb2.AuthResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.sqream.cloud.generated.v1.AuthenticationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AuthenticationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Auth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.sqream.cloud.generated.v1.AuthenticationService/Auth',
            protos_dot_authentication__pb2.AuthRequest.SerializeToString,
            protos_dot_authentication__pb2.AuthResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)