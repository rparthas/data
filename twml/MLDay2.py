#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 10:11:30 2018

@author: rajagopalps
"""


# coding: utf-8

# In[217]:


import os
import tarfile
from six.moves import urllib

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

fetch_housing_data()

# Can directly download from https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.tgz


# In[218]:


# Step 2: Take a quick look at the data

import pandas as pd

def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)

housing = load_housing_data()
housing.head()


# In[219]:


# Step 3: Understanding the data in multiple steps

housing.info()


# In[220]:


# Insights:
# ocean_proximity is non-numeric.

housing["ocean_proximity"].value_counts()


# In[221]:


# Insights we arrive at from above outputs
# 1. total_bedrooms has only 20433 rows
# 2. ocean_proximity is a categorical field


# In[222]:


# Now let's view count, min, max, mean, std deviation etc

housing.describe()


# In[223]:


# Q1 age 18, Q2 age 29, Q3 - 37

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

plt.boxplot(housing['housing_median_age'])


# In[224]:


# Let us plot the values as histograms 

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
housing.hist(bins=50, figsize=(20,15))
plt.show()


# In[225]:


# Some insights from the histogram:
# a. Slightly over 800 districts have a median_house_value equal to about $100,000.
# b. ‘median_income’ attribute doesn’t seem to be in US dollars. They are capped at 15 for higher median incomes, and 0.5 for lower median incomes.
# c. ‘housing_median_age’ is also capped.
# d. ‘median_house_value’ is also capped beyond $500,000. 
# e. All these attributes have been described in different scales.


# In[226]:


# 4. Create Test set

#Since median_income is a continuous numerical value, we first make categories from them so that we can do a 
#stratified split

import numpy as np
print(np.unique(np.ceil(housing["median_income"])))

# So we divide by 1.5 to limit the number of income categories
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)

# Label those values above 5 as 5
housing["income_cat"].where(housing["income_cat"] < 5, 5.0, inplace=True)
print(np.unique(housing["income_cat"]))

# Now we do a stratified split
from sklearn.model_selection import StratifiedShuffleSplit

split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

# remove the income_cat attribute so the data is back to its original state:
for set in(strat_train_set,strat_test_set):
    set.drop(["income_cat"],axis=1,inplace=True)

strat_test_set.head()


# In[227]:


# Step 5. Deep Dive into the data
housing=strat_train_set.copy()
# a. Visualising the data

housing.plot(kind="scatter", 
             x="longitude", 
             y="latitude", 
             alpha=0.4,
             s=housing["population"]/100, 
             c="median_house_value", 
             label="population", 
             figsize=(10,7),
             cmap=plt.get_cmap("jet"), 
             colorbar=True,
    sharex=False)
plt.legend()


# In[228]:


# Housing prices are quite costlier when they closer to the ocean or higher population density


# In[229]:


#5.b Finding Correlations between features
housing.corr()
corr_matrix = housing.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)


# In[230]:


# Towards 1 has positive correlation and towards -1 has negative correlation.
# 1. median_income is highly correlated
# 2. latidude has a negative correlation


# In[231]:


# Experimenting with new feature combinations to see better correlation with median_house_value
housing["rooms_per_household"] = housing["total_rooms"]/housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"]/housing["total_rooms"]
housing["population_per_household"]=housing["population"]/housing["households"]

corr_matrix = housing.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)


# In[232]:


# We found that new attribute bedrooms_per_room has better negative correlation and rooms_per_household has better
# positive correlation.


# In[233]:


# Step 6. Preparing the data.
# a. Data Cleaning

# Drop the median_house_values and copy to a separate variable
housing = strat_train_set.drop("median_house_value", axis=1) # drop labels for training set
housing_labels = strat_train_set["median_house_value"].copy()


# In[234]:


# Handling NA in total_bedrooms - Fill with median

# Set empty values to median
from sklearn.preprocessing import Imputer
imputer = Imputer(strategy="median")

# Remove ocean_proximity as it a text attribute. Will be handled later.
housing_num = housing.drop('ocean_proximity', axis=1)

# Compute median
imputer.fit(housing_num)

# Apply median
X = imputer.transform(housing_num)

housing_tr = pd.DataFrame(X, columns=housing_num.columns)
housing_tr.head()


# In[235]:


# Handling categorical attributes
housing_cat = housing['ocean_proximity']
print(np.unique(housing_cat))

# text labels to numbers
from sklearn.preprocessing import LabelEncoder
encoder=LabelEncoder()
housing_cat_encoded=encoder.fit_transform(housing_cat)
housing_cat_encoded

#  one binary attribute per category -> one-hot encoding
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
housing_cat_1hot = encoder.fit_transform(housing_cat_encoded.reshape(-1,1))
housing_cat_1hot
housing_cat_1hot.toarray()

# Combine to one step
from sklearn.preprocessing import LabelBinarizer
encoder=LabelBinarizer()
housing_cat_1hot=encoder.fit_transform(housing_cat)
housing_cat_1hot


# In[236]:


# Adding additional attributes

from sklearn.base import BaseEstimator, TransformerMixin

# column index
rooms_ix, bedrooms_ix, population_ix, household_ix = 3, 4, 5, 6

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room = True): # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room
    def fit(self, X, y=None):
        return self  # nothing else to do
    def transform(self, X, y=None):
        rooms_per_household = X[:, rooms_ix] / X[:, household_ix]
        population_per_household = X[:, population_ix] / X[:, household_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[X, rooms_per_household, population_per_household,
                         bedrooms_per_room]
        else:
            return np.c_[X, rooms_per_household, population_per_household]

attr_adder = CombinedAttributesAdder(add_bedrooms_per_room=False)
housing_extra_attribs = attr_adder.transform(housing.values)

housing_extra_attribs = pd.DataFrame(housing_extra_attribs, columns=list(housing.columns)+["rooms_per_household", "population_per_household"])
housing_extra_attribs.head()


# In[237]:


# Adding a transformer to select a subset of the whole data set.

from sklearn.base import BaseEstimator, TransformerMixin

# Create a class to select numerical or categorical columns 
# since Scikit-Learn doesn't handle DataFrames yet
class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values
    
    
from sklearn.base import TransformerMixin #gives fit_transform method for free
class MyLabelBinarizer(TransformerMixin):
    def __init__(self, *args, **kwargs):
        self.encoder = LabelBinarizer(*args, **kwargs)
    def fit(self, x, y=0):
        self.encoder.fit(x)
        return self
    def transform(self, x, y=0):
        return self.encoder.transform(x)    


# In[238]:


# Building Data pipeline for Numerical and categorical attributes

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelBinarizer


num_attribs = list(housing_num)
cat_attribs = ["ocean_proximity"]

num_pipeline = Pipeline([
        ('selector', DataFrameSelector(num_attribs)),
        ('imputer', Imputer(strategy="median")),
        ('attribs_adder', CombinedAttributesAdder()),
        ('std_scaler', StandardScaler()),
    ])

cat_pipeline = Pipeline([
        ('selector', DataFrameSelector(cat_attribs)),
        ('cat_encoder', MyLabelBinarizer()),
    ])

#Feature Union

from sklearn.pipeline import FeatureUnion

full_pipeline = FeatureUnion(transformer_list=[
        ("num_pipeline", num_pipeline),
        ("cat_pipeline", cat_pipeline),
    ])
housing_prepared = full_pipeline.fit_transform(housing)
housing_prepared.shape


# In[ ]:

# In[ ]:


#Step 7: Train Your Model and measure performance

# 1. Linear Regression

from sklearn.linear_model import LinearRegression

lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

from sklearn.metrics import mean_squared_error
housing_predictions = lin_reg.predict(housing_prepared)
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)


from sklearn.metrics import mean_absolute_error
lin_mae = mean_absolute_error(housing_labels, housing_predictions)

lin_mae, lin_rmse


# In[ ]:


# 2. Decision Tress

from sklearn.tree import DecisionTreeRegressor

tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(housing_prepared, housing_labels)

housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)

from sklearn.metrics import mean_absolute_error
lin_mae = mean_absolute_error(housing_labels, housing_predictions)

tree_rmse = np.sqrt(tree_mse)
tree_rmse,lin_mae


# In[ ]:


# 3. Random Forests

from sklearn.ensemble import RandomForestRegressor

forest_reg = RandomForestRegressor(random_state=42)
forest_reg.fit(housing_prepared, housing_labels)

housing_predictions = forest_reg.predict(housing_prepared)
forest_mse = mean_squared_error(housing_labels, housing_predictions)
forest_rmse = np.sqrt(forest_mse)
forest_rmse


# In[ ]:


# Compute Cross validation scores for all models

from sklearn.model_selection import cross_val_score

def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())

# Scores for linear regression
lin_scores = cross_val_score(lin_reg, housing_prepared, housing_labels,
                             scoring="neg_mean_squared_error", cv=10)
lin_rmse_scores = np.sqrt(-lin_scores)
display_scores(lin_rmse_scores)


#Scores for Decision tress
scores = cross_val_score(tree_reg, housing_prepared, housing_labels,
                         scoring="neg_mean_squared_error", cv=10)
tree_rmse_scores = np.sqrt(-scores)
display_scores(tree_rmse_scores)

#Scores for Random forests
forest_scores = cross_val_score(forest_reg, housing_prepared, housing_labels,
                                scoring="neg_mean_squared_error", cv=10)
forest_rmse_scores = np.sqrt(-forest_scores)
display_scores(forest_rmse_scores)


# In[ ]:


#Step 8: Evaluating on test set

final_model = forest_reg

X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()

X_test_prepared = full_pipeline.transform(X_test)
final_predictions = final_model.predict(X_test_prepared)

final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)

print(final_rmse)

