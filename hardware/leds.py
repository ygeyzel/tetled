from itertools import product
from typing import Optional, Sequence

from rpi_ws281x import PixelStrip, Color

from common.common import add_positions, Position, HsvColor, RgbColor


def _is_position_out_of_range(pos: Position, pos0: Position, width_heigth: Position) -> bool:
    pos1 = add_positions(pos0, width_heigth)
    return any(pos[i] not in range(pos0[i], pos1[i]) for i in (0, 1))


def _hsv_to_rgb(hsv: HsvColor) -> RgbColor:
    h, s, v = hsv
    c = v * s
    h0 = h / 60
    x = c * (1 - abs((h0 % 2) - 1))
    m = v - c

    rgb0_by_h0 = (
        (c, x, 0),
        (x, c, 0),
        (0, c, x),
        (0, x, c),
        (x, 0, c),
        (c, 0, x)
    )

    rgb0 = rgb0_by_h0[int(h0) - 1]
    r, g, b = [int((color + m) * 255) for color in rgb0]

    return Color(r, g, b)


class DualMatrix:
    def __init__(self, din_pin: int, matrix_max_x: int, matrix_max_y: int):
        self.matrix_max_x = matrix_max_x
        self.max_y = matrix_max_y
        self.max_x = matrix_max_x * 2
        self.leds_num = self.max_x * self.max_y

        self._leds = PixelStrip(self.leds_num, din_pin)
        self._leds.begin()

    # for external usage
    @property
    def dimensions(self) -> Position:
        return (self.max_y, self.max_x)
    
    # for internal usage
    @property
    def _dimensions(self) -> Position:
        return (self.max_x, self.max_y)

    def _get_linear_position(self, position: Position) -> int:
        x, y = position
        if x >= self.matrix_max_x:
            x -= self.matrix_max_x
            y += self.max_y

        if y % 2 == 0:
            x = self.matrix_max_x - x - 1

        return x + (y * self.matrix_max_x)

    def __setitem__(self, index: Position, value: HsvColor):
        if _is_position_out_of_range(index, (0, 0), self._dimensions):
            raise ValueError(
                f"Position {index} is out of matrix boundreis - {self.max_x, self.max_y}")
        linear_position = self._get_linear_position(index)
        rgb = _hsv_to_rgb(value)
        self._leds[linear_position] = rgb

    def clear(self):
        self._leds[:] = Color(0, 0, 0)

    def create_canvas(self, pos0: Position, width_heigth: Position) -> 'Canvas':
        return Canvas(self, pos0, width_heigth)

    def show(self):
        self._leds.show()


class Canvas:
    def __init__(self, matrix: DualMatrix, pos0: Position, width_heigth: Position):
        if any(v < 0 for v in (*pos0, *width_heigth)):
            raise ValueError("Canvas arguments can't be negative")

        end_pos = add_positions(pos0, width_heigth)
        for corner in (pos0, end_pos):
            if any(corner[i] > matrix.dimensions[i] for i in (0, 1)):
                raise ValueError(
                    f"Invalid canvas dimensions: {pos0} + {width_heigth} is outside matrix dimensions {matrix.dimensions}")

        self._matrix = matrix
        self.width_heigth = width_heigth
        self.width, self.height = self.width_heigth

        self.pos0 = pos0

    def __setitem__(self, index: Position, value: HsvColor):
        if _is_position_out_of_range(index, (0, 0), self.width_heigth):
            raise ValueError(
                f"Position {index} is out of canvas boundreis - {self.width_heigth}")

        self._matrix[[index[i] + self.pos0[i]
                      for i in (1, 0)]] = value

    def fill(self, color: HsvColor):
        for i, j in product(range(self.width), range(self.height)):
            self[i, j] = color

    def draw_color_map(self, color_map: Sequence[Sequence[Optional[HsvColor]]], position: Position = (0, 0)):
        for i, line in enumerate(color_map):
            for j, color in enumerate(line):
                if color:
                    color_pos = add_positions(position, (i, j))
                    self[color_pos] = color

    def draw_shape(self, shape: Sequence[Sequence[bool]], color: HsvColor, position: Position = (0, 0)):
        def shape_iterator():
            for i in shape:
                yield (color if j else None for j in i)

        self.draw_color_map(shape_iterator(), position)
