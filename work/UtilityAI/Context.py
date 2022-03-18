from typing import List
from work.Tanks import Tank
from work import Player


class Context:

    def __init__(self, player: Player, curr_tank_index: int,
                 player_tanks: List[Tank], enemy_tanks: List[Tank]):
        super(Context, self).__init__()
        self.player = player
        self.curr_tank_index = curr_tank_index
        self.target_index = 0
        self.desired_hex = None
        self.path_reasoner = None
        self.player_tanks = player_tanks
        self.enemy_tanks = enemy_tanks

    def update_curr_tank_index(self, index: int) -> None:
        self.curr_tank_index = index

    def get_target(self) -> Tank:
        return self.enemy_tanks[self.target_index]

    def get_curr_tank(self) -> Tank:
        return self.player_tanks[self.curr_tank_index]
