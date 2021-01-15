import networkx as nx
import itertools
import matplotlib.pyplot as plt
from board import Board

class Graph():
    """
    A class to visualize a board of Peg solitaire.

    ...

    Attributes
    ----------
    board: Board
        Instance of a game board.
    """

    def __init__(self, board):
        """
        Initializes an instance of a graph to visualize a board of Peg solitaire.

        ...

        Parameters
        ----------
        board: Board
            Instance of a game board.
        """

        self.board = board # Set the game board

        self.G = nx.Graph() # Initialize graph
        self.edges = [] # Initialize edges to be empty

        for space in itertools.chain(*self.board): # Loop through all spaces in the game board
            for n in space.get_neighbors(): # Loop through this space's neighbors
                self.edges.append((space, n)) # Add the (space, neighbor) relationship to edges

    def show_board(self):
        """
        Shows the board as a graph
        """

        self.G.add_nodes_from(itertools.chain(*self.board)) # Add nodes to the graph
        self.G.add_edges_from(self.edges) # Add edges to the graph (egdes calculated at instantiation)
        
        pos = {} # Init empty position dictionary to fill with positions
        for node in self.G: # Loop through the nodes i G
            (x, y) = node.coord # Get the node's coordinate
            # Set position of the node based on it's coordinate and board type (want triangle shape for triangle and diamond shape for diamond).
            # To be honest, theese values for position are trial and error. I just tweaked them until they fit.
            pos[node] = (100 + (-x)*10 + y*20, 100 + (-x)*10) if self.board.board_type == 't' else (100 + (-x)*10 + y*10, 100 + (-y)*10 + -x*10)

        nx.draw(self.G, with_labels=False, pos=pos, node_color=self.node_color()) # Draw the graph with different colors based on their empty status
        plt.show() # Show the graph

    def node_color(self):
        """
        Returns what colors different nodes should have.
        Empty nodes get black color and non-empty nodes get blue.
        """

        colors = [] # Empty colors list
        for node in itertools.chain(*self.board): # Iterate over the board
            if node.has_piece(): # If the space has a piece
                colors.append('blue') # Append blue color
            else:
                colors.append('black') # Else, append black color
        return colors # Return the colors.

if __name__ == '__main__':
    b = Board('d', 11, [])
    g = Graph(b)
    g.show_board()