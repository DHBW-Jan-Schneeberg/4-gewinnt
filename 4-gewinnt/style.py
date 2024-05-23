import random


class MouseSimulation:
    target_position: int

    def __init__(self):
        self.start_position = random.randint(1, 7)
        self.target_position = Game.computer_move

    def calculate_mouse_movement(self, mouse_location: int | None) -> int:
        """
        Calculates which column the computer is hovering over for simulation purpose
        :param mouse_location:
        :return: Next simulated mouse location
        """
        # As soon as the target position is known, move to that position
        # if self.target_position is not None:
        #    mouse_destination = self.target_position

        if not self.target_position:
            if mouse_location > self.target_position:
                mouse_location -= 1
            elif mouse_location < self.target_position:
                mouse_location += 1
            return mouse_location

        else:
            possible_moves = []
            if mouse_location == 0:
                possible_moves.append(1)
            elif mouse_location == 6:
                possible_moves.append(5)
            else:
                possible_moves.append(mouse_location - 1)
                possible_moves.append(mouse_location + 1)

            mouse_location = random.choice(possible_moves)
        print(mouse_location)
        return mouse_location

from main import Game
