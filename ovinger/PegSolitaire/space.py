class Space():
    """
    A class to represent a space in a board of Peg solitaire.

    ...

    Attributes
    ----------
    piece: boolean
        If the space is empty or not
    coord: tuple
        Coordinate of the space
    """

    def __init__(self, piece, coord):
        """
        Initializes the space

        ...

        Attributes
        ----------
        piece: boolean
            If the space is empty or not
        coord: tuple
            Coordinate of the space
        """

        self.piece = piece # Set piece
        self.coord = coord # Set coordinate
        self.neighbors = [] # Set initial neighbors to empty list
    
    def __str__(self):
        """
        When printing the object, return its coordinate and if its empty or not
        """

        return str(self.coord) + ' - ' + str(self.piece)
    
    def has_piece(self):
        """
        Return if the space has a piece
        """

        return self.piece
    
    def add_neighbor(self, space):
        """
        Add neighboring space

        ...

        Parameters
        ----------
        space: Space
            The space to add as neighbor
        """

        self.neighbors.append(space) # Add space to neighbor list

    def get_neighbors(self):
        """
        Return all neighbors of this space
        """
        return self.neighbors
    
    def set_piece(self, piece):
        """
        Set if the space has a piece or not
        """
        self.piece = piece
    