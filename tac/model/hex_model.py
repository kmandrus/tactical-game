def to_empty_grid(pos_list):
    return {pos: Tile() for pos in pos_list}


class Board:
    @classmethod
    def load_grid(cls, filepath):
        grid = {}
        with open(filepath) as file:
            for line in file:
                x, y, is_impassible = line.split()
                if is_impassible == 'True':
                    is_impassible = True
                else:
                    is_impassible = False  
                grid[(int(x), int(y))] = Tile(is_impassible)
        return grid
    
    def __init__(self, grid):
        self.__grid = grid

    def save(self, filepath):
        with open(filepath, 'w') as file:
            for pos, tile in self.__grid.items():
                x, y = pos
                file.write(f"{x} {y} {tile.is_impassible}\n")

    def get_tile(self, pos):
        return self.__grid[pos]

    def add_piece(self, piece, pos):
        self.get_tile(pos).piece = piece
        piece.pos = pos

    def remove_piece(self, pos):
        piece = self.get_piece_at(pos)
        self.get_tile(pos).piece = None
        piece.pos = None

    def move_piece(self, piece, end):
        if self.is_empty_at(end):
            self.remove_piece(piece.pos)
            self.add_piece(piece, end)
        else:
            raise Exception(f"Error moving piece to {end}")
    
    def get_pos_list(self):
        return self.__grid.keys()
    
    def toggle_impassible(self, pos):
        if (tile := self.get_tile(pos)).is_impassible:
            tile.is_impassible = False
        else:
            tile.is_impassible = True
    
    def set_impassible(self, pos, value):
        self.get_tile(pos).is_impassible = value
    
    def is_impassible(self, pos):
        return self.get_tile(pos).is_impassible

    def get_piece_at(self, pos):
        if self.is_valid_pos(pos):
            return self.get_tile(pos).piece
        else:
            raise Exception('Invalid Position')

    def is_empty_at(self, pos):
        return self.get_tile(pos).piece == None
    
    def is_valid_pos(self, pos):
        try:
            self.__grid[pos]
        except KeyError:
            return False
        return True


class Piece:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.pos = None


class Tile:
    def __init__(self, is_impassible=False):
        self.piece = None
        self.is_impassible = is_impassible
        #move cost
        #terrain type
