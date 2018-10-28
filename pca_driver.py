"""
************* Method Description ******************
Author: Satrajit Maitra
Description: Driver to run the PCA
"""

import os
import numpy as np
import gc
import load_data as ld
import scrubber
from PCA import PCA

def load_data(data_dir):
    print("Loading data for: ", data_dir.split('/')[6])

    os.chdir(data_dir)
    cwd = os.getcwd()

    trials = []
    info_files = []

    for path, sub_dirs, files in os.walk(cwd):
        for name in sub_dirs:
            cwd = os.path.join(path, name)
            trial_data = open(cwd + "/data.csv").read()
            # get data by lines but drop last line as it is empty
            trial_data = trial_data.split("\n")[:-1]
            trial_data = np.array([i.split(",") for i in trial_data])
            # trial_data.append(open(cwd + "\\info.data").read())
            trials.append(trial_data)

            info = {}
            with open(cwd + "/info.data") as f:
                for line in f:
                    (key, val) = line.rstrip('\n').split(':')
                    info[key] = val

            info['trial'] = len(trials) - 1
            info_files.append(info)

    print("Done!")
    return info_files, trials  # , meta


def get_related_trials(info, trials):
    result = []
    for item in info:
        i = int(item['trial'])
        result.append(trials[i])
    # print("Done GRT!")
    return result




def main():
    cwd = os.getcwd()

    subjects = ["/Users/satrajitmaitra/fmri/Data/ExtractedData/Subject_04799/",
                    "/Users/satrajitmaitra/fmri/Data/ExtractedData/Subject_04820",
                    "/Users/satrajitmaitra/fmri/Data/ExtractedData/Subject_04847",
                    "/Users/satrajitmaitra/fmri/Data/ExtractedData/Subject_05680",
                    "/Users/satrajitmaitra/fmri/Data/ExtractedData/Subject-05710"]

    trials_data = []
    info = []
    for subject in subjects:
        info_files, trial_data = load_data(subject)
        trials_data.extend(trial_data)
        info.extend(info_files)
        os.chdir(cwd)

    pic_info = [d for d in info if (d['firstStimulus'] == 'P' and int(d['cond']) > 1)]
    sen_info = [d for d in info if (d['firstStimulus'] == 'S' and int(d['cond']) > 1)]

    pic_data = get_related_trials(pic_info, trials_data)
    sen_data = get_related_trials(sen_info, trials_data)

    trim_pic = []
    for item in pic_data:
        trim_pic.append(np.concatenate((item[:][1:16], item[:][17:32])))

    trim_sen = []
    for item in sen_data:
        trim_sen.append(np.concatenate((item[:][1:16], item[:][17:32])))

    final_trim_pic = (np.array(trim_pic)).reshape(100 * 30, 4949)
    final_trim_sen = (np.array(trim_sen)).reshape(100 * 30, 4949)

    pca_object = PCA(final_trim_pic, final_trim_sen)
    data = pca_object.get_top_eigen_vectors(1000)
    print(data)

if __name__ == "__main__":
    main()
