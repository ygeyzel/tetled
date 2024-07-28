from typing import NewType, Tuple


BOARD_WIDTH = 11
BOARD_HEIGHT = 17

Position = NewType('Position', Tuple[int, int])
HsvColor = NewType('HsvColor', Tuple[int, int, int])
RgbColor = NewType('RgbColor', Tuple[int, int, int])
