# Satrajit Maitra
accuracy04799 = [0.69140625, 0.6953125, 0.640625, 0.66796875, 0.6640625]
accuracy04820 = [0.7421875, 0.6796875, 0.6640625, 0.640625, 0.7109375]
accuracy04847 = [0.8046875, 0.7578125, 0.77734375, 0.78515625, 0.76171875]
accuracy05675 = [0.72265625, 0.69921875, 0.69140625, 0.67578125, 0.63671875]
accuracy05680 = [0.6640625, 0.68359375, 0.72265625, 0.70703125, 0.69140625]
accuracy05710 = [0.73828125, 0.7109375, 0.73828125, 0.7421875, 0.71484375]

import os
from scipy.io import loadmat
import dataExtract_latest
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor

mat04799  = loadmat('/Users/satrajitmaitra/Downloads/Data/data-starplus-04799-v7.mat')
mat04820  = loadmat('/Users/satrajitmaitra/Downloads/Data/data-starplus-04820-v7.mat')
mat04847  = loadmat('/Users/satrajitmaitra/Downloads/Data/data-starplus-04847-v7.mat')
mat05675  = loadmat('/Users/satrajitmaitra/Downloads/Data/data-starplus-05675-v7.mat')
mat05680  = loadmat('/Users/satrajitmaitra/Downloads/Data/data-starplus-05680-v7.mat')
mat05710  = loadmat('/Users/satrajitmaitra/Downloads/Data/data-starplus-05710-v7.mat')

mata04799 = dataExtract_latest.getMeta(mat04799)
mata04820 = dataExtract_latest.getMeta(mat04820)
mata04847 = dataExtract_latest.getMeta(mat04847)
mata05675 = dataExtract_latest.getMeta(mat05675)
mata05680 = dataExtract_latest.getMeta(mat05680)
mata05710 = dataExtract_latest.getMeta(mat05710)

info04799 = []
sentence04799 = []
picture04799 = []
rawData04799 = mat04799['data']
for i in range(mata04799['ntrials']):
    infoOfGivenTrial = dataExtract_latest.getInfoFromList(mat04799,i)
    info04799.append(infoOfGivenTrial)
    if infoOfGivenTrial['cond'] == 2 or infoOfGivenTrial['cond'] == 3:
        if infoOfGivenTrial['firstStimulus'] == 'P':
            for j in range(16):
                picture04799.append(rawData04799[i][0][j])
            for j in range(16,32):
                sentence04799.append(rawData04799[i][0][j])
        elif infoOfGivenTrial['firstStimulus'] == 'S':
            for j in range(16):
                sentence04799.append(rawData04799[i][0][j])
            for j in range(16,32):
                picture04799.append(rawData04799[i][0][j])

data04799 = sentence04799+picture04799
labels04799 = [1]*len(sentence04799) + [0]*len(picture04799)

accuracy04799 = []
for i in range(5):
    x_train04799, x_test04799 , y_train04799, y_test04799 = train_test_split(data04799,labels04799,test_size = 0.2)
    rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
    rf.fit(x_train04799, y_train04799)
    predictions = list(rf.predict(x_test04799))
    predicted_classes = []
    for i in range(len(predictions)):
        if predictions[i] > 0.5:
            predicted_classes.append(1)
        else:
            predicted_classes.append(0)
    accuracy04799.append(metrics.accuracy_score(y_test04799, predicted_classes))

mean_accuracy04799 = np.mean(accuracy04799)

# USING ROI

accuracyforeachROI04799 = []
for i in range(25):
    print i
    cols = dataExtract_latest.getColumsFromROI('04799',i)
    newData = []

    for d in data04799:
        temp = []
        for col in cols:
            temp.append(d[col-1])
        newData.append(temp)
    x_train04799, x_test04799 , y_train04799, y_test04799 = train_test_split(newData,labels04799,test_size = 0.2)
    rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
    rf.fit(x_train04799, y_train04799)
    predictions = list(rf.predict(x_test04799))
    predicted_classes = []
    for i in range(len(predictions)):
        if predictions[i] > 0.5:
            predicted_classes.append(1)
        else:
            predicted_classes.append(0)
    accuracyforeachROI04799.append(metrics.accuracy_score(y_test04799, predicted_classes))

top7Rois = np.argpartition(accuracyforeachROI04799, -7)[-7:]
cols = []
for i in top7Rois:
    cols.extend(dataExtract_latest.getColumsFromROI('04799',i))

newData = []

for d in data04799:
    temp = []
    for col in cols:
        temp.append(d[col-1])
    newData.append(temp)
x_train04799, x_test04799 , y_train04799, y_test04799 = train_test_split(newData,labels04799,test_size = 0.2)
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
rf.fit(x_train04799, y_train04799)
predictions = list(rf.predict(x_test04799))
predicted_classes = []
for i in range(len(predictions)):
    if predictions[i] > 0.5:
        predicted_classes.append(1)
    else:
        predicted_classes.append(0)

accuracyfortop7ROIs04799 = metrics.accuracy_score(y_test04799, predicted_classes)


top5Rois = np.argpartition(accuracyforeachROI04799, -5)[-5:]
cols = []
for i in top5Rois:
    cols.extend(dataExtract_latest.getColumsFromROI('04799',i))

newData = []

for d in data04799:
    temp = []
    for col in cols:
        temp.append(d[col-1])
    newData.append(temp)
x_train04799, x_test04799 , y_train04799, y_test04799 = train_test_split(newData,labels04799,test_size = 0.2)
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
rf.fit(x_train04799, y_train04799)
predictions = list(rf.predict(x_test04799))
predicted_classes = []
for i in range(len(predictions)):
    if predictions[i] > 0.5:
        predicted_classes.append(1)
    else:
        predicted_classes.append(0)

accuracyfortop5ROIs04799 = metrics.accuracy_score(y_test04799, predicted_classes)
