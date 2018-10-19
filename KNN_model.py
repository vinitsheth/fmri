#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 08:39:15 2018

@author: manjusharavindranath
"""

from load_dataset import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
(trainLabs,trainImgs)=read(dataset = "training", path = "/Users/manjusharavindranath/Documents/CSE575/Assignments/Assignment2/MNIST/")
(testLabs,testImgs)=read(dataset = "testing", path = "/Users/manjusharavindranath/Documents/CSE575/Assignments/Assignment2/MNIST/")
##plt.imshow(trainImgs[1,:,:])
trainImgs=np.reshape(trainImgs,(60000,28*28))/255
testImgs=np.reshape(testImgs,(10000,28*28))/255
def trainKNN(dataTrain, labTrain, dataTest, labTest):
    retKLabels=np.zeros((np.shape(dataTest)[0],100)) #Returns the train labels of the 100 closest training data to each test data
    for i in range(0,np.shape(dataTest)[0]):
        curDataTest=dataTest[i,:]
        allDistsCurTest=np.zeros((np.shape(dataTrain)[0],1))
        for j in range(0,np.shape(dataTrain)[0]):
            curDataTrain=dataTrain[j,:]
            allDistsCurTest[j]=distance.euclidean(curDataTest,curDataTrain)
        indsClosest=np.argsort(allDistsCurTest[:,0])[0:100]
        labsClosest=labTrain[indsClosest]
        retKLabels[i,:]=np.reshape(labsClosest, (1,100))
        if i%500==0:
            print("Done calculating distance to "+str(i))
    return retKLabels
#testKLabels=trainKNN(trainImgs, trainLabs, testImgs, testLabs)
testKLabels=trainKNN(trainImgs, trainLabs, testImgs, testLabs)

def predictKNN(kLabels,k):
    retPrediction=np.zeros((np.shape(kLabels)[0],1))
    for i in range(0,np.shape(kLabels)[0]):
        neighborLabelsCurTest=kLabels[i,:][0:k]
        (values,counts) = np.unique(neighborLabelsCurTest,return_counts=True)
        ind=np.argmax(counts)
        curLabel=values[ind]
        retPrediction[i,0]=curLabel
    return retPrediction
accK=[]
kVals=[1, 3, 5, 10, 30, 50, 70, 80, 90, 100]
for k in kVals:
    curPreds=predictKNN(testKLabels,k)
    accK.append(np.sum((curPreds[:,0]-testLabs)==0)/10000)
plt.plot(kVals, accK)
plt.xlabel('k-Value')
plt.ylabel('Test Acc')