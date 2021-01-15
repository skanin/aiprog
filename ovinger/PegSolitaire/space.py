class Space():
    def __init__(self, piece, coord):
        self.piece = piece
        self.coord = coord
        self.neighbors = []
    
    def __str__(self):
        return str(self.coord) + ' - ' + str(self.piece)
    
    def has_piece(self):
        return self.piece
    
    def add_neighbor(self, space):
        self.neighbors.append(space)

    def get_neighbors(self):
        return self.neighbors
    
    def set_piece(self, piece):
        self.piece = piece
    