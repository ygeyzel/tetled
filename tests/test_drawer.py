from time import sleep

from common.common import add_positions
from tests.shared import matrix_test
from game.drawer import Drawer
from game.game_board import Board, Block, BLOCK_SHAPES


board_pos_0 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
    [0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
]


drawer = Drawer()


@matrix_test
def test_draw_board(*args, **kwargs):
    board = drawer._board

    current_block = Block('Z')
    next_block = Block('T')

    board.board = board_pos_0
    board.current_block = current_block
    board.current_block_pos = (12, 6)
    board.next_block = next_block

    for _ in range(5):
        drawer._matrix.clear()

        board.current_block_pos = add_positions(board.current_block_pos, (1, 0))
        drawer.draw_board()
        drawer.show()

        sleep(0.3)


@matrix_test
def test_draw_next_shape(*args, **kwargs):
    board = drawer._board
    board.board = [[0 for _ in range(board.width)] for _ in range(board.height)]

    for shape in BLOCK_SHAPES:
        print(f"\t{shape}")
        drawer._matrix.clear()

        board.next_block = Block(shape)
        drawer.draw_board()
        drawer.show()

        sleep(0.2)


if __name__ == "__main__":
    # test_draw_next_shape(matrix=drawer._matrix)
    test_draw_board(matrix=drawer._matrix)
