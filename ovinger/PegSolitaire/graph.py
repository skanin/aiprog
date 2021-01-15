import networkx as nx
import itertools
import matplotlib.pyplot as plt
from board import Board

class Graph():
    def __init__(self, board):
        self.board = board

        self.G = nx.Graph()
        self.edges = [] 

        for space in list(itertools.chain(*self.board)):
            for n in space.get_neighbors():
                self.edges.append((space, n))

    def show_board(self):
        self.G.add_nodes_from(itertools.chain(*self.board))
        self.G.add_edges_from(self.edges)
        
        pos = {}
        for node in self.G:
            (x, y) = node.coord
            pos[node] = (100 + (-x)*10 + y*20, 100 + (-x)*10) if self.board.board_type == 't' else (100 + (-x)*10 + y*10, 100 + (-y)*10 + -x*10)

        nx.draw(self.G, with_labels=False, pos=pos, node_color=self.node_color())

        plt.show()

    def node_color(self):
        colors = []
        for node in itertools.chain(*self.board):
            if node.has_piece():
                colors.append('blue')
            else:
                colors.append('black')
        return colors

if __name__ == '__main__':
    b = Board('d', 11, [])
    g = Graph(b)
    g.show_board()