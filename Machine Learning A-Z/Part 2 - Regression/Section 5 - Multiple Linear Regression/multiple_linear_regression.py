# Data Preprocessing Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('50_Startups.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values

from sklearn.preprocessing import LabelEncoder,OneHotEncoder
labelEncoder =LabelEncoder()
labelEncoder.fit(X[:,3])
X[:,3]=labelEncoder.transform(X[:,3])
oneHotEncoder = OneHotEncoder()
X=oneHotEncoder.fit_transform(X).toarray()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(X_train,y_train)
y_pred=regressor.predict(X_test)


plt.scatter(np.arange(1,y_test.size+1,1),y_test,color='red')
plt.scatter(np.arange(1,y_pred.size+1,1),y_pred,color='blue')
plt.show()

'''
import statsmodels.formula.api as sm
X=np.append(arr=np.ones((50,1)).astype(int),values=X,axis=1)
X_opt=X[:,[0,4,5]]
regressor_ols=sm.ols(endog=y,exog=X_opt).fit()
print(regressor_ols._results.summary())
'''



