# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 15:37:52 2018

@author: aadhavan sadasivam
"""

import os
import pandas as pd
import numpy as np

if __name__ == "__main__":
    path_to_data = "data\extracteddata"
    path_to_subject = []
    for files in os.listdir(path_to_data):
        path_to_subject.append(os.path.join(path_to_data,files))
    path_to_subject = path_to_subject[1:]
    
    voxel_length = []
   
    picturesFrame = []
    sentenceFrame = []  
  
    
    for subject in path_to_subject:
        meta = dict(lines.rstrip('\n').split(':') for lines in open(os.path.join(subject,"meta.data")))
        voxel_length.append(int(meta['nvoxels']))
        
        uniform_voxel = min(voxel_length)
      
    for subject in path_to_subject:
        meta = dict(lines.rstrip('\n').split(':') for lines in open(os.path.join(subject,"meta.data")))
        picture = []
        sentence = []
        for i in range(1,int(meta['ntrials'])+1):
            trial = os.path.join(subject,"Trial"+str(i))
            
            
            info = dict(lines.rstrip('\n').split(':') for lines in open(os.path.join(trial,"info.data")))
           
            if int(info['cond']) == 2 or int(info['cond']) == 3:
                data = pd.read_csv(os.path.join(trial,"data.csv"),header=None)
            
                if info['firstStimulus'] == 'P':
                    picture.append(data.iloc[1:16,:uniform_voxel].values.flatten())
                    sentence.append(data.iloc[17:32,:uniform_voxel].values.flatten())
                else:
                    picture.append(data.iloc[17:32,:uniform_voxel].values.flatten())
                    sentence.append(data.iloc[1:16,:uniform_voxel].values.flatten())
        picturesFrame.append(picture)
        sentenceFrame.append(sentence) 
  
   
    for i in range(len(picturesFrame)):
        sentence = sentenceFrame[i]
        picture = picturesFrame[i]
        column = np.arange(1,len(picture[0])+1)
        picframe = pd.DataFrame(picture,columns = column)
        senframe = pd.DataFrame(sentence,columns = column)
        picframe.to_csv('data/sentenceVSpicture/sentence/sentence'+str(i+1)+'.csv',index=False)
        senframe.to_csv('data/sentenceVSpicture/picture/picture'+str(i+1)+'.csv',index=False)