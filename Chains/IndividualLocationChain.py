from typing import List
from MarkovChain import MarkovChain

class IndividualLocationChain(MarkovChain):

    def __init__(self, transition_matrix: List[List[float]]):
        self.transition_matrix = transition_matrix

    def transition_probability(self, hub1: int, hub2: int):
        return self.transition_matrix[hub1][hub2]

    def transition_probability_indices(self, i, j):
        return self.transition_probability(i, j)
