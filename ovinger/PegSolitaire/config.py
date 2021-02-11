game_config = {
    'board_type': 'T',
    'board_size': 5,
    'initial_empty': [], # (1,1), (2,2), (3,1), (1,3), (3,3)
    'update_freq': .1,
    'pause': False,
    'visual': False,
    'critic': 'ann'
}

actor_config = {
    'learning_rate': 0.1,
    'gamma': 0.9,
    'epsilon': 1,
    'goal_epsilon': 0,
    'eligibility_decay': 0.99
}

critic_config = {
    'learning_rate': 0.1,
    'gamma': 0.9,
    'eligibility_decay': 0.99
}

anncritic_config = {
    'learning_rate': 1e-3,
    'gamma': 0.9,
    'eligibility_decay': 0.9,
    'inp_size': sum(range(game_config['board_size']+1)) if game_config['board_type'].lower() == 't' else game_config['board_size']**2, 
    'layers': [15, 10, 5]
}