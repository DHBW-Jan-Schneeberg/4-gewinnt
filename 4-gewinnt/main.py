import pygame
import numpy as np


class Game:
    screen: pygame.Surface
    clock: pygame.time.Clock
    running: bool

    field: np.ndarray
    current_player: int  # 1 for Yellow, 2 for Red
    winner: str | None

    width: int
    height: int
    spacing: int

    buffered_input: tuple[bool, bool, bool]

    def __init__(self, screen: pygame.Surface, *, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.width = width
        self.height = height
        self.winner = None

        self.field = np.zeros((self.height, self.width))
        self.current_player = 1
        self.buffered_input = (False, False, False)

    def set_in_field(self, x, y, value):
        """
        TODO
        :param x:
        :param y:
        :param value:
        :return:
        """
        self.field.transpose()[x][y] = value

    def get_from_field(self, x, y):
        """
        TODO
        :param x:
        :param y:
        :return:
        """
        return self.field.transpose()[x][y]

    def draw_field(self) -> None:
        self.screen.fill(color="blue")
        for x in range(self.width):
            for y in range(self.height):
                color = "grey" if self.get_from_field(x, y) == 0 else "yellow" if self.get_from_field(x, y) == 1 else "red"
                pygame.draw.circle(self.screen, color,
                                   (x * 105 + 55, y * 105 + 205), radius=50)

        mouse_x, _ = pygame.mouse.get_pos()  # We don't care for y since we place the marker always on top
        self.show_current_selected_position(mouse_x)
        pygame.display.flip()

    def show_current_selected_position(self, mouse_x: int) -> None:
        x = mouse_x // 105
        color = 0xffff66 if self.current_player == 1 else 0xff6666
        pygame.draw.circle(self.screen, color, (x * 105 + 55, 55), radius=50)

    def check_game_over(self) -> None:
        # checkt für jede Reihe horizontal
        for y in range(self.height):
            for x in range(self.width - 4):
                # TODO
                pass

        # checkt für eine Spalte vertikal
        for x in range(self.width):
            for y in range(self.height - 4):
                pass
                # TODO

    def place_marker(self, x: int) -> None:
        # Wenn das Feld bereits besetzt ist
        if self.get_from_field(x, 0) != 0:
            return

        for y in range(self.height):
            y = 5 - y
            if self.get_from_field(x, y) == 0:
                self.set_in_field(x, y, self.current_player)
                break

        # Rotates to the next player
        self.current_player = 1 if self.current_player == 2 else 2

    def start(self) -> None:
        pygame.display.set_caption(title="4 g'winnt")
        self.draw_field()
        while self.running:
            self.draw_field()
            was_currently_clicked = False

            # Limitiert unsere FPS
            self.clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_buttons_pressed = pygame.mouse.get_pressed(3)
            if mouse_buttons_pressed != self.buffered_input:
                was_currently_clicked = True
                self.buffered_input = mouse_buttons_pressed

            if mouse_buttons_pressed[0] and was_currently_clicked:
                mouse_x, _ = pygame.mouse.get_pos()
                self.place_marker(mouse_x // 105)
                pygame.time.delay(500)

            self.check_game_over()
            if self.winner:
                print(f"{self.winner=}")


def main():
    pygame.init()
    screen = pygame.display.set_mode((740, 785))
    game = Game(screen, width=7, height=6)
    game.start()


if __name__ == "__main__":
    main()

