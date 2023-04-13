import os

import pytest

from tac.exceptions import TileDoesNotExistError, InvalidMoveError

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from tac.model.model import Board, Piece, Tile, BoardPosition, get_empty_hex_map

@pytest.fixture
def origin() -> BoardPosition:
    return BoardPosition(0, 0)

@pytest.fixture
def test_tile() -> Tile:
    return Tile("test_tile", False)
    

@pytest.fixture
def piece() -> Piece:
    return Piece("test_piece")


@pytest.fixture
def empty_board() -> Board:
    return Board("test_board", {})


@pytest.fixture
def test_board() -> Board:
    return Board("test_board", get_empty_hex_map(3, 3, "Grass"))


@pytest.fixture
def board_with_piece(piece, origin) -> Board:
    board = Board("test_board_with_piece", get_empty_hex_map(3, 3, "Grass"))
    board.add_piece(piece, origin)
    return board


class TestBoard:
    def test_add_tile(self, empty_board, test_tile, origin):
        empty_board.add_tile(test_tile, origin)
        assert empty_board.get_tile(origin) == test_tile

    def test_add_tile_overwrites_exisiting_tile(self, test_board, test_tile, origin):
        test_board.add_tile(test_tile, origin)
        assert test_board.get_tile(origin) == test_tile 

    def test_is_valid_pos_is_true_for_valid_positions(self, test_board, origin):
        assert test_board.is_valid_pos(origin)

    def test_is_valid_pos_is_false_for_out_of_bounds_positions(self, test_board):
        assert not test_board.is_valid_pos(BoardPosition(100, 100))

    def test_is_valid_pos_is_false_for_non_existent_positions(self, test_board):
        assert not test_board.is_valid_pos(BoardPosition(1, 2))

    def test_get_tile_fetches_correct_tile_for_pos(self, test_board): 
        pos = BoardPosition(1, 1)
        test_board.add_tile(Tile("test", False), pos)
        assert test_board.get_tile(pos).name == "test"

    def test_get_tile_raises_error_for_out_of_bounds_pos(self, test_board):
        out_of_bounds_pos = BoardPosition(100, 100)
        with pytest.raises(TileDoesNotExistError) as e:
            test_board.get_tile(out_of_bounds_pos)
        assert str(out_of_bounds_pos) in str(e) 

    def test_get_tile_raises_error_for_skipped_hex_positions(self, test_board):
        skipped_hex_pos = BoardPosition(1, 2)
        with pytest.raises(TileDoesNotExistError) as e:
            test_board.get_tile(skipped_hex_pos)
        assert str(skipped_hex_pos) in str(e) 

    def test_remove_tile(self, test_board, origin):
        test_board.remove_tile(origin)
        with pytest.raises(TileDoesNotExistError) as e:
            test_board.get_tile(origin)
        assert str(origin) in str(e)

    def test_removing_tile_also_removes_pos_from_positions(self, test_board, origin):
        test_board.remove_tile(origin)
        assert origin not in test_board.positions

    def test_removing_non_existent_tile_does_not_raise_exception(self, empty_board, origin):
        empty_board.remove_tile(origin)

    def test_is_impassable_true_when_pos_is_impassible(self, test_board, origin):
        test_board.add_tile(Tile("test", True), origin)
        assert test_board.is_impassible(origin)

    def test_is_impassable_false_when_pos_is_impassible(self, test_board, origin):
        assert not test_board.is_impassible(origin)

    def test_returns_correct_list_of_positions(self, test_board):
        expected_positions = {
            BoardPosition(0, 0), 
            BoardPosition(2, 0), 
            BoardPosition(1, 1), 
            BoardPosition(0, 2), 
            BoardPosition(2, 2), 
        }
        assert test_board.positions == expected_positions

    def test_add_piece_adds_piece_to_tile(self, test_board, origin, piece):
        origin_tile = test_board.get_tile(origin)
        test_board.add_piece(piece, origin)
        assert origin_tile.piece == piece

    def test_remove_piece(self, test_board, origin, piece):
        origin_tile = test_board.get_tile(origin)
        test_board.add_piece(piece, origin)

        test_board.remove_piece(origin)

        assert not origin_tile.piece

    def test_is_empty_is_false_when_pos_has_piece(self, test_board, piece, origin):
        test_board.add_piece(piece, origin)
        assert not test_board.is_empty(origin)

    def test_is_empty_is_true_when_no_piece_at_pos(self, test_board, origin):
        assert test_board.is_empty(origin)

    def test_move_piece(self, board_with_piece, origin, piece):
        end = BoardPosition(2, 2)

        board_with_piece.move_piece(origin, end)

        assert board_with_piece.is_empty(origin)
        assert not board_with_piece.get_tile(origin).piece
        assert not board_with_piece.is_empty(end)
        assert board_with_piece.get_tile(end).piece == piece

    def test_move_piece_raises_exception_when_no_piece_at_start_position(self, test_board, origin):
        with pytest.raises(InvalidMoveError) as e:
            test_board.move_piece(origin, BoardPosition(0, 2))
        assert str(origin) in str(e)
            

    def test_move_piece_raises_exception_when_end_pos_is_not_empty(self, board_with_piece, origin):
        end = BoardPosition(2, 2)
        end_piece = Piece("end_piece")
        board_with_piece.add_piece(end_piece, end)

        with pytest.raises(InvalidMoveError) as e:
            board_with_piece.move_piece(origin, end)
        assert str(end) in str(e)
