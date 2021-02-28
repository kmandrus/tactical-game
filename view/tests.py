#View unit tests
import math

import pygame as pg

from hexagon_view import HexagonView
from tac_sprite import TacSprite
from hex_board_view import HexBoardView


class MockImage:
    def get_size(self):
        return (32, 32)


#Setup
pg.init()
DIMENSIONS = (800, 600)
HEX_RADIUS = 32
mock_surface = "mock surface"


#HexagonView
center = (400, 300)
hexagon = HexagonView(mock_surface, center, HEX_RADIUS)

#Hexagonl#__init__
assert hexagon.surface == mock_surface
assert hexagon.center == center
assert hexagon.radius == HEX_RADIUS
assert hexagon.half_height == (math.sqrt(3) * HEX_RADIUS) / 2
assert hexagon.is_filled == False
assert not hexagon.fill_color == None

#Hexagon#get_points
points = [
    (384.0, 272.28718707889794), 
    (416.0, 272.28718707889794), 
    (432, 300),
    (416.0, 327.71281292110206), 
    (384.0, 327.71281292110206), 
    (368, 300)]
assert hexagon.get_points() == points


#TacSprite
mock_image = MockImage()
pix_pos = (50, 100)
target_pix_pos = (300, 400)
sprite = TacSprite(mock_image, mock_surface, pix_pos)

assert sprite.image == mock_image
assert sprite.surface == mock_surface
assert sprite.pos == pix_pos
assert sprite.draw_centered == False

#TacSprite#get_center
assert sprite.get_center() == (34, 84)

#TacSprite#get_velocity
sprite.pos = 100, 100
sprite.target_pos = 400, 500
sprite.speed = 5
assert sprite.get_velocity() == (3, 4)

#TacSprite#move
sprite.move()
assert sprite.pos == (103, 104)
sprite.move()
assert sprite.pos == (106, 108)
sprite.target_pos == None
try:
    sprite.move()
    raise AssertionError
except Exception:
    pass


#HexBoardView
hex_positions = [
    (0, 0), (2, 0), (4, 0), (6, 0), 
    (1, 1), (3, 1), (5, 1),
    (0, 2), (2, 2), (4, 2), (6, 2),
    (1, 3), (3, 3), (5, 3)]
board = HexBoardView(mock_surface, DIMENSIONS, HEX_RADIUS, hex_positions)
width, height = DIMENSIONS
pix_units = (HEX_RADIUS * 1.5, HEX_RADIUS * math.sqrt(3) / 2)
#HexBoardView#__init__
assert board.surface == mock_surface
assert board.width == width
assert board.height == height
assert board.hex_radius == HEX_RADIUS
assert board.pix_units == pix_units

#HexBoardView#get_hexagon
for pos in hex_positions:
    assert isinstance(board.get_hexagon(pos), HexagonView)

#HexBoardView#to_pix
x_unit, y_unit = pix_units
origin = (0, 0)
p1_hex = (3, 3)
p1_pix = (3 * x_unit, 3 * y_unit)
p2_hex = (6, 8)
p2_pix = (6 * x_unit, 8 * y_unit)
assert board.to_pix(origin) == origin
assert board.to_pix(p1_hex) == p1_pix
assert board.to_pix(p2_hex) == p2_pix

#HexBoardView#to_hex
assert board.to_hex(origin) == origin
assert board.to_hex(p1_pix) == p1_hex
assert board.to_hex(p2_pix) == p2_hex
#Edge cases
edge_case_pos_pairs = [ 
    ((253, 120), (5, 5)),
    ((276, 124), (6, 4)),
    ((298, 130), (6, 4)),
    ((320, 127), (7, 5))
]
for pix_pos, hex_pos in edge_case_pos_pairs:
    assert board.to_hex(pix_pos) == hex_pos


print("View unit tests successful!")
