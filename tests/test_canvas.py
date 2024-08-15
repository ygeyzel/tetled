from itertools import product

from tests.shared import matrix_test

    
@matrix_test
def test_canvas(matrix):
    canvas = matrix.create_canvas((3, 3), (10, 10))
    x, y = canvas.width_heigth

    print("drawing template on canvas")
    for i,j in product(range(x), range(y)):
        h = 360 * i / x                    
        s = 0.5 + 0.5 * j / (y - 1)
        canvas[i, j] = (h, s, 0.1)
    
    matrix.show()


if __name__ == "__main__":
    test_canvas()
