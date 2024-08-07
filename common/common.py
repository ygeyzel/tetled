from typing import NewType, Tuple


BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_DIMS = (BOARD_WIDTH, BOARD_HEIGHT)

Position = NewType('Position', Tuple[int, int])
HsvColor = NewType('HsvColor', Tuple[int, int, int])
RgbColor = NewType('RgbColor', Tuple[int, int, int])


def add_positions(p0: Position, p1: Position) -> Position:
    return tuple(p0[i] + p1[i] for i in (0,1))
