from abc import ABC, abstractmethod
from work.Hexagon import Hex
from work import Astar
from typing import List


class Tank(ABC):
    def __init__(self, id: int, hp: int, sp: int, damage: int, destroy_points: int, position: dict,
                 spawn_position: dict, owner: int):
        self.id = id
        self.hp = hp
        self.sp = sp
        self.damage = damage
        self.destroy_points = destroy_points
        self.position = Hex(position["x"], position["y"], position["z"])
        self.spawn_position = Hex(spawn_position["x"], spawn_position["y"], spawn_position["z"])
        self.owner = owner

    def move(self, target: Hex) -> bool:
        final_hex = Astar.move_to(self.position, target, self.sp)
        if final_hex != self.position:
            self.position = final_hex
            return True
        return False

    def shoot(self, target) -> None:
        target.take_damage()

    def get_shoot_pos(self, target: Hex):
        return target

    def take_damage(self) -> None:
        self.hp -= 1
        if self.hp <= 0:
            self.position = self.spawn_position
            self.hp = self.destroy_points

    @abstractmethod
    def get_firing_range(self) -> List[Hex]:
        pass

    def in_firing_range(self, firing_range: "dict[Hex]") -> bool:
        for item in firing_range:
            if self.position.x == item.x and self.position.y == item.y:
                return True
        return False
