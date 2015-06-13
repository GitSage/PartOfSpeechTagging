import random
import argparse
import os
import string
import re


class NGram:
    def __init__(self):
        self.model = {}
        self.input_file = ""
        self.default_context = [""]  # after parsing args, this will have n elements (the n in ngram)
        self.output_length = 100

        # parse the command line args
        self.parse_args()

    def parse_args(self):
        # set up the arg-parser
        parser = argparse.ArgumentParser(prog="N-gram random text generator",
                                         description="This program analyzes input text to generate an n-gram model and "
                                                     "then generates random text based on the model",
                                         add_help=True)

        # add the <input-file> argument
        parser.add_argument("--input-file",
                            action="store",
                            help="The path to the input file containing text for learning.",
                            default="text_docs/small.txt")

        # add the <n> argument
        parser.add_argument("--n",
                            type=int,
                            action="store",
                            default=1,
                            help="the 'n' in n-gram")

        # add the <output-length> argument
        parser.add_argument("--output-length",
                            type=int,
                            action='store',
                            help="The number of words to output in the generated text",
                            default=10)

        # parse the arguments
        args = parser.parse_args()

        # check the input file
        self.input_file = args.input_file
        if self.input_file is None:
            raise Exception("No input file provided")
        if not os.path.exists(self.input_file):
            raise Exception("Input file %s does not exist" % self.input_file)
        if not os.path.isfile(self.input_file):
            raise Exception("Input path %s is not a file" % self.input_file)

        # pre-generate the context
        self.default_context = [""] * args.n

        # how many words are we to output?
        self.output_length = args.output_length

    def create_model(self):
        print "Creating model from %s ..." % self.input_file

        # start with the default context
        context = tuple(self.default_context)

        with open(self.input_file, 'r') as in_file:
            text = in_file.read()

            # normalize the string
            text = text.replace('\n', ' ')  # replace all newlines with spaces
            text = text.replace('\r', ' ')  # windows-style newlines too
            text = text.translate(string.maketrans(string.punctuation, ' '*len(string.punctuation)))  # remove all punctuation
            text = text.lower()  # lowercase
            text = re.sub('\s+', ' ', text)  # replace multiple spaces with one space

            # split the text up into words
            for word in text.split():
                # get the word counts dictionary for the current context (create one if it doesn't already exist)
                word_counts = self.model.setdefault(context, {word: 0})

                # get the word count for the current word. Initialize to zero if necessary.
                word_count = word_counts.setdefault(word, 0)

                # increment the word count and add it to the word counts dictionary
                word_counts[word] = word_count + 1

                # update the context with the current word
                context = self.update_context(context, word)

    def generate_output(self):
        print "Generating text ..."

        # get a context to start with
        context = random.sample(self.model.keys(), 1)[0]

        # select words up to the desired length
        for i in range(self.output_length):
            # select the word given the current context
            word = self.get_random_word(context)

            # print out the word (followed by a space)
            print word,

            # update the context with the last word
            context = self.update_context(context, word)

    def get_random_word(self, context):
        # get the dictionary of words for the current context
        word_counts = self.model[context]

        # if there is only one word, then just return that
        if len(word_counts) == 1:
            return word_counts.keys()[0]

        # get the total number of words for the given context
        total_words = sum(word_counts.values())

        # pick a number, any number, between 1 and the total number of words
        num = random.randint(1, total_words)

        word_high = 0
        for word in word_counts:
            word_low = word_high
            word_high = word_low + word_counts[word]

            if word_low < num <= word_high:
                return word

        return word_counts.keys()[0]

    @staticmethod
    def update_context(context, word):
        return tuple((list(context) + [word])[1:])


if __name__ == '__main__':
    try:
        n_gram = NGram()
        n_gram.create_model()
        n_gram.generate_output()
    except Exception, e:
        print e.message
