from .Tank import Tank
from work.Map import Map


class AtSPG(Tank):
    def __init__(self, id, hp, position, owner):
        super(AtSPG, self).__init__(id, hp, 1, 1, 2, position, owner)

    def get_firing_range(self):
        return Map.get_instance().get_hexes_of_axes(self.position, 3)
