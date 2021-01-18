class BoardIterator():
    """
    Iterator class for the class Board. Makes it possible to iterate over rows in the board.
    """
    def __init__(self, board):
        """
        Initializes the Iterator

        ...

        Parameters
        ----------
        board: Board
            Board class
        """
        self.content = board.content # Set the iterator's content to be the content of the board
        self.index = 0 # Start the index on 0 

    def __next__(self):
        if self.index < len(self.content): # When calling next, (explicit or implicit), make sure there are more elements in content
            res = self.content[self.index] # Store the result
            self.index += 1 # Increment index
            return res # Return the result
        raise StopIteration # If there are no more elements, raise StopIteration

