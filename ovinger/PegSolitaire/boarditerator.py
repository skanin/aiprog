class BoardIterator():
    def __init__(self, board):
        self.content = board.content
        self.index = 0

    def __next__(self):
        if self.index < len(self.content):
            res = self.content[self.index]
            self.index += 1
            return res
        raise StopIteration

