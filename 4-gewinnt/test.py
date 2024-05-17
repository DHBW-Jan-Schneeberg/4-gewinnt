# Space for tests
import numpy as np

from board import Board

my_board = Board(np.zeros((5, 5)))
print(my_board.get_from_field(0, 0))
print(type(my_board.get_from_field(0, 0)))
