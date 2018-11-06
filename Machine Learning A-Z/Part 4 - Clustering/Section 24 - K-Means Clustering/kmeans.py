# Data Preprocessing Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:, [3,4]].values

from sklearn.cluster import KMeans
wcss=[]
for i in range(1,13):
    kmeans=KMeans(n_clusters=i,init='k-means++',n_init=10,max_iter=300,random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
    
    
plt.plot(range(1,13),wcss)
plt.title('Elbow method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

kmeans=KMeans(n_clusters=5,init='k-means++',n_init=10,max_iter=300,random_state=0)
y_kmeans=kmeans.fit_predict(X)

colors=['red','blue','green','cyan','magenta']
titles=['Careful','Standard','Target','Careless','Sensible']
for i in range(0,5):
    plt.scatter(X[y_kmeans == i,0],X[y_kmeans == i, 1],s=100,c=colors[i],label=titles[i])

plt.scatter(kmeans.cluster_centers_[:,0],kmeans.cluster_centers_[:, 1],s=300,c='yellow',label='centroids')
plt.title('Kmeans')
plt.xlabel('Income')
plt.ylabel('Score')
plt.legend()
plt.show()

