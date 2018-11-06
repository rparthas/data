#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 10:10:55 2017

@author: ram
"""

import pandas as pd;

dataset = pd.read_csv('Data.csv')
x = dataset.iloc[:, 0:-1].values
y = dataset.iloc[:,-1].values

"""
Missing Data with imputer
"""
from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values="NaN",axis=0,strategy="mean")
imputer.fit(x[:,1:3])
x[:,1:3] = imputer.transform(x[:,1:3])

"""
Categorical Data with Encoder
"""
from sklearn.preprocessing import LabelEncoder
y_encoder =LabelEncoder()
y=y_encoder.fit_transform(y)

from sklearn.preprocessing import OneHotEncoder
x_lblEncoder =LabelEncoder()
x[:,0]=x_lblEncoder.fit_transform(x[:,0])
x_encoder = OneHotEncoder(categorical_features=[0])
x=x_encoder.fit_transform(x).toarray()

"""
Feature Scaling
"""
from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
x=sc_x.fit_transform(x)

"""
Train test split
"""
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=23)