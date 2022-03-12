from typing import List
from work.Hexagon import Hex
from work.Map import Map
from . import Tank


class SPG(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner, capture_points, shoot_range_bonus):
        super(SPG, self).__init__(id, hp, 1, 1, 1, 3, 3, position, spawn_pos, owner, capture_points, shoot_range_bonus)

    def get_firing_range(self) -> List[Hex]:
        return Map().get_hexes_of_circle(self.position, self.shoot_range_max) + \
               Map().get_hexes_of_circle(self.position, self.shoot_range_max + self.shoot_range_bonus)
