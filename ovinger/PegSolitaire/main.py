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

# critic = Critic(
#     critic_config['learning_rate'], 
#     critic_config['gamma'], 
#     critic_config['eligibility_decay'], 
# )

critic = ANNcritic(
    anncritic_config['learning_rate'], 
    anncritic_config['gamma'], 
    anncritic_config['eligibility_decay'],
    anncritic_config['inp_size'],
    anncritic_config['layers']
)

remaining_pegs = []

def run(num_episodes, train=True):

    for episode in range(num_episodes):
        print(f'Episode. {episode}')
        critic.reset_eligibilities()
        actor.reset_eligibilities()
        # actor.reset_epsilon()
        game, state, legal_moves, done = env.reset()
        
        if len(legal_moves) == 0:
            print("No legal moves in this start state")
            break
        
        action = actor.get_move(state, legal_moves)
        episode_actions = [] 

        while not done:
            actor.handle_state(state, legal_moves)
            critic.handle_state(state)

            new_state, reward, done, legal_moves = env.step(action)

            if not train:
                game.show_game()
            
            if done:
                break

            new_action = actor.get_move(new_state, legal_moves)
            
            actor.set_initial_sap_eligibility(state, action)
            
            episode_actions.append((state, action))

            temporal_difference_error = critic.calculate_temporal_difference_error(state, reward, new_state)

            if isinstance(critic, Critic):
                critic.set_initial_eligibility(state)
                critic.update_values_and_eligibilities(episode_actions, temporal_difference_error)
            else:
                critic.update_weights_and_eligibilities(episode_actions, temporal_difference_error)

            actor.update_values_and_eligibilities(episode_actions, temporal_difference_error, state)

            state = new_state
            action = new_action
        # print(f'Episode {episode+1}: {game.get_remaining_pegs()}')
        actor._decrease_epsilon()
        remaining_pegs.append((episode + 1, game.get_remaining_pegs()))


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
