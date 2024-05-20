# Space for tests
import numpy as np

from board import Board
from computer import Computer

board = Board(np.zeros((6, 7)))
board.place_marker(0)
board.place_marker(1)
board.place_marker(0)
board.place_marker(1)
board.place_marker(0)
board.place_marker(0)
board.place_marker(1)
board.place_marker(2)
board.place_marker(1)
board.place_marker(1)
board.place_marker(2)
board.place_marker(2)
board.place_marker(2)
board.place_marker(3)
board.place_marker(3)
board.place_marker(3)
board.place_marker(4)
board.place_marker(3)
board.place_marker(5)
board.place_marker(3)
board.place_marker(3)
board.place_marker(6)
board.place_marker(5)
board.place_marker(6)
board.place_marker(6)
board.place_marker(5)
board.place_marker(5)
board.place_marker(5)
board.place_marker(5)

comp = Computer(board=board, color=1)
print(comp.calculate_move())
