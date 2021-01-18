import itertools
import time
import random
from board import Board
from graph import Graph
from config import config

class Game():
    def __init__(self, 
                board_type=config['board_type'], 
                board_size=config['board_size'],
                initial_empty=config['initial_empty'],
                update_freq=config['update_freq'],
                pause=config['pause']):

        self.board = Board(board_type, board_size, initial_empty)
        self.G = Graph(self.board, pause=pause, update_freq=update_freq)
    
    def show_game(self):
        self.G.show_board()

    def get_legal_moves(self):
        return self.board.get_legal_moves()

    def make_move(self):
        move = random.choice(self.board.get_legal_moves())
        self.board.make_move(move)


if __name__ == '__main__':
    g = Game()
    g.show_game()
    while len(g.get_legal_moves()):
        g.make_move()
        g.show_game()
    g.G.pause = False
    g.show_game()
    
