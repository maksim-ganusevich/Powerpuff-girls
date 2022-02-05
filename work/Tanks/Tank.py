from abc import ABC, abstractmethod
from work.Hexagon import Hex


class Tank(ABC):
    def __init__(self, id, hp, sp, damage, destroy_points, position):
        self.id = id
        self.hp = hp
        self.sp = sp
        self.damage = damage
        self.destroy_points = destroy_points
        self.position = Hex(position["x"], position["y"], position["z"])

    def move(self, target) -> Hex:
        N = Hex.distance(self.position, target)
        if N <= self.sp:
            return target
        return Hex.hex_lerp(self.position, target, 1.0 / N * self.sp).hex_round()

    @abstractmethod
    def get_firing_range(self):
        pass

    def in_firing_range(self, firing_range):
        for item in firing_range:
            if self.x == item.x and self.y == item.y:
                return True
        return False
