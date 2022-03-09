from typing import List
from work.Hexagon import Hex
from work import Map
from .Tank import Tank


class LightTank(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner):
        super(LightTank, self).__init__(id, hp, 3, 1, 1, position, spawn_pos, owner)

    def get_firing_range(self) -> List[Hex]:
        return Map.get_hexes_of_circle(self.position, 2)

