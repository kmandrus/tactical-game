from typing import Dict, List
from collections import namedtuple

BoardPosition = namedtuple("BoardPosition", ["x", "y"])


def to_empty_grid(positions: List[BoardPosition]) -> Dict[BoardPosition, Tile]:
    return {pos: Tile() for pos in positions}


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
        self.id = None
        self.pos = None


class Tile:
    def __init__(self, id_, name, is_impassible):
        self.id_ = id_
        self.name = name
        self.piece = None
        self.is_impassible = is_impassible
        #move cost
        #terrain type
