# -*- coding: utf-8 -*-

from scipy.io import loadmat
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def getMeta(matfile):

    meta = {}
    meta['study'] = matfile['meta'][0][0]['study'][0].encode('utf-8')
    meta['subject'] = matfile['meta'][0][0]['subject'][0].encode('utf-8')
    meta['ntrials'] = matfile['meta'][0][0]['ntrials'][0][0]
    meta['nsnapshots'] = matfile['meta'][0][0]['nsnapshots'][0][0]
    meta['nvoxels'] = matfile['meta'][0][0]['nvoxels'][0][0]
    meta['dimx'] = matfile['meta'][0][0]['dimx'][0][0]
    meta['dimy'] = matfile['meta'][0][0]['dimy'][0][0]
    meta['dimz'] = matfile['meta'][0][0]['dimz'][0][0]
    roi = []
    for item in  matfile['meta'][0][0]['rois'][0]:
        roi.append(item[0][0])
    meta['rois'] = roi
    
    meta['colToROI'] = []
    for item in matfile['meta'][0][0]['colToROI']:
        meta['colToROI'].append(item[0][0])
        
    return meta


def getInfoFromList(matfile, trialNumber):

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

    trialInfoList = []
    trialIndices = meta['ntrials']
    for infoitem in range (0, trialIndices):
        trial = getInfoFromList(matfile,infoitem);
        trialInfoList.append(trial);
    return trialInfoList

def getData(matFileData, meta):
    data = matFileData['data']
    data_array = []
    for item in data:
        data_array.append(item[0].tolist())
    return data_array

def extractData(matFile):
    matFileData = loadmat(matFile)
    meta = getMeta(matFileData)
    info = getInfo(matFileData, meta)
    data = getData(matFileData, meta)
    
    return meta, info, data