import random
from queue import PriorityQueue
from typing import List
from work.Hexagon import Hex
from work.Map import Map


def find_path(start: Hex, goal: Hex) -> List[Hex]:
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        priority, current = frontier.get()

        if current == goal:
            break

        neighbours = Map().get_free_neighbours(current)
        random.shuffle(neighbours)  # paths variation
        for next_hex in neighbours:
            new_cost = cost_so_far[current]  # + hex cost
            if next_hex not in cost_so_far or new_cost < cost_so_far[next_hex]:
                cost_so_far[next_hex] = new_cost
                priority = new_cost + Hex.distance(goal, next_hex)
                frontier.put((priority, next_hex))
                came_from[next_hex] = current

    # construct path by following backwards
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]

    return path


def get_in_range_from(center: Hex, start: Hex, rng: int, sp: int) -> List[Hex]:
    hexes_in_range = []

    for x in range(-sp, sp + 1):
        for y in range(max(-sp, -x - sp), min(sp, -x + sp) + 1):
            res = start + Hex(x, y, -x - y)
            # store hexes that are in range from center
            if Map().hex_is_free(res) and Hex.distance(center, res) == rng:
                hexes_in_range.append(res)

    return hexes_in_range
