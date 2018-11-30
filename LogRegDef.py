# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 23:00:21 2018

@author: aadha
"""
from scipy.stats import uniform
from scipy.optimize import minimize
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd

class LogReg(object):
    
    def __init__(self, data, lambdaa, opt='BFGS', maxiter=100):
        self.data = data
        self.lambdaa = lambdaa
        self.opt = opt
        self.maxiter = maxiter
        
        self.num_params = data.shape[1]
        self.w = uniform.rvs(size=self.num_params) * (2 * 0.1) - 0.1
        self.assessment = []
        
    
    def test(self,data):
        w = self.w[1:]
        b = self.w[0]
        
        y_test = data.iloc[:,-1].values
        X_test = data.iloc[:, :-1].values
        
        predicted_values = pd.Series(np.matmul(X_test, w)) + b
        y_pred = (predicted_values > 0.0) * 1
        
        cm = confusion_matrix(y_test, y_pred)
        return cm
        
    def train(self, data=None):
        if data is None:
            data = self.data
        self.opt_func = optimization_func_call(data, self.lambdaa)
        minimize_options = {'maxiter': self.maxiter, 'disp' :True }
        self.res = minimize(self.opt_func, self.w,  method=self.opt,  tol = 1e-6, options=minimize_options)
        self.w = self.res.x
        return self.w
    
def optimization_func_call(data, lambdaa):
    
    pos_data = data[data[168] == 1]
    pos_data = pos_data.iloc[:,:-1].values.tolist()
    neg_data = data[data[168] == 0]
    neg_data = neg_data.iloc[:,:-1].values
    
    def log_likelihood(weights):
        #
        # Separate weights
        w = weights[1:]
        b = weights[0]
        #
        # Ge the norm of weights
        w_norm = np.dot(w, w)
        #
        # Sum over positive examples
        pos_exp = -1 * pd.Series(np.matmul(pos_data,w)+b)
        pos_sigmoid = 1 / (1+np.exp(pos_exp))
        pos_sum = sum(pos_sigmoid)
        #
        #Sum over negative examples
        neg_exp = -1 * pd.Series(np.matmul(neg_data,w)+b)
        neg_sigmoid = 1 / (1+np.exp(neg_exp))
        neg_sum = sum(neg_sigmoid)
        #
        return (0.5 * w_norm) + lambdaa * (pos_sum + neg_sum)

    return log_likelihood
    