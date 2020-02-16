# Data Preprocessing Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Salary_Data.csv')
X = dataset.iloc[:,0].values
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(np.transpose(np.matrix(X_train)),np.transpose(np.matrix(y_train)))
y_pred=regressor.predict(np.transpose(np.matrix(X_test)))
y_train_pred=regressor.predict(np.transpose(np.matrix(X_train)))

plt.scatter(X_train,y_train,color='red')
plt.plot(X_train,y_train_pred,color='blue')
plt.title('Years of Experience vs Salary (Train)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

plt.scatter(X_test,y_test,color='red')
plt.plot(X_train,y_train_pred,color='blue')
plt.title('Years of Experience vs Salary (Test)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

