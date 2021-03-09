from tac.controller.game import *


class MockSprite:
    def __init__(self):
        self.id = None
    
    def move(self, pix_pos, callback=None, *args):
        if callback:
            callback(*args)


class MockPiece:
    def __init__(self):
        self.id = None
        self.pos = 'test pos'

class MockCharacter:
    def __init__(self, id):
        self.id = id
        self.piece = MockPiece()
        self.piece.id = id
        self.sprite = MockSprite()
        self.sprite.id = id
    
    def get_id(self):
        return self.id

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

    def get_pos_list(self):
        return []

class MockBoardView:
    def add_sprite(self, sprite, pos):
        assert isinstance(sprite, MockSprite)
        self.add_sprite_called = True
    
    def to_pix(self, hex_pos):
        return (30, 81)
    
    def move_sprite(self, sprite, pos, callback=None):
        pass

class MockBoardController:
    def __init__(self):
        self.add_character_called = False

    def add_character(self, *args):
        self.add_character_called = True


#Character
character_1 = Character(MockPiece(), MockSprite())
assert character_1.sprite
assert character_1.piece
assert character_1.get_id()
assert character_1.get_id() == character_1.piece.id == character_1.sprite.id
assert character_1.get_pos() is 'test pos'
character_2 = Character(MockPiece(), MockSprite())
assert character_2.get_id() == character_2.piece.id == character_2.sprite.id
assert character_1.get_id() is not character_2.get_id()

#Board_Controller
board_controller = BoardController(MockBoard(), MockBoardView())

#Board_Controller#add_character
test_character_1 = MockCharacter(1)
test_character_2 = MockCharacter(2)
pos = 'pos'
board_controller.add_character(test_character_1, pos)
assert board_controller.board.add_piece_called
assert board_controller.board_view.add_sprite_called
board_controller.add_character(test_character_2, pos)

#Board_Controller#get_character
assert board_controller.get_character(test_character_1.id) == test_character_1
assert board_controller.get_character(test_character_2.id) == test_character_2
try:
    board_controller.get_character(3)
    raise Exception('#get_character must raise exception when passed an unregistered id')
except:
    pass

#Board_Controller#move_character
    #probably easier to test this in a demo?
    #it's *almost* a wrapper for the corrosponding methods in the board and sprite
    #and those already well tested...

#Board_Controller#save - Wrapper for now, tested in Board
#Board_Controller#get_character_at - Wrapper, tested in Board
#Board_Controller#to_pix - Wrapper, tested in Board_View
#Board_Controller#to_hex - Wrapper, tested in Board_View
#Board_Controller#set_impassible - Wrapper, tested in Board
#Board_Controller#is_valid_pos - Wrapper, tested in Board
#Board_Controller#is_empty_at - Wrapper, tested in Board


#Game
mock_board = MockBoard()
mock_board_view = MockBoardView()
test_game = Game('mock_screen', MockBoardController())

#Game#create_character
#not super sure how to write a unit test for this function since
#getting characters by id is rooted all the way down in the board class...
piece, sprite = MockPiece(), MockSprite()
pos = 'pos'
new_character = test_game.create_character(piece, sprite, pos)
assert new_character.get_id() == new_character.sprite.id == new_character.piece.id
assert test_game.board_controller.add_character_called


#Game#path_move
#Not a perfect unit test - relies on the implementation of BoardController
test_game = Game('screen', BoardController(MockBoard(), MockBoardView()))
path = [(1, 1), (2, 2), (2, 4), (2, 6), (3, 5)]
character = test_game.create_character(MockPiece(), MockSprite(), (1, 1)) 
test_game.board_controller.board.move_piece_called_count = 0
test_game.path_move(character, path)
assert test_game.board_controller.board.move_piece_called_count is len(path)


print("Controller unit tests successful!")
