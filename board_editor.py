import sys
import math

import pygame as pg

import tac.hex.model as model
import tac.hex.view as view
import tac.hex.controller as controller
import tac.hex.controller.game as game
from tac.hex.controller import db_delegate

def create_hex_pos_list(width, height):
    positions = []
    for x in range(width):
        for y in range(height):
            if x % 2 == 0:
                positions.append((x, y * 2))
            else:
                positions.append((x, (y * 2) + 1))
    return [(x + 1, y + 1) for x, y in positions]

def num_hexagons_wide(pix_width, hex_radius):
    return math.floor((2 * pix_width) / (3 * hex_radius) - (1 / 3))

def num_hexagons_tall(pix_height, hex_radius):
    hex_height = math.sqrt(3) * hex_radius
    return math.floor((pix_height / hex_height) - 1/2 )

def autofit(screen_size, hex_radius):
    w_pix, h_pix = screen_size
    w_hex = num_hexagons_wide(w_pix, hex_radius)
    h_hex = num_hexagons_tall(h_pix, hex_radius)
    return create_hex_pos_list(w_hex, h_hex)

class GrassLavaSwap:
    def __init__(self, controller):
        self.controller = controller

    def handle_click(self, click_pix_pos):
        hex_pos = self.controller.board_controller.to_hex(click_pix_pos)
        if self.controller.board_controller.is_valid_pos(hex_pos):
            self.controller.swap_tile(hex_pos)
            self.controller.save()


class Editor(game.Game):
    def swap_tile(self, pos):
        if self.board_controller.get_tile_id_at(pos) == 1:
            tile_c = self.load_tile(2)
        else:
            tile_c = self.load_tile(1)
        self.board_controller.add_tile_controller(tile_c, pos)


HEX_RADIUS = 32
SCREEN_SIZE = (800, 600)

flag, board_name = sys.argv[1:]

pg.init()

#Create the screen
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('Board Editor')

def load_tile(id_, db_delegate):
    data = db_delegate.fetch_tile_data(id_)
    tile = model.Tile(data['id'], data['name'], data['is_impassible'])
    tile_view = view.TileView(data['is_filled'], pg.Color(data['fill_color']))
    return game.TileController(tile, tile_view)


db_delegate = db_delegate.PostgresDelegate('tactical_game')

if flag == '-n':
    if db_delegate.board_exists(board_name):
        raise Exception("Board already exists")
    else:
        pos_list = autofit(SCREEN_SIZE, HEX_RADIUS)
        board_data = []
        for pos in pos_list:
            board_data.append({
                'board_name': board_name, 
                'pos': pos,
                'tile_id': 1, 
                'piece_id': None})
elif flag == '-l':
    if db_delegate.board_exists(board_name):
        board_data = db_delegate.fetch_board_data(board_name)
    else:
        raise Exception("Board does not exist")
else:
    raise Exception("Command not recognized")

board = model.Board(board_name)
board_view = view.BoardView(screen, SCREEN_SIZE, HEX_RADIUS)
board_controller = game.BoardController(board, board_view)

editor = Editor(screen, board_controller, db_delegate)
editor.event_delegate = GrassLavaSwap(editor)

for row in board_data:
    board_controller.add_tile_controller(
        editor.load_tile(row['tile_id']), 
        row['pos'] )

editor.play()
