import random
import argparse
import re


class NGram:
    def __init__(self):

        # parse args
        args = self.setup_parser()

        self.model = {}
        self.output_length = args.n
        self.input_file = args.input_file
        self.default_context = [""] * args.n
        self.output_length = args.output_length

    def setup_parser(self):
        parser = argparse.ArgumentParser(prog="N-gram sentence generator",
                                         description="This program generates an ngram from an input text file, then "
                                                     "prints a random sentence generated from the input file.",
                                         add_help=True)

        parser.add_argument("-i",
                            "--input-file",
                            action="store",
                            default="text_docs/pride_and_prejudice.txt",
                            help="The learning file. Should be ASCII and contain intelligible English. The longer the"
                                 "file is the better the program's output will be.")

        parser.add_argument("-n",
                            type=int,
                            action="store",
                            default=1,
                            help="The size of the ngram (unigram, bigram, etc)")

        parser.add_argument("-o",
                            "--output-length",
                            type=int,
                            action='store',
                            help="The length of the randomly generated sentences",
                            default=50)

        return parser.parse_args()

    def train(self):
        print "Training from input file %s" % self.input_file

        context = tuple(self.default_context)

        with open(self.input_file, 'r') as in_file:
            text = in_file.read()

            for word in text.split():
                c = self.model.setdefault(context, {word: 0})
                wc = c.setdefault(word, 0)
                c[word] = wc + 1
                context = self.next_context(context, word)

        # we have frequencies. Convert them to probabilities.
        for c in self.model.values():
            total = 0.0
            for freq in c.values():
                total += freq
            for key in c.keys():
                c[key] /= total

        print self.model

    def generate(self):
        out = ""
        context = random.sample(self.model.keys(), 1)[0]
        for i in range(self.output_length):
            word = self.get_random_word(context)
            out += word + " "
            context = self.next_context(context, word)

        return re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), out, 1)  # capitalize first letter

    def next_context(self, context, word):
        return tuple((list(context) + [word])[1:])

    def get_random_word(self, context):
        c = self.model[context]
        if len(c) == 1:
            return c.keys()[0]
        total_words = sum(c.values())
        num = random.randint(1, total_words)

        word_high = 0
        for word in c:
            word_low = word_high
            word_high = word_low + c[word]

            if word_low < num <= word_high:
                return word

        return c.keys()[0]


if __name__ == '__main__':
        n_gram = NGram()
        n_gram.train()
        print n_gram.generate()
