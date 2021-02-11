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
        # self.device = torch.device('cpu')
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)
        self.optimizer = optim.SGD(self.model.parameters(), learning_rate, 0.9)
        self.eligibilities = defaultdict(lambda: {})
        self.loss_fn = F.mse_loss
        

    def create_model(self, inp_size, layers):
        model = nn.Sequential()
        inp_layer = nn.Linear(inp_size, layers[0]) # Input size = prev layer out size, output size = next layer output size
        
        model.add_module('linear0', inp_layer)
        model.add_module('relu0', nn.ReLU())

        for i, layer in enumerate(layers):
            l = nn.Linear(layer, layers[i+1] if i < len(layers) - 1 else 1)
            model.add_module(f'linear{i+1}', l)
            model.add_module(f'relu{i+1}', nn.ReLU())
        
        output_layer = nn.Linear(1, 1)
        
        model.add_module(f'linear{len(layers)+1}', output_layer)
        model.add_module(f'relu{len(layers)+1}', nn.LeakyReLU())
    
        return model

    def state_to_list(self, state):
        s = torch.Tensor(list(map(float, list(state)))).to(self.device)
        #print(s)
        return s

    def get_value_from_state(self, state):
        pred = self.model(self.state_to_list(state))
        print(f'pred: {pred.cpu().detach().numpy()[0]}')
        return pred

    def calculate_temporal_difference_error(self, prev_state, reward, new_state):
        # print(prev_state)
        T = torch.add(torch.multiply(self.get_value_from_state(new_state), self.gamma), reward)
        # print(f'Expected: {T}')
        prev = self.get_value_from_state(prev_state)
        # print(f'Got: {prev}')
        temp_diff = T - prev
        # print(temp_diff)
        return T, prev

    def update_weights(self, temporal_difference_error):
        for i, layer in enumerate(self.model):
            if not isinstance(layer, nn.Linear):
                continue
            # print(layer)
            for j, weight in enumerate(layer.weight):
                # print('---------------------------------------------')
                # print(layer.weight[j]) 
                if j not in self.eligibilities[i]:
                    self.eligibilities[i][j] = torch.zeros(weight.size()).to(self.device)
                new = torch.multiply(self.eligibilities[i][j], self.learning_rate * temporal_difference_error)
                # print(new)
                layer.weight[j] = torch.add(new if len(new) > 1 else new[0], weight)
                # print(layer.weight[j])             
                # print('---------------------------------------------')
            
            
            
    def reset_eligibilities(self):
        for key in self.eligibilities:
            for key2 in self.eligibilities[key]:
                self.eligibilities[key][key2] = torch.zeros(self.eligibilities[key][key2].size()).to(self.device)
    
    def update_eligibilities(self, decay=False, state=None, curr_state=None):
        if not decay:
            for i, layer in enumerate(self.model.parameters()):
                # if not isinstance(layer, nn.Linear):
                #     continue
                for j in range(len(layer)):
                    if j not in self.eligibilities[i]:
                        self.eligibilities[i][j] = torch.zeros(layer[j].size()).to(self.device)
                    self.eligibilities[i][j] = torch.add(self.eligibilities[i][j], layer.grad[j])
        else:
            for key in self.eligibilities:
                for key1, val1 in self.eligibilities[key].items():
                    self.eligibilities[key][key1] = torch.multiply(val1, self.gamma * self.eligibility_decay)

    def update_weights_and_eligibilities(self, episode_actions, target, inp):
        self.optimizer.zero_grad()
        #print(temporal_difference_error[0])
        l = self.loss_fn(inp, target)
        # print(f'Target {target}')
        # print(f'Inp {inp}')
        #print(l)
        l.backward()
        
        self.update_eligibilities()
        
        
        with torch.no_grad():
            for s, td, _ in episode_actions:
                self.update_weights(torch.subtract(target, inp))
                self.update_eligibilities(True, s, episode_actions[-1][0])
                
            self.optimizer.step()
        
        
        
    # def calculate_target_value(self, reward, next_state):

    def handle_state(self, state):
        pass

if __name__ == "__main__":
    c = ANNcritic(0.1, 0.99, 0.99, 15, [20, 30, 5])
    s1 = '100111010100101'
    s2 = '100111010010101'
    
    print(c.get_value_from_state(s1).detach().numpy()[0])
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