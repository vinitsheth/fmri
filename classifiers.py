# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:07:01 2018

@author: 
"""
import argparse
from utils.constants import classifiers, PathToSubjects
from operator import itemgetter 
from collections import Counter
from load_data import get_subject_data

if __name__ == "__main__":
    
    # Ignore matplotlib and numpy warnings
    import warnings
    warnings.filterwarnings("ignore")
    

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-model', type =int, help='Classification Algorithm. 1-GNB, 2-LogReg, 3-KNN, 4-SVM')          
    parser.add_argument('-subject', metavar='S', type=int, nargs='+',
                    help='subjects to be considered for classification. ex.,-subject 1 2 3 ')
    parser.add_argument('-sheepda', type=float,
                    help='Learning Rate for the classifier', default = 0.1)
    args = vars(parser.parse_args())
    
    model = args['model']
    subject = args['subject']
    subject = [item-1 for item in subject]
    sheepda = args['sheepda']
    if len(subject) > 1:
        subjectPath = list(itemgetter(*subject)(PathToSubjects))
    else:
        subjectPath = [PathToSubjects[subject[0]]]
    LoadedData = get_subject_data(subjectPath)
    print(Counter(LoadedData[1]))