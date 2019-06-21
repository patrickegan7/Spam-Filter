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
        for i in range(1, 6):
            dir = self.data_path / ("enron" + str(i))

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

        self.file_count = self.spam_file_count + self.ham_file_count
        category_counts = list(np.sum(self.word_counts.values(),  axis=0))
        self.ham_word_count = sum(category_counts[0])
        self.spam_word_count = sum(category_counts[1])
        self.vocabulary_size = len(self.word_counts)

    def __process_ham(self, contents):
        for word in contents:
            if self.__isWord(word):
                # Add word to dictionary
                if word in self.word_counts:
                    self.word_counts[word][0] += 1
                else:
                    self.word_counts[word] = [1, 0]

    def __process_spam(self, contents):
        for word in contents:
            if self.__isWord(word):
                # Add word to dictionary
                if word in self.word_counts:
                    self.word_counts[word][1] += 1
                else:
                    self.word_counts[word] = [0, 1]

    def __isWord(self, word):
        if word in string.punctuation or word == " ":
            return False
        elif word == "cc" or word == "bcc":
            return False
        else:
            return True

    def pickleTrainingData(self):
        self.train()
        training = {"ham_word_count": self.ham_word_count, "spam_word_count": self.spam_word_count,
                    "ham_file_count": self.ham_file_count, "spam_file_count": self.spam_file_count}
        file = open("training_data", "wb")
        pickle.dump(training, file)
        file.close()
        return training

    def print_variables(self):
        print("Number of ham files: " + str(self.ham_file_count))
        print("Number of spam files: " + str(self.spam_file_count))
        print("Size of vocabulary: " + str(self.vocabulary_size))
