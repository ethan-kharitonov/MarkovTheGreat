from MarkovChain import MarkovChain
from States import State
from typing import List
from IndividualLocationChain import IndividualLocationChain
import math

class Phi(MarkovChain):
    def __init__(self, location_chain: IndividualLocationChain, betas: List[float], gamma: float):
        """
        Initialize the Phi Markov Chain.
        
        Args:
            location_chain: The location chain that governs movement between hubs
            beta: Infection rate parameter
            gamma: Recovery rate parameter
        """
        self.location_chain = location_chain
        self.betas = betas
        self.gamma = gamma

    def transition_probability(self, state1: State, state2: State):
        prob = self.location_chain.transition_probability(state1.location_vector, state2.location_vector)
        
        # For each individual i
        for i in range(len(state1.health_vector)):
            current_health = state1.health_vector[i]
            current_location = state1.location_vector[i]
            next_health = state2.health_vector[i]
            
            # Calculate infection rate for current location
            infected_count = sum(1 for j in range(len(state1.health_vector)) 
                               if state1.health_vector[j] == 'I' and state1.location_vector[j] == current_location)
            total_count = sum(1 for j in range(len(state1.health_vector)) 
                            if state1.location_vector[j] == current_location)
            
            if total_count > 0:
                lambda_h = self.betas[current_location] * infected_count / total_count
            else:
                lambda_h = 0
            
            if current_health == 'S':
                infection_prob = 1 - math.exp(-lambda_h)
                
                if next_health == 'I':
                    prob *= infection_prob
                else:
                    return 0
            
            elif current_health == 'I':
                recovery_prob = 1 - math.exp(-self.gamma)
                
                if next_health == 'R':
                    prob *= recovery_prob 
                else:
                    return 0
            
            elif current_health == 'R':
                if next_health != 'R':
                    prob == 0
            
            else:
                raise ValueError("Invalid health state")
        
        return prob

