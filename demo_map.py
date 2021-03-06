import os

import pygame as pg

import model.hex_model as model
import view.hex_views as view
import controller.game as controller

#Utility function to generate a list of positions that represent a board.
#Will likely be moved and/or deprecated later.
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
main_dir = os.path.dirname(__file__)
image_dir = os.path.join(main_dir, 'images')

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

#Load sprites and add them to the board_view.
image = pg.image.load(os.path.join(image_dir, 'token_1.png'))
pos = board_view.to_pix((3, 5))
sprite = view.TacSprite(image, screen, pos, HEX_RADIUS)
board_view.add_sprite(sprite)

#Instatiate and run the game
game = controller.Game(screen, board, board_view)
game.play()

print('Demo Complete')
