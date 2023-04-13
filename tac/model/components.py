from typing import Dict, Set, Optional, NamedTuple

from tac.utils import new_id
from tac.exceptions import TileDoesNotExistError, InvalidMoveError


class BoardPosition(NamedTuple):
    x: int
    y: int


class Piece:
    def __init__(self, name: str):
        self.name = name
        self.id: Optional[str] = None


class Tile:
    def __init__(self, name: str, is_impassible: bool):
        self.name = name
        self.id = new_id(self.name)
        self.piece: Optional[Piece] = None
        self.is_impassible = is_impassible
        #move cost
        #terrain type


def get_empty_hex_map(height: int, width: int, tile_name: str) -> Dict[BoardPosition, Tile]:
    map = {}
    for y in range(height):
        for x in range(width):
            if (y % 2) == (x % 2):
                map[BoardPosition(x, y)] = Tile(tile_name, False)
    return map


class Board:
    def __init__(self, name: str, tiles: Dict[BoardPosition, Tile]):
        self.name = name
        self._tiles = tiles

    @property
    def positions(self) -> Set[BoardPosition]:
        return set(self._tiles.keys())

    def add_tile(self, tile: Tile, pos: BoardPosition) -> None:
        self._tiles[pos] = tile 

    def get_tile(self, pos: BoardPosition) -> Tile:
        if self.is_valid_pos(pos):
            return self._tiles[pos]
        raise TileDoesNotExistError(f"Position: {pos} does not exist")
    
    def remove_tile(self, pos: BoardPosition) -> Tile:
        if self.is_valid_pos(pos):
            self._tiles.pop(pos)

    def add_piece(self, piece: Piece, pos: BoardPosition) -> None:
        self.get_tile(pos).piece = piece

    def remove_piece(self, pos: BoardPosition) -> None:
        self.get_tile(pos).piece = None

    def move_piece(self, start: BoardPosition, end: BoardPosition) -> None:
        if self.is_empty(start):
            raise InvalidMoveError(f"No piece to move at start position: {start}")
        if not self.is_empty(end):
            raise InvalidMoveError(f"End position, {end}, occupied by another piece")
        piece = self.get_tile(start).piece
        self.remove_piece(start)
        self.add_piece(piece, end)
    
    def is_impassible(self, pos: BoardPosition) -> bool:
        return self.get_tile(pos).is_impassible

    def is_empty(self, pos: BoardPosition) -> bool:
        return self.get_tile(pos).piece == None
    
    def is_valid_pos(self, pos: BoardPosition) -> bool:
        try:
            self._tiles[pos]
        except KeyError:
            return False
        return True
