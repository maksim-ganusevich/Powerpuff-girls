from work.ServerHandler import ServerHandler
from work.Hexagon import Hex


class Player:
    def __init__(self, name: str):
        self.name = name
        self.password = ""
        self.server = ServerHandler()
        self.tanks = []
        self.id = None

    def connect(self, game: str, num_players=1):
        self.id = self.server.send_login(name=self.name, game=game, num_players=num_players)

    def get_map(self):
        return self.server.send_request(3)

    def get_state(self):
        return self.server.send_request(4)

    def set_id(self, id: int):
        self.id = id

    def turn(self, send_r=True, wait_r=True):
        self.server.send_request(6, send_req=send_r, wait_res=wait_r)

    def move(self, id: int, move: Hex):
        move_to = {"vehicle_id": id, "target": move.to_dict()}
        self.server.send_request(101, move_to)

    def shoot(self, id: int, shoot_to: Hex):
        self.server.send_shoot(id, shoot_to.to_dict())

    def logout(self):
        self.server.send_request(2)
