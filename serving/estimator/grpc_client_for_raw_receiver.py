
# GRPC remote call using estimator model with build_raw_serving_input_receiver_fn


import tensorflow as tf
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import grpc

tf.app.flags.DEFINE_string('server', 'localhost:8556',
                           'Server host:port.')
tf.app.flags.DEFINE_string('model', 'iris',
                           'Model name.')
FLAGS = tf.app.flags.FLAGS


def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def main(_):
    channel = grpc.insecure_channel(FLAGS.server)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = FLAGS.model
    request.model_spec.signature_name = 'predict'

    p = {
        "SepalLength": [5.0],
        "SepalWidth": [3.3],
        "PetalLength": [1.7],
        "PetalWidth": [0.5]
    }

    request.inputs['SepalLength'].CopyFrom(
        tf.make_tensor_proto([2.2,1.0,2.2,1.0], shape=[4]))
    request.inputs['SepalWidth'].CopyFrom(
        tf.make_tensor_proto([2.2,1.0,2.2,1.0], shape=[4]))
    request.inputs['PetalLength'].CopyFrom(
        tf.make_tensor_proto([2.2,1.0,2.2,1.0], shape=[4]))
    request.inputs['PetalWidth'].CopyFrom(
        tf.make_tensor_proto([2.2,1.0,2.2,1.0], shape=[4]))

    result_future = stub.Predict.future(request, 5.0)
    prediction = result_future.result().outputs['probabilities']

    print(prediction)


if __name__ == '__main__':
    tf.app.run()
