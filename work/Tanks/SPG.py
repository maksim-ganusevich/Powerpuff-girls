from .Tank import Tank
from work.Hexagon import Hex


class SPG(Tank):
    def __init__(self, id, hp, position, owner):
        super(SPG, self).__init__(id, hp, 1, 1, 1, position, owner)

    def get_firing_range(self):
        return self.position.get_hexes_of_circle(3)
