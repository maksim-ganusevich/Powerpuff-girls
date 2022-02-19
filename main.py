from enum import Enum
from work.AI import AI
from work.Player import Player


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
    ai = AI([player1, player2, player3])
    ai.connect()
    ai.start_game()


if __name__ == "__main__":
    main()