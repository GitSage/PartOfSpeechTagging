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

        self.transition = {}  # one part of speech to the next. noun : [verb: 60%, adjective: 40%]
        self.emission = {} # one part of speech to words.      noun : [dog: 60%, cat: 30%, wolf: 10%]

        # used for calculating the confusion matrix
        self.predicted = []  # keeps track of the predicted values
        self.real = []  # keeps track of the real values during the final test

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
                            default="text_docs/traintiny.txt")

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

    def train(self):
        print "Creating model from %s" % self.input_file

        # start with the default context
        context = tuple(self.default_context)

        with open(self.input_file, 'r') as in_file:
            text = in_file.read()

            # normalize the string
            text = text.replace('\n', ' ')  # replace all newlines with spaces
            text = text.replace('\r', ' ')  # windows-style newlines too
            text = re.sub('\s+', ' ', text)  # replace multiple spaces with one space

            for word_pos in text.split():
                word_pos_split = (word_pos.split('_'))
                word = word_pos_split[0]
                pos = word_pos_split[1]

                # transition. Concerned only with parts of speech.
                t_poss = self.transition.setdefault(context[0], {pos: 0})
                t_pos = t_poss.setdefault(pos, 0)
                t_poss[pos] = t_pos + 1

                # emission. Concerned with parts of speech to words.
                e_words = self.emission.setdefault(pos, {word: 0})
                e_word = e_words.setdefault(word, 0)
                e_words[word] = e_word + 1

                # update the context with the current word
                context = self.update_context(context, pos)

        # change frequencies to probabilities
        for t_poss in self.transition:
            total = 0
            for freq in t_poss.values():
                total += freq
            for key in t_poss.keys():
                t_poss[key]

        print "transition: ", self.transition
        print "emission: ", self.emission


    @staticmethod
    def update_context(context, word):
        return tuple((list(context) + [word])[1:])

    def confusion_matrix(self, true, predicted):
        """
        Produce a confusion matrix to display the correctness of our algorithm.
        :param list true: the true values of the words. Ex. [['dog', 'noun']]
        :param list predicted: the predicted values of the words. Ex. [['dog', 'verb']]
        :return string: a string detailing the true answer vs. the predicted answer.
                        For example,
                        Noun: Noun (5), Verb (2)
                        Verb: Verb (6)
                        Adjective: Adjective (2), Pronoun (3)
        """

if __name__ == '__main__':
    try:
        n_gram = NGram()
        n_gram.train()
        n_gram.label()
    except Exception, e:
        print e.message
