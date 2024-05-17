import random

import numpy as np

from board import Board


class Computer:
    board: Board
    color: int

    bitboard: dict[np.ndarray, int]

    def __init__(self, board: Board, color):
        self.board = board
        self.color = color

        self.bitboard = {}

    def calculate_move(self) -> int:
        moves = list(range(7))
        for move in moves:
            next_state = Board(self.board.field.copy())
            # The field needs to be copied in order to not overwrite the original field used in Game
            result = next_state.place_marker(move, self.color)
            if not result:
                moves.remove(move)
            else:
                if next_state.is_game_over():
                    return move
        return random.choice(moves)

    def minimax(self, board: Board, color_to_move: int):
        if board.field in self.bitboard:
            return self.bitboard[board.field]

        if self.color == color_to_move:
            # we want to maximize
            ...
        else:
            # our enemy want's to minimize
            ...
        ...

    # Idee: Maussimulation, damit sich der Cursor über dem Spielfeld zur richtigen Position bewegt, bevor gesetzt wird
    def simulate_mouse_movement(self) -> None:
        while True:
            ...
