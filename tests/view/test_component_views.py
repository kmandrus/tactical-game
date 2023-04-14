import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math

import pygame as pg
import pytest

from tac.view.component_views import HexBoardView, HexTileView 


"""
Is it possible to mock pygame in a way that makes the wrapper module
less painful later?
"""


class TestHexTileView:
    def test_render_with_fill(self):
        pass

    def test_render_without_fill(self):
        pass

    def test_get_points(self):
        pass


class TextHexBoardView:
    def test_get_tile_view(self):
        pass

    def test_to_pix_conversion(self):
        pass

    def test_to_hex_conversion(self):
        pass

    def test_to_hex_edge_cases(self):
        pass

    def test_add_sprite(self):
        pass


class TestTacSprite:
    def test_size(self):
        pass

    def test_id(self):
        pass

    def test_set_target_pos(self):
        pass

    def test_update(self):
        # split into component tests...
        # test position
        pass

#Setup
pg.init()
DIMENSIONS = (800, 600)
HEX_RADIUS = 32
mock_surface = "mock surface"

#TileView
center = (400, 300)
hexagon = TileView(mock_surface, center, HEX_RADIUS)

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
image = pg.image.load('./tac/images/token_1.png')
pix_pos = (50, 100)
target_pix_pos = (300, 400)
sprite = TacSprite(image, mock_surface, HEX_RADIUS)
sprite.pos = pix_pos
sprite_size = (math.floor(HEX_RADIUS * 1.5), math.floor(HEX_RADIUS * 1.5))
assert sprite.image.get_size() == sprite_size
assert sprite.surface == mock_surface
assert sprite.pos == pix_pos
assert sprite.id is None

#TacSprite#get_center
assert sprite.get_center() == (26, 76)

#TacSprite#get_velocity
sprite.pos = 100, 100
sprite.set_target_pos((400, 500))
sprite.speed = 5
assert sprite.get_velocity() == (3, 4)

#TacSprite#update
sprite.update()
assert sprite.pos == (103, 104)
sprite.update()
assert sprite.pos == (106, 108)

#TacSprite#set_target_pos
class Callback:
    def __init__(self):
        self.was_called = False
    
    def __call__(self):
        self.was_called = True

callback = Callback()
sprite.pos = (0, 0)
sprite.set_target_pos((10, 10), callback)
for x in range(5):
    sprite.update()

assert callback.was_called

#BoardView
hex_positions = [
    (0, 0), (2, 0), (4, 0), (6, 0), 
    (1, 1), (3, 1), (5, 1),
    (0, 2), (2, 2), (4, 2), (6, 2),
    (1, 3), (3, 3), (5, 3)]
board = BoardView(mock_surface, DIMENSIONS, HEX_RADIUS, hex_positions)
width, height = DIMENSIONS
pix_units = (HEX_RADIUS * 1.5, HEX_RADIUS * math.sqrt(3) / 2)
#BoardView#__init__
assert board.surface == mock_surface
assert board.width == width
assert board.height == height
assert board.hex_radius == HEX_RADIUS
assert board.pix_units == pix_units
assert isinstance(board.sprites, list)

#BoardView#get_tile_view
for pos in hex_positions:
    assert isinstance(board.get_tile_view(pos), TileView)

#BoardView#to_pix
x_unit, y_unit = pix_units
origin = (0, 0)
p1_hex = (3, 3)
p1_pix = (3 * x_unit, 3 * y_unit)
p2_hex = (6, 8)
p2_pix = (6 * x_unit, 8 * y_unit)
assert board.to_pix(origin) == origin
assert board.to_pix(p1_hex) == p1_pix
assert board.to_pix(p2_hex) == p2_pix

#BoardView#to_hex
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
#BoardView#add_sprite
class MockSprite():
    def __init__(self):
        self.pos = None


mock_sprite = MockSprite()
test_pos = (0, 0)
board.add_sprite(mock_sprite, (0, 0))
assert board.sprites == [mock_sprite]
assert mock_sprite.pos == test_pos

print("View unit tests successful!")
