from typing import List
from work import Map
from work.Hexagon import Hex
from . import Tank


class AtSPG(Tank):
    def __init__(self, idx, hp, position, spawn_pos, owner):
        super(AtSPG, self).__init__(idx, hp, 1, 1, 2, position, spawn_pos, owner)

    def get_shoot_pos(self, target: Hex) -> Hex:
        # for AtSPG: Target hex for direction indication must be adjacent to the vehicle
        direction = (target - self.position).normalize()
        return self.position + direction

    def get_firing_range(self) -> List[Hex]:
        return Map.get_hexes_of_axes(self.position, 3)
