from work import Player
from work.Hexagon import Hex
import random


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

    def shoot(self, player):
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

    def move_to(self, player, pos, tank):
        base_pos = self.pick_base_hex()
        if not base_pos:  # вся база занята
            return False

        base_hex_pos = Hex(base_pos["x"], base_pos["y"], base_pos["z"])
        final_hex = pos.move_to(base_hex_pos, 1)
        if self.hex_is_free(final_hex.__dict__):
            self.game_state["vehicles"][tank]["position"] = final_hex.__dict__
            move_to = {"vehicle_id": tank, "target": final_hex.__dict__}
            player.move(move_to)
        else:
            print("---------------HEX IS OCCUPIED!!!----------------")
        return True

    def game_action(self, player):
        for tank_id, tank_data in self.game_state["vehicles"].items():
            if tank_data["player_id"] == player.id:
                vehicle_pos = tank_data["position"]
                vehicle_hex_pos = Hex(vehicle_pos["x"], vehicle_pos["y"], vehicle_pos["z"])
                if not self.shoot(player):
                    self.move_to(player, vehicle_hex_pos, tank_id)

        player.turn()

    def start_game(self):
        self.game_state = self.players[0].get_state()

        while True:
            if self.game_state['winner']:
                self.finish_game()
                break

            for _ in range(len(self.players)):
                for pl in self.players:
                    if self.game_state["current_player_idx"] == pl.id:
                        self.game_action(pl)
                        self.game_state = pl.get_state()
                        break

    def finish_game(self):
        for pl in self.players:
            pl.logout()