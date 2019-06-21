from classifier import Classifier
from pathlib import Path

test_set = Path("dataset/enron6")
classifier = Classifier()

total_num_classifications = 0
num_ham_errors = 0
num_spam_errors = 0
for email in (test_set / "ham").iterdir():
    total_num_classifications += 1
    num_ham_errors += 1 - \
        classifier.classify(open(str(email), "r", encoding="latin-1"))

for email in (test_set / "spam").iterdir():
    total_num_classifications += 1
    num_spam_errors += classifier.classify(
        open(str(email), "r", encoding="latin-1"))

print("Number of ham misclassifications: " + str(num_ham_errors))
print("Number of spam misclassifications: " + str(num_spam_errors))
print("Error rate: " + str((num_ham_errors +
                            num_spam_errors) / total_num_classifications))
