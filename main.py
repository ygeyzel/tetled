from time import sleep
from game.drawer import Drawer
from game.game_board import Board
from hardware.keys import get_key


def init_game(board: Board):
    board.start()


def game_loop(board: Board, drawer: Drawer):
    drawer.draw_board()

    while not board.is_game_over():
        sleep(1 / board.level)
        key = get_key()
        board.advance_turn(key)

        drawer.clear()
        drawer.draw_board()


def main():
    drawer = Drawer()
    board = drawer.board

    while True:
        init_game(board)
        game_loop(board, drawer)


if __name__ == "__main__":
    main()
