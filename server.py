from flask import Flask, request
from flask import render_template
import keras, sys, json
import numpy as np
application = Flask(__name__)

stored_model = None

@application.route("/")
def hello():
    return render_template('index.html')

@application.route("/predict", methods=['POST'])
def classifyCharacter():
    global stored_model

    body = request.get_json()

    reshapedData = np.array(body['data'])
    reshapedData = reshapedData.reshape(1,28,28,1)
    predict = stored_model.predict(reshapedData)
    classes = np.argmax(predict,axis=1)

    return json.dumps( { 'prediction' : int(classes) } ) 

def start():
    global stored_model

    stored_model = keras.models.load_model('mnist.h5')
    stored_model.make_predict_function()

    application.run(host='0.0.0.0', port=8080)