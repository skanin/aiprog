from space import Space
import itertools
import numpy as np
import math
import random
from boarditerator import BoardIterator

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
            
            if self.board_type == 'T' and coord[0] >= coord[1]: # If the board is a triangle, valid (x, y) pairs are where x >= y
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
    

    def insideBoard(self, coord):
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
                    directions = [(r-1, c+1), (r+1, c-1), (r-1, c), (r+1, c), (r, c-1), (r, c+1)] 
                else:
                    directions = [(r-1, c-1), (r-1, c), (r, c-1), (r+1, c), (r+1, c+1), (r, c+1)] 
                
                for (x, y) in directions: # Loop thorugh all directions
                    if self.insideBoard((x,y)): # If it is a valid coordinate ...
                        space.add_neighbor(self.content[x][y]) # ... We add a new neighbor to space.

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

    # ------------------------ Board methods end -----------------------------


    def __iter__(self):
        """
        Overrides default iterable, so that the class can be iterated over (the board).
        """

        return BoardIterator(self) # return custom iterator