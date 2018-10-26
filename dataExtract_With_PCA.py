# -*- coding: utf-8 -*-
"""
@author: Vinit Seth, Aadhavan Sadasivam, Manjusha Ravindranath

###Have to write file description###
"""

from scipy.io import loadmat
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def getMeta(matfile):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018


    ************* Method Description ******************

    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Returns Dictoinary which contains following values at index

    study - gives the name of the fMRI study

    subject - gives the identifier for the human subject

    ntrials - gives the number of trials in this dataset

    nsnapshots -  gives the total number of images in the dataset

    nvoxels - gives the number of voxels (3D pixels) in each image

    dimx - gives the maximum x coordinate in the brain image. The minimum x
    coordinate is x=1.  meta.dimy and meta.dimz give the same information for the y
    and z coordinates.
    """

    meta = {}
    #
    #print( matfile['meta'][0][0])
    meta['study'] = matfile['meta'][0][0]['study'][0].encode('utf-8')
    meta['subject'] = matfile['meta'][0][0]['subject'][0].encode('utf-8')
    meta['ntrials'] = matfile['meta'][0][0]['ntrials'][0][0]
    meta['nsnapshots'] = matfile['meta'][0][0]['nsnapshots'][0][0]
    meta['nvoxels'] = matfile['meta'][0][0]['nvoxels'][0][0]
    meta['dimx'] = matfile['meta'][0][0]['dimx'][0][0]
    meta['dimy'] = matfile['meta'][0][0]['dimy'][0][0]
    meta['dimz'] = matfile['meta'][0][0]['dimz'][0][0]
    meta['colToCoord'] = matfile['meta'][0][0]['colToCoord'] #added to grab colToCoord to fill cubes
    meta['colToROI'] = matfile['meta'][0][0]['colToROI']
    return meta


def getInfoFromList(matfile, trialNumber):
    
    """
    Author:- Manjusha Ravindranath
    Date:- 09/23/2018
    
    Input: 
        matFileData: loaded mat data file of a subject
        trialNumber: trial Number we want info on
    Output:
        The trial info of the subject corresponding to the trial Number 
    info(18)
 mint: 894
 maxt: 948
 cond: 2       
 firstStimulus: 'P'
 sentence: ''It is true that the star is below the plus.''
 sentenceRel: 'below'
 sentenceSym1: 'star'
 sentenceSym2: 'plus'
 img: sap
 actionAnswer: 0
 actionRT: 3613

info.mint gives the time of the first image in the interval (the minimum time)

info.maxt gives the time of the last image in the interval (the maximum time)

info.cond has possible values 0,1,2,3.  Cond=0 indicates the data in this
segment should be ignored. Cond=1 indicates the segment is a rest, or fixation
interval.  Cond=2 indicates the interval is a sentence/picture trial in which
the sentence is not negated.  Cond=3 indicates the interval is a
sentence/picture trial in which the sentence is negated.

info.firstStimulus: is either 'P' or 'S' indicating whether this trail was
obtained during the session is which Pictures were presented before sentences,
or during the session in which Sentences were presented before pictures.  The
first 27 trials have firstStimulus='P', the remained have firstStimulus='S'.
Note this value is present even for trials that are rest trials.  You can pick
out the trials for which sentences and pictures were presented by selecting just
the trials trials with info.cond=2 or info.cond=3.

info.sentence gives the sentence presented during this trial.  If none, the
value is '' (the empty string).  The fields info.sentenceSym1,
info.sentenceSym2, and info.sentenceRel describe the two symbols mentioned in
the sentence, and the relation between them.

info.img describes the image presented during this trial.  For example, 'sap'
means the image contained a 'star above plus'.  Each image has two tokens, where
one is above the other.  The possible tokens are star (s), plus (p), and dollar
(d).

info.actionAnswer: has values -1 or 0.  A value of 0 indicates the subject is
expected to press the answer button during this trial (either the 'yes' or 'no'
button to indicate whether the sentence correctly describes the picture).  A
value of -1 indicates it is inappropriate for the subject to press the answer
button during this trial (i.e., it is a rest, or fixation trial).

