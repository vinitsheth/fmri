"""
************* Method Description ******************
Author: Avinash Patil
Description: Skeleton for NBC takes input from voxels and classifies brain activity for person viewing image or person reading text.
Input:
Output:
"""


import DataManupulation
from __future__ import division
import math
import re
import glob
import os
from collections import Counter
from decimal import Decimal
from pathlib import Path
import matplotlib.pyplot as plt


# of voxels in each class
countDocs = [0, 0]
# of terms in each class
countTerms = [0, 0]
# store conditional probabilites of words
cond_prob = {}
# of files read in an iteration
dataSize = [[],[]]
# one dict for pos and one for neg
dicts = [{}, {}]


# Results array. First list holds the classification
#results of class 0,"negative". Second one holds results of class 1,"positive".
res = [[0, 0],[0, 0]]

# stop_words = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours','yourself','yourselves','he','him','his','himself','she','her','hers','herself','it','its','itself',
# 'they','them','their','theirs','themselves','what','which','who','whom','this','that','these','those','am','is','are','was','were','be','been','being','have','has','had','having','do',
# 'does','did','doing','a','an','the','and','but','if','or','because','as','until','while','of','at','by','for','with','about','against','between','into','through','during','before','after',
# 'above','below','to','from','up','down','in','out','on','off','over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more',
# 'most','other','some','such','no','nor','not','only','own','same','so','than','too','very','s','t','can','will','just','don','should','now']


# calculate precision of the algorithm
def get_accuracy(result, col):
    tmpresult = result[col][col]/(res[col][col]+res[1-col][col])
    return tmpresult


# output the accuracy for each iteration
def gen_report(result):
    prob_neg = get_accuracy(result, 0)
    prob_pos = get_accuracy(result, 1)
    print('Negative Classification \n\t Accuracy: %.3f' % (prob_neg))
    print('Positive Classification \n\t Accuracy: %.3f\n' % (prob_pos))
    return prob_pos,prob_neg


# calculate conditional probabilities of each word in dictionary. alpha is laplace smoothing co-efficient.
def classify(bag_of_words):

    prob1 = math.log(Decimal(countDocs[0])) - math.log(countDocs[0]+countDocs[1])
    prob2 = math.log(Decimal(countDocs[1])) - math.log(countDocs[0]+countDocs[1])
    cum_prob = Decimal(prob1 - prob2)

    for word in bag_of_words:
        if word in cond_prob:
            con_neg = Decimal(cond_prob[word][0])
            con_pos = Decimal(cond_prob[word][1])
            cum_prob = cum_prob + con_neg - con_pos

    return 0 if cum_prob > 0 else 1


# read files and build the classification results array.
def testing_input(directory, dictionary):
    os.chdir(directory)
    for f in glob.glob("*.txt"):
        bag_of_words = Counter(get_words(open(f, encoding="utf8").read()))
        bag_of_words = clean_bag(bag_of_words)
        c = classify(bag_of_words)
        res[dictionary][c] += 1


# Starts the testing phase.
def do_test():
    global res
    res = [[0,0], [0,0]]
    cwd = os.getcwd()
    testing_input("data/test/neg/", 0)
    # testing_input("data/neg/", 0)
    os.chdir(cwd)
    testing_input("data/test/pos/", 1)
    # testing_input("data/pos/", 1)
    os.chdir(cwd)


# This method calculates the likelyhood using laplace smoothing
def likelyhood(alpha):
    global cond_prob
    cond_prob = {}
    for d, dictionary in enumerate(dicts):
        for k, v in dictionary.items():
            if k not in cond_prob:
                cond_prob[k] = {0: 0, 1: 0}
                if alpha is not 0:
                    cond_prob[k][1-d] = math.log(Decimal(alpha)) - math.log(countTerms[d]+alpha*len(dicts[d]))
            cond_prob[k][d] = math.log(Decimal(v+alpha)) - math.log(countTerms[d]+alpha*len(dicts[d]))


# output sparse matrix in (r,c,v) format
def write_matrix(bag_of_words,file):

    path = os.path.abspath(os.curdir)
    path = Path(path)
    path = path.parent
    path = os.path.join(path, "Matrix.txt")
    MatrixFile= open(path, "a")

    for item in bag_of_words.items():
        out = str(item[0])+", "+file+", "+str(item[1])
        MatrixFile.write(out+"\n")

    MatrixFile.close()


# removes stopwords from input
def clean_bag(bag_of_words):

    # print(list(bag_of_words))
    for stopword in stop_words:
        if stopword in bag_of_words:
            del bag_of_words[stopword]

    # print(list(bag_of_words))
    return bag_of_words


# read files
def training_input(directory, dictionary,ratio):

    os.chdir(directory)
    files_count = int(len(glob.glob("*.txt"))*ratio)
    dataSize[dictionary].append(files_count)

    for file in glob.glob("*.txt"):
        bag_of_words = Counter(get_words(open(file,encoding="utf8").read().lower()))
        bag_of_words = clean_bag(bag_of_words)
        # print(bag_of_words)
        select_dict(bag_of_words, dictionary)
        countDocs[dictionary] += 1
        # write_matrix(bag_of_words,file) Uncomment this to start generating the matrix file.

        files_count -=1
        if files_count==0:
            return


# return words of a file as a list
def get_words(text): return re.findall(r'\w+', text)


# creates class dictionaries.
def select_dict(bag_of_words, dictionary):
    for word in bag_of_words:
        # print(word)
        countTerms[dictionary] += 1
        # print(countTerms[dictionary])

        if word in dicts[dictionary]:
            dicts[dictionary][word] += 1
        else:
            dicts[dictionary][word] = 1


# Train the model
def do_Train(alpha,ratio):
    cwd = os.getcwd()
    training_input("data/test/pos/", 1, ratio)  # positives
    # training_input("data/pos/", 1,ratio) #positives
    os.chdir(cwd)
    training_input("data/test/neg/", 0,ratio) #negatives
    # training_input("data/neg/", 0, ratio)  # negatives
    os.chdir(cwd)
    likelyhood(alpha)


# driver function
def main():
    print("Starting..")
    pos_precisions = []
    neg_precisions = []
    ratios = [0.1, 0.3, 0.5, 0.7, 0.8, 0.9]
    # ratios = [0.9]

    for ratio in ratios:
        print("Begining Training..")
        print("Ratio selected: ",ratio)
        do_Train(0,ratio)
        print("Training Done!")

        print("Calculating likelyhood..")
        likelyhood(1)

        print("Testing..")
        do_test()

        print("Getting Results..")
        result = gen_report(res)
        pos_precisions.append(result[0])
        neg_precisions.append(result[1])

        print("Loop Done. /n")
        print("-------------------------------------------------------------+"+"/n/n/n/n")

    dataSize_pos = dataSize[1]
    dataSize_neg = dataSize[0]

    print(list(dataSize_pos))
    print(list(dataSize_neg))

    plt.plot(dataSize_pos,pos_precisions,'ro', dataSize_neg, neg_precisions, 'bo')
    plt.savefig('plot.png')
    # plt.show()


if __name__=="__main__":
    main()
