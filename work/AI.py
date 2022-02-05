import random
from time import sleep

from work.Hexagon import Hex
from work.Tanks import *


class AI:
    def __init__(self, players):
        self.players = players
        random.shuffle(self.players)
        self.game_name = self.players[0].name + self.players[1].name + self.players[2].name
        self.game_map = None
        self.base = None
        self.game_state = None

    def connect(self):
        self.players[0].connect(self.game_name, 3)
        self.players[1].connect(self.game_name)
        self.players[2].connect(self.game_name)
        self.game_map = self.players[0].get_map()
        self.base = self.game_map['content']['base']

    def check_neutrality(self, player, enemy_tank):
        attack_matrix = self.game_state["attack_matrix"]
        id_all_players = list(attack_matrix.keys())
        id_all_players.remove(str(player.id))
        id_all_players.remove(str(enemy_tank.owner))
        id_third_player = id_all_players[0]
        if player.id in attack_matrix[str(enemy_tank.owner)] or enemy_tank.owner not in attack_matrix[id_third_player]:
            return True
        return False

    def shoot(self, player, tank, enemy_tanks):
        firing_range = tank.get_firing_range()
        for enemy in enemy_tanks:
            if enemy.position in firing_range and self.check_neutrality(player, enemy):
                player.shoot(tank.id, enemy.position)
                return True
        return False

    def hex_is_free(self, hex):
        for v in self.game_state["vehicles"].values():
            if v["position"] == hex:
                return False
        return True

    def pick_base_hex(self):
        # Возвращает Hex базы если там нет ни одного танка
        for b in self.base:
            if self.hex_is_free(b):
                return b

    def move(self, player, tank):
        base_pos = self.pick_base_hex()
        if not base_pos:  # вся база занята
            return False

        base_hex_pos = Hex(base_pos["x"], base_pos["y"], base_pos["z"])
        final_hex = tank.move(base_hex_pos)

        if self.hex_is_free(final_hex.__dict__):
            self.game_state["vehicles"][tank.id]["position"] = final_hex.__dict__
            move_to = {"vehicle_id": tank.id, "target": final_hex.__dict__}
            player.move(move_to)
        else:
            print("---------------HEX IS OCCUPIED!!!----------------")
        return True

    @staticmethod
    def construct_tank(tank_id, tank_data) -> (Tank, int):
        # tanks move order: SPG, LT, HТ, MТ, AtSPG
        tank_types = {
            "spg": (SPG, 0),
            "light_tank": (LightTank, 1),
            "heavy_tank": (HeavyTank, 2),
            "medium_tank": (MediumTank, 3),
            "at_spg": (AtSPG, 4)
        }
        t_type, t_move_order = tank_types[tank_data["vehicle_type"]]
        return t_type(tank_id, tank_data["health"], tank_data["position"], tank_data["player_id"]), t_move_order

    def get_tank_lists(self, player) -> (([], int), []):
        player_tanks = []
        enemy_tanks = []
        for tank_id, tank_data in self.game_state["vehicles"].items():
            tank, tank_move_order = self.construct_tank(tank_id, tank_data)
            if tank_data["player_id"] == player.id:
                player_tanks.append((tank_move_order, tank))
            else:
                enemy_tanks.append(tank)
        return player_tanks, enemy_tanks

    def game_action(self, player):
        player_tanks, enemy_tanks = self.get_tank_lists(player)
        player.tanks = sorted(player_tanks, key=lambda t: t[0])  # sort based on move order

        for tank_move_order, tank in player.tanks:
            if not self.shoot(player, tank, enemy_tanks):
                self.move(player, tank)

    def send_turn(self):
        for player in self.players:
            player.turn(wait_r=False)
        for player in self.players:
            print()
            player.turn(send_r=False)

    def start_game(self):
        self.game_state = self.players[0].get_state()

        while True:
            if self.game_state['winner']:
                self.finish_game()
                break

            for pl in self.players:
                if self.game_state["current_player_idx"] == pl.id:
                    self.game_action(pl)
                    self.send_turn()
                    self.game_state = pl.get_state()
                    break

    def finish_game(self):
        for pl in self.players:
            pl.logout()
