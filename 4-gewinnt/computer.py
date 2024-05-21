from board import Board


class Computer:
    board: Board
    color: int

    bitboard: dict[Board, int]

    def __init__(self, board: Board, color):
        self.board = board
        self.color = color

        self.bitboard = dict()

    def calculate_move(self) -> int:
        """
        Works towards finding the optimal move in the given situation for the computer.
        Uses minimax and heuristic evaluation to search into future board states
        :return: the x-index of the column in which a marker should be dropped
        """
        should_maximize = True if self.color == 1 else False
        best_move = None

        if should_maximize:
            max_score = -42
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = self.minimax(board=next_board, maximize=False, alpha=-42, beta=42, depth=4)
                if score > max_score:
                    max_score = score
                    best_move = move
        else:
            min_score = 42
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = self.minimax(board=next_board, maximize=True, alpha=-42, beta=42, depth=4)
                if score < min_score:
                    min_score = score
                    best_move = move
        return best_move

    def minimax(self, board: Board, maximize: bool, alpha: int, beta: int, depth: int) -> int:
        game_over, winner = board.is_game_over()

        # Check if board configuration is already cached
        if board in self.bitboard.keys():
            print("cache hit", len(self.bitboard))
            return self.bitboard[board]

        # Scenario 1: game is over
        if game_over:
            if winner == 0:
                move_evaluation = 0
            else:
                move_evaluation = 50 * (1 if winner == 1 else -1)
        # Scenario 2: depth exceeded, evaluate position using heuristics
        elif depth == 0:
            move_evaluation = self.eval_field(board)
        # Scenario 3: Minimax
        elif maximize:
            max_eval = -42
            for move in board.get_possible_moves():
                next_board = Board(board.field.copy())
                next_board.place_marker(move)
                score = self.bitboard[next_board] if next_board in self.bitboard.keys() else self.minimax(
                    board=next_board, maximize=False, alpha=alpha, beta=beta, depth=depth - 1)
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            move_evaluation = max_eval
        else:
            min_eval = 42
            for move in board.get_possible_moves():
                next_board = Board(board.field.copy())
                next_board.place_marker(move)
                score = self.bitboard[next_board] if next_board in self.bitboard.keys() else self.minimax(
                    board=next_board, maximize=True, alpha=alpha, beta=beta, depth=depth - 1)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            move_evaluation = min_eval

        # Cache board configuration with fitting score
        self.bitboard[board] = move_evaluation

        return self.bitboard[board]

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
                board_slice = board.is_4_straight_connected(x, y, horizontal=True)[1]
                score += self.heuristic_evaluation_of(board_slice)

        # Scenario 2: four in a column
        for y in range(3):
            for x in range(7):
                board_slice = board.is_4_straight_connected(x, y, horizontal=False)[1]
                score += self.heuristic_evaluation_of(board_slice)

        # Scenario 3: four diagonally
        for x in range(4):
            for y in range(3):
                board_slice = board.is_4_diagonal_connected(x, y, high_to_low=False)[1]
                score += self.heuristic_evaluation_of(board_slice)
                score += self.heuristic_evaluation_of(board_slice)

        return score

    def heuristic_evaluation_of(self, board_slice: tuple) -> int:
        """
        Gives a heuristic evaluation of a small selection
        :param board_slice: the selection from the board
        :return: a score
        """
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
