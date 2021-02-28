import math

import pygame as pg

class TacSprite:
    def __init__(self, image, surface, pos, hex_radius):
        self.__size_factor = 1.5
        self.__size = math.floor(hex_radius * self.__size_factor)
        self.image = pg.transform.scale(image, (self.__size, self.__size))
        self.surface = surface
        self.pos = pos
        self.target_pos = None
        self.__hex_radius = hex_radius
        self.speed = 1

    def draw(self):
        if self.target_pos:
            self.move()
        self.surface.blit(self.image, self.get_center())

    def get_center(self):
        x, y = self.pos
        offset = self.image.get_width() / 2
        return (x - offset, y - offset)

    def move(self):
        if self.target_pos:
            if math.dist(self.pos, self.target_pos) < self.speed:
                self.pos = self.target_pos
            else:
                x, y = self.pos
                delta_x, delta_y = self.get_velocity()
                self.pos = (x + delta_x, y + delta_y)

    def get_velocity(self):
        if self.target_pos:
            steps = math.dist(self.pos, self.target_pos) / self.speed
            delta_x, delta_y = [ 
                target - pos for pos, target
                in zip(self.pos, self.target_pos) ]
            return (delta_x / steps, delta_y / steps)
        else:
            raise Exception("target_pos must contain a pixel_position")
