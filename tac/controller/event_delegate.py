class Nothing_Selected():
    def __init__(self, controller):
        self.controller = controller
        self.board_controller = controller.board_controller

    def handle_click(self, pix_pos):
        pos = self.board_controller.to_hex(pix_pos)
        if (self.board_controller.is_valid_pos(pos) and
            self.board_controller.get_character_at(pos)):
            self.controller.event_delegate = Piece_Selected(
                self.controller, 
                pos)


class Piece_Selected:
    def __init__(self, controller, piece_pos):
        self.piece_pos = piece_pos
        self.controller = controller
        self.board_controller = controller.board_controller
        self.character = self.board_controller.get_character_at(piece_pos)
    
    def handle_click(self, click_pix_pos):
        click_pos = self.board_controller.to_hex(click_pix_pos)
        if self.board_controller.is_empty_at(click_pos):
            self.controller.event_delegate = SelectionFrozen()
            self.board_controller.move_character(
                self.character,
                click_pos, 
                self.on_move_complete)
        
    def on_move_complete(self):
        self.controller.event_delegate = Nothing_Selected(self.controller)
            

class SelectionFrozen:
    def handle_click(self, click_pix_pos):
        pass
