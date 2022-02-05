from .Tank import Tank
from work.Hexagon import Hex


class AtSPG(Tank):
    def __init__(self, id, hp, position):
        super(AtSPG, self).__init__(id, hp, 1, 1, 2, position)

    def get_firing_range(self):
        return self.position.get_hexes_of_axes(3)
