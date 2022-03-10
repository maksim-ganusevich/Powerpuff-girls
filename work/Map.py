from typing import List
from work.Hexagon import Hex
from work.Singleton import Singleton

DIRECTIONS = [
    Hex(+1, 0, -1), Hex(+1, -1, 0), Hex(0, -1, +1),
    Hex(-1, 0, +1), Hex(-1, +1, 0), Hex(0, +1, -1),
]


class Map(metaclass=Singleton):

    def __init__(self):
        self.size = 0
        self.name = ''
        self.spawn_points = []
        self.base = []
        self.catapult = []
        self.hard_repair = []
        self.light_repair = []
        self.obstacles = []
        self.vehicles = set()

    def set_map(self, map_response: dict):
        self.size = map_response["size"]
        self.name = map_response["name"]
        self.spawn_points = map_response["spawn_points"]
        self.base = map_response["content"]["base"]
        self.catapult = map_response["content"]["catapult"]
        self.hard_repair = map_response["content"]["hard_repair"]
        self.light_repair = map_response["content"]["light_repair"]
        self.base = Hex.dict_to_hex_list(map_response["content"]["base"])
        self.obstacles = Hex.dict_to_hex_list(map_response["content"]["obstacle"])

    def set_vehicles(self, vehicles_dict: dict) -> None:
        self.vehicles.clear()
        for v in vehicles_dict:
            self.vehicles.add(Hex(v["position"]["x"], v["position"]["y"], v["position"]["z"]))

    def update_vehicle(self, old_pos: Hex, new_pos: Hex) -> None:
        self.vehicles.remove(old_pos)
        self.vehicles.add(new_pos)

    def hex_is_free(self, h: Hex) -> bool:
        return h not in self.obstacles and h not in self.vehicles

    def in_map_boundaries(self, hex: Hex) -> bool:
        return max(abs(hex.x), abs(hex.y), abs(hex.z)) <= self.size

    def get_free_base_hex(self, ) -> Hex:
        for b in self.base:
            if self.hex_is_free(b):
                return b

    def get_free_neighbours(self, center: Hex) -> List[Hex]:
        results = []
        for d in DIRECTIONS:
            res = center + d
            if self.in_map_boundaries(res) and res not in self.obstacles:
                results.append(res)
        return results

    # all hexes in the area with self as center
    def get_hexes_in_range(self, center, n) -> List[Hex]:
        results = []
        for x in range(-n, n + 1):
            for y in range(max(-n, -x - n), min(n, -x + n) + 1):
                res = center + Hex(x, y, -x - y)
                if self.in_map_boundaries(res) and res not in self.obstacles:
                    results.append(res)
        return results

    # only hexes on the edge of the area
    def get_hexes_of_circle(self, center, r) -> List[Hex]:
        results = []
        x = -r
        for y in range(0, r):
            vector = Hex(x, y, -x - y)
            res = center + vector
            if self.in_map_boundaries(res) and res not in self.obstacles:
                results.append(res)
            for i in range(5):
                vector = Hex(-vector.y, -vector.z, -vector.x)  # rotate 60 degrees
                res = center + vector
                if self.in_map_boundaries(res) and res not in self.obstacles:
                    results.append(res)
        return results

    def get_hexes_of_axes(self, center, d) -> List[Hex]:
        results = []
        for dir in DIRECTIONS:
            for i in range(1, d + 1):
                res = center + dir * i
                if res in self.obstacles:
                    break  # stop looking in direction of obstacle
                if self.in_map_boundaries(res):
                    results.append(res)
        return results
