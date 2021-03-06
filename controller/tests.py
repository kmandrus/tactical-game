import game as controller


class MockSprite:
    def __init__(self):
        self.id = None


class MockPiece:
    def __init__(self):
        self.id = None


class MockBoard:
    #add_piece_called = False

    def add_piece(self, piece, pos):
        assert isinstance(piece, MockPiece)
        self.add_piece_called = True
        

class MockBoardView:
    #add_sprite_called = False

    def add_sprite(self, sprite):
        assert isinstance(sprite, MockSprite)
        self.add_sprite_called = True
    
    def to_pix(self, hex_pos):
        return ('pix', 'pix')



#Character
character_1 = controller.Character(MockPiece(), MockSprite())
assert character_1.sprite
assert character_1.piece
assert character_1.get_id()
assert character_1.get_id() == character_1.piece.id == character_1.sprite.id
character_2 = controller.Character(MockPiece(), MockSprite())
assert character_2.get_id() == character_2.piece.id == character_2.sprite.id
assert character_1.get_id() is not character_2.get_id()
print("Controller unit tests successful!")


#Game
mock_board = MockBoard()
mock_board_view = MockBoardView()
game = controller.Game('mock_screen', mock_board, mock_board_view)

#create_character
character = game.create_character(MockPiece(), MockSprite(), ('int', 'int'))
assert mock_board.add_piece_called
assert mock_board_view.add_sprite_called
assert character.sprite.pos == ('pix', 'pix')

#get_character
assert game.get_character(character.get_id()) is character