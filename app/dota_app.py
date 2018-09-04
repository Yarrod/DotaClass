from __future__ import division, print_function
# coding=utf-8

import logging

import sys
import os
import glob
import re
import numpy as np
import pickle


# Keras
#from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.applications.inception_v3 import preprocess_input
from keras.applications.inception_v3 import decode_predictions
from keras.applications.inception_v3 import InceptionV3
from keras.models import load_model
from keras.preprocessing import image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session


config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.8
set_session(tf.Session(config=config))

#print(os.getcwd())

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# Define a flask app
app = Flask(__name__)

with open('labels.p', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data_dir_list = pickle.load(f)

#print(data_dir_list[0:10])    
# Model saved with Keras model.save()
MODEL_PATH = 'models/inception_model_not_scaled.h5'

# Load your trained model
model = load_model(MODEL_PATH)
model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/


#print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    
    img = image.load_img(img_path, target_size=(299, 299))
    # Preprocessing the image
    img = image.img_to_array(img)
    x = np.expand_dims(img, axis=0)
    # x = np.true_divide(x, 255)
    # x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('about.html')
    
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
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        pred_class = label = data_dir_list[np.argmax(preds)]
        result = str(pred_class)               # Convert to string
        #return result
        os.remove(file_path)
        return result
    return None


if __name__ == '__main__':
    
    #app.logger.debug('this is a DEBUG message')
    #app.logger.info('this is an INFO message')
    #app.logger.warning('this is a WARNING message')
    #app.logger.error('this is an ERROR message')
    #app.logger.critical('this is a CRITICAL message')

    app.run(host = '0.0.0.0',port=80)
    # Serve the app with gevent
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()
