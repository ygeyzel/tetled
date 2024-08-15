from itertools import product
from rpi_ws281x import PixelStrip, Color

from common.common import add_positions, Position, HsvColor, RgbColor


def _is_position_out_of_range(pos: Position, top_left: Position, width_heigth: Position) -> bool:
    bottom_right = add_positions(top_left, width_heigth)
    return any(pos[i] not in range(top_left[i], bottom_right[i]) for i in (0, 1))


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

    @property
    def dimensions(self) -> Position:
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
        if _is_position_out_of_range(index, (0, 0), self.dimensions):
            raise ValueError(
                f"Position {index} is out of matrix boundreis - {self.max_x, self.max_y}")
        linear_position = self._get_linear_position(index)
        rgb = _hsv_to_rgb(value)
        self._leds[linear_position] = rgb

    def clear(self):
        self._leds[:] = Color(0, 0, 0)

    def create_canvas(self, top_left_corner: Position, width_heigth: Position) -> 'Canvas':
        return Canvas(self, top_left_corner, width_heigth)

    def show(self):
        self._leds.show()


class Canvas:
    def __init__(self, matrix: DualMatrix, top_left_corner: Position, width_heigth: Position):
        if any(v < 0 for v in (*top_left_corner, *width_heigth)):
            raise ValueError("Canvas arguments can't be negative")

        bottom_right_corner = add_positions(top_left_corner, width_heigth)
        for corner in (top_left_corner, bottom_right_corner):
            if any(corner[i] > matrix.dimensions[i] for i in (0, 1)):
                raise ValueError(
                    f"Invalid canvas dimensions: {top_left_corner} + {width_heigth} is outside matrix dimensions {matrix.dimensions}")

        self._matrix = matrix
        self.width_heigth = width_heigth
        self.width, self.height = self.width_heigth

        self.top_left_corner = top_left_corner

    def __setitem__(self, index: Position, value: HsvColor):
        if _is_position_out_of_range(index, (0, 0), self.width_heigth):
            raise ValueError(
                f"Position {index} is out of canvas boundreis - {self.width_heigth}")

        self._matrix[[index[i] + self.top_left_corner[i]
                      for i in (0, 1)]] = value

    def fill(self, color: HsvColor):
        for i, j in product(range(self.width), range(self.height)):
            self[i, j] = color
