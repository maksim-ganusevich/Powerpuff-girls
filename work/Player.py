from work.ServerHandler import ServerHandler


class Player:
    def __init__(self, name):
        self.name = name
        self.password = ""
        self.server = ServerHandler()
        self.tanks = []
        self.id = None

    def connect(self, game, num_players=1):
        self.id = self.server.send_login(name=self.name, game=game, num_players=num_players)

    def get_map(self):
        return self.server.send_request(3)

    def get_state(self):
        return self.server.send_request(4)

    def set_id(self, id):
        self.id = id

    def turn(self):
        self.server.send_request(6)

    def move(self, move_to):
        self.server.send_request(101, move_to)

    def logout(self):
        self.server.send_request(2)
