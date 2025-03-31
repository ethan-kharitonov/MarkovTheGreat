from MarkovChain import MarkovChain
from State import State
from typing import List
from IndividualLocationChain import IndividualLocationChain
import math

class Phi(MarkovChain):
    def __init__(self, location_chain: IndividualLocationChain, beta: float, gamma: float):
        """
        Initialize the Phi Markov Chain.
        
        Args:
            location_chain: The location chain that governs movement between hubs
            beta: Infection rate parameter
            gamma: Recovery rate parameter
        """
        self.location_chain = location_chain
        self.beta = beta
        self.gamma = gamma

    def transition_probability(self, state1: State, state2: State):
        """
        Calculate the transition probability from state1 to state2.
        This implements the mathematical model from main.tex, considering both health and location transitions.
        
        Args:
            state1: Current state of the system (X_i(t), L_i(t))_{i ∈ N}
            state2: Next state of the system (X_i(t+1), L_i(t+1))_{i ∈ N}
            
        Returns:
            float: The transition probability from state1 to state2
        """
        prob = 1.0
        
        # For each individual i
        for i in range(len(state1.health_vector)):
            current_health = state1.health_vector[i]
            current_location = state1.location_vector[i]
            next_health = state2.health_vector[i]
            next_location = state2.location_vector[i]
            
            # Calculate infection rate for current location
            infected_count = sum(1 for j in range(len(state1.health_vector)) 
                               if state1.health_vector[j] == 'I' and state1.location_vector[j] == current_location)
            total_count = sum(1 for j in range(len(state1.health_vector)) 
                            if state1.location_vector[j] == current_location)
            
            if total_count > 0:
                lambda_h = self.beta * infected_count / total_count
            else:
                lambda_h = 0
            
            # Calculate transition probability based on current health state
            if current_health == 'S':
                # For susceptible individuals:
                # P(Y_i(t+1) = (I,k) | Y_i(t) = (S,j)) = (1 - exp(-λ_h(t)))P_jk^(i)
                infection_prob = 1 - math.exp(-lambda_h)
                
                if next_health == 'I':
                    prob *= infection_prob * location_prob
                else:
                    return 0  # Invalid transition for susceptible individuals
            
            elif current_health == 'I':
                # For infected individuals:
                # P(Y_i(t+1) = (R,k) | Y_i(t) = (I,h)) = (1 - exp(-γ))P_hk^(i)
                recovery_prob = 1 - math.exp(-self.gamma)
                location_prob = self.location_chain.transition_probability(current_location, next_location)
                
                if next_health == 'R':
                    prob *= recovery_prob * location_prob
                else:
                    return 0  # Invalid transition for infected individuals
            
            elif current_health == 'R':
                # For recovered individuals:
                # P(Y_i(t+1) = (R,k) | Y_i(t) = (R,h)) = P_hk^(i)
                location_prob = self.location_chain.transition_probability(current_location, next_location)
                
                if next_health == 'R':
                    prob *= location_prob
                else:
                    return 0  # Invalid transition for recovered individuals
            
            else:
                return 0  # Invalid health state
        
        return prob

