from typing import Dict, List, Optional
from collections import namedtuple
from hashlib import md5
from datetime import datetime
from random import random

BoardPosition = namedtuple("BoardPosition", ["x", "y"])


def new_id(name: str, creation_time: datetime = datetime.now(), salt: float = random()) -> str:
    unique_hash = md5()
    unique_hash.update(f"{name}_{creation_time}_{salt}".encode('utf8'))
    return f"{name}_{unique_hash.hexdigest()}"  
    

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


def to_hex_map(positions: List[BoardPosition]) -> Dict[BoardPosition, Tile]:
    return {pos: Tile("Grass", False) for pos in positions}


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
