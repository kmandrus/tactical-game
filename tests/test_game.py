import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

class MockPieceController:
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
        self.add_piece_controller_called = False

    def add_piece_controller(self, *args):
        self.add_piece_controller_called = True


#PieceController
piece_controller_1 = PieceController(MockPiece(), MockSprite())
assert piece_controller_1.sprite
assert piece_controller_1.piece
assert piece_controller_1.get_id()
assert piece_controller_1.get_id() == piece_controller_1.piece.id == piece_controller_1.sprite.id
assert piece_controller_1.get_pos() == 'test pos'
piece_controller_2 = PieceController(MockPiece(), MockSprite())
assert piece_controller_2.get_id() == piece_controller_2.piece.id == piece_controller_2.sprite.id
assert piece_controller_1.get_id() is not piece_controller_2.get_id()

#Board_Controller
board_controller = BoardController(MockBoard(), MockBoardView())

#Board_Controller#add_piece_controller
test_piece_controller_1 = MockPieceController(1)
test_piece_controller_2 = MockPieceController(2)
pos = 'pos'
board_controller.add_piece_controller(test_piece_controller_1, pos)
assert board_controller.board.add_piece_called
assert board_controller.board_view.add_sprite_called
board_controller.add_piece_controller(test_piece_controller_2, pos)

#Board_Controller#get_piece_controller
assert board_controller.get_piece_controller(test_piece_controller_1.id) == test_piece_controller_1
assert board_controller.get_piece_controller(test_piece_controller_2.id) == test_piece_controller_2
try:
    board_controller.get_piece_controller(3)
    raise Exception('#get_piece_controller must raise exception when passed an unregistered id')
except:
    pass

#Board_Controller#move_piece_controller
    #probably easier to test this in a demo?
    #it's *almost* a wrapper for the corrosponding methods in the board and sprite
    #and those already well tested...

#Board_Controller#save - Wrapper for now, tested in Board
#Board_Controller#get_piece_at - Wrapper, tested in Board
#Board_Controller#to_pix - Wrapper, tested in Board_View
#Board_Controller#to_hex - Wrapper, tested in Board_View
#Board_Controller#set_impassible - Wrapper, tested in Board
#Board_Controller#is_valid_pos - Wrapper, tested in Board
#Board_Controller#is_empty_at - Wrapper, tested in Board


#Game
mock_board = MockBoard()
mock_board_view = MockBoardView()
test_game = Game('mock_screen', MockBoardController())

#Game#create_piece_controller
#not super sure how to write a unit test for this function since
#getting piece_controllers by id is rooted all the way down in the board class...
piece, sprite = MockPiece(), MockSprite()
pos = 'pos'
new_piece_controller = test_game.create_piece_controller(piece, sprite, pos)
assert new_piece_controller.get_id() == new_piece_controller.sprite.id == new_piece_controller.piece.id
assert test_game.board_controller.add_piece_controller_called


#Game#path_move
#Not a perfect unit test - relies on the implementation of BoardController
test_game = Game('screen', BoardController(MockBoard(), MockBoardView()))
path = [(1, 1), (2, 2), (2, 4), (2, 6), (3, 5)]
piece_controller = test_game.create_piece_controller(MockPiece(), MockSprite(), (1, 1)) 
test_game.board_controller.board.move_piece_called_count = 0
test_game.path_move(piece_controller, path)
assert test_game.board_controller.board.move_piece_called_count is len(path)


print("Controller unit tests successful!")
