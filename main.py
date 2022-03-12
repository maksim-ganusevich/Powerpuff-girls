from threading import Thread
import sys
import argparse
import random
from work.AI import AI
from work.Player import Player
from work.Visualisation import Graphics


def createParser():
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("-n", default=None, type=str, help="Your name")
    parser.add_argument("-p", default="", type=str, help="Your password")
    parser.add_argument("-g", default=None, type=str, help="Game name")
    parser.add_argument("-nt", default=None, type=int, help="Number of turns")
    parser.add_argument("-np", default=1, type=int, help="Number of players")
    parser.add_argument("-obs", default=False, type=bool, help="Are you observer?")
    return parser



def test_game():
    player1 = Player(name="Carlos")
    player2 = Player(name="Semen")
    player3 = Player(name="Woody")
    ai_ = AI([player1, player2, player3])
    ai_.connect(game_name="test_game" + random.choice("1234567890abc"), num_turns=None, num_players=3)
    th_ = Thread(target=ai_.start_game)
    th_.start()
    graphics = Graphics()
    graphics.render()


def scoring_game(player_name, password, game_name, num_turns, num_players, is_observer):
    player = Player(player_name, password, is_observer)
    ai_ = AI([player])
    ai_.connect(game_name=game_name, num_turns=num_turns, num_players=num_players)
    ai_.send_turn()
    th_ = Thread(target=ai_.start_game)
    th_.start()
    graphics = Graphics()
    graphics.render()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        test_game()
    else:
        parser = createParser()
        args = parser.parse_args()
        scoring_game(player_name=args.n, password=args.p,
                     game_name=args.g, num_players=args.np,
                     num_turns=args.nt, is_observer=args.obs)
