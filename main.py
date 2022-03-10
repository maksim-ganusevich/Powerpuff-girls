from threading import Thread
from work.AI import AI
from work.Player import Player
from work.Visualisation import Graphics


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
