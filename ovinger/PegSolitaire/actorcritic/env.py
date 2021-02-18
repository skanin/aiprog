from game.game import Game
from config import config

class Env():
    def __init__(self):
        self.game = Game(
                board_type=config['game_config']['board_type'], 
                board_size=config['game_config']['board_size'],
                initial_empty=config['game_config']['initial_empty'],
                update_freq=config['game_config']['update_freq'],
                pause=False
        )

    def reset(self):
        self.game = Game(
                board_type=config['game_config']['board_type'], 
                board_size=config['game_config']['board_size'],
                initial_empty=config['game_config']['initial_empty'],
                update_freq=config['game_config']['update_freq'],
                pause=False
        )
        return self.game, self.game.string_representation(), self.game.get_legal_moves(), self.game.is_game_over()
    
    def step(self, move):
        return self.game.make_move(move)
