from __future__ import division, print_function
import warnings
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

warnings.filterwarnings('ignore')

# Keras
# from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
# from tensorflow.keras.models import load_model
# from my_utils.preprocess import preprocess_img
# from my_utils.model_loader import load_models
import my_utils.get_predictions as pred
from my_utils import model_loader
# sklearn

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer
from flask_ngrok import run_with_ngrok
import pickle

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
# Define a flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
run_with_ngrok(app)
models = None

# Model saved with Keras model.save()

# # Load trained model
# model_vgg = load_model(MODEL_PATH_VGG)
# # model_vgg = load_model(MODEL_PATH_VGG_CONV_DENSE)
# model_conv_2d = load_model(MODEL_PATH_CONV2D)
# model_mobv2 = load_model(MODEL_PATH_MOBNETV2)
# # model_resnet50 = load_model(MODEL_PATH_RESNET50)
# model_incepv3 = load_model(MODEL_PATH_INCEPTIONV3)
# model_vgg_features = load_model(MODEL_PATH_VGG_FEATURES)
# model_svm_vgg = pickle.load(open(MODEL_PATH_SVM_VGG, "rb"))
# model_rf_vgg = pickle.load(open(MODEL_PATH_RF_VGG, "rb"))


print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index2.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        global models
        if models is None:
            models = model_loader.get_models()
        # Make prediction
        try:
            preds = pred.model_predict(file_path, models=models)
            print(preds)
            return preds
        except Exception as e:
            print("Error occured.")
            print(e)
    return None


if __name__ == '__main__':
    app.run()

           
    