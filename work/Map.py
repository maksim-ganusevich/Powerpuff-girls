from typing import List
from work.Hexagon import Hex
from work.config import base, obstacles, vehicles, map_size

directions = [
    Hex(+1, 0, -1), Hex(+1, -1, 0), Hex(0, -1, +1),
    Hex(-1, 0, +1), Hex(-1, +1, 0), Hex(0, +1, -1),
]


def init_values(_map_size: int, base_list: List, obstacles_list: List) -> None:
    # global base
    # global obstacles
    global map_size
    map_size = _map_size
    base.clear()
    obstacles.clear()
    for b in base_list:
        base.add(Hex(b['x'], b['y'], b['z']))
    for o in obstacles_list:
        obstacles.add(Hex(o['x'], o['y'], o['z']))


def set_vehicles(vehicles_dict: dict) -> None:
    # global vehicles
    vehicles.clear()
    for v in vehicles_dict:
        vehicles.add(Hex(v["position"]["x"], v["position"]["y"], v["position"]["z"]))


def update_vehicle(old_pos: Hex, new_pos: Hex) -> None:
    # global vehicles
    vehicles.remove(old_pos)
    vehicles.add(new_pos)


def hex_is_free(h: Hex) -> bool:
    return h not in obstacles and h not in vehicles


def in_map_boundaries(hex: Hex) -> bool:
    return max(abs(hex.x), abs(hex.y), abs(hex.z)) <= map_size


def get_free_neighbours(center: Hex) -> List[Hex]:
    results = []
    for d in directions:
        res = center + d
        if in_map_boundaries(res) and res not in obstacles:
            results.append(res)
    return results


# all hexes in the area with self as center
def get_hexes_in_range(center, n) -> []:
    results = []
    for x in range(-n, n + 1):
        for y in range(max(-n, -x - n), min(n, -x + n) + 1):
            res = center + Hex(x, y, -x - y)
            if in_map_boundaries(res) and res not in obstacles:
                results.append(res)
    return results


# only hexes on the edge of the area
def get_hexes_of_circle(center, r) -> []:
    results = []
    x = -r
    for y in range(0, r):
        vector = Hex(x, y, -x - y)
        res = center + vector
        if in_map_boundaries(res) and res not in obstacles:
            results.append(res)
        for i in range(5):
            vector = Hex(-vector.y, -vector.z, -vector.x)  # rotate 60 degrees
            res = center + vector
            if in_map_boundaries(res) and res not in obstacles:
                results.append(res)
    return results


def get_hexes_of_axes(center, d) -> []:
    results = []
    for dir in directions:
        for i in range(1, d + 1):
            res = center + dir * i
            if res in obstacles:
                break  # stop looking in direction of obstacle
            if in_map_boundaries(res):
                results.append(res)
    return results
