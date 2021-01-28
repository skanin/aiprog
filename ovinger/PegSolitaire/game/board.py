import itertools
import numpy as np
import math
import random

from enum import Enum
from pprint import pprint

from .boarditerator import BoardIterator
from .space import Space

class Board():
    """
    A class to represent a board of Peg solitaire.

    ...

    Attributes
    ----------
    board_type: str
        What type of board to use in the game. Either "D" for diamond or "T" for triangle
    board_size: int
        The size of the board. The size is the length of each side of the board shape. Cannot be zero or negative.
    initial_empty: list
        List of coordinates in the form of tuples, for which spaces that should initially be empty.
        Coordinates for diamond must be in the range [0, size-1]. E.g. (0, 4) - (4, 4) if the size is 5.
        Coordinates for triangle form must be on the form (0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2) ... (size-1, size-1). I.e, x-value must be <= y-value.
        Default for diamond is the center of the board, default for triangle is the top (as stated by Wikipedia).
    """
    
    def __init__(self, board_type, board_size, initial_empty):
        """
        Initializes an instance of the board

        ...

        Parameters
        ----------
        board_type: str
            What type of board to use. Either "D" for diamond or "T" for triangle
        board_size: int
            The size of the board. The size is the length of each side of the board shape. Cannot be zero or negative.
        initial_empty: list
            List of coordinates in the form of tuples, for which spaces that should initially be empty.
            Coordinates for diamond must be in the range [0, size-1]. E.g. (0, 4) - (4, 4) if the size is 5.
            Coordinates for triangle form must be on the form (0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2) ... (size-1, size-1). I.e, x-value must be <= y-value.
            Default for diamond is the center of the board, default for triangle is the top (as stated by Wikipedia).
        """
        self.check_board_type(board_type) # Check that the board type is valid
        self.board_type = board_type.lower() # Set the board type

        self.check_board_size(board_size) # Check that the board size is valid
        self.board_size = board_size # Set the board size

        self.check_initial_empty(initial_empty) # Check that initial_empty is valid
        self.initial_empty = initial_empty # Set the initial_empty

        self.content = [] # Initialize empty content (board)
        self.init_board() # Initialize the board 

    # ------------------------ Validation methods start ------------------------

    def check_board_type(self, board_type):
        """
        Checks whether board type is valid.

        ...

        Parameters
        ----------
        board_type: str
            What type of board to use. Either "D" for diamond or "T" for triangle 
        """

        self.check_correct_variable_type(board_type, "Board_type", str) # Checks that board type is string

        if board_type.lower() not in "dt": # If board_type is not "d" or "t" ...
            raise Exception('Board type must be either "D" for diamond or "T" for triangle') # ... raise exception
    
    def check_board_size(self, board_size):
        """
        Checks whether board_size is valid.

        ...

        Parameters
        ----------
        board_size: int
            Size of the board
        """

        self.check_correct_variable_type(board_size, "Board_size", int) # Checks that board size is an integer
        
        if board_size <= 0: # If board size is negative ...
            raise Exception('Board size cannot be 0 or less.') # ... raise exception
    
    def check_initial_empty(self, initial_empty):
        """
        Checks whether initial_empty is valid.

        ...

        Parameters
        ----------
        initial_empty: list
            List of initial empty spaces
        """

        self.check_correct_variable_type(initial_empty, "Initial_empty", list) # Checks that initial_empty is list

        for coord in initial_empty:
            self.check_correct_variable_type(coord, "Coordinate in initial_empty", tuple) # Checks that each coordinate is tuple
            if not (len(coord) == 2): # Checks that each coordinate is an (x, y) pair ...
                raise Exception(f'Coordinates in initial_empty should be of length 2.') # ... if not, raise exception
            
            if coord[0] >= self.board_size or coord[0] < 0: # Checks that x-value is inside board ...
                raise Exception(f'Invalid x-value in coordinate {coord}. Should be >= 0 or <= board_size ({self.board_size})') # ... if not, raise exception
            
            if coord[1] >= self.board_size or coord[1] < 0: # Checks that y-value is inside board ...
                raise Exception(f'Invalid y-value in coordinate {coord}. Should be >= 0 or <= board_size ({self.board_size})') # ... if not, raise exception
            
            if self.board_type == 't' and coord[0] < coord[1]: # If the board is a triangle, valid (x, y) pairs are where x >= y
                raise Exception(f'Invalid coordinate {coord} for shape Triangle. X-value should be greater than or equal to y-value') # Raise exception if x < y

    def check_correct_variable_type(self, var, name, expected):
        """
        Checks whether var of name name is of datatype expected.

        ...

        Parameters
        ----------
        var: any
            The variable to check
        name: str
            Name of the variable to check, for printing purposes
        expected: type
            The expected datatype of var
        """

        if not isinstance(var, expected): # If the variable is not of the expected type ...
            raise Exception(f'Exception in creating game obejct. {name} should be {expected}, got {type(var)}') # ... raise exception

    # ------------------------ Validation methods end --------------------------

    # ------------------------ Board methods start -----------------------------

    def generate_diamond(self, size):
        """
        Generates diamond board

        ...

        Parameters
        ----------
        size: int
            Size of the board
        """

        return [[Space(True, (j, i)) for i in range(size)] for j in range(size)]
    
    def generate_triangle(self, size):
        """
        Generates triangle board

        ...

        Parameters
        ----------
        size: int
            Size of the board
        """

        return [[Space(True, (j, i)) for i in range(j+1)] for j in range(size)]
    
    def init_board(self):
        """
        Initializes the specified board type, with neighbors and pieces in the spaces.
        """

        if self.board_type.lower() == "d": # If the board type is a diamond ...
            self.content = self.generate_diamond(self.board_size) # ... Create a diamnod shape
        elif self.board_type.lower() == "t": # If the board type is a triangle ...
            self.content = self.generate_triangle(self.board_size) # ... Create a triangle shape
        
        for coord in self.initial_empty: # Loop through all the initial empty spaces
            space = list(filter(lambda x: x.coord[0] == coord[0] and x.coord[1] == coord[1], itertools.chain(*self.content)))[0] # Filter out the specified space ...
            space.set_piece(False) # ... and set it to empty
        
        if not len(self.initial_empty): # If no initial empty coordinates are specified, the default for triangle is (0, 0) and the center for diamond
            (x, y) = self.get_default_initial_empty() # Get the default initial empty, (0, 0) for triangle, center for diamond ...
            self.content[x][y].set_piece(False) # ... and set the center to empty 
        
        self.add_neighbors() # Add neighbors to each space
    

    def inside_board(self, coord):
        """
        Checks if coordinate coord is inside the board.

        ...

        Parameters
        ----------
        coord: tuple
            Coordinate to be checked. (x, y) tuple.
        """

        if self.board_type == 'd': # If the board is a diamond, it is basically a square so we only have to check if the indicies are valid (0 <= (x, y) < board_size).
            return 0 <= coord[0] < self.board_size and 0 <= coord[1] < self.board_size
        # If the board is a triangle, we also have to check that x >= y
        return 0 <= coord[0] < self.board_size and 0 <= coord[1] < self.board_size and coord[0] >= coord[1]

    def add_neighbors(self):
        """
        Add neighbors to spaces in the game board. 
        """

        for r, row in enumerate(self.content): # Loop thorugh each row, with its index
            for c, space in enumerate(row): # Loop through each column(space) in the rows, with its index
                if self.board_type == 'd': # If the board type is diamond, we have some directions that are legal neighbors, in triangle, we have others, as stated in "Representing hexadiagonal grids". The
                    directions = [(r-1, c), (r+1, c), (r, c-1), (r, c+1), (r-1, c+1), (r+1, c-1)] 
                else:
                    directions = [(r-1, c), (r+1, c), (r, c-1), (r, c+1), (r-1, c-1), (r+1, c+1)] 
                
                for (x, y) in directions: # Loop thorugh all directions
                    if self.inside_board((x,y)): # If it is a valid coordinate ...
                        space.add_neighbor(self.content[x][y]) # ... We add a new neighbor to space.
                    else:
                        space.add_neighbor(None) # ... if not, we add None, to be able to get directions later.

    def get_default_initial_empty(self):
        """
        Get center of the board
        """

        if self.board_type == 't': # If the board is a triangle, just return (0, 0)
            return (0, 0)
        center = tuple(np.mean(list(map(lambda x: x.coord, itertools.chain(*self.content))), axis=0)) # Center is the mean of all coordinates
        if self.board_size % 2 == 0: # If the board size is divisible by 2, there are no center. We have to choose between the two closest to the center
            func = random.choice([math.floor, math.ceil]) # Randomly choose floor or ceil function
            return tuple(map(lambda x: func(x), center)) # Return the "center" based on floor or ceil function
        return tuple(map(lambda x: int(x), center)) # return center if board size is not divisible by 2.

    def get_legal_moves_for_space(self, space):
        """
        Get the legal moves for space.

        ...

        Parameters
        ----------
        space: Space
            The space to get legal moves for.
        """

        moves = [] # Initialize the list of legal moves.
        for direction, n in enumerate(space.get_neighbors()): # Loop through the space's neighbors, with their directions (the order in which they were added as neighbors)
            if not n or not n.has_piece() or not n.get_neighbors()[direction] or n.get_neighbors()[direction].has_piece():
                # If the neighbor is None (illegal direction), the neighbor does not have a piece, 
                # the neighbor's neighbor is None (illegal direction from the neighbor) or the neighbor's neighbor has a piece
                # it is not a legal move. 
                continue
            moves.append((space.get_coords(), direction)) # Add the legal move to moves
        return moves # Return this space's legal moves.
                    
    def get_legal_moves(self):
        """
        Get all legal moves for the current state.
        """
        moves = [] # Init empty moves list
        
        for space in itertools.chain(*self.content): # Loop over all spaces
            if not space.has_piece(): # Check that the space has a piece
                continue
            moves.extend(self.get_legal_moves_for_space(space)) # Add this piece's legal moves.
        # print(f'Moves: {moves}')
        return moves # Return all legal moves

    def _get_space_from_coord(self, coord):
        # print(coord)
        return list(filter(lambda x: x.get_coords() == coord, itertools.chain(*self.content)))[0]

    def is_legal_move(self, move):
        """
        Check that move is a legal move.

        ...

        Parameters
        ----------
        move: tuple
            The move to check.
        """
        return move in self.get_legal_moves_for_space(self._get_space_from_coord(move[0])) # Return true if the move is in the spaces legal moves.

    def make_move(self, move):
        """
        Make move move.

        ...

        Parameters
        ----------
        move: tuple
            Move to make.
        """
        if self.is_legal_move(move): # If the move is legal
            for space in itertools.chain(*self.content): # Loop thorugh all spaces on the board
                space.jumped = False # Set jumped to false (for coloring)
                space.jumped_from = False # Set jumped_from to true (for coloring)
            (coord, direction) = move # Unpack the move
            space = self._get_space_from_coord(coord)
            space.set_piece(False) # Remove the piece from the space
            space.jumped_from = True # Set jumped_from to true (for coloring)
            space.get_neighbors()[direction].set_piece(False) # Remove piece from the space that are jumped over
            space.get_neighbors()[direction].get_neighbors()[direction].set_piece(True) # Add piece to the space that are jumped to
            space.get_neighbors()[direction].get_neighbors()[direction].jumped = True # Set jumped to true (for coloring)
        else: # If the move is not legal
            raise Exception(f'Move {move} is illegal in the current board state') # Raise exception.
        
        return self.string_representation()
    
    def string_representation(self):
        st = ''
        for space in itertools.chain(*self.content):
            if space.has_piece():
                st += '1'
            else:
                st += '0'
        return st
    # ------------------------ Board methods end -----------------------------


    def __iter__(self):
        """
        Overrides default iterable, so that the class can be iterated over (the board).
        """

        return BoardIterator(self) # return custom iterator
