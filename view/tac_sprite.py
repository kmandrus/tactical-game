import math

import pygame as pg

class TacSprite:
    def __init__(self, image, surface, pos, draw_centered=False):
        self.image = image
        self.surface = surface
        self.pos = pos
        self.target_pos = None
        self.draw_centered = draw_centered
        self.speed = 1

    def draw(self):
        if self.draw_centered:
            pos = self.get_center()
        else:
            pos = self.pos
        self.surface.blit(self.image, pos)

    def get_center(self):
        x, y = self.pos
        width, height = self.image.get_size()
        x_offset, y_offset = width / 2, height / 2
        return (x - x_offset, y - y_offset)

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