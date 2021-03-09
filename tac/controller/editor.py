import pygame as pg

from tac.controller.game import Game


class Editor(Game):
    def __init__(self, screen, board_controller, filepath):
        super().__init__(screen, board_controller)
        self.event_delegate = SwapWalkableOnClick(self, filepath)
    

class SwapWalkableOnClick:
    def __init__(self, controller, filepath):
        self.controller = controller
        self.filepath = filepath

    def handle_click(self, click_pix_pos):
        hex_pos = self.controller.board_controller.to_hex(click_pix_pos)
        self.controller.board_controller.toggle_impassible(hex_pos)
        self.controller.board_controller.save(self.filepath)
