import grpc
from pryvx import pryvx_pb2
from pryvx import pryvx_pb2_grpc
import pickle
from concurrent import futures

# Server
class ModelServicer(pryvx_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        self.client_params = {}

    def SendModelParams(self, request, context):
        # Deserialize the model
        loaded_model = pickle.loads(request.params)

        # save model to gcp storage bucket

        print("Received model params from client")

        return pryvx_pb2.ModelParams(params=request.params)


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pryvx_pb2_grpc.add_ModelServiceServicer_to_server(ModelServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on localhost:50051")

    server.wait_for_termination()

