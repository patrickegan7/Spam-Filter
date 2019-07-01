from enron_processor import EnronProcessor
from pathlib import Path


class Classifier:
    def __init__(self, email=None):
        if email != None:
            self.email = email.read().split()
        self.enron_classifier = EnronProcessor()
        if Path("training_data").is_file():
            self.enron_classifier.load_training_data()
        else:
            # trains classifier and saves data
            self.enron_classifier.save_training_data()
        self.probability_ham = self.enron_classifier.ham_file_count / self.enron_classifier.file_count
        self.probability_spam = self.enron_classifier.spam_file_count / self.enron_classifier.file_count

    def change_email(self, email):
        self.email = email.read().split()

    def classify(self, email):
        word_probabilities = self.enron_classifier.calc_word_probabilities(email)
        probability_of_ham = word_probabilities[0] * self.probability_ham
        probability_of_spam = word_probabilities[1] * self.probability_spam

        if probability_of_ham > probability_of_spam:
            return 1
        else:
            return 0
