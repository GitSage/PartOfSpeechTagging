import argparse
import os
from viterbi import Viterbi


class NGram:
    def __init__(self):
        self.model = {}
        self.training_file = ""
        self.testing_file = ""
        self.default_context = [""]  # after parsing args, this will have n elements (the n in ngram)

        self.transition = {}  # one part of speech to the next. noun : [verb: 60%, adjective: 40%]
        self.emission = {} # one part of speech to words.      noun : [dog: 60%, cat: 30%, wolf: 10%]
        self.start = {}

        # used for calculating the confusion matrix
        self.words = []  # keeps track of the actual words
        self.predicted = []  # keeps track of the predicted parts of speech
        self.real = []  # keeps track of the real parts of speech

        # parse the command line args
        self.parse_args()

        self.token_count = 0

    def parse_args(self):
        parser = argparse.ArgumentParser(prog="N-gram random text generator",
                                         description="This program analyzes input text to generate an n-gram model and "
                                                     "then generates random text based on the model",
                                         add_help=True)

        parser.add_argument("--training-file",
                            action="store",
                            help="The path to the input file containing text for learning.",
                            default="text_docs/training.txt")

        parser.add_argument("--testing-file",
                            action="store",
                            help="The path to the input file containing text for testing.",
                            default="text_docs/testsmall.txt")

        # parse the arguments
        args = parser.parse_args()

        self.training_file = args.training_file
        self.testing_file = args.testing_file

        self.default_context = [""]

    def train(self):
        with open(self.training_file, 'r') as in_file:
            text = in_file.read()
            context = tuple(self.default_context)

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
                self.token_count += 1

        # get the starting probability
        for pos in self.emission.keys():
            total = 0
            for t_poss in self.emission[pos]:
                total += self.emission[pos][t_poss]
            pos_probability = float(total) / float(self.token_count)
            self.start[pos] = pos_probability

        # change frequencies to probabilities

        self.convert_freq_to_prob(self.transition)
        self.convert_freq_to_prob(self.emission)

        del self.transition[""]

    def convert_freq_to_prob(self, matrix):
        for t_poss in matrix.values():
            total = 0.0
            for freq in t_poss.values():
                total += freq
            for key in t_poss.keys():
                t_poss[key] /= total

    def update_context(self, context, word):
        return tuple((list(context) + [word])[1:])

    def confusion_matrix(self):
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
        out = ""
        cm = {}
        correct = 0
        incorrect = 0
        for i in range(0, len(self.real)):
            if self.real[i] == self.predicted[i]:
                correct += 1
            else:
                incorrect += 1
            cm.setdefault(self.real[i], {})
            cm[self.real[i]].setdefault(self.predicted[i], 0)
            cm[self.real[i]][self.predicted[i]] += 1
        percentage = float(correct) / (correct + incorrect) * 100
        out += "Result: " + str(percentage) + "% correct.\n"
        out += "Confusion matrix: \n"
        for key, value in cm.iteritems():
            out += "%s: %s\n" % (key, value)

        return out
        # cm = ""
        # for i in range(0, len(self.real)):
        #     print self.predicted[i], self.real[i]

    def label(self):
        vit_obs = []
        hidden_states = []
        vit = Viterbi()
        with open(self.testing_file, 'r') as in_file:
            text = in_file.read()
            for word_pos in text.split():
                word_pos_split = (word_pos.split('_'))
                word = word_pos_split[0]
                pos = word_pos_split[1]
                self.real.append(pos)  # record the true value
                self.words.append(word)
                if pos not in hidden_states:
                    hidden_states.append(pos)
                vit_obs.append(word)

        # print "observation: ", vit_obs
        # print "hidden states: ", hidden_states
        # print "transition: ", self.transition
        # print "emission: ", self.emission
        # print "start: ", self.start
        print "Beginning viterbi algorithm"
        probability, self.predicted = vit.viterbi(vit_obs, hidden_states, self.start, self.transition, self.emission)
        # print "Result of viterbi algorithm: ", self.predicted


if __name__ == '__main__':
    n_gram = NGram()
    print "Training"
    n_gram.train()
    print "Done training"
    print "Labeling"
    n_gram.label()
    print "Done labeling"
    print n_gram.confusion_matrix()
