import joblib
import pandas as pd


def lambda_handler(event, context):
    with open('./model.pkl', 'rb') as f_model:
        model = joblib.load(f_model)
        input_df = pd.DataFrame.from_dict([event], orient='columns')
        y_pred = model.predict(input_df)
        return {'status': 'Defaulter' if float(y_pred) == 1.0 else 'Non Defaulter'}
