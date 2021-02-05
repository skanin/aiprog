game_config = {
    'board_type': 't',
    'board_size': 5,
    'initial_empty': [],
    'update_freq': .5,
    'pause': False,
    'visual': False
}

actor_config = {
    'learning_rate': 0.1,
    'gamma': 0.9,
    'epsilon': 0.5,
    'goal_epsilon': 0.0001,
    'eligibility_decay': 0.9
}

critic_config = {
    'learning_rate': 0.1,
    'gamma': 0.9,
    'eligibility_decay': 0.9
}

anncritic_config = {
    'learning_rate': 0.001,
    'gamma': 0.9,
    'eligibility_decay': 0.9,
    'inp_size': sum(range(game_config['board_size']+1)) if game_config['board_type'].lower() == 't' else game_config['board_size']**2, 
    'layers': [20, 30, 5]
}