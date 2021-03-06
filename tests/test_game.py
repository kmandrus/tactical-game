from tac.controller import game


class MockSprite:
    def __init__(self):
        self.id = None


class MockPiece:
    def __init__(self):
        self.id = None
        self.pos = 'test pos'

class MockBoard:
    def __init__(self):
        self.move_piece_called_count = 0

    def add_piece(self, piece, pos):
        assert isinstance(piece, MockPiece)
        self.add_piece_called = True
    
    def move_piece(self, start, end):
        self.move_piece_called_count += 1

    def is_empty_at(self, pos):
        return True

class MockBoardView:
    def add_sprite(self, sprite, pos):
        assert isinstance(sprite, MockSprite)
        self.add_sprite_called = True
    
    def to_pix(self, hex_pos):
        return (30, 81)
    
    def move_sprite(self, sprite, pos, callback=None):
        pass



#Character
character_1 = game.Character(MockPiece(), MockSprite())
assert character_1.sprite
assert character_1.piece
assert character_1.get_id()
assert character_1.get_id() == character_1.piece.id == character_1.sprite.id
assert character_1.get_hex_pos() is 'test pos'
character_2 = game.Character(MockPiece(), MockSprite())
assert character_2.get_id() == character_2.piece.id == character_2.sprite.id
assert character_1.get_id() is not character_2.get_id()



#Game
mock_board = MockBoard()
mock_board_view = MockBoardView()
test_game = game.Game('mock_screen', mock_board, mock_board_view)

#Game#create_character
character = test_game.create_character(MockPiece(), MockSprite(), (5, 2))
assert mock_board.add_piece_called
assert mock_board_view.add_sprite_called

#Game#get_character
assert test_game.get_character(character.get_id()) is character

#Game#move_character_along_path
#add in test for callback!
#add in tests that should result in errors, collisions, have improper
#arguements, etc.
path = [(1, 1), (2, 2), (2, 4), (2, 6), (3, 5)]
character = test_game.create_character(MockPiece(), MockSprite(), (1, 1)) 
test_game.board.move_piece_called_count = 0
test_game.move_character_along_path(character, path)
assert test_game.board.move_piece_called_count is len(path)
#assert character.get_hex_pos() is path[-1]

print("Controller unit tests successful!")
