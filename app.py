from __future__ import division, print_function
import warnings
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as Image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer
from flask_ngrok import run_with_ngrok

warnings.filterwarnings('ignore')
# Define a flask app
app = Flask(__name__)
run_with_ngrok(app)
# Model saved with Keras model.save()
MODEL_PATH_VGG = 'models/model_vgg.h5'
MODEL_PATH_CONV2D = 'models/model_conv_2d.h5'
MODEL_PATH_MOBNETV2 = 'models/model_mobv2.h5'
MODEL_PATH_RESNET50 = 'models/model_resnet50.h5'
# Load trained model
model_vgg = load_model(MODEL_PATH_VGG)
model_conv_2d = load_model(MODEL_PATH_CONV2D)
model_mobv2 = load_model(MODEL_PATH_MOBNETV2)
model_resnet50 = load_model(MODEL_PATH_RESNET50)

print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')
def preprocess_img(img_path, img_size):
    img = Image.load_img(img_path, target_size=img_size)
    img_tensor = Image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    return img_tensor

def model_predict(img_path):
    DIMS = (224, 224, 3)
    DIMS_CONV = (300, 300, 3)
    img_tensor = preprocess_img(img_path, DIMS)
    img_tensor_conv = preprocess_img(img_path, DIMS_CONV)
    res = {}
    res["VGG19"] = str(model_vgg.predict(img_tensor)[0][0])
    res["CONV2D"] = str(model_conv_2d.predict(img_tensor_conv)[0][0])
    res["MobileNet V2"] = str(model_mobv2.predict(img_tensor)[0][0])
    res["ResNet 50"] = str(model_resnet50.predict(img_tensor)[0][0])

    # if preds[0][0] > 0.5:
    #     return "Lyme - Positive"
    # else:
    #     return "Lyme - Negative"
    return res

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


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

        # Make prediction
        preds = model_predict(file_path)
        return preds
    return None


if __name__ == '__main__':
    app.run()

           
    