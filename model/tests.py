from tile import Tile
from piece import Piece

image_name = 'token_1.png'
piece = Piece(image_name)
assert piece.image_name == image_name

tile = Tile()
assert tile.piece == None
tile.piece = piece
assert tile.piece == piece

print("Model unit tests complete. No errors found.")
