import os
import numpy as np


def load_data(data_dir):
    print("Loading data for: ", data_dir.split('/')[2])

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
            trial_data = np.array([i.split(",") for i in trial_data])
            # trial_data.append(open(cwd + "\\info.data").read())
            trials.append(trial_data)

            info = {}
            with open(cwd + "\\info.data") as f:
                for line in f:
                    (key, val) = line.rstrip('\n').split(':')
                    info[key] = val

            info_files.append(info)

    print("Done!")
    return info_files, trials, meta


def idm_to_examples(info, data, meta):
    print("Done!")
    num_trials = len(info)
    num_voxels = len(data)


def transform_idm(info, data, meta, trials):
    print('Done')
    num_trials = len(trials)
    r_data = np.array()
    return info, data, meta


def main():
    cwd = os.getcwd()
    subjects = ["Data/ExtractedData/Subject_04799/",
                "Data/ExtractedData/Subject_04820",
                "Data/ExtractedData/Subject_04847",
                "Data/ExtractedData/Subject_05680",
                "Data/ExtractedData/Subject-05710"]

    # for subject in subjects:
    info, data, meta = load_data(subjects[0])
    # os.chdir(cwd)

    # collect the non-noise and non-fixation trials: 'cond' > 1
    trials = [d for d in info if int(d['cond']) > 1]

    info1, data1, meta1 = transform_idm(info, data, meta, trials);

    # % seperate P1st and S1st trials
    # [infoP1, dataP1, metaP1] = transformIDM_selectTrials(info1, data1, meta1, find([info1.firstStimulus] == 'P'));
    # [infoS1, dataS1, metaS1] = transformIDM_selectTrials(info1, data1, meta1, find([info1.firstStimulus] == 'S'));

    # examples, labels, expInfo = idm_to_examples(info_files, data, meta);
    print("Finished!")


if __name__ == "__main__":
    main()

# Subject-05710
# Subject_05680
# Subject_05675
# Subject_04847
# Subject_04820
# Subject_04799
