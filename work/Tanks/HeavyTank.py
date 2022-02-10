from .Tank import Tank
from work.Map import Map


class HeavyTank(Tank):
    def __init__(self, id, hp, position, owner):
        super(HeavyTank, self).__init__(id, hp, 1, 1, 3, position, owner)

    def get_firing_range(self):
        return Map.get_instance().get_hexes_in_range(self.position, 2)
