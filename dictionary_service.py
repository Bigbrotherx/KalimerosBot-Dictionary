from protobuf import dictionary_service_pb2_grpc, dictionary_service_pb2
from db_crud import create_word, update_word, delete_word


class DictionaryService(dictionary_service_pb2_grpc.DictionaryServiceServicer):

    async def AddWord(self, request, context):
        result = await create_word(
            user_id=request.user_id, word=request.word, translation=request.translation)
        return dictionary_service_pb2.AddWordResponse(
            message=result.get("message", ""),
            status_code=result.get("status_code", 400))
