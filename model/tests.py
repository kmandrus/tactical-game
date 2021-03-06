from hex_model import *


#Piece Tests
name = 'Ajani'
piece = Piece(name)
assert piece.name == name
assert piece.id is None


#Tile Tests
tile = Tile()
assert tile.piece == None
tile.piece = piece
assert tile.piece == piece
tile.piece = None
assert tile.piece == None


#Board Tests
#board#to_empty_grid
positions = [(x, y) for x in range(10) for y in range(10)]
grid = to_empty_grid(positions)
for pos in positions:
    assert grid[pos]
    assert not grid[pos].piece

board = Board(grid)
pos = (3, 3)
other_pos = (2, 5)
pos_outside_board = (12, 12)

#Board#get_tile
assert board.get_tile(pos)
try:
    board.get_tile(pos_outside_board)
    raise AssertionError
except KeyError:
    pass
assert not board.get_tile(pos).piece

#Board#add_piece
mock_piece = "mock"
board.add_piece(mock_piece, pos)
assert board.get_tile(pos).piece == mock_piece

#Board#get_piece_at
assert board.get_piece_at(pos) == mock_piece

#Board#is_empty_at
assert board.is_empty_at(other_pos)
assert not board.is_empty_at(pos)

#Board#remove_piece
board.remove_piece(pos)
assert not board.get_piece_at(pos)
assert not board.get_tile(other_pos).piece
assert board.is_empty_at(pos)

#Board#move_piece
board.add_piece(mock_piece, pos)
board.move_piece(pos, other_pos)
assert not board.get_tile(pos).piece
assert not board.get_piece_at(pos)
assert board.is_empty_at(pos)
assert board.get_tile(other_pos).piece == mock_piece
assert board.get_piece_at(other_pos) == mock_piece
assert not board.is_empty_at(other_pos)
try:
    board.move_piece(pos, other_pos)
    raise AssertionError
except Exception:
    pass


print("Model unit tests successful!")
