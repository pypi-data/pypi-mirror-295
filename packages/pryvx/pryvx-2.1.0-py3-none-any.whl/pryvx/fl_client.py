import grpc
from pryvx import pryvx_pb2
from pryvx import pryvx_pb2_grpc
from sklearn.linear_model import LogisticRegression
import pickle


def train(features, labels):
    model = LogisticRegression()
    model.fit(features, labels)

    serialized_model = pickle.dumps(model)

    return serialized_model


def send_params(serialized_model, connection_url):

    with grpc.insecure_channel(connection_url) as channel:
        stub = pryvx_pb2_grpc.ModelServiceStub(channel)

        model_params = pryvx_pb2.ModelParams(params=serialized_model)

        response = stub.SendModelParams(model_params)

        return "Model Params sent to server"

