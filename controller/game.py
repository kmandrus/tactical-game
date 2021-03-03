import pygame as pg

class Game:
    def __init__(self, screen, board, board_view):
        self.screen = screen
        self.board = board
        self.board_view = board_view
        self.running = True
    
    def play(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                hex_pos = self.board_view.to_hex(pg.mouse.get_pos())
                sprites = self.board_view.sprites
                for sprite in sprites:
                    sprite.target_pos = self.board_view.to_pix(hex_pos)

    def render(self):
        self.screen.fill((64, 128, 64))
        self.board_view.render()
        pg.display.update()

    def update(self):
        self.board_view.update()