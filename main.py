from concurrent import futures
from contextlib import asynccontextmanager

import grpc
from fastapi import FastAPI

from protobuf import dictionary_service_pb2_grpc
from dictionary_service import DictionaryService


def create_grpc_server():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    dictionary_service_pb2_grpc.add_DictionaryServiceServicer_to_server(
        DictionaryService(), server)
    server.add_insecure_port("[::]:50050")
    return server


grpc_server = create_grpc_server()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Автоматически управляет gRPC-сервером при запуске FastAPI"""
    await grpc_server.start()
    print("🚀 gRPC сервер запущен на порту 50050")
    try:
        yield
    finally:
        await grpc_server.stop(0)
        print("🛑 gRPC сервер остановлен")
app = FastAPI(lifespan=lifespan, )
