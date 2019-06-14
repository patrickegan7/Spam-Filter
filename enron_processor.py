from pathlib import Path

data_path = Path("dataset/enron")
word_counts = dict() # follows the convention: {word : (ham count, spam count)}
ham_file_count = 0
spam_file_count = 0
vocabulary_size = 0

def process():
    for i in range(1:7):
        dir = data_path / "i"

        for file in dir / "ham":
            ham_file_count += 1
            email = open(str(file), "r")
            contents = f.read().split()
            process_ham(contents)

        for file in dir / "spam":
            spam_file_count += 1
            email = open(str(file), "r")
            contents = f.read().split()
            process_spam(contents)

    vocabulary_size = len(word_counts)
    
# determine if a token is a valid 'word'
def isValid(word):
    # TODO: Need to implement
    return false

def process_ham(contents):
    for word in contents:
        if isValid(word):
            # Add word to dictionary
            if word in word_counts:
                word_counts[word][0] += 1
            else:
                word_counts[word] = (1, 0)

def process_spam(contents):
    for word in contents:
        if isValid(word):
            # Add word to dictionary
            if word in word_counts:
                word_counts[word][1] += 1
            else:
                word_counts[word] = (0, 1)
