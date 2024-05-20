from board import Board

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

    bitboard: dict[Board, int]

    def __init__(self, board: Board, color):
        self.board = board
        self.color = color

        self.bitboard = dict()

    def minimax(self, board: Board, maximize: bool, alpha: int, beta: int, depth: int) -> int:
        game_over, winner = board.is_game_over()
        if game_over:
            print(len(self.bitboard))
            if winner == 0:
                return 0
            else:
                score = 50 * (1 if winner == 1 else -1)
                if board not in self.bitboard.keys():
                    self.bitboard[board] = score
                return self.bitboard[board]
        elif depth == 0:
            return self.eval_field(board)

        if board in self.bitboard.keys():
            print("hit", len(self.bitboard))
            return self.bitboard[board]

        if maximize:
            max_eval = -42
            for move in board.get_possible_moves():
                next_board = Board(board.field.copy())
                next_board.place_marker(move)
                score = self.bitboard[next_board] if next_board in self.bitboard.keys() else self.minimax(board=next_board, maximize=False, alpha=alpha, beta=beta, depth=depth-1)
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
                score = self.bitboard[next_board] if next_board in self.bitboard.keys() else self.minimax(board=next_board, maximize=True, alpha=alpha, beta=beta, depth=depth-1)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_eval

    def calculate_move(self) -> int:
        should_maximize = True if self.color == 1 else False
        best_move = None

        if should_maximize:
            max_score = -42
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = self.minimax(board=next_board, maximize=False, alpha=-42, beta=42, depth=5)
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
                score = self.minimax(board=next_board, maximize=True, alpha=-42, beta=42, depth=5)
                if score < min_score:
                    min_score = score
                    best_move = move
                print(f"{move=} {score=}")
                print("Resulting board:\n", next_board.field)
            print("=========================\n=========================")

        return best_move

    def eval_field(self, board: Board) -> int:
        """
        Calculates the evaluation of the current board
        :param board:
        :return: an EVALUATION of the board position
        """
        score = 0

        # Scenario 1: four in a row
        for y in range(6):
            for x in range(4):
                score += self.eval_player_position(board.is_4_straight_connected(x, y, horizontal=True)[1])

        # Scenario 2: four in a column
        for y in range(3):
            for x in range(7):
                score += self.eval_player_position(board.is_4_straight_connected(x, y, horizontal=False)[1])

        # Scenario 3: four diagonally
        for x in range(4):
            for y in range(3):
                score += self.eval_player_position(board.is_4_diagonal_connected(x, y, high_to_low=False)[1])
                score += self.eval_player_position(board.is_4_diagonal_connected(x, y, high_to_low=True)[1])

        print(f"Score: {score}")

        return score

    def eval_player_position(self, board_slice: tuple) -> int:
        should_maximize = True if self.color == 1 else False
        score = 0

        if should_maximize:
            if board_slice.count(self.color) == 3 and board_slice.count(0) == 1:
                score += 3
            elif board_slice.count(self.color) == 2 and board_slice.count(0) == 2:
                score += 2

            if board_slice.count(1 if self.color == 2 else 2) == 3 and board_slice.count(0) == 1:
                score -= 4

        else:
            if board_slice.count(self.color) == 3 and board_slice.count(0) == 1:
                score -= 3
            elif board_slice.count(self.color) == 2 and board_slice.count(0) == 2:
                score -= 2

            if board_slice.count(1 if self.color == 2 else 2) == 3 and board_slice.count(0) == 1:
                score += 4

        return score


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