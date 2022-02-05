from .Tank import Tank


class HeavyTank(Tank):
    def __init__(self, id, hp, position):
        super(HeavyTank, self).__init__(id, hp, 1, 1, 3, position)

    def get_firing_range(self):
        return self.position.get_hexes_in_range(2)
