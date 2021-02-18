import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from collections import defaultdict


class Net(nn.Module):
    def __init__(self, learning_rate, gamma, eligibility_decay, inp_size, layers):
        super(Net, self).__init__()

        self.learning_rate = learning_rate # Set the learning rate
        self.gamma = gamma # Set discount factor
        self.eligibility_decay = eligibility_decay # Set eligibility_decay

        self.eligibilities = defaultdict(lambda: 1) # Init eligibilities

        self.loss_fn = lambda x: torch.mean(x**2) # Set the loss function (here MSE)

        self.init_model(inp_size, layers) # Initialize the model

        self.optimizer = optim.SGD(self.parameters(), learning_rate, 0.9) # Set the optimizer

    def init_model(self, inp_size, layers):
        """
        Initialize the model
        """
        tmp_layers = [nn.Linear(inp_size, layers[0])] # Input layer is appended first

        for i, size in enumerate(layers):
            # Add relu layers and linear layers with sizes given by config
            tmp_layers.append(nn.ReLU())
            tmp_layers.append(nn.Linear(size, layers[i+1] if i < len(layers) - 1 else 1))

        tmp_layers.append(nn.ReLU()) # Add a ReLU output layer

        self.layers = nn.ModuleList(tmp_layers) # Set the layers

        self.init_eligibilities() # Initialize eligibilities

    def init_eligibilities(self):
        """
        Initialize eligibilities
        """
        for i, layer in enumerate(self.parameters()):
            self.eligibilities[i] = torch.zeros(layer.shape)

    def update_weights_and_eligibilities(self, episode_actions, target, inp):
        """
        Update the weights and eligibilities
        """
        self.optimizer.zero_grad() # Needed for backpropragation. Sets grads to zero
        l = self.loss_fn(target - inp) # Calculate the loss
        l.backward(retain_graph=True) # Compute gradients
        
        with torch.no_grad():
            for s, _, _ in episode_actions: # Loop thorugh all episode actions and update eligibilities and the weights
                for i, layer in enumerate(self.parameters()):
                    self.eligibilities[i] += self.eligibilities[i]*self.eligibility_decay*self.gamma + layer.grad
                    layer = layer + self.eligibilities[i]
            self.optimizer.step() # Optimizer is here SGD, updates the layer with -lr * gradient

    def forward(self, state):
        """
        Do a prediction for the state value
        """
        for layer in self.layers:
            state = layer(state)
        return state


class ANNcritic():
    def __init__(self, learning_rate, gamma, eligibility_decay, inp_size, layers):
        self.model = Net(learning_rate, gamma, eligibility_decay, inp_size, layers) # Set the NN.


    def reset_eligibilities(self):
        """
        Init eligibilities
        """
        self.model.init_eligibilities()
    
    def handle_state(self, state):
        pass

    def state_to_list(self, state):
        """
        Return string representation of state as a list, to be used by the NN
        """
        return list(map(float, list(state)))

    def state_to_tensor(self, state):
        """
        Return string representation of state as a tensor, to be used by the NN
        """
        return torch.Tensor(list(map(float, list(state))))

    def calculate_temporal_difference_error(self, state, reward, new_state):
        """
        Calculate the temporal difference error
        """
        target = torch.add(torch.multiply(self.model(self.state_to_tensor(new_state)), self.model.gamma), reward)
        inp = self.model(self.state_to_tensor(state))

        return target, inp
    
    def update_weights_and_eligibilities(self, episode_actions, target, inp):
        """
        Update weights and eligibilities
        """
        self.model.update_weights_and_eligibilities(episode_actions, target, inp)
