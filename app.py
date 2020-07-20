from flask import Flask, request, jsonify, render_template, url_for
from flask.logging import create_logger
import logging

import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

@app.route("/")
def home():
    html = f"<h3>Sklearn Prediction Home</h3>"
    return html.format(format)


@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    return {'message': 'Healthy'}, 200


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', name=name)


@app.route("/predict", methods=['POST'])
def predict():
    json_payload = request.json
    LOG.info(f"JSON payload: \n{json_payload}")
    prediction = 0
    LOG.info(f"Prediction: \n{prediction}")
    return jsonify({'prediction': prediction})


if __name__ == "__main__":
    # load pretrained model as clf
    app.run(host='0.0.0.0', port=8080, debug=True)
