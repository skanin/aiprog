import random

class Critic():
    def __init__(self, learning_rate, gamma, eligibility_decay):
        self.V = {}
        self.eligibilities = {}
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.eligibility_decay = eligibility_decay
        # self.temporal_difference_error = 1

    
    def add_state(self, state):
        self.V[state] = random.uniform(0, 0.1)

    def set_initial_eligibility(self, state):
        self.eligibilities[state] = 1

    def update_state_value(self, state, temporal_difference_error):
        if state not in self.V.keys():
            self.add_state(state)
        
        self.V[state] += self.learning_rate * temporal_difference_error * self.eligibilities.get(state, 1)
    
    def calculate_temporal_difference_error(self, prev_state, reward, new_state):
        if prev_state not in self.V.keys():
            self.add_state(prev_state)
        
        if new_state not in self.V.keys():
            self.add_state(new_state)
        
        inp = self.V[prev_state]
        T = reward + (self.gamma * self.V[new_state])
        return T, inp
    
    # def set_temporal_difference_error(self, prev_state, reward, new_state):
    #     self.temporal_difference_error = self.calculate_temporal_difference_error(prev_state, reward, new_state)

    def reset_eligibilities(self):
        for state in self.eligibilities: 
            self.eligibilities[state] = 0

    def update_eligibilities(self, state, curr_state):
        if state == curr_state:
            self.eligibilities[state] = 1
        else:
        # self.eligibilities[state] = 1 if state == curr_state else self.gamma * self.eligibility_decay * self.eligibilities[state] # + (1 * int(state == curr_state))
            self.eligibilities[state] = self.gamma * self.eligibility_decay * self.eligibilities[state] # + (1 * int(state == curr_state))

    def update_values_and_eligibilities(self, episode_actions, temporal_difference_error):
        for s, _ in episode_actions:
            self.update_state_value(s, temporal_difference_error)
            self.update_eligibilities(s, episode_actions[-1][0])
    
    def handle_state(self, state):
        if state not in self.V.keys():
            self.add_state(state)