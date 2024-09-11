import grpc

from . import token_pb2, token_pb2_grpc


def token_exists(token: str, address: str) -> token_pb2.ExistsTokenResponse:
    with grpc.insecure_channel(address) as channel:
        stub = token_pb2_grpc.TokenServiceStub(channel)
        request = token_pb2.ExistsTokenRequest(token=token)
        try:
            return stub.ExistsToken(request)
        except grpc.RpcError as e:
            print(f"gRPC error: {e.details()}")
            return None
