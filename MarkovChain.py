from abc import ABC, abstractmethod

class MarkovChain(ABC):
    @abstractmethod
    def transition_probability(self, state1, state2):
        pass

    @abstractmethod
    def transition_probability_indices(self, i, j):
        pass

    
