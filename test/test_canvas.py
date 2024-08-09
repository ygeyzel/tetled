from itertools import product
from time import sleep

import board
from hardware.leds import DualMatrix

matrix = DualMatrix(board.D18, 8, 32)
canvas = matrix.create_canvas((3, 3), (10, 10))

    
print("drawing template on canvas")

x, y = canvas.width_heigth
for i,j in product(range(x), range(y)):
    h = 360 * i / x                    
    s = 0.5 + 0.5 * j / (y - 1)
    canvas[i, j] = (h, s, 0.1)

sleep(1)
    
print("clear canvas")
matrix.clear()

