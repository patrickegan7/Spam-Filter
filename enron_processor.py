from pathlib import Path
import string

data_path = Path("dataset")
word_counts = dict() # follows the convention: {word : (ham count, spam count)}
ham_file_count = 0
spam_file_count = 0
vocabulary_size = 0

def process():
    global ham_file_count
    global spam_file_count
    global vocabulary_size

    for i in range(1, 7):
        dir = data_path / ("enron" + str(i))

        for file in Path(dir/"ham").iterdir():
            ham_file_count += 1
            email = open(str(file), "r", encoding="latin-1")
            contents = email.read().split()
            process_ham(contents)

        for file in Path(dir/"spam").iterdir():
            spam_file_count += 1
            email = open(str(file), "r", encoding="latin-1")
            contents = email.read().split()
            process_spam(contents)

    vocabulary_size = len(word_counts)

def process_ham(contents):
    for word in contents:
        if isWord(word):
            # Add word to dictionary
            if word in word_counts:
                word_counts[word][0] += 1
            else:
                word_counts[word] = [1, 0]

def process_spam(contents):
    for word in contents:
        if isWord(word):
            # Add word to dictionary
            if word in word_counts:
                word_counts[word][1] += 1
            else:
                word_counts[word] = [0, 1]

def isWord(word):
    if word in string.punctuation or word == " ":
        return False
    elif word == "cc" or word == "bcc":
        return False
    else:
        return True

def print_variables():
    print("Number of ham files: " + str(ham_file_count))
    print("Number of spam files: " + str(spam_file_count))
    print("Size of vocabulary: " + str(vocabulary_size))

process()
print_variables()
