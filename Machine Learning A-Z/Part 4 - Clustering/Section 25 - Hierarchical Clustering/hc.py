# Data Preprocessing Template

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Mall_Customers.csv')
X = dataset.iloc[:, [3,4]].values

import scipy.cluster.hierarchy as sch
dendogram=sch.dendrogram(sch.linkage(X,method='ward'))
plt.title('Dendogram')
plt.xlabel('customers')
plt.ylabel('Distance')
plt.show()

from sklearn.cluster import AgglomerativeClustering
hc=AgglomerativeClustering(n_clusters=5,affinity='euclidean',linkage='ward')
y_hc=hc.fit_predict(X)


colors=['red','blue','green','cyan','magenta']
titles=['Careful','Standard','Target','Careless','Sensible']
for i in range(0,5):
    plt.scatter(X[y_hc == i,0],X[y_hc == i, 1],s=100,c=colors[i],label=titles[i])

plt.title('HC')
plt.xlabel('Income')
plt.ylabel('Score')
plt.legend()
plt.show()