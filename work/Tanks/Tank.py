from abc import ABC, abstractmethod
from work.Hexagon import Hex
from work import Astar


class Tank(ABC):
    def __init__(self, id: int, hp: int, sp: int, damage: int, destroy_points: int, position: dict, owner: int):
        self.id = id
        self.hp = hp
        self.sp = sp
        self.damage = damage
        self.destroy_points = destroy_points
        self.position = Hex(position["x"], position["y"], position["z"])
        self.owner = owner

    def move(self, target: Hex) -> bool:
        final_hex = Astar.move_to(self.position, target, self.sp)
        if final_hex != self.position:
            self.position = final_hex
            return True
        return False

    @abstractmethod
    def get_firing_range(self):
        pass

    def in_firing_range(self, firing_range: "dict[Hex]") -> bool:
        for item in firing_range:
            if self.position.x == item.x and self.position.y == item.y:
                return True
        return False
