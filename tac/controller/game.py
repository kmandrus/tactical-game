import pygame as pg

from tac.controller import event_delegate

class Game:
    def __init__(self, screen, board, board_view):
        self.screen = screen
        self.board = board
        self.board_view = board_view
        self.running = True
        self.characters = {}
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

    def render(self):
        self.screen.fill((64, 128, 64))
        self.board_view.render()
        pg.display.update()

    def update(self):
        self.board_view.update()
    
    def create_character(self, piece, sprite, hex_pos):
        new_character = Character(piece, sprite)
        self.characters[new_character.get_id()] = new_character
        self.board.add_piece(piece, hex_pos)
        pix_pos = self.board_view.to_pix(hex_pos)
        self.board_view.add_sprite(sprite, pix_pos)
        return new_character
    
    def get_character(self, id):
        return self.characters[id]
    
    def move_character(self, character, hex_pos, callback=None, *args):
        if self.board.is_empty_at(hex_pos):
            self.board.move_piece(character.piece, hex_pos)
            self.board_view.move_sprite(
                character.sprite, 
                self.board_view.to_pix(hex_pos),
                callback, *args)
        else:
            raise Exception(f'Destination tile at {hex_pos} is not empty')
    
    def path_move(self, character, path):
        if path:
            next_pos, remaining_path = path[0], path[1:]
            self.move_character(character, next_pos,
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
    
    def get_hex_pos(self):
        return self.piece.pos
