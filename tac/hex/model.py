def to_empty_grid(pos_list):
    return {pos: Tile() for pos in pos_list}


class Board:
    def __init__(self, name):
        self.name = name
        self.__tiles = {}    
    
    def add_tile(self, tile, pos):
        self.__tiles[pos] = tile 

    def get_tile(self, pos):
        return self.__tiles[pos]

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
        return self.__tiles.keys()
    
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
            self.__tiles[pos]
        except KeyError:
            return False
        return True


class Piece:
    def __init__(self, name):
        self.name = name
        self.id_ = None
        self.pos = None


class Tile:
    def __init__(self, id_, name, is_impassible):
        self.id_ = id_
        self.name = name
        self.piece = None
        self.is_impassible = is_impassible
        #move cost
        #terrain type
    
    def to_data(self):
        if piece:
            piece_id = piece.id
        else:
            piece_id = None
        return {'tile_id': self.id_, 'piece_id': piece_id}
