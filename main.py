from time import sleep, time
from game.drawer import Drawer
from game.game_board import Board
from hardware.keys import Key, KeyHandler
from hardware.score import print_score


def init_game(board: Board):
    board.start()
    KeyHandler.flush()


def game_over(drawer: Drawer):
    KeyHandler.flush()
    end_time = time()
    
    while KeyHandler.get_key() == Key.NO_KEY or time() - end_time < 2:
        drawer.blink_board()
        sleep(0.2)


def game_loop(board: Board, drawer: Drawer):
    drawer.draw_board()

    while not board.is_game_over():
        KeyHandler.flush()
        sleep(1 / board.level)

        key = KeyHandler.get_key()
        board.advance_turn(key)

        drawer.clear()
        drawer.draw_board()
        print_score(board.score, board.best_score)

    game_over(drawer)


def main():
    drawer = Drawer()
    board = drawer.board

    while True:
        init_game(board)
        game_loop(board, drawer)


if __name__ == "__main__":
    main()
