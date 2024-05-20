from typing import Optional

from board import Board


def eval_field(board: Board) -> int:
    """
    Calculates the evaluation of the current board
    :param board:
    :return: an EVALUATION of the board position
    """
    return 42 - board.filled_fields()


def minimax(board: Board, maximize: bool, alpha: int, beta: int) -> int:
    game_over, winner = board.is_game_over()
    if game_over:
        if winner == 0:
            return 0
        else:
            return eval_field(board) * (1 if winner == 1 else -1)

    if maximize:
        max_eval = -42
        for move in board.get_possible_moves():
            next_board = Board(board.field.copy())
            next_board.place_marker(move)
            score = minimax(board=next_board, maximize=False, alpha=alpha, beta=beta)
            max_eval = max(max_eval, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 42
        for move in board.get_possible_moves():
            next_board = Board(board.field.copy())
            next_board.place_marker(move)
            score = minimax(board=next_board, maximize=True, alpha=alpha, beta=beta)
            min_eval = min(min_eval, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_eval


def find_wins(board: Board, depth: int):
    game_over, winner = board.is_game_over()
    if game_over:
        if winner == 0:
            print("Draw:\n", board)
            return
        else:
            print("Win" if winner == 1 else "Lose\n", board)
            return

    if depth == 0:
        return

    for move in board.get_possible_moves():
        next_board = Board(board.field.copy())
        next_board.place_marker(move)
        find_wins(board=next_board, depth=depth-1)


class Computer:
    board: Board
    color: int

    def __init__(self, board: Board, color):
        self.board = board
        self.color = color

    def calculate_move(self) -> int:
        should_maximize = True if self.color == 1 else False
        best_move = None

        if should_maximize:
            max_score = -42
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = minimax(board=next_board, maximize=False, alpha=-42, beta=42)
                if score > max_score:
                    max_score = score
                    best_move = move
                print(f"{move=} {score=}")
                print("Resulting board:\n", next_board.field)
            print("=========================\n=========================")
        else:
            min_score = 42
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = minimax(board=next_board, maximize=True, alpha=-42, beta=42)
                if score < min_score:
                    min_score = score
                    best_move = move
                print(f"{move=} {score=}")
                print("Resulting board:\n", next_board.field)
            print("=========================\n=========================")

        return best_move

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