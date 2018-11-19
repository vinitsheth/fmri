# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 15:37:52 2018

@author: aadhavan sadasivam
"""

import os
import pandas as pd
import numpy as np
from utils.constants import PathToSubjects

if __name__ == "__main__":
    
    path_to_data = "data\extracteddata"
    
    voxel_length = []
    picturesFrame = []
    sentenceFrame = []  
    restFrame = []
    
    for subject in PathToSubjects:
        meta = dict(lines.rstrip('\n').split(':') for lines in open(os.path.join(subject,"meta.data")))
        voxel_length.append(int(meta['nvoxels']))
        
    uniform_voxel = min(voxel_length)
      
    for subject in PathToSubjects:
        meta = dict(lines.rstrip('\n').split(':') for lines in open(os.path.join(subject,"meta.data")))
        picture = []
        sentence = []
        rest = []
        for i in range(1,int(meta['ntrials'])+1):
            trial = os.path.join(subject,"Trial"+str(i))
            
            info = dict(lines.rstrip('\n').split(':') for lines in open(os.path.join(trial,"info.data")))
           
            if int(info['cond']) == 2 or int(info['cond']) == 3:
                data = pd.read_csv(os.path.join(trial,"data.csv"),header=None)
                rest.append(data.iloc[8:16,:uniform_voxel].values.flatten())
                if info['firstStimulus'] == 'P':
                    picture.append(data.iloc[:8,:uniform_voxel].values.flatten())
                    sentence.append(data.iloc[16:24,:uniform_voxel].values.flatten())
                else:
                    picture.append(data.iloc[16:24,:uniform_voxel].values.flatten())
                    sentence.append(data.iloc[0:8,:uniform_voxel].values.flatten())
        picturesFrame.append(picture)
        sentenceFrame.append(sentence) 
        restFrame.append(rest)
   
    for i in range(len(picturesFrame)):
        sentence = sentenceFrame[i]
        picture = picturesFrame[i]
        rest = restFrame[i]
        
        column = np.arange(1,uniform_voxel+1)
        picframe = pd.DataFrame(columns = column)
        senframe = pd.DataFrame(columns = column)
        restframe = pd.DataFrame(columns=column)
        for j in range(len(sentence)):
            frame1 = picture[j]
            frame2 = sentence[j]
            frame3 = rest[j]
            picframe = pd.concat([picframe,frame1],axis=0)
            senframe = pd.concat([senframe,frame2],axis = 0)
            restframe = pd.concat([restframe,frame3],axis = 0)
        picframe.to_csv('data/sentenceVSpicture/sentence/sentence'+str(i+1)+'.csv',index=False)
        senframe.to_csv('data/sentenceVSpicture/picture/picture'+str(i+1)+'.csv',index=False)
        restframe.to_csv('data/sentenceVSpicture/rest/rest'+str(i+1)+'.csv',index=False)