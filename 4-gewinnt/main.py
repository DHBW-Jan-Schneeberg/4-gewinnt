import random
import sys

import pygame
import numpy as np


class Computer:

    # TODO

    ...


class Game:
    # all the variables listed are for documentation only and have no further use being here
    screen: pygame.Surface
    clock: pygame.time.Clock

    field: np.ndarray
    current_player: int  # 1 for Yellow, 2 for Red
    winner: str | None

    width: int
    height: int
    spacing: int

    buffered_input: tuple[bool, bool, bool]

    robot_enemy: Computer | None
    robot_color = int | None

    MARKER_RADIUS: int = 40  # all caps variable is a constant

    def __init__(self, screen: pygame.Surface, *, width, height, against_computer, computer_color=0):
        """
        :param screen: the surface to draw on
        :param width: the width of the screen
        :param height: the height of the screen
        :param against_computer: if the player wants to play against the computer
        :param computer_color: if the players wants to play against the computer, he can choose whether the computer is yellow or red
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.winner = None

        self.field = np.zeros((self.height, self.width))
        self.current_player = 1
        self.buffered_input = (False, False, False)

        if against_computer and computer_color == 0:
            raise ValueError("Du kannst kein Spiel gegen den Computer starten, ohne ihm eine Farbe zu geben!")

        self.robot_enemy = Computer() if against_computer else None
        self.robot_color = computer_color if computer_color != 0 else None

    def reset(self):
        pygame.display.set_caption(title="4-Gewinnt")
        self.field = np.zeros((self.height, self.width))
        self.current_player = 1
        self.winner = None

    def set_in_field(self, x, y, value) -> None:
        """
        :param x: x-coordinate
        :param y: y-coordinate
        :param value: the value to be set at (x,y) on the field
        """
        self.field.transpose()[x][y] = value

    def get_from_field(self, x, y) -> int:
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

    def draw_field(self, show_cursor_position=True) -> None:
        self.screen.fill(color="blue")
        for x in range(self.width):
            for y in range(self.height):
                color = 0xd0d1d1 if self.get_from_field(x, y) == 0 else "yellow" if self.get_from_field(x, y) == 1 else "red"
                pygame.draw.circle(self.screen, color,
                                   (x * 105 + 55, y * 105 + 205), radius=self.MARKER_RADIUS)

        mouse_x, _ = pygame.mouse.get_pos()  # We don't care about y since we place the marker always on top

        if show_cursor_position:
            self.show_current_selected_position(mouse_x)
        pygame.display.flip()

    def show_current_selected_position(self, mouse_x: int) -> None:
        x = mouse_x // 105
        color = "yellow" if self.current_player == 1 else "red"
        pygame.draw.circle(self.screen, color, (x * 105 + 55, 55), radius=self.MARKER_RADIUS)

    def is_4_straight_connected(self, x: int, y: int, *, horizontal: bool):
        """
        Checks for an x,y coordinate if there are 4 connected, same color markers in a straight line
        :param x: x-coordinate
        :param y: y-coordinate
        :param horizontal: Boolean representing if the check should occur horizontal or vertical
        :return: True if there are 4 connected, same color markers. False, if there are not
        """
        selection = [self.get_from_field(x + (i if horizontal else 0), y + (i if not horizontal else 0)) for i in range(4)]
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
        selection = [self.get_from_field(x + i, y + (i if not high_to_low else 3 - i)) for i in range(4)]

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
        for y in range(self.height):
            for x in range(self.width - 3):
                if self.is_4_straight_connected(x, y, horizontal=True):
                    return True

        # Case 3: four in a column
        for y in range(self.height - 3):
            for x in range(self.width):
                if self.is_4_straight_connected(x, y, horizontal=False):
                    return True

        # Case 4: four diagonally
        for x in range(self.width - 3):
            for y in range(self.height - 3):
                if self.is_4_diagonal_connected(x, y, high_to_low=True) or self.is_4_diagonal_connected(x, y, high_to_low=False):
                    return True

        return False

    def place_marker(self, x: int) -> bool:
        """
        :param x: x-index of the column
        :return:  False if the placement was not successful due to a full column
        """
        if self.get_from_field(x, 0) != 0:
            return False

        for y in range(self.height):
            y = 5 - y
            if self.get_from_field(x, y) == 0:
                self.set_in_field(x, y, self.current_player)
                return True

    def swap_player(self) -> None:
        self.current_player = 1 if self.current_player == 2 else 2

    def start(self) -> None:
        self.reset()
        self.draw_field()

        play_again_button = Button(268, 50, 249, 60, "Erneut spielen", self.screen)
        game_over = False

        while True:
            # Limiting FPS and waiting on input, else the program gets "frozen"
            self.clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if game_over:
                if self.filled_fields() == 42:
                    pygame.display.set_caption(title=("Unentschieden"))
                else:
                    self.winner = "Geld" if self.current_player == 2 else "Rot"
                    pygame.display.set_caption(title=self.winner + " gewinnt")

                if not play_again_button.clicked:
                    play_again_button.process()
                    pygame.display.flip()
                else:
                    self.reset()
                    play_again_button.clicked = False
                    game_over = False
                continue

            # Hier beginnt tatsächlich so die "richtige" game loop
            if self.robot_enemy and self.current_player == self.robot_color:
                # TODO
                pygame.time.delay(int(3500 * random.random()))  # Player should feel as if the computer needs to "think"
                # take move from computer
                # play it
                ...
            else:
                mouse_buttons_pressed = pygame.mouse.get_pressed(3)
                if mouse_buttons_pressed != self.buffered_input:
                    self.buffered_input = mouse_buttons_pressed

                    if mouse_buttons_pressed[0]:
                        mouse_x, _ = pygame.mouse.get_pos()
                        if self.place_marker(mouse_x // 105):
                            self.swap_player()

            game_over = self.is_game_over()
            if game_over:
                self.draw_field(show_cursor_position=False)

                # Waits so the player can release the pressed mouse button to not immediately restart the game
                pygame.time.delay(100)
            else:
                self.draw_field(show_cursor_position=True)


def start_game(*, against_computer: bool, computer_color: int | None = None):
    screen = pygame.display.set_mode((740, 785))
    game = Game(screen, width=7, height=6, against_computer=against_computer, computer_color=computer_color)
    game.start()


class Button:
    def __init__(self, x, y, width, height, text: str, screen: pygame.Surface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clicked = False
        self.screen = screen

        self.fillColors = {
            'normal': 0xd0d1d1,
            'hover': 0x666666,
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = pygame.font.SysFont("Comic Sans MS", 30).render(text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.clicked = True

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)


class OptionScreen:
    screen: pygame.Surface
    clock: pygame.time.Clock

    buttons: list[Button]

    def __init__(self):
        self.screen = pygame.display.set_mode((600, 350))
        self.clock = pygame.time.Clock()

        self.buttons = [Button(165, 50, 270, 50, "Spiele gegen Gelb", self.screen),
                        Button(165, 150, 270, 50, "Spiele gegen Rot", self.screen),
                        Button(35, 250, 530, 50, "Spiele gegen einen anderen Spieler", self.screen)
                        ]

    def await_input(self):
        while True:
            self.clock.tick(10)
            self.screen.fill(0x3333ff)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            for i in range(3):
                self.buttons[i].process()

                if not self.buttons[i].clicked:
                    continue

                pygame.time.delay(200)
                if i == 2:
                    start_game(against_computer=False)
                    break
                else:
                    start_game(against_computer=True, computer_color=i+1)
                    break

            pygame.display.flip()


def main():
    pygame.init()
    option_screen = OptionScreen()
    option_screen.await_input()


if __name__ == "__main__":
    main()

