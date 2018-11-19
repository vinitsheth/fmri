#Starplus experimentation
from dataExtract_With_PCA import extractData, trainPCA
from KNN_model import trainKNN, predictKNN, predictKNNConfBinary, computeROC
import numpy as np
import matplotlib.pyplot as plt
subList=['04799','04847','04820','05710','05675','05680']
rois=['CALC','LIPL','LIPS','LOPER','LDLPFC','LT','LTRIA']
data, labels, subjects=extractData(subList, rois)
subjects=np.squeeze(subjects)
uniqueSubjects=np.unique(subjects)
allConfs=[]
allLabels=[]
compAccuracy=[]
avgAccuracy=0.0
subjectCount=0
for subject in uniqueSubjects: #This is crossval, subject is currrent test subject, train on other subjects
    trainData=data[np.logical_not(subjects==subject),:]
    trainLabels=labels[np.logical_not(subjects==subject),:]
    testData=data[subjects==subject,:]
    testLabels=labels[subjects==subject,:]
    trainLabels=trainLabels-1 #Make labels between 0 and 1
    testLabels=testLabels-1 #Make labels between 0 and 1
    #PCA here
    featMultiplier=trainPCA(trainData,25) #Maybe try 50
    newTrainData=np.matmul(trainData,featMultiplier)
    newTestData=np.matmul(testData,featMultiplier)
    testKLabels=trainKNN(newTrainData, trainLabels, newTestData, testLabels)
    curPreds=predictKNN(testKLabels,5) #You can change the value of k
    acc=np.sum((curPreds[:,0]-testLabels[:,0])==0)/np.shape(curPreds)[0]
    print("Subject: "+str(subject))
    print(acc)
    avgAccuracy= avgAccuracy+acc
    curConfs=predictKNNConfBinary(testKLabels,5)
    if subjectCount==0:
        allConfs=curConfs
        allLabels=testLabels
    else:
        allConfs=np.concatenate((allConfs,curConfs), axis=0)
        allLabels=np.concatenate((allLabels,testLabels), axis=0)
    subjectCount=subjectCount+1
print("Average Accuracy "+str(avgAccuracy/6))
compAccuracy.append(avgAccuracy/6)
pds,pfas=computeROC(allConfs,allLabels) #Pds = TP/(# truth labels==1) Pfas = FP/(# truth labels==0)
plt.plot(pfas,pds)
plt.xlabel('Probability of False Alarm')
plt.ylabel('Probability of Detection')
#ROC for all folds together