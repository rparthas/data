#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler,LabelEncoder,MinMaxScaler,OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.linear_model import Ridge,Lasso,LinearRegression
import seaborn as sns
from sklearn.feature_selection import SelectKBest,f_regression,RFE


# In[39]:


data = pd.read_csv('trainingData.csv')


# In[40]:


data.describe()


# In[41]:


data.head()


# ## Descriptive Analytics

# In[42]:


data.isnull().sum()


# In[43]:


clean_data = data.drop(columns=['Id']).dropna()
clean_data.head()


# In[44]:


sns.set()
plot_data = clean_data.copy(deep=True)
le = LabelEncoder()
for label in ['city','sex','social_class','primary_business','secondary_business','type_of_house','loan_purpose']:
    plot_data[label] = le.fit_transform(plot_data[label])
plt.figure(figsize=(24,17))
ax = sns.heatmap(plot_data.corr(),cmap="YlGnBu", square=True,annot=True, fmt=".2f")


# In[45]:


print(clean_data['sex'].value_counts())
sns.countplot(clean_data['sex'], color='green')


# In[46]:


clean_data['city'].value_counts()


# In[47]:


plt.figure(figsize=(18,4))
print(clean_data['loan_purpose'].value_counts())
sns.countplot(clean_data['loan_purpose'], color='green')


# In[48]:


clean_data['social_class'].value_counts()


# In[49]:


clean_data['primary_business'].value_counts()


# In[50]:


plt.figure(figsize=(10,2))
print(clean_data['secondary_business'].value_counts())
sns.countplot(clean_data['secondary_business'], color='green')


# In[51]:


plt.figure(figsize=(10,2))
print(clean_data['type_of_house'].value_counts())
sns.countplot(clean_data['type_of_house'], color='green')


# ## Preprocessing

# In[171]:


clean_data = pd.get_dummies(data.drop(columns=['Id']).dropna(), columns= ['city','sex','social_class','primary_business','secondary_business','type_of_house','loan_purpose'])


# In[172]:


cols = clean_data.columns.drop('loan_amount')
sc_X = StandardScaler()
sc_y = StandardScaler()
X = sc_X.fit_transform(clean_data.loc[:,clean_data.columns != 'loan_amount'])
y = sc_y.fit_transform(clean_data.loc[:,clean_data.columns == 'loan_amount'])
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size =0.2)


# ## Feature Selection

# In[173]:


def return_best_features(features,target,cols):
    bestfeatures = SelectKBest(score_func=f_regression, k='all')
    fit = bestfeatures.fit(features,target)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(cols)
    featureScores = pd.concat([dfcolumns,dfscores,pd.DataFrame(bestfeatures.pvalues_)],axis=1)
    featureScores.columns = ['Specs','Score','Pvalue'] 
    sorted = featureScores.sort_values(by='Score',ascending=False)
    return sorted[sorted['Pvalue'] <= 0.05].iloc[:,0]


# In[176]:


best_features = np.asarray(return_best_features(X,y,cols))
print(best_features)


# ## Prediction

# In[175]:


model = Ridge(random_state =42)
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
print(f"MSE:{mean_squared_error(y_test,y_pred):.4f}, R2:{r2_score(y_test,y_pred):.4f}")
plt.scatter(range(y_test.shape[0]),y_test,color='g')
plt.plot(range(y_test.shape[0]),y_pred,color='r')


# Multi........

# In[69]:


best_feature_map = {}
for value in clean_data['loan_purpose'].unique():
    rel_data = clean_data[clean_data['loan_purpose'] == value].drop('loan_purpose',axis=1)
    X,y = minMaxScaling(rel_data)
    cols = clean_data.columns.drop('loan_amount').drop('loan_purpose')
    best_feature_map[value] = np.asarray(return_best_features(X,y,cols))


# In[70]:


remove_key = []
for key in best_feature_map:
    print(f"{key} -> {best_feature_map[key].shape}")
    if best_feature_map[key].shape[0] == 0:
        remove_key.append(key)

for key in remove_key:
    best_feature_map.pop(key,'None')


# In[72]:


def plot(y_test,y_pred):
    plt.scatter(range(y_test.shape[0]),y_test,color='g')
    plt.plot(range(y_test.shape[0]),y_pred,color='r')


# In[71]:


def scale(features, target):
    sc_X = StandardScaler()
    sc_y = StandardScaler()
    X = sc_X.fit_transform(features)
    y = sc_y.fit_transform(target)
    return X,y,sc_X,sc_y


# In[73]:


def predict(features,target):
    


# ## Prediction

# In[74]:


result = {}
for loan_purpose in best_feature_map:
    print(f"Running for loan purpose {loan_purpose}")
    cols = np.append(best_feature_map[loan_purpose],'loan_amount')
    data_for_loan_purpose = clean_data[clean_data['loan_purpose'] ==loan_purpose][cols]
    X = data_for_loan_purpose.loc[:,data_for_loan_purpose.columns != 'loan_amount']
    y = data_for_loan_purpose.loc[:,data_for_loan_purpose.columns == 'loan_amount']
    y_test,y_pred,model= predict(X,y)
    result[loan_purpose] = y_test,y_pred,model


# In[75]:


for key in result:
  y_test,y_pred,_ = result[key]
  print(f"MAE for {key} is {mean_absolute_error(y_test,y_pred):.4f}")
  plt.figure()
  plt.title(f"Pred vs Test({key})")
  plot(y_test,y_pred)


# In[76]:


cols = np.append(best_features,'loan_amount')
data_for_loan_purpose = clean_data[cols]
X = data_for_loan_purpose.loc[:,data_for_loan_purpose.columns != 'loan_amount']
y = data_for_loan_purpose.loc[:,data_for_loan_purpose.columns == 'loan_amount']

y_test,y_pred,model= predict(X,y)
print(f"MAE  is {mean_absolute_error(y_test,y_pred):.4f}")
plt.figure()
plt.title(f"Pred vs Test")
plot(y_test,y_pred)


clean_data = data.drop(columns=['Id']).dropna()
enc = OrdinalEncoder()
X= enc.fit_transform(clean_data.loc[:,clean_data.columns != 'loan_amount'])
y =  clean_data.loc[:,clean_data.columns == 'loan_amount']



bestfeatures = SelectKBest(score_func=f_regression, k='all')
fit = bestfeatures.fit(X_train,y_train)
# plot the scores
plt.bar([i for i in range(len(fit.scores_))], fit.scores_)
plt.show()


bestfeatures = SelectKBest(score_func=f_regression, k=4)
fit = bestfeatures.fit(X_train,y_train)
np.sort(fit.scores_)[::-1]
X_train = fit.transform(X_train)
X_test = fit.transform(X_test)

model = Ridge(random_state=42)
model.fit(X_train,y_train)
y_pred = model.predict(X_test)
print(f"MSE:{mean_squared_error(y_test,y_pred):.4f}, R2:{r2_score(y_test,y_pred):.4f}")



model = Ridge(random_state=42)

rfe = RFE(model, 4)
fit = rfe.fit(X_train, y_train)
df = pd.DataFrame()
df['Features'] = clean_data.columns.drop('loan_amount')
df['rank'] = fit.ranking_
print(df[df['rank']<=1])

X_train_f = fit.transform(X_train)
X_test_f = fit.transform(X_test)


model.fit(X_train_f,y_train)
y_pred = model.predict(X_test_f)
print(f"MSE:{mean_squared_error(y_test,y_pred):.4f}, R2:{r2_score(y_test,y_pred):.4f}")
