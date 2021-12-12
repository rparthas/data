import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

data = pd.read_csv('data/train.csv')
X = data.loc[:, data.columns != 'Loan Status']
y = data['Loan Status']
sm = SMOTE(sampling_strategy='auto', k_neighbors=1, random_state=43)


numerical = ['Loan Amount', 'Funded Amount', 'Funded Amount Investor', 'Term',
             'Interest Rate', 'Home Ownership', 'Debit to Income',
             'Delinquency - two years', 'Inquires - six months', 'Open Account',
             'Public Record', 'Revolving Balance', 'Revolving Utilities',
             'Total Accounts', 'Total Received Interest',
             'Total Received Late Fee', 'Recoveries', 'Collection Recovery Fee',
             'Collection 12 months Medical', 'Last week Pay',
             'Accounts Delinquent', 'Total Collection Amount',
             'Total Current Balance', 'Total Revolving Credit Limit']
categorical = ['Grade', 'Sub Grade', 'Employment Duration', 'Verification Status', 'Initial List Status',
               'Application Type', 'Loan Title']

cat_pipe = Pipeline([
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
])

num_pipe = Pipeline([
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer([
    ('cat', cat_pipe, categorical),
    ('num', num_pipe, numerical)],
    remainder='drop'
)

pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('sm', sm),
    ('model', XGBClassifier(use_label_encoder=False, n_jobs=-1))
])

pipe.fit(X, y)
joblib.dump(pipe, 'model.pkl', compress=1)

