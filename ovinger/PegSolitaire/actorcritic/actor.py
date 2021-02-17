import random
from sympy.solvers import solve
from sympy import Symbol

class Actor():
    def __init__(self, learning_rate, gamma, epsilon, goal_epsilon, eligibility_decay, num_episodes):
        self.policy = {} # Init empty policy
        self.learning_rate = learning_rate # Set learning rate
        self.gamma = gamma # Set discount factor
        self.eligibilities = {} # Init empty eligibilities
        self.eligibility_decay = eligibility_decay # SEt eligibility decay
        self.epsilon = epsilon # Set epsilon
        x = Symbol('x') # Init x as a symbol to be used with Sumpy
        self.num_episodes = num_episodes # Set num episodes
        self.goal_epsilon = goal_epsilon # Set goal epsilon
        self.epsilon_decrease = abs(solve(x**(num_episodes) - self.goal_epsilon, x)[0])  # calculate epsilon decrease

    
    def reset_eligibilities(self):
        """
        Reset eligibilities to 0
        """
        for state in self.eligibilities:
            for action in self.eligibilities[state]:
                self.eligibilities[state][action] = 0

    def set_initial_sap_eligibility(self, state, action):
        """
        Set the initial sap eligibility to 1
        """
        if state not in self.eligibilities.keys():
            self.eligibilities[state] = {
                action: 1
            }
        else:
            self.eligibilities[state][action] = 1

    def update_values_and_eligibilities(self, episode_actions, temporal_difference_error, curr_state):
        """
        Loop through all actions and states in a given episode to update the policy and eligibilities
        """
        for s, _, a in episode_actions:
            self.update_policy(s, a, temporal_difference_error)
            self.update_eligibilities(s, a, curr_state)
    
    def _should_random_move(self):
        """
        Determines if the actor should do a random or greedy move
        """
        return random.uniform(0, 1) < self.epsilon

    def _decrease_epsilon(self, episode):
        """
        Decrease epsilon so that the actor does more and more greedy choices
        """
        self.epsilon = (self.epsilon * self.epsilon_decrease) if self.epsilon > self.goal_epsilon else self.epsilon 

    def get_move(self, state, legal_moves=[]):
        """
        Returns a move to make. Either greedy or random.
        """
        if (state not in self.policy.keys()): # If we haven't seen this state before, we have to do a random move
            return random.choice(legal_moves)

        if self._should_random_move(): # If we should random move, choose a move you haven't tried before 
            moves_to_choose_from = list(filter(lambda x: x[1] == 0, self.policy[state].items()))
            return random.choice(moves_to_choose_from)[0] if len(moves_to_choose_from) > 0 else random.choice(list(self.policy[state].keys()))

        # Make sure the greedy move is a move you have tried before
        max_val = float('-inf')
        a = None
        for action, val in self.policy[state].items():
            if val > max_val and val != 0:
                max_val = val
                a = action
        
        a = max(self.policy[state].items(), key=lambda x: x[1])[0] if a is None else a
        return a
        
    def update_eligibilities(self, state, action, curr_state):
        """
        Update eligibilities
        """
        if state == curr_state:
            self.eligibilities[state][action] = 1
        else:
            self.eligibilities[state][action] = self.gamma * self.eligibility_decay * self.eligibilities[state][action] # + (1 * int(state == curr_state))
        

    def reset_epsilon(self):
        """
        Reset epsilon to 1. Used between episodes
        """
        self.epsilon = 1


    def set_epsilon_zero(self):
        """
        Set epsilon to zero, to make only greedy moves
        """
        self.epsilon = 0

    def _add_to_policy(self, state, action):
        """
        Add new sap to policy
        """
        self.policy[state] = {
            action: 0
        }

    def update_policy(self, state, action, temporal_difference_error):
        """
        Update the policy
        """
        if state not in self.policy.keys():
            self._add_to_policy(state, action)
        self.policy[state][action] = self.policy[state].get(action, 0) + self.learning_rate * temporal_difference_error * self.eligibilities.get(state, {}).get(action, 1)
    
    def handle_state(self, state, legal_moves):
        """
        Handle a new state, add all legal actions.
        """
        if state not in self.policy.keys():
            self.policy[state] = {}
            for move in legal_moves:
                self.policy[state][move] = 0