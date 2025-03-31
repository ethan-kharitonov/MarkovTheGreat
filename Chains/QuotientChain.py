
from typing import List
from Phi import Phi
from State import State
from MarkovChain import MarkovChain
from itertools import combinations, product
from QuotientUtils import get_transient_state


class QuotientChain():
    def __init__(self, phi: Phi, N: int, H: int):
        self.phi = phi
        self.N = N
        self.H = H
        self._absorbing_cache = {}

    def get_transient_state(self, i: int) -> State:
        return get_transient_state(i, self.N, self.H)

    def get_absorbing_class(self, r: int) -> List[State]:
        if r in self._absorbing_cache:
            return self._absorbing_cache[r]

        healths = ['S'] * self.N
        states = []
        for idxs in combinations(range(self.N), r):
            for locations in product(range(self.H), repeat=self.N):
                healths_copy = healths[:]
                for i in idxs:
                    healths_copy[i] = 'R'
                states.append(State(health_vector=healths_copy, location_vector=list(locations)))
        self._absorbing_cache[r] = states
        return states

    def q_tt_entry(self, i: int, j: int) -> float:
        s1 = self.get_transient_state(i)
        s2 = self.get_transient_state(j)
        return self.phi.transition_probability(s1, s2)

    def r_tr_entry(self, i: int, r: int) -> float:
        s1 = self.get_transient_state(i)
        C_r = self.get_absorbing_class(r)
        return sum(self.phi.transition_probability(s1, s2) for s2 in C_r)
