# -*- coding: utf-8 -*-
"""
@author: Vinit Seth, Aadhavan Sadasivam, Manjusha Ravindranath

###Have to write file description###
"""

from scipy.io import loadmat

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
    meta['study'] = matfile['meta'][0][0]['study'][0].encode('utf-8')
    meta['subject'] = matfile['meta'][0][0]['subject'][0].encode('utf-8')
    meta['ntrials'] = matfile['meta'][0][0]['ntrials'][0][0]
    meta['nsnapshots'] = matfile['meta'][0][0]['nsnapshots'][0][0]
    meta['nvoxels'] = matfile['meta'][0][0]['nvoxels'][0][0]
    meta['dimx'] = matfile['meta'][0][0]['dimx'][0][0]
    meta['dimy'] = matfile['meta'][0][0]['dimy'][0][0]
    meta['dimz'] = matfile['meta'][0][0]['dimz'][0][0]

    return meta


def getInfoFromList(matfile, trialNumber):
    
    """
    @Manjusha. write a method description here.
    """
    
    info = {}     
    #print(trialNumber)
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
    @Manjusha. write a method description here.
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
    
    return []
    
if __name__ == "__main__":
    
    matFilePath = "Data/Subject_04847/data-starplus-04847-v7.mat"
    matFileData = loadmat(matFilePath)
    
    meta = getMeta(matFileData)
    info = getInfo(matFileData, meta)
    data = getData(matFileData, meta)