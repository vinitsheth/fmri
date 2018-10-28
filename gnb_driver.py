import load_data
from numpy import concatenate
# from LoadDataNBC2 import main

subjects = ["Data/ExtractedData/Subject_04799",
                "Data/ExtractedData/Subject_04820",
                "Data/ExtractedData/Subject_04847",
                "Data/ExtractedData/Subject_05680",
                "Data/ExtractedData/Subject_05675",
                "Data/ExtractedData/Subject-05710"]

# training_subjects = ["Data/ExtractedData/Subject_04799/"]
# testing_subjects = ["Data/ExtractedData/Subject-05710"]

# info1, trails1 = main(training_subjects[0])
# info2, trails2 = main(training_subjects[1])
# info3, trails3 = main(training_subjects[2])
# info4, trails4 = main(training_subjects[3])
# info5, trails5 = main(training_subjects[4])

examples, labels, freq = load_data.get_subject_data(subjects)

print(freq)

# training_examples,training_labels,testing_examples,testing_labels = segregate_data(test_Subjects, examples, labels, freq)

training_examples = concatenate((examples[:100][:], examples[120:220][:]))
training_labels = concatenate((labels[:100], labels[120:220]))


print("getting test data")
testing_examples, testing_labels = examples[100:120][:], labels[200:]

testing_examples = concatenate((examples[100:120][:], examples[220:][:]))
testing_labels = concatenate((labels[100:120], labels[220:]))

from GNB import GaussianNB
# from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

print("Fitting..")
clf.fit(training_examples, training_labels)

print("predicting")
# result = clf.predict(testing_examples)
score = clf.score(testing_examples, testing_labels)

# score = 0
# for i in range(0, len(testing_labels)):
#     if result[i] == int(testing_labels[i]):
#         score += 1
#
# score = score/len(testing_labels)

print(score)


def segregate_data(test_Subjects, examples, labels, freq):
    for item in freq:
        print(item)