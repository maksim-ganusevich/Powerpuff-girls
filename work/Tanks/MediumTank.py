from .Tank import Tank, List, Hex
from work import Map


class MediumTank(Tank):
    def __init__(self, id, hp, position, owner):
        super(MediumTank, self).__init__(id, hp, 2, 1, 2, position, owner)

    def get_firing_range(self) -> List[Hex]:
        return Map.get_hexes_of_circle(self.position, 2)
