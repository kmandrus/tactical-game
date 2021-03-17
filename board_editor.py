import sys

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
    return positions


class GrassLavaSwap:
    def __init__(self, controller):
        self.controller = controller

    def handle_click(self, click_pix_pos):
        hex_pos = self.controller.board_controller.to_hex(click_pix_pos)
        self.controller.swap_tile(hex_pos)
        self.controller.save_update()


class Editor(game.Game):
    def swap_tile(self, pos):
        if self.board_controller.get_tile_id_at(pos) == 1:
            tile_c = self.load_tile(2)
        else:
            tile_c = self.load_tile(1)
        self.board_controller.add_tile_controller(tile_c, pos)


HEX_RADIUS = 64
SCREEN_SIZE = (800, 600)

flag, name = sys.argv[1:]

pg.init()

#Create the screen
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('Board Editor')

def load_tile(id_, db_delegate):
    data = db_delegate.fetch_tile_data(id_)
    tile = model.Tile(data['id'], data['name'], data['is_impassible'])
    tile_view = view.TileView(data['is_filled'], pg.Color(data['fill_color']))
    return game.TileController(tile, tile_view)

if flag == '-n':
    board = model.Board(name)
#elif flag == '-l':
    #pass
else:
    raise Exception("Command not recognized")


board_view = view.BoardView(screen, SCREEN_SIZE, HEX_RADIUS)
board_controller = game.BoardController(board, board_view)

db_delegate = db_delegate.PostgresDelegate('tactical_game')
editor = Editor(screen, board_controller, db_delegate)
editor.event_delegate = GrassLavaSwap(editor)

pos_list = create_hex_pos_list(13, 9)
for pos in pos_list:
    board_controller.add_tile_controller(editor.load_tile(1), pos)

editor.save_new()
editor.play()
