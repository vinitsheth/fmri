def getMata(matfile):
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

    ans = {}
    ans['study'] = matfile['meta'][0][0]['study'][0].encode('utf-8')
    ans['subject'] = matfile['meta'][0][0]['subject'][0].encode('utf-8')
    ans['ntrials'] = matfile['meta'][0][0]['ntrials'][0][0]
    ans['nsnapshots'] = matfile['meta'][0][0]['nsnapshots'][0][0]
    ans['nvoxels'] = matfile['meta'][0][0]['nvoxels'][0][0]
    ans['dimx'] = matfile['meta'][0][0]['dimx'][0][0]
    ans['dimy'] = matfile['meta'][0][0]['dimy'][0][0]
    ans['dimz'] = matfile['meta'][0][0]['dimz'][0][0]

    return ans


def colToCoord(matfile, col):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018

    ************* Method Description ******************

    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Returns the coordinates for the given column number

    Remember the column number starts from 0 as python index starts from 0.
    Starts from index 0
    """
    return matfile['meta'][0][0]['colToCoord'][col]


def getROINameFromColumn(matfile, col):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018

    ************* Method Description ******************
    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Remember the column number starts from 0 as python index starts from 0.

    Returns the ROI (Region of interest) for the given column number
    """
    return matfile['meta'][0][0]['colToROI'][col][0][0]


def getColumnsFromROIName(matfile, roi):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018

    ************* Method Description ******************
    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Returns array of column numbers for the given Roi name.
    """

    for i in range(len(matfile['meta'][0][0]['rois'][0])):
        if roi == matfile['meta'][0][0]['rois'][0][i][0][0].encode('utf-8'):
            return matfile['meta'][0][0]['rois'][0][i][2][0]


def getColumnsFromROINumber(matfile, roi):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018

    ************* Method Description ******************
    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Remember the roi starts from 0 to 24 as python index starts from 0.

    Returns array of column numbers for the given Roi number
    """

    return matfile['meta'][0][0]['rois'][0][roi][2][0]


def getInfoOfTrial(matfile, trialIndex):
    """
    Author :- Vinit Sheth
    Date :- 09/20/2018

    ************* Method Description ******************

    matfile argument is the variable reference which you can get after executing the loadmat() function in scipy.io
    ex. mat = loadmat('/Users/vinitsheth/SmlFinalProject/Data/data-starplus-05710-v7.mat')

    Remember the travelIndex starts from 0  as python index starts from 0.

    Return Dictoinary which contains information about the given trial.

    mint gives the time of the first image in the interval (the minimum time)

    maxt gives the time of the last image in the interval (the maximum time)

    cond has possible values 0,1,2,3.  Cond=0 indicates the data in this
    segment should be ignored. Cond=1 indicates the segment is a rest, or fixation
    interval.  Cond=2 indicates the interval is a sentence/picture trial in which
    the sentence is not negated.  Cond=3 indicates the interval is a
    sentence/picture trial in which the sentence is negated.

    firstStimulus: is either 'P' or 'S' indicating whether this trail was
    obtained during the session is which Pictures were presented before sentences,
    or during the session in which Sentences were presented before pictures.  The
    first 27 trials have firstStimulus='P', the remained have firstStimulus='S'.
    Note this value is present even for trials that are rest trials.  You can pick
    out the trials for which sentences and pictures were presented by selecting just
    the trials trials with info.cond=2 or info.cond=3.

    sentence gives the sentence presented during this trial.  If none, the
    value is '' (the empty string).  The fields info.sentenceSym1,

    sentenceSym2, and info.sentenceRel describe the two symbols mentioned in
    the sentence, and the relation between them.

    img describes the image presented during this trial.  For example, 'sap'
    means the image contained a 'star above plus'.  Each image has two tokens, where
    one is above the other.  The possible tokens are star (s), plus (p), and dollar
    (d).

    actionAnswer: has values -1 or 0.  A value of 0 indicates the subject is
    expected to press the answer button during this trial (either the 'yes' or 'no'
    button to indicate whether the sentence correctly describes the picture).  A
    value of -1 indicates it is inappropriate for the subject to press the answer
    button during this trial (i.e., it is a rest, or fixation trial).

    actionRT: gives the reaction time of the subject, measured as the time at
    which they pressed the answer button, minus the time at which the second
    stimulus was presented.  Time is in milliseconds.  If the subject did not press
    the button at all, the value is 0.
    """

    # Get the number of trials for this dataset and check if it is in the range of number of trials

    numberOftrials = matfile['meta']['ntrials'][0][0][0][0]

    if (trialIndex + 1) > numberOftrials and (trialIndex + 1) > 0:
        print("Invalid trial number. Total trials are " + str(numberOftrials))
    else:
        ans = {}
        ans['mint'] = matfile['info'][0][trialIndex]['mint'][0][0]
        ans['maxt'] = matfile['info'][0][trialIndex]['maxt'][0][0]
        ans['cond'] = matfile['info'][0][trialIndex]['cond'][0][0]
        ans['firstStimulus'] = matfile['info'][0][trialIndex]['firstStimulus'][0][0].encode('utf-8')
        ans['sentence'] = matfile['info'][0][trialIndex]['sentence'][0][:].encode('utf-8')
        ans['sentenceRel'] = matfile['info'][0][trialIndex]['sentenceRel'][0][:].encode('utf-8')
        ans['sentenceSym1'] = matfile['info'][0][trialIndex]['sentenceSym1'][0][:].encode('utf-8')
        ans['sentenceSym2'] = matfile['info'][0][trialIndex]['sentenceSym2'][0][:].encode('utf-8')
        ans['img'] = matfile['info'][0][trialIndex]['img'][0][:].encode('utf-8')
        ans['actionAnswer'] = matfile['info'][0][trialIndex]['actionAnswer'][0][0]
        ans['actionRT'] = matfile['info'][0][trialIndex]['actionRT'][0][0]
        return ans
