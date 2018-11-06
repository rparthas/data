# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

# Cleaning the texts
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting Naive Bayes to the Training set
#0.73 0.883495145631 0.684210526316 0.771186440678
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
#0.71 0.543689320388 0.835820895522 0.658823529412
from sklearn.ensemble import RandomForestClassifier
#classifier=RandomForestClassifier(n_estimators=90,criterion='entropy')
#0.735 0.805825242718 0.715517241379 0.75799086758
from sklearn.svm import SVC
#classifier =SVC(kernel='rbf',random_state=0)
#0.755 0.747572815534 0.77 0.758620689655
from sklearn.linear_model import LogisticRegression
#classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)


# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)


accuracy=(cm[0,0]+cm[1,1])/(cm[0,0]+cm[0,1]+cm[1,0]+cm[1,1])
precision=cm[1,1]/(cm[1,1]+cm[1,0])
recall=cm[1,1]/(cm[1,1]+cm[0,1])
f1=2*precision*recall/(precision+recall)
print(accuracy,precision,recall,f1)