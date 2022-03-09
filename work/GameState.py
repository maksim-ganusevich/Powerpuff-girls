from work import Singleton


class Info(metaclass=Singleton):
    def __init__(self):
        """map"""
        self.size = 0
        self.name = ''
        self.spawn_points = []
        self.base = []
        self.catapult = []
        self.hard_repair = []
        self.light_repair = []
        self.obstacle = []
        """game state"""
        self.num_players = 3
        self.num_turns = 45
        self.current_turn = 0
        self.players = []
        self.current_player_idx = 0
        self.finished = False
        self.vehicles = dict()
        self.attack_matrix = 0
        self.winner = None
        self.win_points = dict()
        self.catapult_usage = []

    def set_map(self, map_response: dict):
        self.size = map_response["size"]
        self.name = map_response["name"]
        self.spawn_points = map_response["spawn_points"]
        self.base = map_response["content"]["base"]
        self.catapult = map_response["content"]["catapult"]
        self.hard_repair = map_response["content"]["hard_repair"]
        self.light_repair = map_response["content"]["light_repair"]
        self.obstacle = map_response["content"]["obstacle"]

    def set_game_state(self, gs_response):
        self.num_players = gs_response["num_players"]
        self.num_turns = gs_response["num_turns"]
        self.current_turn = gs_response["current_turn"]
        self.players = gs_response["players"]
        self.current_player_idx = gs_response["current_player_idx"]
        self.finished = gs_response["finished"]
        self.vehicles = gs_response["vehicles"]
        self.attack_matrix = gs_response["attack_matrix"]
        self.winner = gs_response["winner"]
        self.win_points = gs_response["win_points"]
        self.catapult_usage = gs_response["catapult_usage"]
