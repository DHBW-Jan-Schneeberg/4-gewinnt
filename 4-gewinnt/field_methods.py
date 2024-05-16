import numpy as np

if __name__ == "__main__":
    print("Safe for import")


def set_in_field(field: np.ndarray, x, y, value) -> None:
    """
    :param field:
    :param x: x-coordinate
    :param y: y-coordinate
    :param value: the value to be set at (x,y) on the field
    """
    field.transpose()[x][y] = value


def get_from_field(field: np.ndarray, x, y) -> int:
    """
    :param field:
    :param x: x-coordinate
    :param y: y-coordinate
    :return: the value at (x,y) on the field
    """
    return field.transpose()[x][y]


def filled_fields(field: np.ndarray) -> int:
    """
    TODO
    :return:
    """
    return np.count_nonzero(field)


def is_4_straight_connected(x: int, y: int, *, horizontal: bool, field: np.ndarray):
    """
    Checks for an x,y coordinate if there are 4 connected, same color markers in a straight line
    :param field:
    :param x: x-coordinate
    :param y: y-coordinate
    :param horizontal: Boolean representing if the check should occur horizontal or vertical
    :return: True if there are 4 connected, same color markers. False, if there are not
    """
    selection = tuple(get_from_field(field, x + (i if horizontal else 0), y + (i if not horizontal else 0)) for i in range(4))
    if selection[0] == 0:  # Obviously we can't have 4 connected pieces if the first entry is empty
        return False

    for elem in selection:
        if elem != selection[0]:
            return False

    return True


def is_4_diagonal_connected(x: int, y: int, *, high_to_low: bool, field: np.ndarray):
    """
    Checks for an x,y coordinate if there are 4 connected, same color markers in a diagonal line
    :param field:
    :param x: x-coordinate
    :param y: y-coordinate
    :param high_to_low: Boolean representing if the check should occur from upper-left to lower-right or lower-left to upper-right
    :return: True if there are 4 connected, same color markers. False, if there are not
    """
    selection = tuple(get_from_field(field, x + i, y + (i if not high_to_low else 3 - i)) for i in range(4))

    if selection[0] == 0:  # Obviously we can't have 4 connected pieces if the first entry is empty
        return False

    for elem in selection:
        if elem != selection[0]:
            return False

    return True


def is_game_over(field: np.ndarray) -> bool:
    # Case 1: tie
    if filled_fields(field) == 42:
        return True

    # Case 2: four in a row
    for y in range(len(field)):
        for x in range(len(field[0]) - 3):
            if is_4_straight_connected(x, y, horizontal=True, field=field):
                return True

    # Case 3: four in a column
    for y in range(len(field) - 3):
        for x in range(len(field[0])):
            if is_4_straight_connected(x, y, horizontal=False, field=field):
                return True

    # Case 4: four diagonally
    for x in range(len(field[0]) - 3):
        for y in range(len(field) - 3):
            if is_4_diagonal_connected(x, y, high_to_low=True, field=field) or is_4_diagonal_connected(x, y, high_to_low=False, field=field):
                return True

    return False