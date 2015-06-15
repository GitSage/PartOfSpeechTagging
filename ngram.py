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
        self.sentence_starters = {}
        self.output_length = args.output_length

    def setup_parser(self):
        parser = argparse.ArgumentParser(prog="N-gram sentence generator",
                                         description="This program generates an ngram from an input text file, then "
                                                     "prints a random sentence generated from the input file.",
                                         add_help=True)

        parser.add_argument("-i",
                            "--input-file",
                            action="store",
                            # default="text_docs/bible-kjv.txt",
                            default="text_docs/2009-Obama.txt",
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
                if len(context[0]) > 0 and context[0][0].isupper():
                    self.sentence_starters.setdefault(context, 0)
                    self.sentence_starters[context] += 1

                c = self.model.setdefault(context, {word: 0})
                wc = c.setdefault(word, 0)
                c[word] = wc + 1
                context = self.next_context(context, word)
            c = self.model.setdefault(context, {word: 0})
            wc = c.setdefault(word, 0)
            c[word] = wc + 1

        # print self.sentence_starters


    def next_context(self, context, word):
        return tuple((list(context) + [word])[1:])

    def generate(self):
        starter = self.get_random_sentence_starter()
        out = starter[0] + " "
        context = starter
        for i in range(self.output_length):
            word = self.get_random_word(context)
            out += word + " "
            context = self.next_context(context, word)

        return out

    def get_random_sentence_starter(self):
        total = sum(self.sentence_starters.values())
        num = random.randint(1, total)
        h = 0
        for c in self.sentence_starters:
            l = h
            h = l + self.sentence_starters[c]

            if l < num <= h:
                return c

    def get_random_word(self, context):
        try:
            c = self.model[context]
        except KeyError:
            c = self.model[self.get_random_sentence_starter()]
        if len(c) == 1:
            return c.keys()[0]
        total_words = sum(c.values())
        num = random.randint(1, total_words)

        h = 0
        for word in c:
            l = h
            h = l + c[word]

            if l < num <= h:
                return word

        return c.keys()[0]


if __name__ == '__main__':
        n_gram = NGram()
        n_gram.train()
        print n_gram.generate()
