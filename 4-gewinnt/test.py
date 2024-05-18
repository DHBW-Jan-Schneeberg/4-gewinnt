# Space for tests
import numpy as np

from board import Board
from computer import Computer

board_with_clear_best_move = Board(np.zeros((6, 7)))
board_with_clear_best_move.place_marker(1)
board_with_clear_best_move.place_marker(2)
board_with_clear_best_move.place_marker(1)
board_with_clear_best_move.place_marker(2)
board_with_clear_best_move.place_marker(1)
board_with_clear_best_move.place_marker(2)
board_with_clear_best_move.place_marker(1)

comp = Computer(board=board_with_clear_best_move, color=1)
print(comp.calculate_move())  # alright, we know the base case works. fucking amazing
