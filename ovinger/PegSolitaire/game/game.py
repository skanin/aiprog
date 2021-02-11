import itertools
import time
import random
import numpy as np
from .board import Board
from .graph import Graph

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
                board_type, 
                board_size,
                initial_empty,
                update_freq,
                pause):
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

    def make_move(self, move):
        """
        Make a move. For now, this is random.
        """
        # move = random.choice(self.board.get_legal_moves()) # Randomly choose a move from the legal moves
        return self.board.make_move(move), self.calc_reward(), self.is_game_over(), self.get_legal_moves() # Make the move

    def get_remaining_pegs(self):
        """
        Get the remaining pegs on the board.
        """
        return len(list(filter(lambda x: x.has_piece(), itertools.chain(*self.board.content))))

    
    def is_game_over(self):
        return self.is_win() or len(self.get_legal_moves()) == 0

    def is_win(self):
        return self.get_remaining_pegs() == 1

    def calc_reward(self, incremental=True):

        """
        Okay, thanks! 
        Final question: What is a reasonable setup for rewards for the Peg solitaire game? 
        I'm currently using +10 for win and -1 for everything else. 
        This means that the RL system has no preference for losing with few pegs remaining
        (as this just gives more penalty than losing with many pegs), 
        but if it finds a winning state it will converge to always winning, 
        given enough episodes.
        """
        # return (2 * (1 - self.get_remaining_pegs()) / (len(list(itertools.chain(*self.board))) - 2)) + 1
        # if self.is_win():
        #     return 1
        # rew =  1/(len(list(itertools.chain(*self.board))) - 1)
        # print(rew)
        # return rew
        # reward = 0
        
        # if self.is_win():
        #     print('Heyheyheyhey')
        #     reward += 100
        
        # if self.is_game_over() and not self.is_win():
        #     reward += -100
        
        # # #  -1 * 100/self.get_remaining_pegs()
        # for space in itertools.chain(*self.board):
        #     reward += 10 if not space.has_piece() else -10
        # return reward
        # return np.tanh(reward)
        # if not self.is_win() and not self.is_game_over():
        #     return 0.1
        
        # if self.is_game_over() and not self.is_win():
        #     return -10
        
        # return 10
        num_pegs = len(list(itertools.chain(*self.board)))
        remaining_pegs = self.get_remaining_pegs()
        empty_holes = num_pegs - remaining_pegs

        reward = empty_holes/remaining_pegs

        if self.is_win():
            reward += 100
        
        if self.is_game_over() and not self.is_win():
            reward -= 100

        print(reward)
        return reward
        

    def string_representation(self):
        return self.board.string_representation()


if __name__ == '__main__':
    g = Game()
    g.show_game()
    while len(g.get_legal_moves()):
        g.make_move()
        print(g.get_remaining_pegs())
        g.show_game()
    g.G.pause = False
    g.show_game()
    
