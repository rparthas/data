import joblib
import pandas as pd
from custom_transformer import FeatureSelector


def lambda_handler(event, context):
    with open('./model.pkl', 'rb') as f_model:
        model = joblib.load(f_model)
        y_pred = model.predict(pd.DataFrame.from_dict([event], orient='columns'))
        return {'price': float(y_pred)}
