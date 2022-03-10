from typing import List
from work.Hexagon import Hex
from work.Map import Map
from . import Tank


class MediumTank(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner):
        super(MediumTank, self).__init__(id, hp, 2, 1, 2, position, spawn_pos, owner)

    def get_firing_range(self) -> List[Hex]:
        return Map().get_hexes_of_circle(self.position, 2)
