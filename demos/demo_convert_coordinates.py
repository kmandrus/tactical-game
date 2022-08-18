import pygame as pg

from tac.hex.view import BoardView

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

DIMENSIONS = (800, 600)
RADIUS = 32

screen = pg.display.set_mode(DIMENSIONS)
pg.display.set_caption("Pixel to Hexagonal Coordinate Conversion Demo")

# create_hex_pos_list(18, 13)
board = BoardView(screen, DIMENSIONS, RADIUS)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONUP:
            pix_pos = pg.mouse.get_pos()
            hex_pos = board.to_hex(pix_pos)
            print(f"pix_pos: {pix_pos}, hex_pos: {hex_pos}")
        screen.fill((64, 128, 64))
        board.render()
        pg.display.update()
