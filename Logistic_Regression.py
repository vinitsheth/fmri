from __future__ import division
import numpy as np
from matplotlib import pyplot
import matplotlib as mpl


class LogisticRegressionOVA(object):
    def __init__(self, eta=0.1, n_iter=50):
        self.eta = eta
        self.n_iter = n_iter

    def fit(self, X, y):
        X = np.insert(X, 0, 1, axis=1)
        self.w = []
        m = X.shape[0]

        for i in np.unique(y):
            y_copy = np.where(y == i, 1, 0)
            w = np.ones(X.shape[1])

            for _ in range(self.n_iter):
                output = X.dot(w)
                errors = y_copy - self._sigmoid(output)
                w += self.eta / m * errors.dot(X)
            self.w.append((w, i))
        return self

    def predict(self, X):
        return [self._predict_one(i) for i in np.insert(X, 0, 1, axis=1)]

    def _predict_one(self, x):
        return max((x.dot(w), c) for w, c in self.w)[1]

    def score(self, X, y):
        return sum(self.predict(X) == y) / len(y)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
