from .Tank import Tank


class LightTank(Tank):
    def __init__(self, id, hp, position, owner):
        super(LightTank, self).__init__(id, hp, 3, 1, 1, position, owner)

    def get_firing_range(self):
        return self.position.get_hexes_of_circle(2)

