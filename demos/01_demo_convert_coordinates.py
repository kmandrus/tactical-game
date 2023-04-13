import pygame as pg

from tac.view.component_views import HexBoardView, HexTileView
from tac.utils import Dimensions


HEX_RADIUS = 32
SCREEN_DIMENSIONS = Dimensions(width = 800, height = 600) 


class HexConfig:
    def __init__(self, screen_dimensions: Dimensions, hex_radius: int):
        self.screen_dimensions = screen_dimensions
        self.hex_radius = hex_radius
        self.board_dimensions = Dimensions(
            width = screen_dimensions.width // self.hex_radius, 
            height = screen_dimensions.height // self.hex_radius
        )


def get_board_view(screen, config: HexConfig):
    board_view = HexBoardView(screen, config.screen_dimensions, config.hex_radius)
    # add tiles
    fill_color = (0, 0, 0)
    is_filled = False
    for y in range(config.board_dimensions.height):
        for x in range(config.board_dimensions.width):
            if (y % 2) == (x % 2):
                board_view.add_tile_view(HexTileView(is_filled, fill_color), (x,y))
    return board_view
    

def init_pg_and_get_screen(config):
    pg.init()
    screen = pg.display.set_mode(config.screen_dimensions)
    pg.display.set_caption("Pixel to Hexagonal Coordinate Conversion Demo")
    return screen


def run_game(board_view):
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONUP:
                pix_pos = pg.mouse.get_pos()
                hex_pos = board_view.to_hex(pix_pos)
                print(f"pix_pos: {pix_pos}, hex_pos: {hex_pos}")
            screen.fill((64, 128, 64))
            board_view.render()
            pg.display.update()



if __name__ == "__main__":
    config = HexConfig(SCREEN_DIMENSIONS, HEX_RADIUS)
    screen = init_pg_and_get_screen(config)
    board_view = get_board_view(screen, config)
    run_game(board_view)
