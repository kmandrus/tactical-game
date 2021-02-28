import math

import pygame as pg

class HexagonView:
    def __init__(self, surface, center, radius):
        self.surface = surface
        self.center = center
        self.radius = radius
        self.half_height = (math.sqrt(3) * radius) / 2
        self.is_filled = False
        self.fill_color = pg.Color(0, 0, 200)

    def draw(self):
        pg.draw.aalines(self.surface, (0, 0, 0), True, self.get_points())
        if self.is_filled:
            pg.draw.polygon(self.surface, self.fill_color, self.get_points(), 0)

    def get_points(self):
        deltas = [
            (-self.radius / 2, -self.half_height),
            (self.radius / 2, -self.half_height),
            (self.radius, 0),
            (self.radius / 2, self.half_height),
            (-self.radius / 2, self.half_height),
            (-self.radius, 0)
        ]
        return [self.__apply_delta(self.center, delta) for delta in deltas]

    def __apply_delta(self, pos, delta):
        x, y = pos
        dx, dy = delta
        return (x + dx, y + dy)

