from threading import Thread
from work.AI import AI
from work.Player import Player
from work.Visualisation import Graphics


def main():
    player1 = Player(name="Carlos")
    player2 = Player(name="Semen")
    player3 = Player(name="Woody")
    ai = AI([player1, player2, player3])
    ai.connect()

    th = Thread(target=ai.start_game)
    th.start()
    graphics = Graphics()
    graphics.render()


if __name__ == "__main__":
    main()
