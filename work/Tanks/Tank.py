from abc import ABC, abstractmethod
from work.Hexagon import Hex


class Tank(ABC):
    def __init__(self, id: int, hp: int, sp: int, damage: int, destroy_points: int, position: dict, owner: int):
        self.id = id
        self.hp = hp
        self.sp = sp
        self.damage = damage
        self.destroy_points = destroy_points
        self.position = Hex(position["x"], position["y"], position["z"])
        self.owner = owner

    def move(self, target: Hex) -> Hex:
        N = Hex.distance(self.position, target)
        if N <= self.sp:
            self.position = target
            return target
        final_hex = Hex.hex_lerp(self.position, target, 1.0 / N * self.sp).hex_round()
        self.position = final_hex
        return final_hex

    @abstractmethod
    def get_firing_range(self):
        pass

    def in_firing_range(self, firing_range: "dict[Hex]") -> bool:
        for item in firing_range:
            if self.position.x == item.x and self.position.y == item.y:
                return True
        return False
