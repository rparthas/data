import pickle

customer ={"contract": "two_year", "tenure": 12, "monthlycharges": 19.7}


with open('./model1.bin', 'rb') as f_model: 
    model = pickle.load(f_model)
    with open('./dv.bin', 'rb') as f_dv: 
        dv = pickle.load(f_dv)
        X = dv.transform([customer])     
        y_pred = model.predict_proba(X)[:, 1]     
        churn = y_pred >= 0.5 
        result = { 'churn_probability': float(y_pred),  'churn': bool(churn)}
        print(result)  