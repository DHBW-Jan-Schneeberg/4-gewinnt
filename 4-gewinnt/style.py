from main import Game


class MouseSimulation:
    target_position: int

    def __init__(self):
        self.target_position = Game.robot_move

    # Idee: Maussimulation, damit sich der Cursor über dem Spielfeld zur richtigen Position bewegt, bevor gesetzt wird
    def simulate_mouse_movement(self) -> None:
        pass
        #while True:
            #if self.target_position is not None:
                #break
