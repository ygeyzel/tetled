from itertools import product

from game.game_board import Board
from common.common import add_positions
from hardware.leds import DualMatrix


BOARD_TOP_LEFT_POS = (4, 4)
SINGLE_MATRIX_WIDTH = 8
MATRIX_HEIGHT = 32
MATRIX_DPIN = 18


BRICK_COLOR_HSV = (100, 1, 0.1)


class Drawer:
    def __init__(self, game_board: Board):
        self._matrix = DualMatrix(MATRIX_DPIN, SINGLE_MATRIX_WIDTH, MATRIX_HEIGHT)
        self._board = game_board
        
        self._board_canvas = self._matrix.create_canvas(
            BOARD_TOP_LEFT_POS,  game_board.dimensions)

        left_border_canvas_args = (
            add_positions(BOARD_TOP_LEFT_POS, (-1, 0)), (1, game_board.height))
        rigth_border_canvas_args = (
            add_positions(BOARD_TOP_LEFT_POS, (game_board.width, 0)),
            (1, game_board.height))
        bottom_border_canvas_args = (
            add_positions(BOARD_TOP_LEFT_POS,
                add_positions((0, game_board.height), (-1, 0))), (game_board.width + 2, 1))

        self._board_external_border_canvases = tuple(
            self._matrix.create_canvas(top_left, width_heigth)
            for top_left, width_heigth in (
                left_border_canvas_args, rigth_border_canvas_args, bottom_border_canvas_args
                )
        )

    def _draw_board_borders(self):
        for canvas in self._board_external_border_canvases:
            canvas.fill((20, 0.5, 0.3))

    def draw_board(self):
        self._draw_board_borders()
        for i, j in product(range(self._board.width), range(self._board.height)):
            self._board_canvas[i, j] = BRICK_COLOR_HSV if self._board.board[j][i] else (0, 0, 0)

    def show(self):
        self._matrix.show()
