import os

from flask import Flask, jsonify, request
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
import tflearn
from src.models.cnn_model import CNNModel
from matplotlib.pyplot import imread
# from src.models.predict_model import load_images
hdfs_file = '../data/test.h5'

app = Flask(__name__)
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# ALLOWED_EXTENSIONS_MODEL_FILE = set(['pkl'])
ALLOWED_EXTENSIONS_DATA_FILE = set(['jpeg',"jpg","png"])
model = None


def allowed_data_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_DATA_FILE


# def allowed_model_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_MODEL_FILE


# @app.route('/model-upload', methods=['POST'], endpoint='upload_file')
# def upload_file():
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         resp = jsonify({'message': 'No file part in the request'})
#         resp.status_code = 400
#         return resp
#     file = request.files['file']
#     if file.filename == '':
#         resp = jsonify({'message': 'No file selected for uploading'})
#         resp.status_code = 400
#         return resp
#     if file and allowed_model_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         resp = jsonify({'message': 'File successfully uploaded'})
#         resp.status_code = 201
#         ml_model.__init__()
#         return resp
#     else:
#         resp = jsonify({'message': 'Allowed file type is pkl'})
#         resp.status_code = 400
#         return resp


@app.route('/data-upload', methods=['POST'], endpoint='upload_data_file')
def upload_data_file():
    # check if the post request has the file part
    if 'Image' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files.get('Image', '') 
    # file = file.request.get_data()
    # print(file)
    # print(file)
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_data_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        # file = imread(path)
        file = Image.open(path)
        file = file.resize((50,50))
        file = np.array(file).reshape(1,50,50,1)
        print(file)
        print(file.shape)
        # file = file.reshape([1,50,50,1])
        # print(file.shape)
        convnet  = CNNModel()
        network = convnet.define_network(file)
        model = tflearn.DNN(network, tensorboard_verbose=0,\
                checkpoint_path='./src/models/nodule3-classifier.tfl.ckpt')
        model.load("./src/models/nodule3-classifier.tfl")
        result = model.predict(file)
        resp = jsonify({'message': result})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'message': 'Allowed file type is jpg,jpeg,png'})
        resp.status_code = 400
        return resp


# @app.route('/predict', methods=['POST'], endpoint='predict')
# def predict():
#     content = request.json
#     req_model = PredictReq()
#     try:
#         result = req_model.load(content)
#         value = ml_model.predict(result['radius_mean'], result['perimeter_mean'], result['area_mean'],
#                                  result['concavity_mean'],
#                                  result['concave_points_mean'], result['radius_worst'], result['perimeter_worst'],
#                                  result['area_worst'], result['concavity_worst'], result['concave_points_worst'])
#         response = PredictRes(value)
#     except ValidationError as err:
#         return jsonify(err.messages), 400
#     return response.to_json(), 200


if __name__ == '__main__':
    print('init: ML Model...started')
    print('init:ML Model is completed')
    app.run(host='0.0.0.0', port=5000)