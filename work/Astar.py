from queue import PriorityQueue
from typing import List
from work.Hexagon import Hex
from work.Map import Map


def get_in_range_from(center: Hex, start: Hex, rng: int, sp: int) -> List[Hex]:
    hexes_in_range = []

    for x in range(-sp, sp + 1):
        for y in range(max(-sp, -x - sp), min(sp, -x + sp) + 1):
            res = start + Hex(x, y, -x - y)
            # store hexes that are in range from center
            if Map().hex_is_free(res) and Hex.distance(center, res) == rng:
                hexes_in_range.append(res)

    return hexes_in_range


# traverses came_from and gets all hexes
def traverse_path(curr: Hex, came_from: dict, cost_so_far: dict, path: List[Hex], sp: int) -> None:
    children = came_from[curr]
    for node in children:
        if node and node not in path:
            traverse_path(node, came_from, cost_so_far, path, sp)
    if cost_so_far[curr] <= sp:  # is curr reachable?
        path.append(curr)


# finds hexes of all possible paths from A to B
def find_all_paths(start: Hex, goal: Hex, sp: int) -> List[Hex]:
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = [None]
    cost_so_far[start] = 0

    path_found = False
    last_priority = 0

    while not frontier.empty():
        priority, current = frontier.get()
        if current == goal:
            # path found, but continue looking for good hexes in the queue
            path_found = True
            last_priority = priority
            continue

        if path_found and priority > last_priority:
            break

        neighbours = Map().get_free_neighbours(current)
        for next_hex in neighbours:
            new_cost = cost_so_far[current] + 1
            if next_hex not in cost_so_far or new_cost < cost_so_far[next_hex]:
                cost_so_far[next_hex] = new_cost
                priority = new_cost + Hex.distance(goal, next_hex)
                frontier.put((priority, next_hex))
                came_from[next_hex] = [current]
            elif next_hex in cost_so_far and new_cost == cost_so_far[next_hex]:
                came_from[next_hex].append(current)

    path = []
    traverse_path(goal, came_from, cost_so_far, path, sp)
    return path
