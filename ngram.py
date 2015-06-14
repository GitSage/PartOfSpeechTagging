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
        parser = argparse.ArgumentParser(prog="N-gram random text generator",
                                         description="This program analyzes input text to generate an n-gram model and "
                                                     "then generates random text based on the model",
                                         add_help=True)

        parser.add_argument("--input-file",
                            action="store",
                            help="The path to the input file containing text for learning.",
                            default="text_docs/pride_and_prejudice.txt")

        parser.add_argument("--n",
                            type=int,
                            action="store",
                            default=3,
                            help="the 'n' in n-gram")

        parser.add_argument("--output-length",
                            type=int,
                            action='store',
                            help="The number of words to output in the generated text",
                            default=50)

        args = parser.parse_args()

        self.input_file = args.input_file
        if self.input_file is None:
            raise Exception("No input file provided")
        if not os.path.exists(self.input_file):
            raise Exception("Input file %s does not exist" % self.input_file)
        if not os.path.isfile(self.input_file):
            raise Exception("Input path %s is not a file" % self.input_file)

        self.default_context = [""] * args.n
        self.output_length = args.output_length

    def train(self):
        print "Creating model from %s ..." % self.input_file

        context = tuple(self.default_context)

        with open(self.input_file, 'r') as in_file:
            text = in_file.read()

            text = text.replace('\n', ' ')  # replace all newlines with spaces
            text = text.replace('\r', ' ')  # windows-style newlines too
            text = re.sub('\s+', ' ', text)  # replace multiple spaces with one space

            for word in text.split():
                word_counts = self.model.setdefault(context, {word: 0})
                word_count = word_counts.setdefault(word, 0)
                word_counts[word] = word_count + 1
                context = self.update_context(context, word)

    def generate(self):
        context = random.sample(self.model.keys(), 1)[0]
        for i in range(self.output_length):
            word = self.get_random_word(context)
            print word,
            context = self.update_context(context, word)

    @staticmethod
    def update_context(context, word):
        return tuple((list(context) + [word])[1:])

    def get_random_word(self, context):
        word_counts = self.model[context]
        if len(word_counts) == 1:
            return word_counts.keys()[0]
        total_words = sum(word_counts.values())
        num = random.randint(1, total_words)

        word_high = 0
        for word in word_counts:
            word_low = word_high
            word_high = word_low + word_counts[word]

            if word_low < num <= word_high:
                return word

        return word_counts.keys()[0]




if __name__ == '__main__':
    try:
        n_gram = NGram()
        n_gram.train()
        n_gram.generate()
    except Exception, e:
        print e.message
