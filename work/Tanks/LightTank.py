from .Tank import Tank
from work import Map


class LightTank(Tank):
    def __init__(self, id, hp, position, owner):
        super(LightTank, self).__init__(id, hp, 3, 1, 1, position, owner)

    def get_firing_range(self):
        return Map.get_hexes_of_circle(self.position, 2)

