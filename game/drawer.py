from game.game_board import Board
from common.common import add_positions, BOARD_DIMS
from hardware.leds import DualMatrix


BOARD_POS_0 = (8, 2)
SINGLE_MATRIX_WIDTH = 8
MATRIX_HEIGHT = 32
MATRIX_DPIN = 18

NEXT_CELL_POS_0 = (1, 4)
NEXT_CELL_HEIGHT_WIDTH = (7, 8)


BRICK_COLOR_HSV = (100, 1, 0.1)
BORDER_COLOR_HSV = (20, 0.5, 0.3)


class Drawer:
    def __init__(self):
        self._matrix = DualMatrix(
            MATRIX_DPIN, SINGLE_MATRIX_WIDTH, MATRIX_HEIGHT)
        board = Board(BOARD_DIMS)

        self._board_canvas = self._matrix.create_canvas(
            BOARD_POS_0,  add_positions(board.dimensions_for_canvas(), (1, 2)))

        self._next_cell_canvas = self._matrix.create_canvas(
            NEXT_CELL_POS_0, NEXT_CELL_HEIGHT_WIDTH)

        self._board = board

    def _draw_board_current_block(self):
        if block := self._board.current_block:
            self._board_canvas.draw_shape(
                block.shape, block.color, self._board.current_block_pos)

    def _draw_next_block_cell(self):
        self._next_cell_canvas.draw_borders(BORDER_COLOR_HSV)

        if block := self._board.next_block:
            pos_in_cell = tuple(int((cell_dim - shape_dim) / 2) for cell_dim,
                                shape_dim in zip(NEXT_CELL_HEIGHT_WIDTH, block.size()))
            self._next_cell_canvas.draw_shape(block.shape, block.color, pos_in_cell)

    def draw_board(self):
        self._board_canvas.draw_shape(self._board.board, BRICK_COLOR_HSV, (0, 1))
        self._board_canvas.draw_borders(BORDER_COLOR_HSV, "ulb")
        self._draw_board_current_block()
        self._draw_next_block_cell()

        self.show()

    def show(self):
        self._matrix.show()
