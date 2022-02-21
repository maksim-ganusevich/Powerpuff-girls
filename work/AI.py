import random
import logging
from typing import List, Dict, Tuple
from work.Player import Player
from work.Tanks import *
from work import Map
from work.config import global_state, base
from work.UtilityAI.Brain import Brain
from work.UtilityAI.Context import Context

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%H:%M:%S')


class AI:
    def __init__(self, players: List[Player]):
        self.players = players

        self.game_name = ''
        for pl in self.players:
            self.game_name += pl.name
        self.game_name += random.choice("~`,./?!*+-^&@#$%_=")

        self.game_state = None
        self.brain = Brain()

    def connect(self) -> None:
        for pl in self.players:
            pl.connect(self.game_name, 3)
        map_dict = self.players[0].get_map()
        Map.init_values(map_dict['size'], map_dict['content']['base'],
                        map_dict['content']['obstacle'])
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
                      tank_data["spawn_position"], tank_data["player_id"]), t_move_order

    def get_tank_lists(self, player: Player) -> Tuple[List[Tuple[int, Tank]], List[Tank]]:
        player_tanks = []
        enemy_tanks = []
        Map.set_vehicles(self.game_state["vehicles"].values())

        for tank_id, tank_data in self.game_state["vehicles"].items():
            tank, tank_move_order = self.construct_tank(tank_id, tank_data)
            if tank_data["player_id"] == player.id:
                player_tanks.append((tank_move_order, tank))
            else:
                enemy_tanks.append(tank)
        return player_tanks, enemy_tanks

    def make_action(self, player: Player) -> None:
        player_tanks, enemy_tanks = self.get_tank_lists(player)
        player.tanks = sorted(player_tanks, key=lambda t: t[0])  # sort based on move order
        context = Context(player, 0, [t[1] for t in player.tanks], enemy_tanks, self.game_state["attack_matrix"])
        for i, (tank_move_order, tank) in enumerate(player.tanks):
            context.update_curr_tank_index(i)
            self.brain.act(context)

    def send_turn(self) -> None:
        for player in self.players:
            player.turn(wait_r=False)
        for player in self.players:
            player.turn(send_r=False)

    def start_game(self) -> None:
        self.game_state = self.players[0].get_state()

        while True:
            if self.game_state['finished']:
                self.finish_game()
                break

            for pl in self.players:

                if self.game_state["current_player_idx"] == pl.id:
                    self.make_action(pl)
                    self.send_turn()
                    self.game_state = pl.get_state()
                    global_state.update(self.game_state)
                    break

    def finish_game(self) -> None:
        for pl in self.players:
            pl.logout()
