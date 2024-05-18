import random
import sys
from typing import Optional

import pygame

from computer import Computer
from board import Board


class Game:
    # all the variables listed are for documentation only and have no further use being here
    screen: pygame.Surface
    clock: pygame.time.Clock

    board: Board
    current_player: int  # 1 for Yellow, 2 for Red
    winner: Optional[str]

    width: int
    height: int
    spacing: int

    buffered_input: tuple[bool, bool, bool]

    computer_enemy: Optional[Computer]
    computer_color = Optional[int]

    MARKER_RADIUS: int = 40  # all caps variable is a constant
    MARKER_SPACING: int = 105

    def __init__(self, screen: pygame.Surface, *, width, height, against_computer, computer_color=None):
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

        self.buffered_input = (False, False, False)

        if against_computer and computer_color == 0:
            raise ValueError("Du kannst kein Spiel gegen den Computer starten, ohne ihm eine Farbe zu geben!")

        self.computer_color = computer_color if computer_color else None

    @property
    def current_player(self):
        return 1 if self.board.filled_fields() % 2 == 0 else 2

    def reset(self) -> None:
        pygame.display.set_caption(title="4-Gewinnt")
        self.board = Board(field=None, width=self.width, height=self.height)
        self.computer_enemy = Computer(board=self.board, color=self.computer_color) if self.computer_color else None
        self.winner = None

    def draw_field(self, show_cursor_position: bool = True) -> None:
        self.screen.fill(color="blue")
        for x in range(self.width):
            for y in range(self.height):
                color = 0xd0d1d1 if self.board[x][y] == 0 else "yellow" if self.board[x][y] == 1 else "red"
                pygame.draw.circle(self.screen, color,
                                   (x * self.MARKER_SPACING + 55, y * self.MARKER_SPACING + 205), radius=self.MARKER_RADIUS)

        mouse_x, _ = pygame.mouse.get_pos()  # We don't care about y since we place the marker always on top

        if show_cursor_position:
            if self.computer_enemy and self.current_player == self.computer_color:
                # need to somehow display the action the computer is going to take
                # (optional)
                ...
            else:
                self.show_current_selected_position(mouse_x // self.MARKER_SPACING)
        pygame.display.flip()

    def show_current_selected_position(self, x: int) -> None:
        """
        Renders a circle
        :param x: x-index of the column
        :return: None
        """
        color = "yellow" if self.current_player == 1 else "red"
        pygame.draw.circle(self.screen, color, (x * self.MARKER_SPACING + 55, 55), radius=self.MARKER_RADIUS)

    def start(self) -> None:
        self.reset()
        self.draw_field()

        play_again_button = Button(100, 50, 239, 60, "Erneut spielen", self.screen)
        return_button = Button(400, 50, 290, 60, "Spielmodus wählen", self.screen)
        game_over = False
        winner_code = -1

        while True:
            # Limiting FPS and waiting on input, else the program gets "frozen"
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if game_over:
                if winner_code == 0:
                    pygame.display.set_caption(title="Unentschieden")
                else:
                    self.winner = "Gelb" if winner_code == 1 else "Rot"
                    pygame.display.set_caption(title=self.winner + " gewinnt")

                # Case 1: game is running
                if not play_again_button.clicked and not return_button.clicked:
                    play_again_button.process()
                    return_button.process()
                    pygame.display.flip()
                # Case 2: Play another round
                elif play_again_button.clicked:
                    self.reset()
                    play_again_button.clicked = False
                    game_over = False
                # Case 3: Get back to modus menu
                else:
                    option_screen = OptionScreen()
                    option_screen.await_input()
                    return_button = False
                continue

            # Here starts the "real" game loop
            if self.computer_enemy and self.current_player == self.computer_color:
                pygame.time.delay(int(100 * random.randint(2, 5)))  # Player should feel as if the computer needs to "think"
                robot_move = self.computer_enemy.calculate_move()

                self.board.place_marker(robot_move)
            else:
                mouse_buttons_pressed = pygame.mouse.get_pressed(3)
                if mouse_buttons_pressed != self.buffered_input:
                    self.buffered_input = mouse_buttons_pressed

                    if mouse_buttons_pressed[0]:
                        mouse_x, _ = pygame.mouse.get_pos()
                        x = mouse_x // self.MARKER_SPACING
                        if self.board.can_play(x):
                            self.board.place_marker(x)

            game_over, winner_code = self.board.is_game_over()
            if game_over:
                self.draw_field(show_cursor_position=False)

                # Waits so the player can release the pressed mouse button to not immediately restart the game
                pygame.time.delay(100)
            else:
                self.draw_field(show_cursor_position=True)


def start_game(*, against_computer: bool, computer_color: Optional[int] = None) -> None:
    screen = pygame.display.set_mode((740, 785))
    game = Game(screen, width=7, height=6, against_computer=against_computer, computer_color=computer_color)
    game.start()


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, screen: pygame.Surface) -> None:
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

    def process(self) -> None:
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

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((600, 350))
        self.clock = pygame.time.Clock()

        self.buttons = [Button(165, 50, 270, 50, "Spiele gegen Gelb", self.screen),
                        Button(165, 150, 270, 50, "Spiele gegen Rot", self.screen),
                        Button(35, 250, 530, 50, "Spiele gegen einen anderen Spieler", self.screen)
                        ]

    def await_input(self) -> None:
        pygame.display.set_caption("Spielmodus auswählen")
        while True:
            self.clock.tick(30)
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


def main() -> None:
    pygame.init()
    option_screen = OptionScreen()
    option_screen.await_input()


if __name__ == "__main__":
    main()
