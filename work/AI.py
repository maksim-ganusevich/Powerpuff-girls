import logging
from time import sleep
from typing import List, Dict, Tuple
from work import Singleton
from work import Player
from work.GameState import GameState
from work.Tanks import *
from work.UtilityAI import Brain
from work.UtilityAI import Context

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%H:%M:%S')


class AI(metaclass=Singleton):
    def __init__(self, players: List[Player]):
        self.players = players
        self.brain = Brain()

    def connect(self, game_name, num_players, num_turns) -> None:
        for pl in self.players:
            pl.connect(game_name, num_players, num_turns)
        self.players[0].get_map()  # initializes Map singleton
        self.brain.init_reasoners()

    @staticmethod
    def construct_tank(tank_id: int, tank_data: Dict) -> Tuple[Tank, int]:
        # tanks move order: SPG, LT, HТ, MТ, AtSPG
        tank_types = {
            "spg": (SPG, 0),
            "light_tank": (LightTank, 1),
            "heavy_tank": (HeavyTank, 2),
            "medium_tank": (MediumTank, 3),
            "at_spg": (AtSPG, 4)
        }
        t_type, t_move_order = tank_types[tank_data["vehicle_type"]]
        return t_type(tank_id, tank_data["health"], tank_data["position"],
                      tank_data["spawn_position"], tank_data["player_id"],
                      tank_data["capture_points"], tank_data["shoot_range_bonus"]), t_move_order

    def get_tank_lists(self, player: Player) -> Tuple[List[Tuple[int, Tank]], List[Tank]]:
        player_tanks = []
        enemy_tanks = []

        for tank_id, tank_data in GameState().vehicles.items():
            tank, tank_move_order = self.construct_tank(tank_id, tank_data)
            if tank_data["player_id"] == player.id:
                player_tanks.append((tank_move_order, tank))
            else:
                enemy_tanks.append(tank)
        return player_tanks, enemy_tanks

    def make_action(self, player: Player) -> None:
        player_tanks, enemy_tanks = self.get_tank_lists(player)
        player.tanks = sorted(player_tanks, key=lambda t: t[0])  # sort based on move order
        context = Context(player, 0, [t[1] for t in player.tanks], enemy_tanks)
        self.brain.think(context)
        self.brain.act(context)

    def send_turn(self) -> None:
        for player in self.players:
            player.turn(wait_r=False)
        for player in self.players:
            player.turn(send_r=False)

    def send_solo_turn(self):
        self.send_turn()
        while GameState().current_player_idx != self.players[0].id:
            self.players[0].get_state()

    def finish_game(self) -> None:
        for player in self.players:
            player.logout()

    def multiplayer_game(self) -> None:
        pl = self.players[0]
        pl.get_state()  # initializes GameState singleton
        while True:
            if GameState().finished:
                self.finish_game()
                break

            if GameState().current_player_idx == pl.id:
                self.make_action(pl)
                self.send_turn()
                pl.get_state()  # updates GameState singleton
            else:
                self.send_turn()
                pl.get_state()
                sleep(0.1)

    def singleplayer_game(self) -> None:
        self.players[0].get_state()  # initializes GameState singleton
        while True:
            if GameState().finished:
                self.finish_game()
                break
            for pl in self.players:
                if GameState().current_player_idx == pl.id:
                    self.make_action(pl)
                    self.send_turn()
                    pl.get_state()  # updates GameState singleton
                    break

    def start_game(self) -> None:
        if len(self.players) == 1:
            self.multiplayer_game()
        else:
            self.singleplayer_game()