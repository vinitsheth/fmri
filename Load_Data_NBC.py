import os
import numpy as np
import gc


def load_data(data_dir):
    print("Loading data for: ", data_dir.split('/')[2])

    os.chdir(data_dir)
    cwd = os.getcwd()

    # meta = {}
    # with open(cwd + "\\meta.data") as f:
    #     for line in f:
    #         (key, val) = line.rstrip('\n').split(':')
    #         meta[key] = val

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

            info['trial'] = len(trials) - 1
            info_files.append(info)

    print("Done!")
    return info_files, trials  # , meta


def get_related_trials(info, trials):
    # print('Inside GRT')
    result = []
    for item in info:
        i = int(item['trial'])
        result.append(trials[i])
    # print("Done GRT!")
    return result


def data_to_examples(info, data):
    # print("Inside D2E")
    num_trials = len(info)
    num_voxels = len(data[0][0])
    trials = [v['cond'] for v in info]

    unique_conds = np.unique(trials)
    num_conds = len(unique_conds)
    trial_len_cond = np.zeros((num_trials, num_conds))
    ntrialsCond = np.zeros((1, num_conds)).flatten()

    for i in range(0, num_trials):
        if trials[i] in unique_conds:
            # get index of trial[i] in uniqueConds
            tmp, = np.where(unique_conds == trials[i])
            # row size of data[i]
            trial_len_cond[i, tmp] = np.shape(data[i])[0]
            ntrialsCond[tmp] = ntrialsCond[tmp] + 1;

    minTrialLen = trial_len_cond[trial_len_cond > 0].min()
    num_features = minTrialLen * num_voxels
    num_examples = num_trials
    examples = np.zeros((int(num_examples), int(num_features)))
    labels = np.array(trials).reshape(len(trials), 1)

    for j in range(0, num_trials):
        tmp_data = data[j][:][:int(minTrialLen)]
        tmp_data = np.reshape(tmp_data, int(num_voxels * minTrialLen));
        examples[j] = tmp_data

    # print('Done D2E')
    return examples, labels


def main():
    cwd = os.getcwd()

    subjects = ["Data/ExtractedData/Subject_04799/",
                         "Data/ExtractedData/Subject_04820",
                         "Data/ExtractedData/Subject_04847",
                         "Data/ExtractedData/Subject_05680",
                         "Data/ExtractedData/Subject-05710"]

    all_pic_examples = []
    all_sen_examples = []
    all_pic_lables = []
    all_sen_lables = []

    for subject in subjects:
        info, trials_data = load_data(subject)

        print("Cleaning Data..")

        # collect the non-noise and non-fixation trials: 'cond' > 1
        pic_info = [d for d in info if (d['firstStimulus'] == 'P' and int(d['cond']) > 1)]
        sen_info = [d for d in info if (d['firstStimulus'] == 'S' and int(d['cond']) > 1)]

        pic_data = get_related_trials(pic_info, trials_data)
        sen_data = get_related_trials(sen_info, trials_data)

        del (info, trials_data)
        gc.collect()

        # Trim the data which are just blanks
        trim_pic = []
        for item in pic_data:
            trim_pic.append(np.concatenate((item[:][1:16], item[:][17:32])))

        del pic_data
        p_examples, p_labels = data_to_examples(pic_info, trim_pic)

        all_pic_examples.extend(p_examples)
        all_pic_lables.extend(p_labels)

        del pic_info, trim_pic, p_examples, p_labels
        gc.collect()

        trim_sen = []
        for item in sen_data:
            trim_sen.append(np.concatenate((item[:][1:16], item[:][17:32])))

        del sen_data
        s_examples, s_labels = data_to_examples(sen_info, trim_sen)
        all_sen_examples.extend(s_examples)
        all_sen_lables.extend(s_labels)

        del sen_info, trim_sen, s_examples, s_labels
        gc.collect()

        os.chdir(cwd)
        print("Finished!")

    examples = []
    examples.extend(all_pic_examples)
    examples.extend(all_sen_examples)
    examples = np.array(examples)

    del all_pic_examples, all_sen_examples

    labels = []
    labels.extend(all_pic_lables)
    labels.extend(all_sen_lables)
    labels = np.array(labels).ravel()

    del all_pic_lables, all_sen_lables

    print('Done')

    return examples, labels


if __name__ == "__main__":
    main()

# Subject-05710
# Subject_05680
# Subject_05675
# Subject_04847
# Subject_04820
# Subject_04799
