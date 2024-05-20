# Space for tests
import numpy as np

from board import Board
from computer import Computer
from computer import find_wins

board = Board(np.zeros((6, 7)))

comp = Computer(board=board, color=1)
print("Finding wins")
find_wins(board, depth=7)
