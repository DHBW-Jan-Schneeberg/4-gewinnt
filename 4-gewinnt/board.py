import numpy as np

from typing import Optional


def selection_is_connected(selection: tuple[int, ...]) -> bool:
    """
    Checks if a selection contains only one unique element
    :param selection:
    :return: Boolean
    """
    selection = set(selection)
    if 0 in selection or len(selection) > 1:
        return False

    return True


class Board:
    field: np.ndarray
    latest_move_x: int
    latest_move_y: int

    height: int
    width: int

    def __init__(self, field: Optional[np.ndarray] = None, *, width: Optional[int] = None, height: Optional[int] = None):
        """
        Creates a new board for a game to be played at
        WARNING: width and height arguments are only to be used when field is None
        :param field: ndarray symbolizing the field the game is played at
        :param width: width of the field
        :param height: height of the field
        """
        self.field = field if field is not None else np.zeros((height, width))
        self.height, self.width = height, width
        self.latest_move_x, self.latest_move_y = 0, 0

    @property
    def current_player(self):
        return 1 if self.filled_fields() % 2 == 0 else 2

    def __repr__(self):
        return str(self.field)

    def __getitem__(self, item: int) -> np.ndarray:
        return self.field.transpose()[item]

    def __len__(self) -> int:
        return len(self.field)

    def reset(self) -> None:
        """
        Clears all values in the field
        :return: None, since this method is a modifier
        """
        self.field = np.zeros((self.height, self.width))

    def filled_fields(self) -> int:
        """
        Returns the number of filled fields on the board
        :return: int
        """
        return np.count_nonzero(self.field)

    def is_4_straight_connected(self, x: int, y: int, *, horizontal: bool) -> tuple[bool, tuple[int, ...]]:
        """
        Checks for an x,y coordinate if there are 4 connected, same color markers in a straight line
        :param x: x-coordinate
        :param y: y-coordinate
        :param horizontal: Boolean representing if the check should occur horizontal or vertical
        :return: Boolean representing if the condition was met, as well as the made selection
        """
        selection = tuple(int(self[x + (i if horizontal else 0)][y + (i if not horizontal else 0)]) for i in range(4))
        return selection_is_connected(selection), selection

    def is_4_diagonal_connected(self, x: int, y: int, *, high_to_low: bool) -> tuple[bool, tuple[int, ...]]:
        """
        Checks for an x,y coordinate if there are 4 connected, same color markers in a diagonal line
        :param x: x-coordinate
        :param y: y-coordinate
        :param high_to_low: Boolean representing if the check should occur from upper-left to lower-right or lower-left to upper-right
        :return: Boolean representing if the condition was met, as well as the made selection
        """
        selection = tuple(int(self[x + i][y + (i if not high_to_low else 3 - i)]) for i in range(4))
        return selection_is_connected(selection), selection

    def is_game_over(self) -> tuple[bool, int | np.ndarray, Optional[list[tuple[int, int]]]]:
        """
        Checks if the draw or winning condition is met
        :return: a boolean representing if the game is over,
            the winner (0 = draw, 1 = yellow, 2 = red),
            as well as a list containing the (x, y) coords of the "win-causing" markers
        """
        # Case 1: tie
        upper_row = [self[x][0] for x in range(7)]
        if 0 not in upper_row:
            return True, 0, None

        # Case 2: four in a row
        # This works by looking at the latest move played and comparing the right and left markers
        # at a maximum of 3 markers to both its sides
        for x in range(max(0, self.latest_move_x - 3), 4):
            if self.is_4_straight_connected(x, self.latest_move_y, horizontal=True)[0]:
                return True, self[x][self.latest_move_y], [(x_, self.latest_move_y) for x_ in range(x, x+4)]

        # Case 3: four in a column
        # Only if the marker was placed in the upper 3 rows, a connect-4 can be achieved vertically
        if self.latest_move_y <= 2 and self.is_4_straight_connected(self.latest_move_x, self.latest_move_y, horizontal=False)[0]:
            return True, self[self.latest_move_x][self.latest_move_y], [(self.latest_move_x, y_) for y_ in range(self.latest_move_y, self.latest_move_y+4)]

        # Case 4: four diagonally
        for x in range(4):
            for y in range(3):
                if self.is_4_diagonal_connected(x, y, high_to_low=False)[0]:
                    return True, self[x][y], [(x+i, y+i) for i in range(4)]
                elif self.is_4_diagonal_connected(x, y, high_to_low=True)[0]:
                    return True, self[x][y+3], [(x+i, y+3-i) for i in range(4)]

        return False, -1, None

    def can_play(self, x: int) -> bool:
        """
        Checks if a marker can be placed in column x
        :param x: x-index of the column
        :return: True if a marker can be placed, False otherwise
        """
        if self[x][0] == 0:
            return True

        return False

    def place_marker(self, x: int) -> None:
        """
        :param x: x-index of the column
        :return: None
        :raises ValueError: if the column is full
        """
        if not self.can_play(x):
            raise ValueError("Cannot place marker because the column is full")

        # Looks cursed, but this
        for y in range(len(self.field) - 1, -1, -1):
            if self[x][y] == 0:
                self[x][y] = self.current_player
                self.latest_move_x, self.latest_move_y = x, y
                return

    def get_possible_moves(self) -> list[int]:
        """
        Returns a list of possible columns where a marker can be placed
        :return: List of column indices
        """
        return [move for move in [3, 4, 2, 5, 1, 6, 0] if self.can_play(move)]
