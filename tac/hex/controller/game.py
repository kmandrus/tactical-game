import pygame as pg

from tac.hex.controller import event_delegate
from tac.hex.controller import db_delegate
from tac.hex import model
from tac.hex import view

class Game:
    def __init__(self, screen, board_controller, db_delegate):
        self.screen = screen
        self.board_controller = board_controller
        self.running = True
        self.event_delegate = event_delegate.Nothing_Selected(self)
        self.db_delegate = db_delegate
    
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
                self.event_delegate.handle_click(pg.mouse.get_pos())
    
    def update(self):
        self.board_controller.update()

    def render(self):
        #self.screen.fill((64, 128, 64)) #push to board_controller and delete Game's Screen reference?
        self.board_controller.render()
        pg.display.update()

    def create_piece_controller(self, piece, sprite, pos):
        new_pc = PieceController(piece, sprite)
        self.board_controller.add_pice_controller(new_pc, pos)
        return new_pc
    
    def path_move(self, piece_controller, path):
        if path:
            next_pos, remaining_path = path[0], path[1:]
            self.board_controller.move_piece_controller(
                piece_controller, next_pos,
                self.path_move, piece_controller, remaining_path)
        else:
            self.event_delegate = event_delegate.Nothing_Selected(self)
    
    def load_tile(self, id_):
        data = self.db_delegate.fetch_tile_data(id_)
        tile = model.Tile(data['id'], data['name'], data['is_impassible'])
        tile_view = view.TileView(
            data['is_filled'], pg.Color(data['fill_color']) )
        return TileController(tile, tile_view)
    
    def save_new(self):
        self.db_delegate.save_new_board(self.board_controller.get_save_data())
    
    def save_update(self):
        self.db_delegate.update_board(self.board_controller.get_save_data())
        

class PieceController:
    __id_counter= 0
    @classmethod
    def new_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    def __init__(self, piece, sprite):
        self.sprite = sprite
        self.piece = piece
        self.__id = PieceController.new_id()
        self.piece.id_ = self.__id
        self.sprite.id_ = self.__id
    
    def get_id(self):
        return self.__id
    
    def get_pos(self):
        return self.piece.pos


class BoardController:
    @classmethod
    def load(cls, filepath):
        pass

    def __init__(self, board, board_view):
        self.board = board
        self.board_view = board_view
        self.__tile_controllers = {}
        self.__piece_controllers_by_id = {}

    def update(self):
        for tc in self.__tile_controllers.values():
            tc.update()
        self.board_view.update()
        
    def render(self):
        self.board_view.render()
        pg.display.update()
    
    def add_tile_controller(self, tile_controller, pos):
        self.__tile_controllers[pos] = tile_controller
        self.board.add_tile(tile_controller.tile, pos)
        self.board_view.add_tile_view(tile_controller.tile_view, pos)

    def get_piece_controller(self, id_):
        return self.__piece_controllers_by_id[id_]

    def add_piece_controller(self, piece_controller, pos):
        pc = piece_controller
        self.__piece_controllers_by_id[pc.get_id()] = pc
        self.board.add_piece(pc.piece, pos)
        pix_pos = self.board_view.to_pix(pos)
        self.board_view.add_sprite(pc.sprite, pix_pos)

    def move_piece_controller(
        self, piece_controller, target_pos, 
        callback=None, *args):
        if self.is_empty_at(target_pos):
            self.board.move_piece(piece_controller.piece, target_pos)
            piece_controller.sprite.move(
                self.board_view.to_pix(target_pos),
                callback, *args)

    def get_piece_controller_at(self, pos):
        if piece := self.board.get_piece_at(pos):
            return self.get_piece_controller(piece.id_)
        else:
            return None
    
    def to_pix(self, pos):
        return self.board_view.to_pix(pos)

    def to_hex(self, pix_pos):
        return self.board_view.to_hex(pix_pos)

    def is_impassible(self, pos):
        return self.__tile_controllers[pos].is_impassible()

    def is_valid_pos(self, pos):
        return self.board.is_valid_pos(pos)

    def is_empty_at(self, pos):
        return self.board.is_empty_at(pos)
    
    def get_tile_id_at(self, pos):
        return self.board.get_tile(pos).id_
    
    def get_save_data(self):
        data = []
        for pos, tc in self.__tile_controllers.items():
            x, y = pos
            data.append( {
                'board_name': self.board.name,
                'x': x, 'y': y,
                'tile_id': tc.get_id(),
                'piece_id': tc.get_piece_id()
            } )
        return data
    

class TileController:
    def __init__(self, tile, tile_view):
        self.tile = tile
        self.tile_view = tile_view
    
    def update(self):
        self.tile_view.update()

    def render(self):
        self.tile_view.render()

    def is_impassible(self):
        return self.tile.is_impassible
    
    def set_impassible(self, boolean):
        self.tile.is_impassible = boolean

    def get_piece(self):
        return self.tile.piece
    
    def get_piece_id(self):
        if self.tile.piece:
            return self.tile.piece_id
        return None

    def remove_piece(self):
        self.tile.piece = None

    def add_piece(self, piece):
        self.tile.piece = piece

    def is_filled(self):
        return self.tile_view.is_filled

    def set_fill(self, boolean):
        self.tile_view.is_filled = boolean
    
    def get_id(self):
        return self.tile.id_

