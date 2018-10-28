import numpy as np


def clean_data(trials, info):
    counts = []
    print("Cleaning Data..")
    # select_trials like code
    # collect the non-noise and non-fixation trials: 'cond' > 1
    pic_info = [d for d in info if (d['firstStimulus'] == 'P' and int(d['cond']) > 1)]
    sen_info = [d for d in info if (d['firstStimulus'] == 'S' and int(d['cond']) > 1)]

    pic_data = get_related_trials(pic_info, trials)
    sen_data = get_related_trials(sen_info, trials)

    del (info, trials)

    # count the number of trials selected from every trial
    # use it later to segregate testing and training data.
    from collections import defaultdict
    fq = {'subject': defaultdict(int)}
    for row in pic_info:
        for field in fq:
            fq[field][row[field]] += 1

    # Trim the data which are just blanks
    trim_pic = []
    for item in pic_data:
        trim_pic.append(np.concatenate((item[:][1:16], item[:][17:32])))

    del pic_data
    p_examples, p_labels = data_to_examples(pic_info, trim_pic)

    trim_sen = []
    for item in sen_data:
        trim_sen.append(np.concatenate((item[:][1:16], item[:][17:32])))

    del sen_data
    s_examples, s_labels = data_to_examples(sen_info, trim_sen)

    examples = []
    examples.extend(p_examples)
    examples.extend(s_examples)
    examples = np.array(examples)

    labels = []
    labels_p = np.zeros((p_examples.shape[0], 1))
    labels_s = np.ones((s_examples.shape[0], 1))
    # labels.extend(p_labels)
    # labels.extend(s_labels)
    labels.extend(labels_p)
    labels.extend(labels_s)
    labels = np.array(labels).ravel()

    print('Done')
    return examples, labels, fq


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



