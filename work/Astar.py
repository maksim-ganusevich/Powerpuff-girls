from queue import PriorityQueue
from work.Hexagon import Hex
from work.Map import Map
from typing import List


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

        for next in Map().get_free_neighbours(current):
            new_cost = cost_so_far[current]  # + hex cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + Hex.distance(goal, next)
                frontier.put((priority, next))
                came_from[next] = current

    # construct path by following backwards
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]

    return path


def move_to(start: Hex, goal: Hex, speed_points: int) -> Hex:
    if not Map().in_map_boundaries(goal):
        return start
    path = find_path(start, goal)
    if len(path) <= speed_points:
        return goal
    for i in range(speed_points, 0, -1):
        final_hex = path[len(path) - i]  # intermediate hex on the path
        if final_hex not in Map().vehicles:  # check if occupied by other vehicle
            return final_hex
    return start
