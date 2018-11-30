# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:23:07 2018

@author: Aadhavan Sadasivam
"""

#from LogRegDef import LogReg, optimization_func_call
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from scipy.stats import uniform
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
       
        
pictureFrame = []
sentenceFrame = []
for i in range(1,7):
    
    frame1 = pd.read_csv('Data\sentenceVSpicture\picture\picture_individual{}.csv'.format(i))
    frame2 = pd.read_csv('Data\sentenceVSpicture\sentence\sentence_individual{}.csv'.format(i))
    frame1['label'] = 0
    frame2['label'] = 1
    pictureFrame.append(frame1)
    sentenceFrame.append(frame2)
    
for i in range(len(sentenceFrame)):
    print("Testing on subject {}".format(i+1))
    Test = pd.concat([pictureFrame[i], sentenceFrame[i]], axis = 0)
    Train = pd.DataFrame(columns = Test.columns)
    for j in range(len(sentenceFrame)):
        if j != i:
            Train = pd.concat([Train, pictureFrame[j], sentenceFrame[j]], axis = 0)
    X_train = Train.iloc[:,:-2].values
    X_test = Test.iloc[:,:-2].values
    y_train = Train.iloc[:,-1].values.tolist()
    y_test = Test.iloc[:,-1].values.tolist()
        
    # Feature Scaling
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    # Fitting Logistic Regression to the Training set
    classifier = LogisticRegression()
  
    classifier.fit(X_train, y_train)
    
    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    # Making the Confusion Matrix
       
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print("accuracy:", (cm[0][0]+cm[1][1])/(sum(cm[0])+sum(cm[1])) )
    #print("max_iter = ", classifier.n_iter_)