info.actionRT: gives the reaction time of the subject, measured as the time at
which they pressed the answer button, minus the time at which the second
stimulus was presented.  Time is in milliseconds.  If the subject did not press
the button at all, the value is 0.

    """
    
    info = {}     
     
    info['mint'] = matfile['info'][0][trialNumber]['mint'][0][0]
    info['maxt'] = matfile['info'][0][trialNumber]['maxt'][0][0]
    info['cond'] = matfile['info'][0][trialNumber]['cond'][0][0]  
    info['firstStimulus'] = matfile['info'][0][trialNumber]['firstStimulus'][0][0]
    sentence = matfile['info'][0][trialNumber]['sentence']
    
    if sentence.size > 0 :
        info['sentence']=sentence[0][:].encode('utf-8')
    else:
        info['sentence']=''
        
    sentenceRel = matfile['info'][0][trialNumber]['sentenceRel']   
    if sentenceRel.size > 0 :
        info['sentenceRel'] = sentenceRel[0][:].encode('utf-8')
    else:
        info['sentenceRel']=''    
    sentenceSym1=matfile['info'][0][trialNumber]['sentenceSym1']
    if sentenceSym1.size > 0:
        info['sentenceSym1'] = sentenceSym1[0][:].encode('utf-8')
    else:
        info['sentenceSym1']=''     
    sentenceSym2= matfile['info'][0][trialNumber]['sentenceSym2']  
    if sentenceSym2.size > 0:
        info['sentenceSym2'] = sentenceSym2[0][:].encode('utf-8')
    else:
        info['sentenceSym2']=''     
    img = matfile['info'][0][trialNumber]['img']
    if img.size > 0:
        info['img'] = img[0][0]
    else:
        info['img']=''  
        
    info['actionAnswer'] = matfile['info'][0][trialNumber]['actionAnswer'][0][0]
    info['actionRT'] = matfile['info'][0][trialNumber]['actionRT'][0][0]

         
    return info  
   

def getInfo(matfile, meta):
    """
    Author:- Manjusha Ravindranath
    Date:- 09/23/2018
    
    Input: 
        matFileData: loaded mat data file of a subject
        meta: meta data about the subject
    Output:
        A 2d list containing all the trial info of the subject 
    
    There are 54 trials.
    
    Get all trials in range from 0 th row to 53th row in trialIndices
    """
    
    trialInfoList = []
    trialIndices = meta['ntrials']
    for infoitem in range (0, trialIndices):
        trial = getInfoFromList(matfile,infoitem);
        trialInfoList.append(trial);
    return trialInfoList

def getData(matFileData, meta):
    """
    Author:- Aadhavan Sadasivam
    Date:- 09/23/2018
    
    Input: 
        matFileData: loaded mat data file of a subject
        meta: meta data about the subject
    Output:
        A 2d list containing all the trial data of the subject 
    """
    data = matFileData['data']
    data_array = []
    for item in data:
        #print(item[0].tolist())
        data_array.append(item[0].tolist())
    return data_array
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""
def convertDataToVolume(curInput, colToCoord): #using the metadata coord to cond
    trialVols=np.zeros((np.shape(curInput)[0],64,64,8))
    for curSeqInd in range(0,np.shape(curInput)[0]):
        for i in range(0,np.shape(curInput)[1]):
            trialVols[curSeqInd,colToCoord[i,0]-1,colToCoord[i,1]-1,colToCoord[i,2]-1]=curInput[curSeqInd,i]
    #plt.matshow(trialVols[10,:,:,4])
    #plt.show()
    return trialVols
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""
def trainPCA(inputFeatures, numberComponents):
    cov=np.matmul(np.transpose(inputFeatures),inputFeatures)
    plt.matshow(cov)
    (eigenval,eigenvector)=np.linalg.eig(cov)
    eigenval=np.real(eigenval)
    eigenvector=np.real(eigenvector)
    #np.matmul(eigenvector[:,1],np.transpose(eigenvector[:,5]))
    featMultiplier=eigenvector[:,0:numberComponents]
    return featMultiplier
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""
def convertDataToROIAverage(curInput, colToROI, listOfROIs): #List Containing the ROIs we care about
    trialAvgs=np.zeros((np.shape(curInput)[0],len(listOfROIs)))
    indROI=0
    for ROI in listOfROIs:
        for curSeqInd in range(0,np.shape(curInput)[0]):
            curSavedVoxels=[]
            for i in range(0,np.shape(curInput)[1]):
                if colToROI[i][0][0]==ROI:
                    curSavedVoxels.append(curInput[curSeqInd,i])
            trialAvgs[curSeqInd,indROI]=np.average(curSavedVoxels)
        indROI=indROI+1
    return trialAvgs
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""
def normalizeData(curInput):
    for i in range(0,np.shape(curInput)[0]):
        curInput[i,:]=(curInput[i,:]-np.min(curInput[i,:]))/(np.max(curInput[i,:])-np.min(curInput[i,:]))
    return curInput
"""
Created on Fri Oct 26 10:34:14 2018

