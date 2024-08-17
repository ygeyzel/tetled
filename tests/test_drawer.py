from time import sleep

from common.common import add_positions
from tests.shared import matrix_test
from game.drawer import Drawer
from game.game_board import Board, Block


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


board = Board(10, 20)
drawer = Drawer(board)


@matrix_test
def test_drawer(*args, **kwargs):
    current_block = Block('Z')
    board.board = board_pos_0
    board.current_block = current_block
    board.current_block_pos = (6, 12)

    for _ in range(5):
        drawer._matrix.clear()

        board.current_block_pos = add_positions(board.current_block_pos, (0, 1))
        drawer.draw_board()
        drawer.show()

        sleep(0.3)


if __name__ == "__main__":
    test_drawer(matrix=drawer._matrix)
