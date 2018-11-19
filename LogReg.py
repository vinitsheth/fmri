# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:23:07 2018

@author: aadha
"""
import pandas as pd

sentence = pd.read_csv('Data/sentenceVSpicture/sentence/sentence1.csv')
picture = pd.read_csv('Data/sentenceVSpicture/picture/picture1.csv')
rest = pd.read_csv('Data/sentenceVSpicture/rest/rest1.csv')


for k in range(2,7):
    frame = pd.read_csv('Data/sentenceVSpicture/picture/picture'+str(k)+'.csv')
    frame1 = pd.read_csv('Data/sentenceVSpicture/sentence/sentence'+str(k)+'.csv')
    frame2 = pd.read_csv('Data/sentenceVSpicture/rest/rest'+str(k)+'.csv')
    picture = pd.concat([picture,frame],axis=0)
    sentence = pd.concat([sentence,frame1],axis=0)
    rest = pd.concat([rest,frame2],axis=0)
    
sentence['label'] = 0
picture['label'] = 1
rest['label'] =  2

data = pd.concat([sentence,rest,picture],axis = 0)

X = data.iloc[:, :-2].values
y = data.iloc[:, -1].values


from sklearn.model_selection import StratifiedKFold
skf = StratifiedKFold(n_splits=8,random_state = 0)

for train_index, test_index in skf.split(X, y):
    #print(train_index,test_index)
    X_train = data.iloc[train_index,:-2].values
    X_test = data.iloc[test_index,:-2].values
    y_train = data.iloc[train_index,-1].values
    y_test = data.iloc[test_index,-1].values
            
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    """
    # Applying PCA
    from sklearn.decomposition import PC
    pca = PCA(n_components = 1000)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    explained_variance = pca.explained_variance_ratio_
    """
    
    # Fitting Logistic Regression to the Training set
    from sklearn.linear_model import LogisticRegression
    classifier = LogisticRegression(random_state = 0,max_iter=1000)
    classifier.fit(X_train, y_train)
     
    # Predicting the Test set results
    y_pred = classifier.predict(X_test)
     
    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
       
    
    print("Accuracy",(cm[0][0]+cm[1][1])/(sum(cm[0])+sum(cm[1])))
    print(cm)
"""
"""
from sklearn.model_selection import StratifiedKFold
skf = StratifiedKFold(n_splits=8,random_state = 0)
"""
feature_accuracy = []
y = data.iloc[:, -1].values

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


for i in range(4634):
    X = data.iloc[:, i].values.reshape(-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.22, random_state=42)
                
    X_train = X_train.reshape(-1, 1)
    X_test = X_test.reshape(-1, 1)
    
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
    accuracy = (cm[0][0]+cm[1][1])/(sum(cm[0])+sum(cm[1]))
    #print("Accuracy - Feature"+str(i+1)+":", accuracy)
    feature_accuracy.append(accuracy)
    
final_accuracy = pd.Series(feature_accuracy)
"""