import matplotlib.pyplot as plt
import pickle
from actorcritic.env import Env
from actorcritic.actor import Actor
from actorcritic.critic import Critic
from actorcritic.nncritic import ANNcritic
from config import actor_config, critic_config, game_config, anncritic_config

env = Env()

num_episodes = 1000
actor = Actor(
    actor_config['learning_rate'], 
    actor_config['gamma'], 
    actor_config['epsilon'], 
    actor_config['goal_epsilon'], 
    actor_config['eligibility_decay'], 
    num_episodes
    )

pickle.dump(actor, open('not_trained_actor', 'wb'))

if game_config['critic'] == 'table':
    critic = Critic(
        critic_config['learning_rate'], 
        critic_config['gamma'], 
        critic_config['eligibility_decay'], 
    )
else:
    critic = ANNcritic(
        anncritic_config['learning_rate'], 
        anncritic_config['gamma'], 
        anncritic_config['eligibility_decay'],
        anncritic_config['inp_size'],
        anncritic_config['layers']
    )

remaining_pegs = []
rewards = []
def run(num_episodes, train=True):
    
    for episode in range(num_episodes):
        if episode % 10 == 0:
            print(f'Episode: {episode}')
        critic.reset_eligibilities()
        actor.reset_eligibilities()
        # actor.reset_epsilon()
        game, state, legal_moves, done = env.reset()
        
        if len(legal_moves) == 0:
            print("No legal moves in this start state")
            break
        
        action = actor.get_move(state, legal_moves)
        episode_actions = [] 
        episode_rewards = 0
        while not done:
            actor.handle_state(state, legal_moves)
            critic.handle_state(state)

            new_state, reward, done, legal_moves = env.step(action)
            episode_rewards += reward
            if not train:
                game.show_game()
            
            if done:
                break

            new_action = actor.get_move(new_state, legal_moves)
            
            actor.set_initial_sap_eligibility(state, action)
            
            target, inp = critic.calculate_temporal_difference_error(state, reward, new_state)
            episode_actions.append((state, target-inp, action))
            if isinstance(critic, Critic):
                critic.set_initial_eligibility(state)
                critic.update_values_and_eligibilities(episode_actions, target-inp)
            else:
                critic.update_weights_and_eligibilities(episode_actions, target, inp)

            actor.update_values_and_eligibilities(episode_actions, target-inp, state)
            
            state = new_state
            action = new_action
        # print(f'Episode {episode+1}: {game.get_remaining_pegs()}')
        actor._decrease_epsilon()
        remaining_pegs.append((episode + 1, game.get_remaining_pegs()))
        # print(episode_rewards)
        rewards.append((episode + 1, episode_rewards))

run(1000)

def run_after_train(actor):
    actor.epsilon = 0
    game, state, legal_moves, done = env.reset()
    game.G.pause = True
    action = actor.get_move(state, legal_moves)
    while not done:
        state, _, done, legal_moves = env.step(action)
        if not done:
            action = actor.get_move(state, legal_moves)
        game.show_game()
    game.G.pause = False
    game.show_game()

f = open('trained_actor', 'w')
pickle.dump(actor, open('trained_actor', 'wb'))

run_after_train(actor)


x = list(map(lambda x: x[0], remaining_pegs))
y = list(map(lambda x: x[1], remaining_pegs))

plt.plot(x, y)
plt.xlabel('Episode')
plt.ylabel('Remaining pegs')
plt.show()

x1 = list(map(lambda x: x[0], rewards))
y1 = list(map(lambda x: x[1], rewards))

plt.plot(x1, y1)
plt.xlabel('Episode')
plt.ylabel('Rewards')
plt.show()