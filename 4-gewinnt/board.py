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

    def set_in_field(self, x: int, y: int, value: int) -> None:
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :param value: the value to be set at (x,y) on the field
        """
        self.field.transpose()[x][y] = value

    def get_from_field(self, x: int, y: int) -> np.ndarray:
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :return: the value at (x,y) on the field
        """
        return self.field.transpose()[x][y]

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
        selection = tuple(self.get_from_field(x + (i if horizontal else 0), y + (i if not horizontal else 0)) for i in range(4))
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
        selection = tuple(self.get_from_field(x + i, y + (i if not high_to_low else 3 - i)) for i in range(4))

        if selection[0] == 0:  # Obviously we can't have 4 connected pieces if the first entry is empty
            return False

        for elem in selection:
            if elem != selection[0]:
                return False

        return True

    def is_game_over(self) -> bool:
        # Case 1: tie
        if self.filled_fields() == 42:
            return True

        # Case 2: four in a row
        for y in range(len(self.field)):
            for x in range(len(self.field[0]) - 3):
                if self.is_4_straight_connected(x, y, horizontal=True):
                    return True

        # Case 3: four in a column
        for y in range(len(self.field) - 3):
            for x in range(len(self.field[0])):
                if self.is_4_straight_connected(x, y, horizontal=False):
                    return True

        # Case 4: four diagonally
        for x in range(len(self.field[0]) - 3):
            for y in range(len(self.field) - 3):
                if self.is_4_diagonal_connected(x, y, high_to_low=True) or self.is_4_diagonal_connected(x, y, high_to_low=False):
                    return True

        return False

    def place_marker(self, x: int, player: int) -> bool:
        """
        :param player:
        :param x: x-index of the column
        :return:  False if the placement was not successful due to a full column
        """
        if self.get_from_field(x, 0) != 0:
            return False

        for y in range(len(self.field)):
            y = 5 - y
            if self.get_from_field(x, y) == 0:
                self.set_in_field(x, y, player)
                return True
