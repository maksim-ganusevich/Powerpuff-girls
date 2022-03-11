from typing import Dict
from work.ServerHandler import ServerHandler
from work.Hexagon import Hex
from work.GameState import GameState
from work.Map import Map
from work.ServerCommands import Action


class Player:
    def __init__(self, name: str, password="", is_observer=False):
        self.name = name
        self.password = password
        self.is_observer = is_observer
        self.server = ServerHandler()
        self.tanks = []
        self.id = None

    def connect(self, game: str, num_players=1, num_turns = None) -> None:
        self.id = self.server.send_login(name=self.name, password=self.password,
                                         game=game, num_turns=num_turns,
                                         num_players=num_players, is_observer=self.is_observer)

    def get_map(self) -> Dict:
        map_dict = self.server.send_request(Action.MAP)
        Map().set_map(map_dict)
        return map_dict

    def get_state(self) -> Dict:
        game_state = self.server.send_request(Action.GAME_STATE)
        GameState().set_game_state(game_state)
        Map().set_vehicles(GameState().vehicles.values())
        return game_state

    def set_id(self, id: int) -> None:
        self.id = id

    def turn(self, send_r=True, wait_r=True) -> None:
        self.server.send_request(Action.TURN, send_req=send_r, wait_res=wait_r)

    def move(self, id: int, move: Hex) -> None:
        move_to = {"vehicle_id": id, "target": move.to_dict()}
        self.server.send_request(Action.MOVE, move_to)

    def shoot(self, id: int, shoot_to: Hex) -> None:
        self.server.send_shoot(id, shoot_to.to_dict())

    def logout(self) -> None:
        self.server.send_request(Action.LOGOUT)
