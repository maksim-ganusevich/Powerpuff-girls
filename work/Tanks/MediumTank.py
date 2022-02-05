from .Tank import Tank
from work.Hexagon import Hex


class MediumTank(Tank):
    def __init__(self, id, hp, position):
        super(MediumTank, self).__init__(id, hp, 2, 1, 2, position)

    def get_firing_range(self):
        return self.position.get_hexes_of_circle(2)
