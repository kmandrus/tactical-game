from typing import List, Optional
from collections import namedtuple

from tac.hex.model.utils import new_id 

BoardPosition = namedtuple("BoardPosition", ["x", "y"])


class Piece:
    def __init__(self, name: str):
        self.name = name
        self.id: Optional[str] = None
        self.pos: Optional[BoardPosition] = None


class Tile:
    def __init__(self, name: str, is_impassible: bool):
        self.name = name
        self.id = new_id(self.name)
        self.piece: Optional[Piece] = None
        self.is_impassible = is_impassible
        #move cost
        #terrain type


class Board:
    def __init__(self, name: str):
        self.name = name
        self._tiles = {}    

    def add_tile(self, tile: Tile, pos: BoardPosition) -> None:
        self._tiles[pos] = tile 

    def get_tile(self, pos: BoardPosition) -> Tile:
        return self._tiles[pos]

    def add_piece(self, piece: Piece, pos: BoardPosition) -> None:
        self.get_tile(pos).piece = piece
        piece.pos = pos

    def remove_piece(self, pos: BoardPosition) -> None:
        piece = self.get_piece_at(pos)
        self.get_tile(pos).piece = None
        piece.pos = None

    def move_piece(self, piece: Piece, end: BoardPosition) -> None:
        if self.is_empty_at(end):
            self.remove_piece(piece.pos)
            self.add_piece(piece, end)
        else:
            raise Exception(f"Error moving piece to {end}")
    
    def get_pos_list(self) -> List[BoardPosition]:
        return self._tiles.keys()
    
    def is_impassible(self, pos: BoardPosition) -> bool:
        return self.get_tile(pos).is_impassible

    def get_piece_at(self, pos: BoardPosition) -> Piece:
        if not self.is_valid_pos(pos):
            raise Exception('Invalid Position')
        return self.get_tile(pos).piece

    def is_empty_at(self, pos: BoardPosition) -> bool:
        return self.get_tile(pos).piece == None
    
    def is_valid_pos(self, pos: BoardPosition) -> bool:
        try:
            self._tiles[pos]
        except KeyError:
            return False
        return True
