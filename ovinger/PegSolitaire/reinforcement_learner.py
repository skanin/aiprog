import matplotlib.pyplot as plt
from actorcritic.env import Env
from actorcritic.actor import Actor
from actorcritic.critic import Critic
from actorcritic.ANNcritic import ANNcritic

class ReinfocementLearner():
    def __init__(self, config):
        self.env = Env()
        self.actor = Actor(
                config['actor_config']['learning_rate'], 
                config['actor_config']['gamma'], 
                config['actor_config']['epsilon'], 
                config['actor_config']['goal_epsilon'], 
                config['actor_config']['eligibility_decay'], 
                config['num_episodes']
                )

        if config['critic'] == 'table':
            self.critic = Critic(
                config['critic_config']['learning_rate'], 
                config['critic_config']['gamma'], 
                config['critic_config']['eligibility_decay'], 
            )
        elif config['critic'] == 'ann':
            self.critic = ANNcritic(
                config['anncritic_config']['learning_rate'], 
                config['anncritic_config']['gamma'], 
                config['anncritic_config']['eligibility_decay'],
                sum(range(config['game_config']['board_size']+1)) if config['game_config']['board_type'].lower() == 't' else config['game_config']['board_size']**2,
                config['anncritic_config']['layers']
            )
        else:
            raise Exception('Critic must be either table or ann')

        self.remaining_pegs = []
        self.rewards = []
        self.num_episodes = config['num_episodes']
        self.config = config


    def train(self):
        self.remaining_pegs = []
        self.rewards = []
        for episode in range(self.num_episodes):
            if episode % 10 == 0:
                print(f'Episode: {episode}')
            self.critic.reset_eligibilities()
            self.actor.reset_eligibilities()

            game, state, legal_moves, done = self.env.reset()
            
            if len(legal_moves) == 0:
                print("No legal moves in this start state")
                break
            
            action = self.actor.get_move(state, legal_moves)
            episode_actions = [] 
            episode_rewards = 0
            while not done:
                self.actor.handle_state(state, legal_moves)
                self.critic.handle_state(state)

                new_state, reward, done, legal_moves = self.env.step(action)
                episode_rewards += reward
                
                if done:
                    break

                new_action = self.actor.get_move(new_state, legal_moves)
                
                self.actor.set_initial_sap_eligibility(state, action)
                
                target, inp = self.critic.calculate_temporal_difference_error(state, reward, new_state)
                episode_actions.append((state, target-inp, action))
                if isinstance(self.critic, Critic):
                    self.critic.set_initial_eligibility(state)
                    self.critic.update_values_and_eligibilities(episode_actions, target-inp)
                else:
                    self.critic.update_weights_and_eligibilities(episode_actions, target, inp)

                self.actor.update_values_and_eligibilities(episode_actions, target-inp, state)
                
                state = new_state
                action = new_action
            # print(f'Episode {episode+1}: {game.get_remaining_pegs()}')
            self.actor._decrease_epsilon(episode+1)
            self.remaining_pegs.append((episode + 1, game.get_remaining_pegs()))
            # print(episode_rewards)
            self.rewards.append((episode + 1, episode_rewards))

    def play_game(self):
        self.actor.set_epsilon_zero()
        game, state, legal_moves, done = self.env.reset()
        action = self.actor.get_move(state, legal_moves)
        while not done:
            state, _, done, legal_moves = self.env.step(action)
            if not done:
                action = self.actor.get_move(state, legal_moves)
            if self.config['game_config']['visual']:
                self.show_game(game, True)
        if self.config['game_config']['visual']:
            self.show_game(game, False)
        

    def show_game(self, game, pause):
        game.G.pause = pause
        game.show_game()

    def show_learning_graph(self):
        x = list(map(lambda x: x[0], self.remaining_pegs))
        y = list(map(lambda x: x[1], self.remaining_pegs))

        plt.plot(x, y)
        plt.xlabel('Episode')
        plt.ylabel('Remaining pegs')
        plt.show()

    def show_reward_graph(self):
        x1 = list(map(lambda x: x[0], self.rewards))
        y1 = list(map(lambda x: x[1], self.rewards))

        plt.plot(x1, y1)
        plt.xlabel('Episode')
        plt.ylabel('Rewards')
        plt.show()

