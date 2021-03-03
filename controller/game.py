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
            self.next_frame()
            self.render()
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                hex_pos = self.board_view.to_hex(pg.mouse.get_pos())

    def render(self):
        self.screen.fill((64, 128, 64))
        self.board_view.draw()
        pg.display.update()

    def next_frame(self):
        pass