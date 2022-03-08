from typing import List
from .Tank import Tank
from work.Hexagon import Hex
from work.Map import Map


class LightTank(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner):
        super(LightTank, self).__init__(id, hp, 3, 1, 1, position, spawn_pos, owner)

    def get_firing_range(self) -> List[Hex]:
        return Map().get_hexes_of_circle(self.position, 2)

