from board import Board


def get_modular_depth(filled_fields: int) -> int:
    """
    A helper method, representing a simple mathematical function that takes the amount of filled fields on the board
    and returns a depth value suited for the algorythm to be performant
    :param filled_fields: the amount of filled fields in the board
    :return: an integer representing the amount of moves to go into the future
    """
    if filled_fields < 15:
        return 4
    if filled_fields < 18:
        return 5
    if filled_fields < 22:
        return 6
    if filled_fields < 25:
        return 7

    return 42 - filled_fields  # this is the max depth until every marker is placed


class Computer:
    board: Board
    color: int

    def __init__(self, board: Board, color):
        self.board = board
        self.color = color

    @property
    def should_maximize(self):
        return True if self.color == 1 else False

    def calculate_move(self) -> int:
        """
        Works towards finding the optimal move in the given situation for the computer
        Uses minimax and heuristic evaluation to search into future board states
        :return: the x-index of the column in which a marker should be dropped
        """
        best_move = None
        modular_depth = get_modular_depth(self.board.filled_fields())

        # Check directly if the computer can win with the next move
        # This makes sure, the computer doesn't stall on its winning move, which would frustrate the player
        for move in self.board.get_possible_moves():
            next_board = Board(self.board.field.copy())
            next_board.place_marker(move)
            if next_board.is_game_over()[0]:
                return move

        # If it cannot win directly, it will generate all possible board combinations and evaluate them
        if self.should_maximize:
            max_score = -43
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = self.minimax(board=next_board, maximize=False, alpha=-42, beta=42, depth=modular_depth)
                if score > max_score:
                    max_score = score
                    best_move = move
        else:
            min_score = 43
            for move in self.board.get_possible_moves():
                next_board = Board(self.board.field.copy())
                next_board.place_marker(move)
                score = self.minimax(board=next_board, maximize=True, alpha=-42, beta=42, depth=modular_depth)
                if score < min_score:
                    min_score = score
                    best_move = move
        return best_move

    def minimax(self, board: Board, maximize: bool, alpha: int, beta: int, depth: int) -> int:
        """
        Searches into the all future board positions and evaluates them
        :param board: the board to evaluate
        :param maximize: if the algorythm should maximize or minimize
        :param alpha: parameter to prune branches, shows the highest possible score for a branch
        :param beta: parameter to prune branches, shows the lowest possible score for a branch
        :param depth: how many moves to algorythm shall look into the future
        :return: an evaluation of the board
        """
        game_over, winner, _ = board.is_game_over()

        # Scenario 1: game is over
        if game_over:
            if winner == 0:
                return 0
            else:
                return 42 * (1 if winner == 1 else -1)
        # Scenario 2: depth exceeded, evaluate position using heuristics
        elif depth == 0:
            return self.eval_field(board)
        # Scenario 3: minimax evaluation
        elif maximize:
            max_eval = -42
            for move in board.get_possible_moves():
                next_board = Board(board.field.copy())
                next_board.place_marker(move)
                score = self.minimax(board=next_board, maximize=False, alpha=alpha, beta=beta, depth=depth - 1)
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
                score = self.minimax(board=next_board, maximize=True, alpha=alpha, beta=beta, depth=depth - 1)
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_eval

    def eval_field(self, board: Board) -> int:
        """
        Calculates the evaluation of the current board if depth of minimax is exceeded
        :param board: the board to be evaluated
        :return: an EVALUATION of the board position
        """
        score = 0

        # Scenario 1: four in a row
        for y in range(6):
            for x in range(4):
                _, board_slice = board.is_4_straight_connected(x, y, horizontal=True)
                score += self.heuristic_evaluation_of(board_slice)

        # Scenario 2: four in a column
        for y in range(3):
            for x in range(7):
                _, board_slice = board.is_4_straight_connected(x, y, horizontal=False)
                score += self.heuristic_evaluation_of(board_slice)

        # Scenario 3: four diagonally
        for x in range(4):
            for y in range(3):
                score += self.heuristic_evaluation_of(board.is_4_diagonal_connected(x, y, high_to_low=False)[1])
                score += self.heuristic_evaluation_of(board.is_4_diagonal_connected(x, y, high_to_low=True)[1])

        return score

    def heuristic_evaluation_of(self, board_slice: tuple[int, ...]) -> int:
        """
        Gives a heuristic evaluation of a small selection
        :param board_slice: the selection from the board
        :return: a score
        """
        score = 0

        if self.should_maximize:
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
