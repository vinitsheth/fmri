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