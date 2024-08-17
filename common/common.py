from typing import NewType, Sequence, Tuple


BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_DIMS = (BOARD_WIDTH, BOARD_HEIGHT)

Position = NewType('Position', Tuple[int, int])
HsvColor = NewType('HsvColor', Tuple[int, int, int])
RgbColor = NewType('RgbColor', Tuple[int, int, int])


def add_positions(*positions: Sequence[Position]) -> Position:
    x, y = 0, 0
    for pos in positions:
        x += pos[0]
        y += pos[1]

    return x, y