@author: manjusharavindranath
"""
def extractData(subjectList, rois): #This function gives the normalized data for each subject
    allData=[]
    allLabels=[]
    allSubjects=[]#This stores what subject each datapoint belongs to
    allTrialLens=[]
    minTrialLen=0 #This will change
    #Establish the minTrialLen
    for curSubject in subjectList: #Gets the minimum trial len over all subjects
        matFilePath = "./Data/Subject_"+curSubject+"/data-starplus-"+curSubject+"-v7.mat"
        matFileData = loadmat(matFilePath)
        
        meta = getMeta(matFileData)
        #print(meta)
        info = getInfo(matFileData, meta)
        data = getData(matFileData, meta)
        for i in range(meta['ntrials']):
            if not info[i]['cond']==0:
                allTrialLens.append(np.shape(data[i])[0])
    minTrialLen=np.min(allTrialLens)
    #print("The minimum trial len is"+str(minTrialLen))
    subjectsCompleted=0
    for curSubject in subjectList: #Loop through the subjects to get data for each subject
        matFilePath = "./Data/Subject_"+curSubject+"/data-starplus-"+curSubject+"-v7.mat"
        matFileData = loadmat(matFilePath)
        
        meta = getMeta(matFileData)
        info = getInfo(matFileData, meta)
        data = getData(matFileData, meta)
        
        numTrialsGood=0
        for i in range(meta['ntrials']): #Determines the number of non noisy trials for a given subject
            if (not info[i]['cond']==0) and (not info[i]['cond']==1):
                numTrialsGood=numTrialsGood+1
        #curSubjectData=np.zeros((numTrialsGood,minTrialLen*meta['nvoxels']))
        curLabels=np.zeros((numTrialsGood*2,1))
        curSubjects=np.zeros((numTrialsGood*2,1))
        goodTrialInd=0
        allVolsSubject=[]
        for i in range(meta['ntrials']):
            if (not info[i]['cond']==0) and (not info[i]['cond']==1): # we only care about cond 2 or 3
                #For each good trial you will add a picture and a sentence example to the dataset, so you will also add two labels (one picture one sentence) as well as 2 subject values (both the same)
                curData=np.asarray(data[i])
                #curData=curData[0:minTrialLen,:]
                #curVols=convertDataToVolume(curData,meta['colToCoord']) #gets the sequence of volumes for a trial
                #Split into picture and sentence
                if info[i]['firstStimulus']=='P':
                    curDataPicture=curData[0:16,:]
                    curDataSentence=curData[16:32,:]
                else: #THis is firstStimulus S
                    curDataPicture=curData[16:32,:]
                    curDataSentence=curData[0:16,:]                    
                curPictureVols=convertDataToROIAverage(curDataPicture,meta['colToROI'],rois) #Converts sequence of scans to average of each roi for each time step, returns matrix size [n time steps, n rois]
                curSentenceVols=convertDataToROIAverage(curDataSentence,meta['colToROI'],rois)

                curPictureVols=normalizeData(curPictureVols)
                curSentenceVols=normalizeData(curSentenceVols)

                curPictureVols=np.reshape(curPictureVols,(1,np.prod(np.shape(curPictureVols)))) #Convert suquence of volumes to one long feature vector for current trial
                curSentenceVols=np.reshape(curSentenceVols,(1,np.prod(np.shape(curSentenceVols))))
                allVolsSubject.append(curPictureVols)  
                allVolsSubject.append(curSentenceVols)
                curLabels[goodTrialInd*2,:]=1 #Picture is label 1 sentence label 2
                curLabels[goodTrialInd*2+1,:]=2
                curSubjects[goodTrialInd*2,:]=int(curSubject)
                curSubjects[goodTrialInd*2+1,:]=int(curSubject)
                goodTrialInd=goodTrialInd+1
        if subjectsCompleted==0:
            allData=allVolsSubject
            allLabels=curLabels
            allSubjects=curSubjects
        else:
            allData=np.concatenate((allData,np.reshape(allVolsSubject, (np.shape(allVolsSubject)[0],np.shape(allVolsSubject)[2]))))
            allLabels=np.concatenate((allLabels,curLabels))
            allSubjects=np.concatenate((allSubjects,curSubjects))
        subjectsCompleted=subjectsCompleted+1
        print("Done Extracting Subject "+str(curSubject))
        allData=np.squeeze(allData)
    return allData, allLabels, allSubjects #This could be a pandas dataframe if you want to make it that

#featMultiplier=trainPCA(allData,100)
#newTrain=np.matmul(allData,featMultiplier)