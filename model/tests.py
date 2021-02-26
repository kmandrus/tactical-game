from tile import Tile
from piece import Piece

name = 'Ajani'
piece = Piece(name)
assert piece.name == name

tile = Tile()
assert tile.piece == None
tile.piece = piece
assert tile.piece == piece
tile.piece = None
assert tile.piece == None

print("Model unit tests complete. No errors found.")
