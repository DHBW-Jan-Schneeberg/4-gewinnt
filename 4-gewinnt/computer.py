import random

from board import Board


class Computer:
    def __init__(self, board: Board):
        self.board = board
        ...

    def calculate_move(self) -> int: # Könnte bisher auch noch außerhalb definiert werden (für Zukunft schon einmal innerhalb der Klasse gepackt)
        return random.randint(0, 6)
        # Will end up being more complex

    # Idee: Maussimulation, damit sich der Cursor über dem Spielfeld zur richtigen Position bewegt, bevor gesetzt wird
    def simulate_mouse_movement(self) -> None:
        while True:
            ...
