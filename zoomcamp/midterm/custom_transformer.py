import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import mutual_info_regression


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.indices = []

    def fit(self, X, y=None):
        scores = mutual_info_regression(X, y, random_state=43)
        self.indices = np.where(scores == 0.0)[0]
        X = np.delete(X, tuple(self.indices), axis=1)
        return self

    def transform(self, X, y=None):
        return np.delete(X, tuple(self.indices), axis=1)
