# -*- coding: utf-8 -*-
"""
Manjusha Ravindranath 09/23/2018

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
import scipy.io


def getInfo(matfile, trialNumber):
    
        ans = {}     
       
           
        #print(trialNumber)
        
        mint=matfile['info'][0][trialNumber]['mint'][0][0];
        ans['mint']=mint;
        ans['maxt'] = matfile['info'][0][trialNumber]['maxt'][0][0]
        ans['cond'] = matfile['info'][0][trialNumber]['cond'][0][0]  
        
        ans['firstStimulus'] = matfile['info'][0][trialNumber]['firstStimulus'][0][0]
        sentence = matfile['info'][0][trialNumber]['sentence']
        if sentence.size > 0 :
            ans['sentence']=sentence[0][:].encode('utf-8')
        else:
            ans['sentence']=''
        sentenceRel = matfile['info'][0][trialNumber]['sentenceRel']   
        if sentenceRel.size > 0 :
            ans['sentenceRel'] = sentenceRel[0][:].encode('utf-8')
        else:
            ans['sentenceRel']=''    
        sentenceSym1=matfile['info'][0][trialNumber]['sentenceSym1']
        if sentenceSym1.size > 0:
            ans['sentenceSym1'] = sentenceSym1[0][:].encode('utf-8')
        else:
            ans['sentenceSym1']=''     
        sentenceSym2= matfile['info'][0][trialNumber]['sentenceSym2']  
        if sentenceSym2.size > 0:
            ans['sentenceSym2'] = sentenceSym2[0][:].encode('utf-8')
        else:
            ans['sentenceSym2']=''     
        img=matfile['info'][0][trialNumber]['img']
        if img.size > 0:
            ans['img'] = img[0][0]
        else:
            ans['img']=''     
        ans['actionAnswer'] = matfile['info'][0][trialNumber]['actionAnswer'][0][0]
        ans['actionRT'] = matfile['info'][0][trialNumber]['actionRT'][0][0]

         
        return ans  
    #
    

   
 
def getInfoFromList(matfile):
    trialList=[]
    trialIndices=54
    for infoitem in range (0, trialIndices):
        trial=getInfo(matfile,infoitem);
        trialList.append(trial);
        #print(trialList);
    return trialList
       
if __name__ == "__main__":

    path = 'Data/Subject_04847/data-starplus-04847-v7.mat'
    mat = scipy.io.loadmat(path)
    
    trialList=getInfoFromList(mat)
    
    print(trialList)
     

