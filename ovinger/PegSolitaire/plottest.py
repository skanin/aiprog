import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from space import Space
import networkx as nx
import itertools
from random import randint

def generateDiamond(size):
    return [[Space(True, (j, i)) for i in range(size)] for j in range(size)]



def printDiamond(diamond):
    directions = {
        'rightUp': (-1, 1),
        'leftDown': (1, -1),
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    steps = [(1, 0), (0, 1)]

    # for i in range(len(diamond)):
    #     for j in range(i+1):
    #         if i == 0 and j == 0:


    for i in range(len(diamond)):
        for j in range(i+1):
            print([i, j], end=" ")
        print()

    for i in range(len(diamond)-1, 0, -1):
        for j in range(i):
            print([i, j], end=" ")
        print()


# pprint(generateDiamond(3))

# printDiamond(generateDiamond(3))

def insideBoard(coord, size):
    return 0 <= coord[0] < size and 0 <= coord[1] < size

lst = generateDiamond(3)

for r, row in enumerate(lst):
    for c, space in enumerate(row):
        directions = [(r-1, c+1), (r+1, c-1), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        
        for (x, y) in directions:
            if insideBoard((x,y), 3):
                space.add_neighbor(lst[x][y])


for n in lst[0][0].neighbors:
    print(n)

edges = []
nodes = []

for space in list(itertools.chain(*lst)):
    for n in space.neighbors:
        edges.append((space, n))

G = nx.Graph()
G.add_nodes_from(list(itertools.chain(*lst)))
G.add_edges_from(edges)

pos = {}
fixed_nodes = []
top = 100
count = 3
for node in G:
    (x, y) = node.coord
    if x == y:
        pos[node] = (100 + count//3 * -x, 100 + count//3 * -y)
        count -= 1
        fixed_nodes.append(node)

pos = nx.spring_layout(G,pos=pos)

nx.draw(G, with_labels=True, pos=pos)

plt.show()