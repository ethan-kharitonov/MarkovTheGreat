from MarkovChain import MarkovChain
from State import State
from typing import List
from IndividualLocationChain import IndividualLocationChain


class LocationChain(MarkovChain):

    def __init__(self, location_chains: List[IndividualLocationChain]):
        self.location_chains = location_chains

    def transition_probability(self, state1: State, state2: State):
        return None

    def transition_probability_indices(self, i, j):
        return None
