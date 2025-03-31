from MarkovChain import MarkovChain
from State import State
from typing import List
from IndividualLocationChain import IndividualLocationChain


class LocationChain(MarkovChain):

    def __init__(self, location_chains: List[IndividualLocationChain]):
        self.location_chains = location_chains

    def transition_probability(self, state1: State, state2: State):
        probability = 1.0
        for chain in self.location_chains:
            probability *= chain.transition_probability(state1, state2)
        return probability

    def transition_probability_indices(self, i, j):
        return self.transition_probability(i, j)
