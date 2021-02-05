import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

from collections import defaultdict

class ANNcritic():
    def __init__(self, learning_rate, gamma, eligibility_decay, inp_size, layers):
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.eligibility_decay = eligibility_decay
        self.model = self.create_model(inp_size, layers)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.eligibilities = defaultdict(lambda: {})
        print(self.model)

    def create_model(self, inp_size, layers):
        model = nn.Sequential()
        inp_layer = nn.Linear(inp_size, layers[0]) # Input size = prev layer out size, output size = next layer output size
        
        model.add_module('linear0', inp_layer)
        # model.add_module('relu0', nn.ReLU())

        for i, layer in enumerate(layers):
            l = nn.Linear(layer, layers[i+1] if i < len(layers) - 1 else 1)
            model.add_module(f'linear{i+1}', l)
            # model.add_module(f'relu{i+1}', nn.ReLU())
        
        output_layer = nn.Linear(1, 1)
        
        model.add_module(f'linear{len(layers)+1}', output_layer)
        model.add_module(f'relu{len(layers)+1}', nn.ReLU())
    
        return model

    def state_to_list(self, state):
        return torch.Tensor(list(map(lambda x: float(x), list(state))))
    
    def get_value_from_state(self, state):
        return self.model(self.state_to_list(state))

    def calculate_temporal_difference_error(self, prev_state, reward, new_state):
        return reward + ((self.gamma * self.get_value_from_state(new_state)) - self.get_value_from_state(prev_state))

    def update_weights(self, temporal_difference_error):
        for i, layer in enumerate(self.model.parameters()):
            for j, node in enumerate(layer):
                if j not in self.eligibilities[i]:
                    self.eligibilities[i][j] = torch.ones(node.size())
                new = self.learning_rate * temporal_difference_error * self.eligibilities[i][j]
                node.data += new if len(new) > 1 else new[0]
                
            self.optimizer.step()
            
    def reset_eligibilities(self):
        for key in self.eligibilities:
            for key2 in self.eligibilities[key]:
                self.eligibilities[key][key2] = torch.ones(self.eligibilities[key][key2].size())
    
    def update_eligibilities(self, state, curr_state):
        for key in self.eligibilities:
            for key1, val1 in self.eligibilities[key].items():
                self.eligibilities[key][key1] = self.gamma * self.eligibility_decay * val1 + (1 * int(curr_state == state))
    
    def update_weights_and_eligibilities(self, episode_actions, temporal_difference_error):
        self.model.zero_grad()
        with torch.no_grad():
            for s, _ in episode_actions:
                self.update_weights(temporal_difference_error)
                self.update_eligibilities(s, episode_actions[-1][0])
        

    def handle_state(self, state):
        pass

if __name__ == "__main__":
    c = ANNcritic(0.1, 0.99, 0.99, 15, [20, 30, 5])
    s1 = '100111010100101'
    s2 = '100111010010101'
    
    print(float(c.get_value_from_state(s1)[0]))
    episode_actions = [(s1, 2)]

    for param in c.model.parameters():
        for weight in param:
            print(weight)
            break
        break

    c.update_weights_and_eligibilities(episode_actions, c.calculate_temporal_difference_error(s1, 2, s2))
    #c.update_weights_and_eligibilities(episode_actions, c.calculate_temporal_difference_error(s1, 2, s2))
    
    for param in c.model.parameters():
        for weight in param:
            print(weight)
            break
        break

    # for m in c.model.modules():
    #     if isinstance(m, nn.Linear):
    #         for weight in m.weight:
    #             weight = weight * torch.zeros(weight.size())
    #             print(weight)