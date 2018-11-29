# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
from data_extract import extractData

from classifier import stratified

import matplotlib.pyplot as plt

if __name__ == '__main__':
    pathToData = 'data/subject'
    MatFilesPath = []
    
    for files in os.listdir(pathToData):
        MatFilesPath.append(os.path.join(pathToData, files))
    
    metaTotal = []
    infoTotal = []
    dataTotal = []
    
    uniform_voxel = 1e10
    #
    #Load data for each subject
    for i in range(len(MatFilesPath)):
        print("Loading data from matfile for subject {}".format(i+1))
        file = MatFilesPath[i]
        meta, info,data = extractData(file)
        uniform_voxel = min(uniform_voxel, meta['nvoxels'])
        metaTotal.append(meta)
        infoTotal.append(info)
        dataTotal.append(data)
        
    print("..............................")
    
    acc = []
    ac = []
    top = []
    top_val = []
    
    #classification for each subject
    for j in range(len(MatFilesPath)):
        print("Preparing data for classification on subject {}".format(j+1))
        meta, info, data = metaTotal[j], infoTotal[j], dataTotal[j]
        
        
        Picture = []
        Sentence = []
        negated = []
        nonNegated = []
        for i in range(len(info)):
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
                    
                if cond == 3:
                    negated.append(pic)
                    #negated.append(sum(pic, []))
                else:
                    nonNegated.append(pic)
                    #nonNegated.append(sum(pic, []))
    
                #Picture.append(sum(pic, []))
                #Sentence.append(sum(sen, []))
                Picture.append(pic)
                Sentence.append(sen)
        #break
        
        
        SentenceFrame = pd.DataFrame.from_records(sum(Sentence,[]))
        PictureFrame = pd.DataFrame.from_records(sum(Picture,[]))
        
        data = pd.concat([SentenceFrame, PictureFrame], axis = 0)
        print("Data ready for classification..")
        #SentenceFrame['label'] = 0
        #PictureFrame['label'] = 1
        
        #
        #Get ROI
        ROI = [str(np.asarray(item)) for item in meta['rois']]
        ROIFrame = pd.DataFrame(meta['colToROI'])
        
        accuracy = {}
        roidata = {}
        #
        #combine data based on ROI
        for r in ROI:
            print("ROI {}".format(r))
            ROIcolumn = ROIFrame.loc[ROIFrame[0] == r].index.tolist()
            ROIcolumn.append(data.shape[1]-1)
            picData = PictureFrame.iloc[:,ROIcolumn]
            senData = SentenceFrame.iloc[:,ROIcolumn]
            
            sen = []
            pic = []
            #
            #flatten ROI data
            for m in range(40):
                start = m * 16
                end = (m+1) * 16
                sen.append(senData.iloc[start:end,:].values.flatten().tolist())
                pic.append(picData.iloc[start:end,:].values.flatten().tolist())
            roiPic = pd.DataFrame.from_records(pic)
            roiSen = pd.DataFrame.from_records(sen)
            roiPic['label'] = 0
            roiSen['label'] = 1
            #
            #ROI data
            Data = pd.concat([roiPic, roiSen], axis = 0)
            roidata[r] = Data
            accuracy[r] = stratified(Data, 5)
            
        ac.append(accuracy)
        accc = sorted(accuracy.items(), key=lambda x: x[1], reverse=True)
        
        
        #
        #Change here for top n
        topROI = [accc[i][0] for i in range(3)]
        top.append(topROI)
        top_val.append([accuracy[r] for r in topROI])
        finalData = roidata[topROI[0]]
        
        #
        #Top Roi
        for m in range(1,len(topROI)):
            finalData = pd.concat([finalData,roidata[topROI[m]]], axis = 1)
        
        acc.append(stratified(finalData, 5))
       
        
    f = 1
    for i in range(len(top)):
        values = top_val[i]
        x = np.arange(len(values))
        xticks = top[i]
        plt.cla()
        plt.bar(x, values, width=0.5, color = 'red')
        plt.xlabel('Region Of Interest')
        plt.ylabel('Accuracy')
        plt.title('Best 3 ROI for subject '+str(f))
        plt.xticks(x, xticks)
        plt.savefig('plot/image_roi'+str(f)+'.jpg')
        f += 1
    