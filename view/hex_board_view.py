import math

import pygame as pg

from hexagon_view import HexagonView


class HexBoardView:
    """
    A View to represent a Hexagonal Coordinate System

    The coordinates are numbered like this:
    (0, 0)   (2, 0)   (4, 0)   (6, 0)
        (1, 1)   (3, 1)   (5, 1)
    (0, 2)   (2, 2)   (4, 2)   (6, 2)   
        (1, 3)   (3, 3)   (5, 3)
    (0, 4)   (2, 4)   (4, 4)   (6, 4)

    It is assumed to be a 'flat-topped' hex grid (see Amit's game programming
    webpage), but doesn't follow any systems he lays out. 

    When the hexagons' centers are mapped to pixel coordinates, the x-unit is
    1.5 a hexagon's radius and the y-unit is half the height of a hexagon
    (a hexagons radius time the square root of 3 over 2).

    When calculating conversions between pixel and hexagonal coordinates,
    all of the other implicit points on the hexagonal coordinate grid are 
    assumed present with doing computations. These are points like (1, 0), 
    (3, 2), etc. These implict points are NOT in the dictionary of hexagons,
    since none of they lay at the center of a hexagon.

    The function to convert from pixel to hex coordinates is... complicated.
    Unfortunately, it's essential to the UI, since it is used to convert the 
    location of a mouse click to the hexagon it lies in. I must remember to draw
    a hexagonal grid with ALL (both implict and explitict) coordinates listed 
    to understand it. Sorry to myself... in the future.
    """
    def __init__(self, surface, dimensions, hex_radius, hex_pos_list):
        self.surface = surface
        self.width, self.height = dimensions
        self.hex_radius = hex_radius
        self.pix_units = (self.hex_radius * 1.5,
                          self.hex_radius * (math.sqrt(3) / 2))
        self.__hexagons = {
            pos: HexagonView(surface, self.to_pix(pos), hex_radius)
            for pos in hex_pos_list}

    def get_hexagon(self, hex_pos):
        return self.__hexagons[hex_pos]

    def draw(self):
        for hexagon in self.__hexagons.values():
            hexagon.draw()

    def to_pix(self, hex_pos):
        x_hex, y_hex = hex_pos
        x_unit, y_unit = self.pix_units
        return (x_unit * x_hex, y_unit * y_hex)

    def to_hex(self, pix_pos):
        partial_hex_pos, remainders = self.__to_partial_hex_pos_and_remainders(
            pix_pos)
        x_hex, y_hex = partial_hex_pos
        if x_hex % 2 == 0:
            if y_hex % 2 == 0:
                return self.__hex_pos_for_up_slope(partial_hex_pos, remainders)
            else:
                return self.__hex_pos_for_down_slope(partial_hex_pos, remainders)
        else:
            if y_hex % 2 == 0:
                return self.__hex_pos_for_down_slope(partial_hex_pos, remainders)
            else:
                return self.__hex_pos_for_up_slope(partial_hex_pos, remainders)

    def __to_partial_hex_pos_and_remainders(self, pix_pos):
        x_unit, y_unit = self.pix_units
        x_pix, y_pix = pix_pos
        x_hex, x_remainder = x_pix // x_unit, x_pix % x_unit
        y_hex, y_remainder = y_pix // y_unit, y_pix % y_unit
        return ((x_hex, y_hex), (x_remainder, y_remainder))

    def __hex_pos_for_up_slope(self, top_left_hex_pos, remainders):
        """
        O's are centers of hexagons in a region of the grid.
        If the remainder lies to the left of the upward sloping line,
        return the top left hex coordinate. Otherwise, return the bottom
        right hex coordinate.
        O . . . . . . . . . . . 
        .             .       .
        .            .        . 
        .           .         .
        .          .          .
        .         .           .
        .        .            .
        . . . . . . . . . . . O
        """

        x_r, y_r = remainders
        if x_r < (self.hex_radius - (math.sqrt(3) / 3) * y_r):
            return top_left_hex_pos
        else:
            x, y = top_left_hex_pos
            return (x + 1, y + 1)

    def __hex_pos_for_down_slope(self, top_left_hex_pos, remainders):
        """
        O's are centers of hexagons in a region of the grid.
        If the remainder lies to the left of the downward sloping line,
        return the bottom left hex coordinate. Otherwise, return the top
        right hex coordinate.
        . . . . . . . . . . . O
        .        .            .
        .         .           .
        .          .          .
        .           .         .
        .            .        .
        .             .       .
        O . . . . . . . . . . .
        """

        x, y = top_left_hex_pos
        x_r, y_r = remainders
        if x_r < (y_r / math.sqrt(3) + self.hex_radius / 2):
            return (x, y + 1)
        else:
            return (x + 1, y)
