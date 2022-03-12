from typing import List
from .Tank import Tank
from work.Map import Map
from work.Hexagon import Hex


class AtSPG(Tank):
    def __init__(self, idx, hp, position, spawn_pos, owner, capture_points, shoot_range_bonus):
        super(AtSPG, self).__init__(idx, hp, 1, 1, 2, 1, 3,
                                    position, spawn_pos, owner, capture_points, shoot_range_bonus)

    def get_shoot_pos(self, target: Hex) -> Hex:
        # for AtSPG: Target hex for direction indication must be adjacent to the vehicle
        direction = (target - self.position).normalize()
        return self.position + direction

    def get_firing_range(self) -> List[Hex]:
        return Map().get_hexes_of_axes(self.position, self.shoot_range_max + self.shoot_range_bonus)
