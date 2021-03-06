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

@app.route('/predict', methods=['POST'], endpoint='upload_data_file')
def upload_data_file():
    # check if the post request has the file part
    if 'Image' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files.get('Image', '') 
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_data_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        file = Image.open(path)
        file = file.resize((50,50))
        file = np.array(file).reshape(1,50,50,1)
        print(file)
        print(file.shape)
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

if __name__ == '__main__':
    print('init: ML Model...started')
    print('init:ML Model is completed')
    app.run(host='0.0.0.0', port=5000)