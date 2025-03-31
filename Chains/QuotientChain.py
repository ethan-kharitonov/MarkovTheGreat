from MarkovChain import MarkovChain
from State import State
from typing import List
from Phi import Phi


class QuotientChain(MarkovChain):

    def __init__(self, phi: Phi):
        self.phi = phi

    def transition_probability(self, state1: List[State], state2: List[State]):
        if len(state1) > 1 and len(state2) > 1:
            return 1 if state1 == state2 else 0
        if len(state1) > 1:
            return 0

        return sum(self.phi.transition_probability(state1[0], state2[i]) for i in range(len(state2)))


    def transition_probability_indices(self, i, j):
        return self.transition_probability(i, j)
