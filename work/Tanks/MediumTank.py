from typing import List
from work.Hexagon import Hex
from work.Map import Map
from . import Tank


class MediumTank(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner, capture_points, shoot_range_bonus):
        super(MediumTank, self).__init__(id, hp, 2, 1, 2, 2, 2,
                                         position, spawn_pos, owner, capture_points, shoot_range_bonus)

    def get_firing_range(self) -> List[Hex]:
        return Map().get_hexes_of_circle(self.position, self.shoot_range_max) + \
               Map().get_hexes_of_circle(self.position, self.shoot_range_max + self.shoot_range_bonus)
