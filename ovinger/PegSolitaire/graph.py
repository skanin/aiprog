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

    def __init__(self, board, pause, update_freq=1):
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
        
        self.pause = pause
        self.init_graph()
        self.positions = self.generate_positions()

        self.update_freq = update_freq

    def init_graph(self):
        if self.pause:
            plt.ion()
        self.G.clear()
        self.G.add_nodes_from(itertools.chain(*self.board)) # Add nodes to the graph
        self.G.add_edges_from(self.edges) # Add edges to the graph (egdes calculated at instantiation)
    
    def generate_positions(self):
        pos = {} # Init empty position dictionary to fill with positions
        for node in self.G: # Loop through the nodes i G
            (x, y) = node.coord # Get the node's coordinate
            # Set position of the node based on it's coordinate and board type (want triangle shape for triangle and diamond shape for diamond).
            # To be honest, theese values for position are trial and error. I just tweaked them until they fit.
            pos[node] = (100 + (-x)*10 + y*20, 100 + (-x)*10) if self.board.board_type == 't' else (100 + (-x)*10 + y*10, 100 + (-y)*10 + -x*10)
        return pos

    def show_board(self):
        """
        Shows the board as a graph
        """
        plt.clf()
        nx.draw(self.G, with_labels=False, pos=self.positions, node_color=self.node_color(), node_size=300) # Draw the graph with different colors based on their empty status
        if self.pause:
            plt.pause(self.update_freq) 
        else:
            plt.show(block=True)
        

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
    b = Board('d', 10)
    g = Graph(b, pause=True)
    for move in b.get_legal_moves():
        print(move[0], move[1])
    g.show_board()
    space = list(filter(lambda x: x.coord[0] == 0 and x.coord[1] == 0, itertools.chain(*b)))[0]
    space.set_piece(False)
    g.pause = False
    g.show_board()