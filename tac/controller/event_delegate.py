class Nothing_Selected():
    def __init__(self, controller):
        self.controller = controller
        self.board = controller.board
        self.board_view = controller.board_view

    def handle_click(self, pix_pos):
        hex_pos = self.board_view.to_hex(pix_pos)
        if (self.board.is_valid_pos(hex_pos) and 
            self.board.get_piece_at(hex_pos)):
            self.controller.event_delegate = Piece_Selected(
                self.controller, 
                hex_pos)


class Piece_Selected:
    def __init__(self, controller, piece_pos):
        self.piece_pos = piece_pos
        self.controller = controller
        self.board = controller.board
        self.board_view = controller.board_view
        self.piece = self.board.get_piece_at(piece_pos)
        self.character = controller.get_character(self.piece.id)
    
    def handle_click(self, click_pix_pos):
        click_hex_pos = self.board_view.to_hex(click_pix_pos)
        if self.board.is_empty_at(click_hex_pos):
            self.controller.event_delegate = SelectionFrozen()
            self.controller.move_character(
                self.character,
                click_hex_pos, 
                self.on_move_complete)
        
    def on_move_complete(self):
        self.controller.event_delegate = Nothing_Selected(self.controller)
            

class SelectionFrozen:
    def handle_click(self, click_pix_pos):
        pass
