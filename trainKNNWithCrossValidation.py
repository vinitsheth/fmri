#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""

#Starplus experimentation
from dataExtract_With_PCA import extractData, trainPCA
from KNN_model import trainKNN, predictKNN
import numpy as np

if __name__ == "__main__":
    
    subList=['04799','04847','05710','05675','05680']
    rois=['CALC','LIPL','LIPS','LOPER','LDLPFC','LT','LTRIA']
    data, labels, subjects=extractData(subList, rois)
    subjects=np.squeeze(subjects)
    uniqueSubjects=np.unique(subjects)
    for subject in uniqueSubjects: #This is crossval, subject is currrent test subject, train on other subjects
        print("Testing subject")
        print(subject)
        trainData=data[np.logical_not(subjects==subject),:]
        trainLabels=labels[np.logical_not(subjects==subject),:]
        testData=data[subjects==subject,:]
        testLabels=labels[subjects==subject,:]
        #PCA here
        featMultiplier=trainPCA(trainData,100) #Maybe try 50
        newTrainData=np.matmul(trainData,featMultiplier)
        newTestData=np.matmul(testData,featMultiplier)
        testKLabels=trainKNN(newTrainData, trainLabels, newTestData, testLabels)
        curPreds=predictKNN(testKLabels,5) #You can change the value of k
        acc=np.sum((curPreds[:,0]-testLabels[:,0])==0)/np.shape(curPreds)[0]
        print("Subject: "+str(subject))
        print(acc)
