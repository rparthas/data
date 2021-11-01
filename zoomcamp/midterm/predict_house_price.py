import joblib
import pandas as pd
from flask import Flask, request, jsonify
from custom_transformer import FeatureSelector

app = Flask('house_price')

with open('./model.pkl', 'rb') as f_model:
    model = joblib.load(f_model)


@app.route('/ping', methods=['GET'])
def ping():
    return 'PONG'


@app.route('/predict', methods=['POST'])
def predict():
    return jsonify(predict_price(request.get_json()))


def predict_price(data):
    y_pred = model.predict(pd.DataFrame.from_dict([data], orient='columns'))
    return {'price': float(y_pred)}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
