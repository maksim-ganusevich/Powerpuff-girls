from typing import Dict
from work.ServerHandler import ServerHandler
from work.Hexagon import Hex
from work.GameState import GameState
from work.Map import Map


class Player:
    def __init__(self, name: str):
        self.name = name
        self.password = ""
        self.server = ServerHandler()
        self.tanks = []
        self.id = None

    def connect(self, game: str, num_players=1) -> None:
        self.id = self.server.send_login(name=self.name, game=game, num_players=num_players)

    def get_map(self) -> Dict:
        map_dict = self.server.send_request(3)
        Map().set_map(map_dict)
        return map_dict

    def get_state(self) -> Dict:
        game_state = self.server.send_request(4)
        GameState().set_game_state(game_state)
        Map().set_vehicles(GameState().vehicles.values())
        return game_state

    def set_id(self, id: int) -> None:
        self.id = id

    def turn(self, send_r=True, wait_r=True) -> None:
        self.server.send_request(6, send_req=send_r, wait_res=wait_r)

    def move(self, id: int, move: Hex) -> None:
        move_to = {"vehicle_id": id, "target": move.to_dict()}
        self.server.send_request(101, move_to)

    def shoot(self, id: int, shoot_to: Hex) -> None:
        self.server.send_shoot(id, shoot_to.to_dict())

    def logout(self) -> None:
        self.server.send_request(2)
