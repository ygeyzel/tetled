from collections import namedtuple
from typing import Tuple, NewType

import neopixel


Position = NewType('Position', Tuple[int, int])
HsvColour = NewType('HsvColour', Tuple[int, int, int])
RgbColour = NewType('RgbColour', Tuple[int, int, int])


def _hsv_to_rgb(hsv: HsvColour) -> RgbColour:
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

    return r, g, b


class DualMatrix:
    def __init__(self, din_pin, matrix_max_x: int, matrix_max_y: int):
        self.matrix_max_x = matrix_max_x
        self.max_y = matrix_max_y
        self.max_x = matrix_max_x * 2
        self.leds_num = self.max_x * self.max_y

        self._leds = neopixel.NeoPixel(din_pin, self.leds_num)

    def _get_linear_position(self, position: Position) -> int:
        x, y = position
        if x >= self.matrix_max_x:
            x -= self.matrix_max_x
            y += self.max_y

        if y % 2 == 0:
            x = self.matrix_max_x - x - 1

        return x + (y * self.matrix_max_x)

    def __setitem__(self, index: Position, value: HsvColour):
        linear_position = self._get_linear_position(index)
        rgb = _hsv_to_rgb(value)
        self._leds[linear_position] = rgb

    def clear(self):
        self._leds.fill((0, 0, 0))
