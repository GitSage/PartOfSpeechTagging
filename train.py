import string
import re

def train(filename):
    ngram_words = {}  # dictionary of string word to NGramWord object

    # get the contents of the text file
    f = open(filename, 'r')
    text = f.read()
    f.close()

    # normalize the string
    text = text.replace('\n', ' ')  # replace all newlines with spaces
    text = text.replace('\r', ' ')  # windows-style newlines too
    text = text.translate(string.maketrans("", ""), string.punctuation)  # remove all punctuation
    text = text.lower()  # lowercase
    text = re.sub('\s+', ' ', text)  # replace multiple spaces with one space

    all_words = text.split(" ")
    for i in range(0, len(all_words) - 1):  # the last word has nothing following it, so don't work on it
        curr = all_words[i]
        next_word = all_words[i+1]

        # if first time seeing word, initialize it
        if curr not in ngram_words:
            ngram_words[curr] = NGramWord()

        # if first time seeing word pair combination, add the second word
        if next_word not in ngram_words[curr].next_words:
            ngram_words[curr].next_words[next_word] = 0

        # increment
        ngram_words[curr].next_words[next_word] += 1

    return ngram_words


class NGramWord:
    def __init__(self):
        self.next_words = {}  # dictionary of word to frequency (string to int)

    def __repr__(self):
        return str(self.next_words)

if __name__ == "__main__":
    ngram = train("text_docs/pride_and_prejudice.txt")
    print ngram
