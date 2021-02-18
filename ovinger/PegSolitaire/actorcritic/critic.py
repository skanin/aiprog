import random

class Critic():
    def __init__(self, learning_rate, gamma, eligibility_decay):
        self.V = {} # Initialize empty state values dict
        self.eligibilities = {} # Init empty eligibilities
        self.learning_rate = learning_rate # Set learning rate
        self.gamma = gamma # Set discount factor
        self.eligibility_decay = eligibility_decay # Set eligibility decay

    
    def add_state(self, state):
        """
        Add a new state to the value dict. Initialize it with a random small value.
        """
        self.V[state] = random.uniform(0, 1)

    def set_initial_eligibility(self, state):
        """
        Set initial eligibilities to be 1
        """
        self.eligibilities[state] = 1

    def update_state_value(self, state, temporal_difference_error):
        """
        Update state value
        """
        if state not in self.V.keys():
            self.add_state(state)
        
        self.V[state] += self.learning_rate * temporal_difference_error * self.eligibilities.get(state, 1)
    
    def calculate_temporal_difference_error(self, prev_state, reward, new_state):
        """
        Calculate temporal difference error
        """
        if prev_state not in self.V.keys():
            self.add_state(prev_state)
        
        if new_state not in self.V.keys():
            self.add_state(new_state)
        
        inp = self.V[prev_state]
        T = reward + (self.gamma * self.V[new_state])
        return T, inp
    

    def reset_eligibilities(self):
        """
        Reset the eligibilities to be 0. This is done between each episode
        """
        for state in self.eligibilities: 
            self.eligibilities[state] = 0

    def update_eligibilities(self, state, curr_state):
        """
        Update eligibilities; decay and discount
        """
        if state == curr_state:
            self.eligibilities[state] = 1
        else:
            self.eligibilities[state] = self.gamma * self.eligibility_decay * self.eligibilities[state]

    def update_values_and_eligibilities(self, episode_actions, temporal_difference_error):
        """
        Loop through all actions and states in a given episode to update the policy and eligibilities
        """
        for s, _, _ in episode_actions:
            self.update_state_value(s, temporal_difference_error)
            self.update_eligibilities(s, episode_actions[-1][0])
    
    def handle_state(self, state):
        """
        Handle a new state. Add it to the value table.
        """
        if state not in self.V.keys():
            self.add_state(state)