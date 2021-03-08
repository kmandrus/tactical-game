import pygame as pg

from tac.controller import event_delegate

class Game:
    def __init__(self, screen, board_controller):
        self.screen = screen
        self.board_controller = board_controller
        self.running = True
        self.event_delegate = event_delegate.Nothing_Selected(self)
    
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
        self.screen.fill((64, 128, 64)) #push to board_controller and delete Game's Screen reference?
        self.board_controller.render()
        pg.display.update()

    def create_character(self, piece, sprite, pos):
        new_character = Character(piece, sprite)
        self.board_controller.add_character(new_character, pos)
        return new_character
    
    def path_move(self, character, path):
        if path:
            next_pos, remaining_path = path[0], path[1:]
            self.board_controller.move_character(
                character, next_pos,
                self.path_move, character, remaining_path)
        else:
            self.event_delegate = event_delegate.Nothing_Selected(self)


class Character:
    __id_counter= 0
    @classmethod
    def new_id(cls):
        cls.__id_counter += 1
        return cls.__id_counter

    def __init__(self, piece, sprite):
        self.sprite = sprite
        self.piece = piece
        self.__id = Character.new_id()
        self.piece.id = self.__id
        self.sprite.id = self.__id
    
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
        self.__characters_by_id = {}

    def update(self):
        self.board_view.update()
        
    def render(self):
        ##Add line that renders the background
        self.board_view.render()
        pg.display.update()

    def get_character(self, id):
        return self.__characters_by_id[id]

    def add_character(self, character, pos):
        self.__characters_by_id[character.get_id()] = character
        self.board.add_piece(character.piece, pos)
        pix_pos = self.board_view.to_pix(pos)
        self.board_view.add_sprite(character.sprite, pix_pos)

    def move_character(self, character, target_pos, callback=None, *args):
        if self.is_empty_at(target_pos):
            self.board.move_piece(character.piece, target_pos)
            character.sprite.move(
                self.board_view.to_pix(target_pos),
                callback, *args)
    
    def save(self, filepath):
        self.board.save(filepath)

    def get_character_at(self, pos):
        if piece := self.board.get_piece_at(pos):
            return self.get_character(piece.id)
        else:
            return None
    
    def to_pix(self, pos):
        return self.board_view.to_pix(pos)

    def to_hex(self, pix_pos):
        return self.board_view.to_hex(pix_pos)

    def set_impassible(self, pos, value):
        self.board.set_impassible(pos, value)

    def is_impassible(self, pos):
        return self.board.is_impassible(pos)

    def is_valid_pos(self, pos):
        return self.board.is_valid_pos(pos)

    def is_empty_at(self, pos):
        return self.board.is_empty_at(pos)
