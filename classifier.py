import enron_processor

class Classifier:
    def __init__(self, email):
        self.enron_classifier = EnronProcessor()
        self.enron_classifier.train()
        self.email = email.read().split()
        self.probability_ham = enron_classifier.ham_file_count / enron_classifier.file_count
        self.probability_spam = enron_classifier.spam_file_count / enron_classifier.file_count

    def __calc_word_probabilities(self):
        # caclulate conditional probability for ham
        conditional_ham_probability = 1.0
        conditional_spam_probability = 1.0
        ham_denominator = self.enron_classifier.ham_word_count + self.enron_classifier.vocabulary_size
        spam_denominator = self.enron_classifier.spam_word_count + self.enron_classifier.vocabulary_size
        for word in self.email:
            ham_numerator = 1.0 # laplace smoothing
            spam_numerator = 1.0
            if word in self.enron_classifier.word_counts:
                ham_numerator += self.enron_classifier.word_counts[word][0]
                spam_numerator += self.enron_classifier.word_counts[word][1]
            conditional_ham_probability *= (ham_numerator / ham_denominator)
            conditional_spam_probability *= (spam_numerator / spam_denominator)

        return [conditional_ham_probability, conditional_spam_probability]

    def classify(self):
        word_probabilities = self.__calc_word_probabilities()
        probability_of_ham = word_probabilities[0] * self.probability_ham
        probability_of_spam = word_probabilities[1] * self.probability_spam

        if probability_of_ham > probability_of_spam:
            return "Ham, " + str(probability_of_ham)
        else:
            return "Spam, " + str(probability_of_spam)