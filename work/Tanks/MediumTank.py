from .Tank import Tank
from work.Map import Map


class MediumTank(Tank):
    def __init__(self, id, hp, position, owner):
        super(MediumTank, self).__init__(id, hp, 2, 1, 2, position, owner)

    def get_firing_range(self):
        return Map.get_instance().get_hexes_of_circle(self.position, 2)
