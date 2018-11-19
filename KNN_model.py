import numpy as np
from scipy.spatial import distance
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""
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
    return retKLabels

def predictKNN(kLabels,k):
    retPrediction=np.zeros((np.shape(kLabels)[0],1))
    for i in range(0,np.shape(kLabels)[0]):
        neighborLabelsCurTest=kLabels[i,:][0:k]
        (values,counts) = np.unique(neighborLabelsCurTest,return_counts=True)
        ind=np.argmax(counts)
        curLabel=values[ind]
        retPrediction[i,0]=curLabel
    return retPrediction

def predictKNNConfBinary(kLabels,k): #Binary means classes are just 0 or 1
    retPrediction=np.zeros((np.shape(kLabels)[0],1))
    for i in range(0,np.shape(kLabels)[0]):
        neighborLabelsCurTest=kLabels[i,:][0:k]
        retPrediction[i,0]=np.sum(neighborLabelsCurTest)/len(neighborLabelsCurTest)
    return retPrediction



def computeROC(confVals, labels):
    #Sweep through thresholds
    thresholds=list(np.unique(confVals))
    #Need a -1 threshold
    thresholds=[-1]+thresholds
    pds=[]
    pfas=[]
    for curThresh in thresholds:
        #If the confidence is above threshold assign class 1, otherwise assign class 0
        curLabelsThresh=confVals>curThresh
        #Compute pd and pf
        indexPos=labels==1
        indexNeg=labels==0
        curPd=np.sum(curLabelsThresh[indexPos])/np.sum(labels) #Sum of true positives divided by number of positives
        curPfa=np.sum(curLabelsThresh[indexNeg])/np.sum(labels==0) #Sum of false positives divided by number of negatives
        pds.append(curPd)
        pfas.append(curPfa)
    return pds,pfas  