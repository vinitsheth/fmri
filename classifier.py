# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:39:42 2018

@author: Aadhavan Sadasivam
"""


import pandas as pd
import numpy as np
from scipy.stats import uniform
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_auc_score,accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from scipy.optimize import minimize
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

def stratified(data, fold):
    
    skf = StratifiedKFold(n_splits=fold, random_state = 42)
    X = data.iloc[:,:-1].values
    y = data.iloc[:,-1].values.tolist()
    i = 0
    accuracy = []
    for train_index, test_index in skf.split(X, y):
        
        X_train, X_test = data.iloc[train_index,:-1].values, data.iloc[test_index,:-1].values
        y_train, y_test = data.iloc[train_index,-1].values.tolist(), data.iloc[test_index,-1].values.tolist()
    
        # Feature Scaling
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        
        """
        # Applying PCA
        pca = PCA(n_components = 50)
        X_train = pca.fit_transform(X_train)
        X_test = pca.transform(X_test)
        """
        
        #
        #choose classifier
        
        classifier = LogisticRegression(penalty= 'l2', C=.01, max_iter = 1000, tol = 1e-6, solver = 'lbfgs', fit_intercept=True)
        #classifier = GaussianNB()
        #classifier = KNeighborsClassifier(n_neighbors = 5)
        #classifier = SVC(kernel = 'linear')
        #classifier = RandomForestClassifier(n_estimators = 1000)
        
        # Fitting classifier to the Training set
        classifier.fit(X_train, y_train)
        
        
        # Predicting the Test set results
        y_pred = classifier.predict(X_test)

        # Making the Confusion Matrix
        #cm = confusion_matrix(y_test, y_pred)
        accuracy.append(accuracy_score(y_test, y_pred))
       
        i+=1
   
    return sum(accuracy)/len(accuracy)   