from math import log
import sys

__author__ = 'lexi'


class Viterbi:
    def __init__(self):
        pass

    def viterbi(self, observations, hiddenStates, start_p, trans_p, emiss_p):
        """
        :param observations: the observable sequence of things (For example: Words).
        :param hiddenStates: a set of the hidden states (For example: Parts of speech). Order does not matter.
        :param start_p: Our belief about what the state is without knowing any previous states/observations.
        :param trans_p: For example: Given a hidden state, what is the probability that the NEXT hidden state will be xyz?
        :param emiss_p: For example, Given a hidden state xyz, what is the probability that the corresponding OBSERVED state is abc?
        :return: list of hiddenStates that most likely correspond to the sequence of observations.
        """
        SMALL = 0.000001
        # V_{t,k}: "the probability of the most probable state sequence responsible for the
        # first t observations that has k as its final state." - Wikipedia
        V = [{}]
        path = {}

        # Initialize base cases (t == 0)
        # States = ('Healthy', 'Fever') on Wikipedia. In our example, they are "Parts of Speech".

        count = 0
        # For each hidden state possible...
        for hiddenState in hiddenStates:
            # For example:  (Likelihood of first state being the hidden state)  =
            # (probability of this hidden state being first) *
            # (probability that this hidden state corresponds to the first observation)
            V[0][hiddenState] = log(start_p[hiddenState]) + log(emiss_p[hiddenState].setdefault(observations[0], SMALL))

            # ????
            path[hiddenState] = [hiddenState]

        # Run Viterbi for t > 0
        # Range: [included, not included). So basically, iterate starting at the 2nd observation,
        # and continue up to AND INCLUDING the last observation.
        for t in range(1, len(observations)):
            # Add an empty dictionary
            count += 1
            V.append({})
            newpath = {}

            # Make an entry in the "newpath" dictionary for each possible hiddenState.
            # -----------------------------------------------------------------------------
            # For each possible hiddenState, what is the most likely state to precede it?
            # -----------------------------------------------------------------------------
            for hiddenState in hiddenStates:
                # ??? = tuple:
                #           ( THIS_HIDDEN_STATE)  ---> (hiddenState)
                #                   |                        |
                #                   v                        v
                #             observations[t-1]        observations[t]
                #
                #           (maximum probability of:
                #                     Likelihood that the first t-1 observations have THIS_HIDDEN_STATE as the final
                #                     state  *TIMES* probability of hiddenState, given that the previous state was THIS_
                #                     HIDDEN_STATE *TIMES* probability that hiddenState generated the t'th observation
                #           , THIS_HIDDEN_STATE that produced the maximum probability)


                # Most likely state to precede it, and its probability.
                (prob, state) = max((V[t-1][THIS_HIDDEN_STATE] +
                                     log(trans_p[THIS_HIDDEN_STATE].setdefault(hiddenState, SMALL)) +
                                     log(emiss_p[hiddenState].setdefault(observations[t], SMALL)),
                                     THIS_HIDDEN_STATE)
                                    for THIS_HIDDEN_STATE in hiddenStates)

                # Likelihood that the first t observations have hiddenState as the final state ====== the probability
                # that the most-likely-state precedes it.
                V[t][hiddenState] = prob
                newpath[hiddenState] = path[state] + [hiddenState]

            sys.stdout.write("\rWorking on observation %d of %d" % (count, len(observations)))
            sys.stdout.flush()

            # Don't need to remember the old paths
            path = newpath

        sys.stdout.write("\rWorking on observation %d of %d \n" % (count+1, len(observations)))
        sys.stdout.flush()

        # if len(observations) == 1:
        lastObservationIndex = 0  # if only one element is observed max is sought in the initialization values
        if len(observations) != 1:
            # t is the array-index of the last element of the observations. (It is observation-length minus 1.)
            lastObservationIndex = t

        # Likelihood that all the observations have "hiddenState" as the final state.
        (prob, state) = max((V[lastObservationIndex][hiddenState], hiddenState) for hiddenState in hiddenStates)
        return prob, path[state]

    # Don't study this, it just prints a table of the steps.
    def print_dptable(self, V):
        s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
        for y in V[0]:
            s += "%4s: " % y
            s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
            s += "\n"
        print(s)

if __name__ == "__main__":
    states = ('Healthy', 'Fever')

    observations = ('normal', 'cold', 'dizzy')

    start_probability = {'Healthy': 0.6, 'Fever': 0.4}

    transition_probability = {
       'Healthy' : {'Healthy': 0.7, 'Fever': 0.3},
       'Fever' : {'Healthy': 0.4, 'Fever': 0.6}
       }

    emission_probability = {
       'Healthy' : {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1},
       'Fever' : {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}
       }
    #a = self.getProb(start_probability, hiddenState) * self.getProb2(emission_probability, hiddenState, self.getProb(observations, 0))
        #(prob, state) = max((V[t-1][THIS_HIDDEN_STATE] * self.getProb2(transition_probability, THIS_HIDDEN_STATE, hiddenState) * self.getProb2(emission_probability, hiddenState, self.getProb(observations, t)), THIS_HIDDEN_STATE) for THIS_HIDDEN_STATE in hiddenStates)

    v = Viterbi()
    print v.viterbi(observations,
                       states,
                       start_probability,
                       transition_probability,
                       emission_probability)
