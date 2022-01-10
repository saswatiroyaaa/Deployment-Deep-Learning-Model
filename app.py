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
MODEL_PATH = 'models/model_vgg.h5'

# Load trained model
model = load_model(MODEL_PATH)
print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')
def preprocess_img(img_path, model, img_size):
    img = Image.load_img(img_path, target_size=img_size)
    img_tensor = Image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    return img_tensor

def model_predict(img_path, model):
    DIMS = (224, 224, 3)
    img_tensor = preprocess_img(img_path, model, DIMS)
    
    preds = model.predict(img_tensor)
    if preds[0][0] > 0.5:
        return "Lyme - Positive"
    else:
        return "Lyme - Negative"

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
        preds = model_predict(file_path, model)
        return preds
    return None


if __name__ == '__main__':
    app.run()

           
    