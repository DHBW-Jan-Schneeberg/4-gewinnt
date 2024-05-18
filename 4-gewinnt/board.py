import numpy as np


class Board:
    field: np.ndarray

    def __init__(self, field: np.ndarray | None = None, *, width: int | None = None, height: int | None = None):
        """
        Creates a new Board for a Game to be played at
        WARNING: width and height arguments are only to be used when field is None
        :param field: ndarray symbolizing the field the game is played at
        :param width: width of the field
        :param height: height of the field
        """
        self.field = field if field is not None else np.zeros((height, width))

    def __getitem__(self, item):
        return self.field.transpose()[item]

    def __len__(self):
        return len(self.field)

    def filled_fields(self) -> int:
        """
        TODO
        :return:
        """
        return np.count_nonzero(self.field)

    def is_4_straight_connected(self, x: int, y: int, *, horizontal: bool):
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

    def is_4_diagonal_connected(self, x: int, y: int, *, high_to_low: bool):
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

    def is_game_over(self) -> tuple[bool, int]:
        # Case 1: tie
        if self.filled_fields() == 42:
            return True, 0

        # Case 2: four in a row
        for y in range(6):
            for x in range(4):
                if self.is_4_straight_connected(x, y, horizontal=True):
                    return True, self[x][y]

        # Case 3: four in a column
        for y in range(3):
            for x in range(7):
                if self.is_4_straight_connected(x, y, horizontal=False):
                    return True, self[x][y]

        # Case 4: four diagonally
        for x in range(4):
            for y in range(3):
                if self.is_4_diagonal_connected(x, y, high_to_low=False):
                    return True, self[x][y]
                elif self.is_4_diagonal_connected(x, y, high_to_low=True):
                    return True, self[x][y+3]

        return False, -1

    def can_play(self, x: int) -> bool:
        if self[x][0] != 0:
            return False
        return True

    def place_marker(self, x: int) -> None:
        """
        :param x: x-index of the column
        :return:  False if the placement was not successful due to a full column
        """
        if not self.can_play(x):
            raise ValueError("Das hätte nicht passieren dürfen")
        for y in range(len(self.field)):
            y = 5 - y
            if self[x][y] == 0:
                self[x][y] = 1 if self.filled_fields() % 2 == 0 else 2
                return

    def get_possible_moves(self) -> list[int]:
        return [move for move in range(7) if self.can_play(move)]
