from pathlib import Path
import string
import numpy as np
import pickle


class EnronProcessor:
    def __init__(self):
        self.data_path = Path("dataset")
        # follows the convention: {word : (ham count, spam count)}
        self.word_counts = dict()
        self.ham_file_count = 0
        self.ham_word_count = 0
        self.spam_file_count = 0
        self.spam_word_count = 0
        self.file_count = 0
        self.vocabulary_size = 0

    def train(self):
        error_rates = list()
        # follows format: [..., [error_rate, word_counts, ham_file_count, spam_file_count] , ...]
        for i in range(1, 7):
            for j in range(1,7):
                if i != j:
                    dir = self.data_path / ("enron" + str(j))

                    for file in Path(dir / "ham").iterdir():
                        self.ham_file_count += 1
                        email = open(str(file), "r", encoding="latin-1")
                        contents = email.read().split()
                        self.__process_ham(contents)

                    for file in Path(dir / "spam").iterdir():
                        self.spam_file_count += 1
                        email = open(str(file), "r", encoding="latin-1")
                        contents = email.read().split()
                        self.__process_spam(contents)

                        category_counts = self.__get_word_counts(self.word_counts)
                        self.ham_word_count = category_counts[0]
                        self.spam_word_count = category_counts[1]
                        self.vocabulary_size = category_counts[2]
                        self.file_count = self.ham_file_count + self.spam_file_count


            self.__calc_error_rate(i, error_rates)
            error_rates[i - 1].append(self.word_counts)
            error_rates[i - 1].append(self.ham_file_count)
            error_rates[i - 1].append(self.spam_file_count)

        # find best Classifier from error_rate
        min = error_rates[0][0]
        min_index = 0
        for i in range(len(error_rates)):
            if min > error_rates[i][0]:
                min = error_rates[i][0]
                min_index = i

        print(min)

        min_classifier = error_rates[min_index]
        self.file_count = min_classifier[2] + min_classifier[3] #spam_file_count + ham_file_count
        category_counts = self.__get_word_counts(min_classifier[1])#list(np.sum(min_classifier[1].values(),  axis=0))
        self.ham_word_count = category_counts[0]
        self.spam_word_count = category_counts[1]
        self.vocabulary_size = category_counts[2]

    def __calc_error_rate(self, index, error_rates):
        num_classifications = 0
        misclassifications = 0
        test_path = self.data_path / ("enron" + str(index))

        for file in Path(test_path / "ham").iterdir():
            email = open(file, "r", encoding="latin-1")
            num_classifications += 1
            conditional_prob = self.calc_word_probabilities(email.read().split())

            if conditional_prob[1]*(self.spam_file_count/self.file_count) >= conditional_prob[0]*(self.ham_file_count/self.file_count):
                misclassifications += 1

            email.close()

        for file in Path(test_path / "spam").iterdir():
            email = open(file, "r", encoding="latin-1")
            num_classifications += 1
            conditional_prob = self.calc_word_probabilities(email.read().split())

            if conditional_prob[1]*(self.spam_file_count/self.file_count) < conditional_prob[0]*(self.ham_file_count/self.file_count):
                misclassifications += 1

            email.close()

        error_rates.append([misclassifications / num_classifications])


    def calc_word_probabilities(self, email):
        # caclulate conditional probability for ham
        conditional_ham_probability = 1.0
        conditional_spam_probability = 1.0
        ham_denominator = self.ham_word_count + self.vocabulary_size
        spam_denominator = self.spam_word_count + self.vocabulary_size
        for word in email:
            ham_numerator = 1.0 #Laplace smoothing
            spam_numerator = 1.0
            if word in self.word_counts:
                ham_numerator += self.word_counts[word][0]
                spam_numerator += self.word_counts[word][1]\
            conditional_ham_probability *= ham_numerator
            conditional_spam_probability *= spam_numerator

        return [conditional_ham_probability/ham_denominator, conditional_spam_probability/spam_denominator]

    def __get_word_counts(self, word_counts):
        category_counts = list(np.sum(word_counts.values(),  axis=0))
        return [sum(category_counts[0]), sum(category_counts[1]), len(word_counts)]


    def __process_ham(self, contents):
        for word in contents:
            if self.__is_word(word):
                # Add word to dictionary
                if word in self.word_counts:
                    self.word_counts[word][0] += 1
                else:
                    self.word_counts[word] = [1, 0]

    def __process_spam(self, contents):
        for word in contents:
            if self.__is_word(word):
                # Add word to dictionary
                if word in self.word_counts:
                    self.word_counts[word][1] += 1
                else:
                    self.word_counts[word] = [0, 1]

    def __is_word(self, word):
        if word in string.punctuation or word == " ":
            return False
        elif word == "cc" or word == "bcc":
            return False
        else:
            return True

    def save_training_data(self):
        self.train()
        training_data = {"ham_word_count": self.ham_word_count, "spam_word_count": self.spam_word_count,
                         "ham_file_count": self.ham_file_count, "spam_file_count": self.spam_file_count,
                         "word_counts": self.word_counts, "vocabulary_size": self.vocabulary_size}
        data_file = open("training_data", "wb")
        pickle.dump(training_data, data_file)
        data_file.close()

    def load_training_data(self):
        data_file = open("training_data", "rb")
        training_data = pickle.load(data_file)
        data_file.close()
        self.ham_word_count = training_data["ham_word_count"]
        self.spam_word_count = training_data["spam_word_count"]
        self.ham_file_count = training_data["ham_file_count"]
        self.spam_file_count = training_data["spam_file_count"]
        self.word_counts = training_data["word_counts"]
        self.vocabulary_size = training_data["vocabulary_size"]
        self.file_count = self.ham_file_count + self.spam_file_count

    def print_variables(self):
        print("Number of ham files: " + str(self.ham_file_count))
        print("Number of spam files: " + str(self.spam_file_count))
        print("Size of vocabulary: " + str(self.vocabulary_size))
