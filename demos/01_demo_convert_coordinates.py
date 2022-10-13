import pygame as pg


from tac.hex.view import BoardView, TileView


DIMENSIONS = (800, 600)
RADIUS = 32
HEX_HEIGHT = DIMENSIONS[0] // RADIUS
HEX_WIDTH = DIMENSIONS[1] // RADIUS


pg.init()
screen = pg.display.set_mode(DIMENSIONS)
pg.display.set_caption("Pixel to Hexagonal Coordinate Conversion Demo")


# Setup
board = BoardView(screen, DIMENSIONS, RADIUS)
# Add tiles to the board
fill_color = (0, 0, 0)
is_filled = False
for y in range(HEX_HEIGHT):
    for x in range(HEX_WIDTH):
        if (y % 2) == (x % 2):
            board.add_tile_view(TileView(is_filled, fill_color), (x,y))

# Run
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
