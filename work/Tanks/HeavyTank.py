from .Tank import Tank, List, Hex
from work import Map


class HeavyTank(Tank):
    def __init__(self, id, hp, position, spawn_pos, owner):
        super(HeavyTank, self).__init__(id, hp, 1, 1, 3, position, spawn_pos, owner)

    def get_firing_range(self) -> List[Hex]:
        return Map.get_hexes_in_range(self.position, 2)
