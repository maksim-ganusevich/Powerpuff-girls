from typing import List
from .Tank import Tank
from work.Hexagon import Hex
from work.Map import Map


class HeavyTank(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner, capture_points, shoot_range_bonus):
        super(HeavyTank, self).__init__(id, hp, 1, 1, 3, 1, 2,
                                        position, spawn_pos, owner, capture_points, shoot_range_bonus)

    def get_firing_range(self) -> List[Hex]:
        return Map().get_hexes_in_range(self.position, self.shoot_range_max + self.shoot_range_bonus)
