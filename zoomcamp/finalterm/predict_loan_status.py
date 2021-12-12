import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask('predict_loan_status')

with open('./model.pkl', 'rb') as f_model:
    model = joblib.load(f_model)


@app.route('/ping', methods=['GET'])
def ping():
    return 'PONG'


@app.route('/predict', methods=['POST'])
def predict():
    return jsonify(predict_loan_status(request.get_json()))


def predict_loan_status(data):
    input_df = pd.DataFrame.from_dict([data], orient='columns')
    y_pred = model.predict(input_df)
    return {'status': 'Defaulter' if float(y_pred) == 1.0 else 'Non Defaulter'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
