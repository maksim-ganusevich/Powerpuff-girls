import random
import logging
from work.Player import Player
from work.Hexagon import Hex
from work.Tanks import *
from work import Map

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%H:%M:%S')


class AI:
    def __init__(self, players: "list[Player]"):
        self.players = players
        random.shuffle(self.players)
        self.game_name = self.players[0].name + self.players[1].name + self.players[2].name
        self.game_state = None

    def connect(self) -> None:
        self.players[0].connect(self.game_name, 3)
        self.players[1].connect(self.game_name)
        self.players[2].connect(self.game_name)
        map_dict = self.players[0].get_map()
        Map.init_values(map_dict['size'], map_dict['content']['base'],
                        map_dict['content']['obstacle'])

    # checking the possibility of firing according to the rule of neutrality
    def check_neutrality(self, player: Player, enemy_tank: Tank) -> bool:
        attack_matrix = self.game_state["attack_matrix"]
        id_all_players = list(attack_matrix.keys())
        id_all_players.remove(str(player.id))
        id_all_players.remove(str(enemy_tank.owner))
        id_third_player = id_all_players[0]
        if player.id in attack_matrix[str(enemy_tank.owner)] or enemy_tank.owner not in attack_matrix[id_third_player]:
            return True
        return False

    def shoot(self, player: Player, tank: Tank, enemy_tanks: "list[Tank]") -> bool:
        firing_range = tank.get_firing_range()
        for enemy in enemy_tanks:
            if enemy.position in firing_range and self.check_neutrality(player, enemy):
                player.shoot(tank.id, enemy.position)
                return True
        return False

    @staticmethod
    def pick_base_hex() -> Hex:
        for b in Map.base:
            if Map.hex_is_free(b):
                return b

    def move(self, player: Player, tank: Tank) -> bool:
        base_pos = self.pick_base_hex()
        if not base_pos:  # base is occupied
            return False

        prev_pos = tank.position
        if tank.move(base_pos):
            Map.update_vehicle(prev_pos, tank.position)
            move_to = {"vehicle_id": tank.id, "target": tank.position.to_dict()}
            player.move(move_to)
        else:
            logging.warning(msg="Hexes in the way are occupied!")
            return False
        return True

    @staticmethod
    def construct_tank(tank_id: int, tank_data: dict) -> (Tank, int):
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

    def get_tank_lists(self, player: Player) -> (([], int), []):
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

        for tank_move_order, tank in player.tanks:
            if not self.shoot(player, tank, enemy_tanks):
                self.move(player, tank)

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
                    break

    def finish_game(self) -> None:
        for pl in self.players:
            pl.logout()
