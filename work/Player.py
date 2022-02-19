from work.ServerHandler import ServerHandler
from typing import Dict


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
        return self.server.send_request(3)

    def get_state(self) -> Dict:
        return self.server.send_request(4)

    def set_id(self, id: int) -> None:
        self.id = id

    def turn(self, send_r=True, wait_r=True) -> None:
        self.server.send_request(6, send_req=send_r, wait_res=wait_r)

    def move(self, move_to: Dict) -> None:
        self.server.send_request(101, move_to)

    def shoot(self, id: int, shoot_to: dict) -> None:
        self.server.send_shoot(id, shoot_to.__dict__)

    def logout(self) -> None:
        self.server.send_request(2)
