from .Tank import Tank


class MediumTank(Tank):
    def __init__(self, id, hp, position, owner):
        super(MediumTank, self).__init__(id, hp, 2, 1, 2, position, owner)

    def get_firing_range(self):
        return self.position.get_hexes_of_circle(2)
