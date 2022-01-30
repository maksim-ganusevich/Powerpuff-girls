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

    return login["idx"]


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



def shoot(game_server, player_id, tank_id, vehicle_hex_pos, game_state):
    """Стреляет если в радиусе обстрела есть танк,
    Возвращает False если танков нет"""
    firing_range = vehicle_hex_pos.get_firing_range(2) #Получаем гексы в которые можем стрелять
    for k, v in game_state["vehicles"].items():
        if v["player_id"] != player_id: #перебираем все танки противников
            vehicle_pos_enemy = v["position"]
            vehicle_hex_pos_enemy = Hex(vehicle_pos_enemy["x"], vehicle_pos_enemy["y"], vehicle_pos_enemy["z"])

            if vehicle_hex_pos_enemy.in_firing_range(firing_range): #проверяем можем ли стрельнуть в танк
                shoot_action = {"vehicle_id": tank_id, "target": vehicle_hex_pos_enemy.__dict__}
                game_server.send_request(Action.SHOOT, shoot_action)
                return True
    return False


def move_to(game_server, vehicle_hex_pos, tank_id, base, game_state):
    """Двигается в сторону базы если ничего не мешает,
    возвращает False если не удается сдвинуться"""
    base_pos = pick_base_hex(base, game_state["vehicles"])  # выбор hex базы для захвата
    if not base_pos:  # вся база занята
        return False
    base_hex_pos = Hex(base_pos["x"], base_pos["y"], base_pos["z"])

    # ход в сторону выбранного hex базы с дефолтной скоростью 2 и получение промежуточного hex
    final_hex = vehicle_hex_pos.move_to(base_hex_pos, 2)
    if hex_is_free(final_hex.__dict__, game_state["vehicles"]):
        game_state["vehicles"][tank_id]["position"] = final_hex.__dict__
        move_to = {"vehicle_id": tank_id, "target": final_hex.__dict__}
        game_server.send_request(Action.MOVE, move_to)
    else:
        print("---------------HEX IS OCCUPIED!!!----------------")
    return True


def game_action(game_server, player_id, base, game_state):
    for tank_id, tank_data in game_state["vehicles"].items():  # получение координат каждого танка
        if tank_data["player_id"] == player_id:  # проверка принадлежнсти танка чтобы управлять только своими
            vehicle_pos = tank_data["position"]
            vehicle_hex_pos = Hex(vehicle_pos["x"], vehicle_pos["y"], vehicle_pos["z"])

            if not shoot(game_server, player_id, tank_id, vehicle_hex_pos, game_state):  # Проверка возможности выстрелить и стрельба
                move_to(game_server, vehicle_hex_pos, tank_id, base, game_state)    #едем если не можем стрелять

    game_server.send_request(Action.TURN)


def main():
    game_server1 = ServerHandler.ServerHandler()
    game_server2 = ServerHandler.ServerHandler()
    player_id1 = send_login(game_server1, name="Carlos1", game="game1", num_players=2)
    player_id2 = send_login(game_server2, name="Carlos2", game="game1")

    game_map = game_server1.send_request(Action.MAP)
    base = game_map['content']['base']

    while True: #Игровой цикл пока не получим победителя от сервера
        game_state = game_server1.send_request(Action.GAME_STATE)
        if game_state['winner']:
            print_all_positions(game_state)
            game_server1.send_request(Action.LOGOUT)
            game_server2.send_request(Action.LOGOUT)
            break

        if game_state["current_player_idx"] == player_id1:
            game_action(game_server1, player_id1, base, game_state)
        elif game_state["current_player_idx"] == player_id2:
            game_action(game_server2, player_id2, base, game_state)





if __name__ == "__main__":
    main()