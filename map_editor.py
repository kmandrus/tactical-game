import sys

import pygame as pg

import tac.model.hex_model as model
import tac.view.hex_views as view
import tac.controller.editor as controller
import tac.controller.game as game

def create_hex_pos_list(width, height):
    positions = []
    for x in range(width):
        for y in range(height):
            if x % 2 == 0:
                positions.append((x, y * 2))
            else:
                positions.append((x, (y * 2) + 1))
    return positions

HEX_RADIUS = 64
SCREEN_SIZE = (800, 600)

pg.init()

#Create the screen
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('Map Editor')

mode, filepath = sys.argv[1:3]
if mode == '-n' or not mode:
    pos_list = create_hex_pos_list(9, 6)
    grid = model.to_empty_grid(pos_list)
elif mode == '-o':
    grid = model.Board.load_grid(filepath)
else:
    raise Exception("invalid arguments")


board = model.Board(grid)
board_view = view.BoardView(screen, SCREEN_SIZE, HEX_RADIUS, board.get_pos_list())
board_controller = game.BoardController(board, board_view)

editor = controller.Editor(screen, board_controller, filepath)
editor.play()
