from abc import ABC, abstractmethod
from typing import List
from work.GameState import GameState
from work.Hexagon import Hex


class Tank(ABC):
    def __init__(self, id: int, hp: int, sp: int, damage: int, destroy_points: int, shoot_range_min: int,
                 shoot_range_max: int, position: dict, spawn_position: dict, owner: int, capture_points: int,
                 shoot_range_bonus: int):
        self.id = id
        self.hp = hp
        self.sp = sp
        self.damage = damage
        self.destroy_points = destroy_points
        self.position = Hex(position["x"], position["y"], position["z"])
        self.spawn_position = Hex(spawn_position["x"], spawn_position["y"], spawn_position["z"])
        self.owner = owner
        self.capture_points = capture_points
        self.shoot_range_min = shoot_range_min
        self.shoot_range_max = shoot_range_max
        self.shoot_range_bonus = shoot_range_bonus

    def move(self, target: Hex) -> bool:
        if target != self.position:
            self.position = target
            return True
        return False

    @staticmethod
    def shoot(target) -> None:
        target.take_damage()

    @staticmethod
    def get_shoot_pos(target: Hex) -> Hex:
        return target

    def take_damage(self) -> None:
        self.hp -= 1
        if self.hp <= 0:
            self.position = self.spawn_position
            self.hp = self.destroy_points
            GameState().vehicles[str(self.id)]["position"] = self.position.convert_to_dict()

    def get_range_min(self) -> int:
        return self.shoot_range_min

    def get_range_max(self) -> int:
        return self.shoot_range_max + self.shoot_range_bonus

    @abstractmethod
    def get_firing_range(self) -> List[Hex]:
        pass
