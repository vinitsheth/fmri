from load_data import get_subject_data
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

examples, labels = get_subject_data(subjects)
training_examples, training_labels = examples[:200][:], labels[:200]

print("getting test data")
testing_examples, testing_labels = examples[200:][:], labels[200:]

from GNB import GaussianNB
# from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

print("Fitting..")
clf.fit(training_examples, training_labels)

print("predicting")
result = clf.predict(testing_examples)
###score = clf.score(testing_examples, testing_labels)

for i in range(0, len(testing_labels)):
    if testing_labels[i] == '3':
        testing_labels[i] = 1
    else:
        testing_labels[i] = 0

score = 0
for i in range(0, len(testing_labels)):
    if result[i] == int(testing_labels[i]):
        score += 1

score = score/len(testing_labels)
print(score)