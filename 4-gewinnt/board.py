import numpy as np

from typing import Optional
class Board:
    field: np.ndarray
    latest_move_x: int
    latest_move_y: int

    def __init__(self, field: Optional[np.ndarray] = None, *, width: Optional[int] = None, height: Optional[int] = None):
        """
        Creates a new Board for a Game to be played at
        WARNING: width and height arguments are only to be used when field is None
        :param field: ndarray symbolizing the field the game is played at
        :param width: width of the field
        :param height: height of the field
        """
        self.field = field if field is not None else np.zeros((height, width))
        self.latest_move_x, self.latest_move_y = 0, 0

    def __repr__(self):
        return str(self.field)

    def __hash__(self):
        return int("".join(str(int(x)) for row in self.field for x in row), base=3)

    def __getitem__(self, item: int) -> np.ndarray:
        return self.field.transpose()[item]

    def __len__(self) -> int:
        return len(self.field)

    def filled_fields(self) -> int:
        """
        Returns the number of filled fields on the board
        :return: int
        """
        return np.count_nonzero(self.field)

    def is_4_straight_connected(self, x: int, y: int, *, horizontal: bool) -> bool:
        """
        Checks for an x,y coordinate if there are 4 connected, same color markers in a straight line
        :param x: x-coordinate
        :param y: y-coordinate
        :param horizontal: Boolean representing if the check should occur horizontal or vertical
        :return: True if there are 4 connected, same color markers. False, if there are not
        """
        selection = tuple(self[x + (i if horizontal else 0)][y + (i if not horizontal else 0)] for i in range(4))
        if selection[0] == 0:  # Obviously we can't have 4 connected pieces if the first entry is empty
            return False

        for elem in selection:
            if elem != selection[0]:
                return False

        return True

    def is_4_diagonal_connected(self, x: int, y: int, *, high_to_low: bool) -> bool:
        """
        Checks for an x,y coordinate if there are 4 connected, same color markers in a diagonal line
        :param x: x-coordinate
        :param y: y-coordinate
        :param high_to_low: Boolean representing if the check should occur from upper-left to lower-right or lower-left to upper-right
        :return: True if there are 4 connected, same color markers. False, if there are not
        """
        selection = tuple(self[x + i][y + (i if not high_to_low else 3 - i)] for i in range(4))

        if selection[0] == 0:  # Obviously we can't have 4 connected pieces if the first entry is empty
            return False

        for elem in selection:
            if elem != selection[0]:
                return False

        return True

    def is_game_over(self) -> tuple[bool, int | np.ndarray]:
        # Case 1: tie
        upper_row = [self[x][0] for x in range(7)]
        if 0 not in upper_row:
            return True, 0

        # Case 2: four in a row
        # todo explain the max() thing
        for x in range(max(0, self.latest_move_x - 3), 4):
            if self.is_4_straight_connected(x, self.latest_move_y, horizontal=True):
                return True, self[x][self.latest_move_y]

        # Case 3: four in a column
        # todo explain why we dont loop
        if self.latest_move_y <= 2 and self.is_4_straight_connected(self.latest_move_x, self.latest_move_y, horizontal=False):
            return True, self[self.latest_move_x][self.latest_move_y]

        # Case 4: four diagonally
        for x in range(4):
            for y in range(3):
                if self.is_4_diagonal_connected(x, y, high_to_low=False):
                    return True, self[x][y]
                elif self.is_4_diagonal_connected(x, y, high_to_low=True):
                    return True, self[x][y+3]

        return False, -1

    def can_play(self, x: int) -> bool:
        """
        Checks if a marker can be placed in column x
        :param x: x-index of the column
        :return: True if a marker can be placed, False otherwise
        """
        if self[x][0] != 0:
            return False
        return True

    def place_marker(self, x: int) -> None:
        """
        :param x: x-index of the column
        :return: None
        :raises ValueError: if the column is full
        """
        if not self.can_play(x):
            raise ValueError("Cannot place marker because the column is full")
        for y in range(len(self.field)):
            y = 5 - y
            if self[x][y] == 0:
                self[x][y] = 1 if self.filled_fields() % 2 == 0 else 2
                self.latest_move_x, self.latest_move_y = x, y
                return

    def get_possible_moves(self) -> list[int]:
        """
        Returns a list of possible columns where a marker can be placed
        :return: List of column indices
        """
        return [move for move in range(7) if self.can_play(move)]
