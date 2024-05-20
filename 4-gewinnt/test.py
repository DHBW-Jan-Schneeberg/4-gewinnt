# Space for tests
import numpy as np

from board import Board
from computer import Computer

board = Board(np.zeros((6, 7)))
board.place_marker(1)
board.place_marker(2)
board.place_marker(1)
board.place_marker(2)
board.place_marker(1)
board.place_marker(2)

comp = Computer(board=board, color=1)
print(comp.calculate_move())
