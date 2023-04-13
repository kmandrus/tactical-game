import math

import pygame as pg


class BoardView:
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
    assumed present when doing computations. These are points like (1, 0), 
    (3, 2), etc. These implict points are NOT in the dictionary of hexagons,
    since none of they lay at the center of a hexagon.

    The function to convert from pixel to hex coordinates is... complicated.
    Unfortunately, it's essential to the UI, since it is used to convert the 
    location of a mouse click to the hexagon it lies in. I must remember to draw
    a hexagonal grid with ALL (both implict and explitict) coordinates listed 
    to understand it. Sorry to myself in the future.
    """

    def __init__(self, surface, dimensions, hex_radius):
        self.surface = surface
        self.width, self.height = dimensions
        self.hex_radius = hex_radius
        self.pix_units = (self.hex_radius * 1.5,
                          self.hex_radius * (math.sqrt(3) / 2))
        self._tile_views = {}
        self.sprites = []

    def get_tile_view(self, hex_pos):
        return self._tile_views[hex_pos]
    
    def add_tile_view(self, tile_view, pos):
        tile_view.surface = self.surface
        tile_view.center = self.to_pix(pos)
        tile_view.radius = self.hex_radius
        self._tile_views[pos] = tile_view
    
    def update(self):
        for sprite in self.sprites:
            sprite.update()
        for tile in self._tile_views.values():
            tile.update()

    def render(self):
        for hexagon in self._tile_views.values():
            hexagon.render()
        for sprite in self.sprites:
            sprite.render()
    
    def to_pix(self, hex_pos):
        x_hex, y_hex = hex_pos
        x_unit, y_unit = self.pix_units
        return (x_unit * x_hex, y_unit * y_hex)

    def add_sprite(self, sprite, pos):
        self.sprites.append(sprite)
        sprite.pos = pos
    
    def toggle_fill(self, hex_pos):
        if (tile_view := self.get_tile_view(hex_pos)).is_filled:
            tile_view.is_filled = False
        else:
            tile_view.is_filled = True

    def to_hex(self, pix_pos):
        partial_hex_pos, remainders = self._to_partial_hex_pos_and_remainders(
            pix_pos)
        x_hex, y_hex = partial_hex_pos
        if x_hex % 2 == 0:
            if y_hex % 2 == 0:
                return self._hex_pos_for_up_slope(partial_hex_pos, remainders)
            else:
                return self._hex_pos_for_down_slope(partial_hex_pos, remainders)
        else:
            if y_hex % 2 == 0:
                return self._hex_pos_for_down_slope(partial_hex_pos, remainders)
            else:
                return self._hex_pos_for_up_slope(partial_hex_pos, remainders)

    def _to_partial_hex_pos_and_remainders(self, pix_pos):
        x_unit, y_unit = self.pix_units
        x_pix, y_pix = pix_pos
        x_hex, x_remainder = x_pix // x_unit, x_pix % x_unit
        y_hex, y_remainder = y_pix // y_unit, y_pix % y_unit
        return ((x_hex, y_hex), (x_remainder, y_remainder))

    def _hex_pos_for_up_slope(self, top_left_hex_pos, remainders):
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

    def _hex_pos_for_down_slope(self, top_left_hex_pos, remainders):
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


class TileView:
    def __init__(self, is_filled: bool, fill_color: tuple[int, int, int]):
        self.surface = None
        self.center = None
        self.radius = None
        self.is_filled = is_filled
        self.fill_color = fill_color

    def update(self):
        pass

    def half_height(self):
        return math.sqrt(3) * self.radius / 2

    def render(self):
        if self.is_filled:
            pg.draw.polygon(self.surface, self.fill_color, self.get_points(), 0)
        pg.draw.aalines(self.surface, (0, 0, 0), True, self.get_points())

    def get_points(self):
        deltas = [
            (-self.radius / 2, -self.half_height()),
            (self.radius / 2, -self.half_height()),
            (self.radius, 0),
            (self.radius / 2, self.half_height()),
            (-self.radius / 2, self.half_height()),
            (-self.radius, 0)
        ]
        return [self._apply_delta(self.center, delta) for delta in deltas]

    def _apply_delta(self, pos: tuple[int, int], delta: tuple[int, int]):
        x, y = pos
        dx, dy = delta
        return (x + dx, y + dy)


class TacSprite:
    def __init__(self, image, surface, hex_radius):
        self._size_factor = 1.5
        self._size = math.floor(hex_radius * self._size_factor)
        self.image = pg.transform.scale(image, (self._size, self._size))

        self.surface = surface
        self.pos = None
        self._target_pos = None
        self._hex_radius = hex_radius
        self.speed = 1
        self.id_ = None
        self._on_move_complete = None
        self._args = None
    
    def update(self):
        if self._target_pos:
            self._move_update()

    def render(self):
        self.surface.blit(self.image, self.get_center())
    
    def move(self, pix_pos, callback=None, *args):
        self._target_pos = pix_pos
        if callback:
            self._on_move_complete = callback
            self._args = args

    def get_center(self):
        x, y = self.pos
        offset = self.image.get_width() / 2
        return (x - offset, y - offset)

    def _move_update(self):
        if self._target_pos:
            if math.dist(self.pos, self._target_pos) < self.speed:
                self.pos = self._target_pos
                self._target_pos = None
                if callback := self._on_move_complete:
                    self._on_move_complete = None
                    args = self._args
                    self._args = None
                    callback(*args)
            else:
                x, y = self.pos
                delta_x, delta_y = self.get_velocity()
                self.pos = (x + delta_x, y + delta_y)

    def get_velocity(self):
        if self._target_pos:
            steps = math.dist(self.pos, self._target_pos) / self.speed
            delta_x, delta_y = [
                target - pos for pos, target
                in zip(self.pos, self._target_pos)]
            return (delta_x / steps, delta_y / steps)
        else:
            raise Exception("target_pos must contain a pixel_position")
    
    ##Deprecate in favor of #move
    def set_target_pos(self, pos, callback=None, *args):
        self._target_pos = pos
        if callback:
            self._on_move_complete = callback
            self._args = args
