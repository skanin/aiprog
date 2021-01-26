import random
from sympy.solvers import solve
from sympy import Symbol

class Actor():
    def __init__(self, learning_rate, gamma, epsilon, goal_epsilon, eligibility_decay, num_episodes):
        self.policy = {}
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.eligibilities = {}
        self.eligibility_decay = eligibility_decay
        self.epsilon = epsilon
        x = Symbol('x')
        self.num_episodes = num_episodes
        self.epsilon_decrease = solve(self.epsilon - num_episodes*x - goal_epsilon, x)[0]
        print(self.epsilon_decrease)

    def _initialize_policy(self):
        for state in self.policy:
            for action in self.policy[state]:
                self.policy[state][action] = 0
    
    def reset_eligibilities(self):
        for state in self.eligibilities:
            for action in self.eligibilities[state]:
                self.eligibilities[state][action] = 0

    def set_initial_sap_eligibility(self, state, action):
        if state not in self.eligibilities.keys():
            self.eligibilities[state] = {
                action: 1
            }
        else:
            self.eligibilities[state][action] = 1

    def update_values_and_eligibilities(self, episode_actions, temporal_difference_error, curr_state):
        for s, a in episode_actions:
            self.update_policy(s, a, temporal_difference_error)
            self.update_eligibilities(s, a, curr_state)
    
    def _should_random_move(self):
        return random.uniform(0, 1) < self.epsilon

    def _decrease_epsilon(self):
        self.epsilon -= self.epsilon_decrease

    def get_move(self, state, legal_moves=[]):
        if (state not in self.policy.keys()) or (state in self.policy.keys() and self._should_random_move()):
            print('Exploration')
            a = random.choice(legal_moves)
        else:
            print('Greedy')
            a = max(self.policy[state].items(), key=lambda x: x[1])[0]
        
        return a

    def update_eligibilities(self, state, action, curr_state):
        self.eligibilities[state][action] = self.gamma * self.eligibility_decay * self.eligibilities[state][action] + (1 * int(state == curr_state))

    def reset_epsilon(self):
        self.epsilon = 0.5

    def _add_to_policy(self, state, action):
        self.policy[state] = {
            action: 0
        }

    def update_policy(self, state, action, temporal_difference_error):
        if state not in self.policy.keys():
            self._add_to_policy(state, action)
        self.policy[state][action] = self.policy[state].get(action, 0) + self.learning_rate * temporal_difference_error * self.eligibilities.get(state, {}).get(action, 1)