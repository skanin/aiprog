game_config = {
    'board_type': 't',
    'board_size': 5,
    'initial_empty': [],
    'update_freq': 0.00001,
    'pause': False,
    'visual': False
}

actor_config = {
    'learning_rate': 0.1,
    'gamma': 0.99,
    'epsilon': 0.5,
    'goal_epsilon': 0.001,
    'eligibility_decay': 0.99
}

critic_config = {
    'learning_rate': 0.1,
    'gamma': 0.99,
    'eligibility_decay': 0.99
}