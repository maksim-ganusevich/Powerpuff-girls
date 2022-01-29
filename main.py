from enum import Enum
from work import ServerHandler
from work.Hexagon import Hex


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


def send_login(game_server, name, password="", game=None, num_turns=None, num_players=1, is_observer=False):

    """Возвращает id текущего игрока"""

    data = {"name": name, "password": password, "game": game, "num_turns": num_turns, "num_players": num_players,
            "is_observer": is_observer}

    login = game_server.send_request(Action.LOGIN, data)

    print("-----LOGIN1: " + str(login))
    print()

    player_id = login["idx"]
    return player_id


def pick_base_hex(base_hexes, vehicles):

    """Возвращает Hex базы если там нет ни одного танка"""

    for b in base_hexes:
        if hex_is_free(b, vehicles):
            return b


def hex_is_free(hex, vehicles):
    for v in vehicles.values():
        if v["position"] == hex:
            return False
    return True


def print_all_positions(game_state):
    for k, v in game_state["vehicles"].items():
        vehicle_pos = v["position"]
        print(k + ": " + str(vehicle_pos))

def get_firing_range(center_hex, firing_radius):

    """Возвращает список шестиугольников в радиусе обстрела"""

    hexes_in_firing_range = []
    for q in range(-firing_radius, firing_radius + 1):
        for r in range(max(-firing_radius, -q - firing_radius), min(+firing_radius, -q + firing_radius) + 1):
            s = - q - r
            if q != 0 or r != 0 or s != 0:
                hexes_in_firing_range.append(center_hex + Hex(q, r, s))
    return hexes_in_firing_range

def shoot(game_server, player_id, vehicle_hex_pos, game_state):
    firing_range = get_firing_range(vehicle_hex_pos, 2)
    for k1, v1 in game_state["vehicles"].items():
        if v1["player_id"] != player_id:
            vehicle_pos_enemy = v1["position"]
            vehicle_hex_pos_enemy = Hex(vehicle_pos_enemy["x"], vehicle_pos_enemy["y"], vehicle_pos_enemy["z"])
            if vehicle_hex_pos_enemy in firing_range:
                shoot_action = {"vehicle_id": player_id, "target": vehicle_hex_pos_enemy.__dict__}
                game_server.send_request(Action.SHOOT , shoot_action)
                return True

def move_to(game_server, player_id, base, game_state, move):
    pass

def game_action(game_server, player_id, base, game_state, move):
    for k, v in game_state["vehicles"].items():  # ход каждым танком
        if v["player_id"] == player_id:  # проверка принадлежнсти танка
            vehicle_pos = v["position"]
            vehicle_hex_pos = Hex(vehicle_pos["x"], vehicle_pos["y"], vehicle_pos["z"])

            if not shoot(game_server, player_id, vehicle_hex_pos, game_state): #Проверка возможности выстрелить и стрельба
                base_pos = pick_base_hex(base, game_state["vehicles"])  # выбор hex базы для захвата
                if not base_pos:  # вся база занята
                    break
                base_hex_pos = Hex(base_pos["x"], base_pos["y"], base_pos["z"])

                # ход в сторону выбранного hex базы с дефолтной скоростью 2 и получение промежуточного hex
                final_hex = vehicle_hex_pos.move_to(base_hex_pos, 2)
                if hex_is_free(final_hex.__dict__, game_state["vehicles"]):
                    game_state["vehicles"][k]["position"] = final_hex.__dict__
                    move["vehicle_id"] = k
                    move["target"] = final_hex.__dict__
                    game_server.send_request(Action.MOVE, move)
                else:
                    print("---------------HEX IS OCCUPIED!!!----------------")

    game_server.send_request(Action.TURN)


def main():
    game_server = ServerHandler.ServerHandler()
    player_id = send_login(game_server, name="Carlos")

    game_map = game_server.send_request(Action.MAP)
    base = game_map['content']['base']

    game_state = game_server.send_request(Action.GAME_STATE)
    move = {"vehicle_id": 1, "target": {"x": 0, "y": 0, "z": 0}}  # формат хода из доки

    while not game_state['winner']:
        game_action(game_server, player_id, base, game_state, move)
        game_state = game_server.send_request(Action.GAME_STATE)

    print_all_positions(game_state)


if __name__ == "__main__":
    main()
