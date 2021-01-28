game_config = {
    'board_type': 'd',
    'board_size': 4,
    'initial_empty': [(2,1)],
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