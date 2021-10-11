import pickle

from flask import Flask, request, jsonify

app = Flask('churn')

with open('./model1.bin', 'rb') as f_model:
    model = pickle.load(f_model)
with open('./dv.bin', 'rb') as f_dv:
    dv = pickle.load(f_dv)


@app.route('/ping', methods=['GET'])
def ping():
    return 'PONG'


@app.route('/predict', methods=['POST'])
def predict():
    return jsonify(predict_customer(request.get_json()))


def predict_customer(customer):
    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[:, 1]
    churn = y_pred >= 0.5
    return {'churn_probability': float(y_pred), 'churn': bool(churn)}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
