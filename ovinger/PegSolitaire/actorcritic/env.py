from game.game import Game
from .actor import Actor
from config import game_config

class Env():
    def __init__(self):
        self.game = Game(
                board_type=game_config['board_type'], 
                board_size=game_config['board_size'],
                initial_empty=game_config['initial_empty'],
                update_freq=game_config['update_freq'],
                pause=game_config['pause']
        )

    def reset(self):
        self.game = Game(
                board_type=game_config['board_type'], 
                board_size=game_config['board_size'],
                initial_empty=game_config['initial_empty'],
                update_freq=game_config['update_freq'],
                pause=game_config['pause']
        )
        return self.game, self.game.string_representation(), self.game.get_legal_moves(), self.game.is_game_over()
    
    def step(self, move):
        return self.game.make_move(move)
