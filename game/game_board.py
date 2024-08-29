import math
import os

from enum import Enum
from functools import partial
from itertools import product
from random import choice, getrandbits
from typing import Optional

from common.common import add_positions
from hardware.keys import Key


BEST_SCORE_FILE_NAME = "best_score"
BRICKS_VAL = 0.2

BLOCK_SHAPES = {
    'T':
    ([[0, 1, 0],
     [1, 1, 1]], (0, 1, BRICKS_VAL)),
    'L':
    ([[1, 0],
     [1, 0],
     [1, 1]], (20, 1, BRICKS_VAL)),
    'S':
    ([[0, 1, 1],
     [1, 1, 0]], (100, 1, BRICKS_VAL)),
    'Z':
    ([[1, 1, 0],
     [0, 1, 1]], (50, 1, BRICKS_VAL)),
    'O':
    ([[1, 1],
     [1, 1]], (200, 1, BRICKS_VAL)),
    'I':
    ([[1, 1, 1, 1]], (250, 1, BRICKS_VAL))
}


class Direction(Enum):
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Board:
    """Board representation"""

    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = None
        self.lines = None
        self.best_score = None
        self.level = None

    def dimensions_for_canvas(self):
        return self.dimensions

    def start(self):
        """Start game"""

        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = 0
        self.lines = 0
        self.level = 1
        self.best_score = self._read_best_score()

        self._place_new_block()

    def is_game_over(self):
        """Is game over"""

        return self.game_over

    def rotate_block(self):
        rotated_shape = list(map(list, zip(*self.current_block.shape[::-1])))

        if self._can_move(self.current_block_pos, rotated_shape):
            self.current_block.shape = rotated_shape

    def advance_turn(self, key: Key):
        key_func_swich = {
            Key.NO_KEY: partial(self.move_block, Direction.DOWN),
            Key.LEFT: partial(self.move_block, Direction.LEFT),
            Key.RIGHT: partial(self.move_block, Direction.RIGHT),
            Key.UP: self.rotate_block,
            Key.DOWN: self.drop
        }
        key_func_swich[key]()

    def move_block(self, direction: Direction):
        """Try to move block"""

        pos = self.current_block_pos
        new_pos = add_positions(pos, direction.value)

        if self._can_move(new_pos, self.current_block.shape):
            self.current_block_pos = new_pos
        elif direction == Direction.DOWN:
            self._block_reach_bottom()

    def _block_reach_bottom(self):
        self._land_block()
        self._burn()
        self._place_new_block()

    def drop(self):
        """Move to very very bottom"""

        i = 1
        while self._can_move((self.current_block_pos[0] + 1, self.current_block_pos[1]), self.current_block.shape):
            i += 1
            self.move_block(Direction.DOWN)
        
    def _get_new_board(self):
        """Create new empty board"""

        return [[0 for _ in range(self.dimensions[1])] for _ in range(self.dimensions[0])]

    def _place_new_block(self):
        """Place new block and generate the next one"""

        if self.next_block is None:
            self.current_block = self._get_new_block()
            self.next_block = self._get_new_block()
        else:
            self.current_block = self.next_block
            self.next_block = self._get_new_block()

        size = Block.get_size(self.current_block.shape)
        col_pos = math.floor((self.dimensions[1] - size[1]) / 2)
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos, self.current_block.shape):
            self.game_over = True
            self._save_best_score()
        else:
            self.score += 5

    def _land_block(self):
        """Put block to the board and generate a new one"""

        size = Block.get_size(self.current_block.shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if self.current_block.shape[row][col] == 1:
                    self.board[self.current_block_pos[0] +
                               row][self.current_block_pos[1] + col] = 1

    def _burn(self):
        """Remove matched lines"""

        for row in range(self.dimensions[0]):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.dimensions[1])]
                self.score += 100
                self.lines += 1
                if self.lines % 10 == 0:
                    self.level += 1

    def _check_overlapping(self, pos, shape):
        """If current block overlaps any other on the board"""

        size = Block.get_size(shape)
        for row, col in product(range(size[0]), range(size[1])):
            if shape[row][col] == 1:
                if self.board[pos[0] + row][pos[1] + col] == 1:
                    return True
        return False

    def _can_move(self, pos, shape):
        """Check if move is possible"""

        size = Block.get_size(shape)
        if pos[1] < 0 or pos[1] + size[1] > self.dimensions[1] \
                or pos[0] + size[0] > self.dimensions[0]:
            return False

        return not self._check_overlapping(pos, shape)

    def _save_best_score(self):
        """Save best score to file"""

        if self.best_score < self.score:
            with open(BEST_SCORE_FILE_NAME, "w") as file:
                file.write(str(self.score))

    @staticmethod
    def _read_best_score():
        """Read best score from file"""

        if os.path.exists(f"./{BEST_SCORE_FILE_NAME}"):
            with open(BEST_SCORE_FILE_NAME) as file:
                return int(file.read())
        return 0

    @staticmethod
    def _get_new_block():
        """Get random block"""

        block = Block()

        # flip it randomly
        if getrandbits(1):
            block.flip()

        return block


class Block:
    """Block representation"""

    def __init__(self, block_shape: Optional[str] = None):
        if block_shape is None:
            block_shape = choice(list(BLOCK_SHAPES))
            
        self.shape, self.color = BLOCK_SHAPES[block_shape]

    def flip(self):
        self.shape = list(map(list, self.shape[::-1]))

    def _get_rotated(self):
        return list(map(list, zip(*self.shape[::-1])))

    def size(self):
        """Get size of the block"""

        return self.get_size(self.shape)

    @staticmethod
    def get_size(shape):
        """Get size of a shape"""

        return [len(shape), len(shape[0])]
