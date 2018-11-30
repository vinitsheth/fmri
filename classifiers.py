# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:07:01 2018

@author: 
"""

import argparse
import pandas as pd
import os

from data_extract import extractData
from utils.constants import classifiers, PathToSubjects

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, roc_auc_score,accuracy_score
from sklearn.model_selection import StratifiedKFold

#from GNB import GaussianNB
from sklearn.naive_bayes import GaussianNB

def PrepareData(meta, info, data):
    
    Picture = []
    Sentence = []
    
    for i in range(meta['ntrials']):
        TrialInfo = info[i]
        TrialData = data[i]
        cond = TrialInfo['cond']
        stimulus = TrialInfo['firstStimulus']
        if cond == 2 or cond == 3:
            pic, sen = [],[]
            if stimulus == 'P':
                pic = TrialData[:16]
                sen = TrialData[16:32]
            else:
                pic = TrialData[16:32]
                sen = TrialData[:16]
            
            Picture.append(sum(pic, []))
            Sentence.append(sum(sen, []))
            #Picture.append(pic)
            #Sentence.append(sen)
  
    SentenceFrame = pd.DataFrame.from_records(Sentence)
    PictureFrame = pd.DataFrame.from_records(Picture)
    SentenceFrame['label'] = 0
    PictureFrame['label'] = 1
    data = pd.concat([SentenceFrame, PictureFrame], axis = 0)
    return data

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
        
        classifier = GaussianNB()
        
        classifier.fit(X_train, y_train)

        score = classifier.score(X_test, y_test)
        
        accuracy.append(score)
        i+=1
    print(sum(accuracy)/len(accuracy))
    return sum(accuracy)/len(accuracy)   
    
if __name__ == "__main__":
    
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    
    #
    #input algorithm for classification
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-model', type =int, help='Classification Algorithm. 1-GNB, 2-LogReg, 3-KNN, 4-SVM, 5- Random Forest')          
    args = vars(parser.parse_args())
    
    model = args['model']
    print(classifiers[model-1])
    
    MatFilesPath = []
    
    for files in os.listdir(PathToSubjects):
        MatFilesPath.append(os.path.join(PathToSubjects, files))
    
    acc = []
    #
    #Load data for each subject
    for i in range(len(MatFilesPath)):
        print("Loading data from matfile for subject {}".format(i+1))
        file = MatFilesPath[i]
        meta, info, data = extractData(file)
        print("Preparing data for classification on subject {}".format(i+1))
        
        print("Classification on subject {}".format(i+1))
        ClassificationData = PrepareData(meta, info, data)
        accuracy = []
        for k in range(2,42,2):
            
            accuracy.append(stratified(ClassificationData, k))
            print("Fold {} : {}".format(k, accuracy[-1]))
            
        acc.append(max(accuracy))