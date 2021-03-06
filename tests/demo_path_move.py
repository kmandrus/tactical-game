import os

import pygame as pg

import tac.model.hex_model as model
import tac.view.hex_views as view
import tac.controller.game as controller
import tac.controller.event_delegate as event_delegate

#Utility function to generate a list of positions that represent a board.
#Will likely be moved and/or deprecated later.

class TestPathMove:
    def __init__(self, controller):
        self.controller = controller
        self.board = controller.board

    def handle_click(self, click_pix_pos, callback=None):
        id = 1
        path = [(2, 2), (2, 4), (2, 6), (3, 5)]
        character = self.controller.get_character(id)
        self.controller.event_delegate = event_delegate.SelectionFrozen()
        self.controller.path_move(character, path)


def create_hex_pos_list(width, height):
    positions = []
    for x in range(width):
        for y in range(height):
            if x % 2 == 0:
                positions.append((x, y * 2))
            else:
                positions.append((x, (y * 2) + 1))
    return positions


#Create filepaths for the main directory and images directory
test_dir = os.path.dirname(__file__)
main_dir = os.path.split(test_dir)[0]
image_dir = os.path.join(main_dir, 'tac/images')

#Set constants for the radius of a hexagon in pixels and the screen size
HEX_RADIUS = 64
SCREEN_SIZE = (800, 600)

pg.init()

#Create the screen
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('Battle Map Example')

#Define list of positions on the board
pos_list = create_hex_pos_list(9, 6)

#Define the grid, instantiate the board model and view.
grid = model.to_empty_grid(pos_list)
board = model.Board(grid)
board_view = view.BoardView(screen, SCREEN_SIZE, HEX_RADIUS, pos_list)

#Load sprites and models.
image_1 = pg.image.load(os.path.join(image_dir, 'token_1.png'))
hex_pos_1 = (1, 1)
sprite_1 = view.TacSprite(image_1, screen, HEX_RADIUS)
piece_1 = model.Piece("Makeda")

#Instatiate and run the game
game = controller.Game(screen, board, board_view)
game.create_character(piece_1, sprite_1, hex_pos_1)
game.event_delegate = TestPathMove(game)
game.play()
