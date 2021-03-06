def to_empty_grid(pos_list):
    return {pos: Tile() for pos in pos_list}


class Board:
    def __init__(self, grid):
        self.__grid = grid

    def get_tile(self, pos):
        return self.__grid[pos]

    def add_piece(self, piece, pos):
        self.get_tile(pos).piece = piece

    def remove_piece(self, pos):
        self.get_tile(pos).piece = None

    def move_piece(self, start, end):
        if (piece := self.get_tile(start).piece) and self.is_empty_at(end):
            self.remove_piece(start)
            self.add_piece(piece, end)
        else:
            raise Exception(f"Error moving piece from {start} to {end}")

    def get_piece_at(self, pos):
        return self.get_tile(pos).piece

    def is_empty_at(self, pos):
        return self.get_tile(pos).piece == None


class Piece:
    def __init__(self, name):
        self.name = name
        self.id = None


class Tile:
    def __init__(self):
        self.piece = None
        #move cost
        #terrain type
