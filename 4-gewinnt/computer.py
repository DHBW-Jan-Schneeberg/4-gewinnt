import random

import numpy as np

from board import Board


def eval_field(board: Board) -> int:
    """
    Calculates the evaluation of the current board
    :param board:
    :return: an EVALUATION of the board position
    """
    return 43 - board.filled_fields()


class Computer:
    board: Board
    color: int

    bitboard: dict[np.ndarray, int]

    def __init__(self, board: Board, color):
        self.board = board
        self.color = color

        self.bitboard = {}

    def calculate_move(self) -> int:
        move_evaluations = []
        for move in range(7):
            next_board = Board(self.board.field.copy())
            move_evaluations.append(self.minimax(next_board, self.color == 1))
        print(move_evaluations)
        return move_evaluations.index(max(move_evaluations))

    def minimax(self, board: Board, maximize: bool) -> int:
        """

        :param maximize:
        :param board:
        :return:
        """
        #if board.field in self.bitboard.keys():
        #    return self.bitboard[board.field]

        if board.is_game_over()[0]:
            return eval_field(board)

        if maximize:
            max_eval = float("-inf")
            for move in range(7):
                next_board = Board(board.field.copy())
                could_place = next_board.place_marker(move, 1)
                if could_place:
                    max_eval = max(max_eval, self.minimax(next_board, False))
            return max_eval
        else:
            min_eval = float("+inf")
            for move in range(7):
                next_board = Board(board.field.copy())
                could_place = next_board.place_marker(move, 2)
                if could_place:
                    min_eval = min(min_eval, self.minimax(next_board, True))
            return min_eval

    # Idee: Maussimulation, damit sich der Cursor über dem Spielfeld zur richtigen Position bewegt, bevor gesetzt wird
    def simulate_mouse_movement(self) -> None:
        while True:
            ...


"""
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
"""