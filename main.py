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


def pick_base_hex(base, vehicles):
    for b in base:
        for v in vehicles.values():
            if v["position"] == b:  # hex базы занят
                break
        else:
            return b


def hex_is_free(hex, vehicles):
    for v in vehicles.values():
        if v["position"] == hex:
            return False
    return True


def main():
    game_server = ServerHandler.ServerHandler()

    data = {"name": "Carlos"}
    login = game_server.send_request(Action.LOGIN, data)
    print("-----LOGIN: " + str(login))
    print()

    game_map = game_server.send_request(Action.MAP)
    base = game_map['content']['base']

    game_state = game_server.send_request(Action.GAME_STATE)
    move = {"vehicle_id": 1, "target": {"x": 0, "y": 0, "z": 0}}  # формат хода из доки

    while not game_state['winner']:
        for k, v in game_state["vehicles"].items():  # ход каждым танком
            vehicle_pos = v["position"]
            vehicle_hex_pos = Hex(vehicle_pos["x"], vehicle_pos["y"], vehicle_pos["z"])

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
        game_state = game_server.send_request(Action.GAME_STATE)

    print()
    print()
    for k, v in game_state["vehicles"].items():
        vehicle_pos = v["position"]
        print(k + ": " + str(vehicle_pos))



if __name__ == "__main__":
    main()
