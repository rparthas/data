import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE




data = pd.read_csv('data/train.csv')

def dummy_column(col_name, df):
    temp_df = pd.get_dummies(df[col_name],prefix_sep='_',prefix=col_name, drop_first=True)
    temp_df = pd.concat([df,temp_df],axis=1)
    return temp_df.drop(col_name,axis=1)

def preprocess(data_in):
    data_out = data_in.drop(['Payment Plan','ID','Batch Enrolled'],axis=1)
    categorical = [ 'Grade', 'Sub Grade', 'Employment Duration', 'Verification Status',  'Initial List Status', 'Application Type','Loan Title']
    for col in categorical:
        data_out = dummy_column(col,data_out)
    return data_out

def get_features_and_labels(data):
    X = data.loc[ : , data.columns != 'Loan Status']
    y = data['Loan Status']
    sm = SMOTE(sampling_strategy='auto', k_neighbors=1, random_state=43)
    return sm.fit_resample(X, y)


X,y = get_features_and_labels(preprocess(data))
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=43,stratify=y)

xgb_model = XGBClassifier(use_label_encoder=False,n_jobs=-1)
xgb_model.fit(X_train,y_train)

joblib.dump(xgb_model, 'model.pkl', compress=1)