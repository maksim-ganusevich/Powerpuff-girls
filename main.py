from enum import Enum
from threading import Thread

from work.AI import AI
from work.Player import Player
from work.Visualisation import Graphics


class Action(Enum):
    LOGIN = 1
    LOGOUT = 2
    MAP = 3
    GAME_STATE = 4
    GAME_ACTIONS = 5
    TURN = 6
    CHAT = 100
    MOVE = 101
    SHOOT = 102


def main():
    player1 = Player(name="Carlos")
    player2 = Player(name="Semen")
    player3 = Player(name="Woody")
    ai_ = AI([player1, player2, player3])
    ai_.connect()

    th_ = Thread(target=ai_.start_game)
    th_.start()
    graphics = Graphics()
    graphics.render()


if __name__ == "__main__":
    main()
