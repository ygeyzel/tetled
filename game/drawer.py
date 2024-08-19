from itertools import product

from game.game_board import Board
from common.common import add_positions
from hardware.leds import DualMatrix


BOARD_TOP_LEFT_POS = (3, 8)
SINGLE_MATRIX_WIDTH = 8
MATRIX_HEIGHT = 32
MATRIX_DPIN = 18

NEXT_CELL_TOP_LEFT_POS = (4, 1)
NEXT_CELL_HEIGHT_WIDTH = (8, 7)


BRICK_COLOR_HSV = (100, 1, 0.1)
BORDER_COLOR_HSV = (20, 0.5, 0.3)


class Drawer:
    def __init__(self, game_board: Board):
        self._matrix = DualMatrix(
            MATRIX_DPIN, SINGLE_MATRIX_WIDTH, MATRIX_HEIGHT)
        self._board = game_board

        self._board_canvas = self._matrix.create_canvas(
            BOARD_TOP_LEFT_POS,  game_board.dimensions)

        self._next_cell_canvas = self._matrix.create_canvas(
            NEXT_CELL_TOP_LEFT_POS, NEXT_CELL_HEIGHT_WIDTH)

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

    def _draw_board_bricks(self):
        for i, j in product(range(self._board.width), range(self._board.height)):
            self._board_canvas[i, j] = BRICK_COLOR_HSV if self._board.board[j][i] else (
                0, 0, 0)

    def _draw_board_borders(self):
        for canvas in self._board_external_border_canvases:
            canvas.fill(BORDER_COLOR_HSV)

    def _draw_board_current_block(self):
        if block := self._board.current_block:
            self._board_canvas.draw_shape(
                block.shape, block.color, self._board.current_block_pos)

    def _draw_next_block_cell(self):
        horizonal_border = [[1 for _ in range(NEXT_CELL_HEIGHT_WIDTH[1])]]
        vertical_border = [[1] for _ in range(NEXT_CELL_HEIGHT_WIDTH[0])]

        self._next_cell_canvas.draw_shape(vertical_border, BORDER_COLOR_HSV)
        self._next_cell_canvas.draw_shape(
            vertical_border, BORDER_COLOR_HSV, (0, NEXT_CELL_HEIGHT_WIDTH[1] - 1))
        self._next_cell_canvas.draw_shape(horizonal_border, BORDER_COLOR_HSV)
        self._next_cell_canvas.draw_shape(
            horizonal_border, BORDER_COLOR_HSV, (NEXT_CELL_HEIGHT_WIDTH[0] - 1, 0))

        if block := self._board.next_block:
            pos_in_cell = tuple(int((cell_dim - shape_dim) / 2) for cell_dim,
                                shape_dim in zip(NEXT_CELL_HEIGHT_WIDTH, block.size()))
            self._next_cell_canvas.draw_shape(block.shape, block.color, pos_in_cell)

    def draw_board(self):
        self._draw_board_bricks()
        self._draw_board_borders()
        self._draw_board_current_block()
        self._draw_next_block_cell()

    def show(self):
        self._matrix.show()
