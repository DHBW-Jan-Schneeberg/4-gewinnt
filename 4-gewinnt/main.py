import random
import sys
from typing import Optional
import time

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
    computer_color: Optional[int]
    computer_move: Optional[int]

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
        self.board = Board(field=None, width=self.width, height=self.height)

        if against_computer and computer_color == 0:
            raise ValueError("Du kannst kein Spiel gegen den Computer starten, ohne ihm eine Farbe zu geben!")

        self.computer_enemy = Computer(self.board, computer_color) if against_computer else None
        self.computer_color = computer_color if against_computer else None
        self.computer_move = None
        self.computer_mouse_position = None

    def reset(self) -> None:
        """
        Resets the game board and the winner
        """
        pygame.display.set_caption(title="4-Gewinnt")
        self.board.reset()
        self.winner = None

    def draw_field(self, show_cursor_position: bool = True, winning_markers: Optional[list[tuple[int, int]]] = None) -> None:
        """
        Draws the game field and shows the current selected position of computer and human players
        :param show_cursor_position: if a marker should be displayed above the column the player is hovering
        :param winning_markers: if a connect-4 was scored, this list shall contain the (x, y) coords of the 4 markers
        """
        self.screen.fill(color="blue")
        for x in range(self.width):
            for y in range(self.height):
                color = 0xd0d1d1 if self.board[x][y] == 0 else "yellow" if self.board[x][y] == 1 else "red"
                pygame.draw.circle(self.screen, color, (x * self.MARKER_SPACING + 55, y * self.MARKER_SPACING + 205), radius=self.MARKER_RADIUS)

        if show_cursor_position:
            if self.computer_enemy and self.current_player == self.computer_color:
                self.calculate_mouse_movement()
                self.show_selected_position(self.computer_mouse_position)
            else:
                mouse_x, _ = pygame.mouse.get_pos()  # We don't care about y since we place the marker always on top
                self.show_selected_position(mouse_x // self.MARKER_SPACING)
        if winning_markers:
            self.show_connect_four(winning_markers)
        pygame.display.flip()

    def show_selected_position(self, x: int) -> None:
        """
        Draws a marker above the selected column
        :param x: x-index of the column
        :return: None
        """
        color = "yellow" if self.current_player == 1 else "red"
        pygame.draw.circle(self.screen, color, (x * self.MARKER_SPACING + 55, 55), radius=self.MARKER_RADIUS)

    def simulate_mouse_movement(self) -> None:
        if self.computer_move is None:
            time.sleep(0.5)
            for _ in range(4):
                self.draw_field()
                time.sleep(0.4)
        elif self.computer_move == self.computer_mouse_position:
            time.sleep(0.4)
        else:
            for _ in range(abs(self.computer_move - self.computer_mouse_position)):
                self.draw_field()
                time.sleep(0.4)

    def calculate_mouse_movement(self) -> None:
        """
        Calculates which column the computer is hovering over for simulation purpose
        """
        # Case 1: Initialize computer mouse in the middle of the screen
        if self.computer_mouse_position is None:
            self.computer_mouse_position = 3
        # Case 2: Move computer mouse towards the calculated position
        elif self.computer_move is not None:
            if self.computer_mouse_position > self.computer_move:
                self.computer_mouse_position -= 1
            elif self.computer_mouse_position < self.computer_move:
                self.computer_mouse_position += 1
        # Case 3: Move computer mouse in a random direction
        else:
            # When on the edge, move towards the field, otherwise pick random between left and right
            self.computer_mouse_position = \
                1 if self.computer_mouse_position == 0 \
                else 5 if self.computer_mouse_position == 6 \
                else self.computer_mouse_position + random.choice([-1, 1])

    def show_connect_four(self, coords: list[tuple[int, int]]) -> None:
        """
        Highlights the four connected circles by drawing a black X over them
        :param coords: a list containing (x, y) tuples indicating the index of each colum/row position a winning marker is at
        """
        pass

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
                    winner_text = TextField(200, 110, f"{self.winner} gewinnt das Match!", self.screen)
                    winner_text.process()

                # Case 1: play another round
                if play_again_button.clicked:
                    self.reset()
                    play_again_button.clicked = False
                    game_over = False
                # Case 2: get back to modus menu
                elif return_button.clicked:
                    option_screen = OptionScreen()
                    option_screen.await_input()
                    return_button = False
                # Case 3: game is over, but no button pressed yet
                else:
                    play_again_button.process()
                    return_button.process()
                    pygame.display.flip()

                continue

            # Here starts the "real" game loop
            if self.computer_enemy and self.current_player == self.computer_color:
                self.simulate_mouse_movement()
                self.computer_move = self.computer_enemy.calculate_move()
                self.simulate_mouse_movement()
                self.board.place_marker(self.computer_move)

                pygame.mixer.Sound.play(sound_tile)
                self.computer_mouse_position = None
                self.computer_move = None
            else:
                mouse_buttons_pressed = pygame.mouse.get_pressed(3)
                if mouse_buttons_pressed != self.buffered_input:
                    self.buffered_input = mouse_buttons_pressed

                    if mouse_buttons_pressed[0]:
                        mouse_x, _ = pygame.mouse.get_pos()
                        x = mouse_x // self.MARKER_SPACING
                        if self.board.can_play(x):
                            self.board.place_marker(x)
                            pygame.mixer.Sound.play(sound_tile)

            game_over, winner_code, winning_markers = self.board.is_game_over()
            if game_over:
                self.draw_field(show_cursor_position=False, winning_markers=winning_markers)

                # Waits so the player can release the pressed mouse button to not immediately restart the game
                pygame.time.delay(100)
            else:
                self.draw_field()


def start_game(*, against_computer: bool, computer_color: Optional[int] = None) -> None:
    """
    Initializes the first game field
    :param against_computer:
    :param computer_color:
    :return:
    """
    screen = pygame.display.set_mode((740, 785))
    game = Game(screen, width=7, height=6, against_computer=against_computer, computer_color=computer_color)
    game.start()


# Loading sounds for buttons and tiles
pygame.mixer.init()
sound_tile = pygame.mixer.Sound("4-gewinnt/4-gewinnt/style/sounds/sound_1.mp3")
sound_button = pygame.mixer.Sound("4-gewinnt/4-gewinnt/style/sounds/sound_2.mp3")


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
        """
        Provides functionality and visual appearance to buttons
        """
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.clicked = True
                pygame.mixer.Sound.play(sound_button)
                time.sleep(0.1)

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)


class TextField:
    screen: pygame.surface

    def __init__(self, x: int, y: int, text: str, screen: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.screen = screen
        self.text = text

    def process(self) -> None:
        """
        Displays text
        """
        game_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = game_font.render(self.text, False, 0xd0d1d1)
        self.screen.blit(self.text_surface, (self.x, self.y))


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
        """
        Checks which game mode gets chosen
        """
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
