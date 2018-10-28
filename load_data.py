"""
************* Method Description ******************
Author: Avinash Patil
Description: Data pre processing for feeding it to ML models
Input: List of paths to data folder for each subject
Output: Data Matrix and Label Matrix
"""

import os
import numpy as np
import scrubber


def get_raw_data(data_dir, idx):
    subject = data_dir.split('/')[2]
    print("Loading data for: ", subject)

    os.chdir(data_dir)
    cwd = os.getcwd()

    meta = {}
    with open(cwd + "\\meta.data") as f:
        for line in f:
            (key, val) = line.rstrip('\n').split(':')
            meta[key] = val

    trials = []
    info_files = []

    for path, sub_dirs, files in os.walk(cwd):
        for name in sub_dirs:
            cwd = os.path.join(path, name)
            trial_data = open(cwd + "\\data.csv").read()
            # get data by lines but drop last line as it is empty
            trial_data = trial_data.split("\n")[:-1]
            # trial_data = np.array([i.split(",") for i in trial_data])
            trial_data = np.array([i.split(",") for i in trial_data])
            # trial_data.append(open(cwd + "\\info.data").read())
            # trials.append(trial_data)
            trials.append(trial_data[:, :4633])

            info = {}
            with open(cwd + "\\info.data") as f:
                for line in f:
                    (key, val) = line.rstrip('\n').split(':')
                    info[key] = val

            info['trial'] = idx + len(trials) - 1
            info['subject'] = subject
            info_files.append(info)

    print("Done!")
    return info_files, trials, meta


def get_subject_data(subjects):
    cwd = os.getcwd()

    # subjects = ["Data/ExtractedData/Subject_04799/",
    #                      "Data/ExtractedData/Subject_04820",
    #                      "Data/ExtractedData/Subject_04847",
    #                      "Data/ExtractedData/Subject_05680",
    #                      "Data/ExtractedData/Subject-05710"]

    trials_data = []
    info = []
    meta = []
    for subject in subjects:
        info_files, trial_data, meta_files = get_raw_data(subject, len(trials_data))
        trials_data.extend(trial_data)
        info.extend(info_files)
        meta.extend(meta_files)
        os.chdir(cwd)

    return scrubber.clean_data(trials_data, info)
