# Data Preprocessing Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Position_Salaries.csv')
X = dataset.iloc[:,1:2].values
y = dataset.iloc[:, 2].values
level=3

from sklearn.linear_model import LinearRegression
linear=LinearRegression()
regressor=linear.fit(X,y)
x_pred=np.ones((1,1))
x_pred[0,0]=level
linear_pred=regressor.predict(x_pred)

plt.scatter(X,y,color='red')
plt.plot(X,regressor.predict(X),color='blue')
plt.xlabel('Level')
plt.ylabel('Salary')
plt.title('Salary Linear Predictor')
plt.show()

from sklearn.preprocessing import PolynomialFeatures
features=PolynomialFeatures(degree=4)
X_poly=features.fit_transform(X)

linear=LinearRegression()
regressor=linear.fit(X_poly,y)
x_poly_pred=features.fit_transform(x_pred)

poly_pred=regressor.predict(x_poly_pred)
plt.scatter(X,y,color='red')
plt.plot(X,regressor.predict(X_poly),color='blue')
plt.xlabel('Level')
plt.ylabel('Salary')
plt.title('Salary Polynomial Predictor')
plt.show()


print("Linear=",linear_pred," vs Poly=",poly_pred," for a level of ",level)
