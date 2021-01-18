import itertools
import time
import random
from board import Board
from graph import Graph
from config import config

class Game():
    """
    A class to represent a game of Peg solitaire.

    ...

    Attributes
    ----------
    board_type: str
        What type of board to use in the game. Either "D" for diamond or "T" for triangle. Default is D.
    board_size: int
        The size of the board. The size is the length of each side of the board shape. Cannot be zero or negative. The default is 9.
    initial_empty: list
        List of coordinates in the form of tuples, for which spaces that should initially be empty. The default is an empty list
    pause: boolean
        Wether or not the graph should live update or not. Default is True
    update_freq: float
        The update frequency of the live update graph. Default is .01
    """
    def __init__(self, 
                board_type=config['board_type'], 
                board_size=config['board_size'],
                initial_empty=config['initial_empty'],
                update_freq=config['update_freq'],
                pause=config['pause']):
        """
        Initialize a game of Peg solitaire

        ...

        Parameters
        ----------
        board_type: str
            What type of board to use in the game. Either "D" for diamond or "T" for triangle. Default is D.
        board_size: int
            The size of the board. The size is the length of each side of the board shape. Cannot be zero or negative. The default is 9.
        initial_empty: list
            List of coordinates in the form of tuples, for which spaces that should initially be empty. The default is an empty list
        pause: boolean
            Wether or not the graph should live update or not. Default is True
        update_freq: float
            The update frequency of the live update graph. Default is .01
        """
        self.board = Board(board_type, board_size, initial_empty) # Init the board
        self.G = Graph(self.board, pause=pause, update_freq=update_freq) # Init the graph
    
    def show_game(self):
        """
        Show the game as a graph
        """
        self.G.show_board() # Call the graph's show_board.

    def get_legal_moves(self):
        """
        Get all legal moves for the current board state
        """
        return self.board.get_legal_moves() # Call board's get_legal_moves

    def make_move(self):
        """
        Make a move. For now, this is random.
        """
        move = random.choice(self.board.get_legal_moves()) # Randomly choose a move from the legal moves
        self.board.make_move(move) # Make the move

    def get_remaining_pegs(self):
        """
        Get the remaining pegs on the board.
        """
        return len(list(filter(lambda x: x.has_piece(), itertools.chain(*self.board.content))))


if __name__ == '__main__':
    g = Game()
    g.show_game()
    while len(g.get_legal_moves()):
        g.make_move()
        print(g.get_remaining_pegs())
        g.show_game()
    g.G.pause = False
    g.show_game()
    
