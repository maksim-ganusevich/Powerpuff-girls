from work import Singleton


class GameState(metaclass=Singleton):
    def __init__(self):
        self.num_players = 1
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
        self.max_catapult_usage = 3
        self.attack_matrix_corrected = False

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
        self.attack_matrix_corrected = False
