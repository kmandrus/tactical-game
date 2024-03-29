"""
View package tests for visual inspection
"""
import os

import pygame as pg

from tac.hex.view import *

def create_hex_pos_list(width, height):
    positions = []
    for x in range(width):
        for y in range(height):
            if x % 2 == 0:
                positions.append((x, y * 2))
            else:
                positions.append((x, (y * 2) + 1))
    return positions


pg.init()

main_dir = os.path.split(os.path.dirname(__file__))[0]
images_dir = os.path.join(main_dir, 'tac/images')

DIMENSIONS = (800, 600)
RADIUS = 64

screen = pg.display.set_mode(DIMENSIONS)
pg.display.set_caption("Render tests for the View package")

board_view = BoardView(screen, DIMENSIONS, RADIUS, create_hex_pos_list(18, 13))

token_art = pg.image.load(os.path.join(images_dir, 'token_1.png'))
start_pos = board_view.to_pix((3, 5))
sprite = TacSprite(token_art, screen, RADIUS)

board_view.add_sprite(sprite, start_pos)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP:
            hex_pos = board_view.to_hex(pg.mouse.get_pos())
            center_of_hex = board_view.to_pix(hex_pos)
            sprite.set_target_pos(center_of_hex)
    screen.fill((64, 128, 64))
    board_view.update()
    board_view.render()        
    pg.display.update()
