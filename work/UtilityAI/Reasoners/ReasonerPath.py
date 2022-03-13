from typing import List
from work.Hexagon import Hex
from . import Reasoner
from work.UtilityAI.Actions import Action
from work.UtilityAI import Context
from work import Astar
from work.Map import Map


# helper reasoner to retrieve a best path
class ReasonerPath(Reasoner):

    def __init__(self, action_set: List[Action]):
        super(ReasonerPath, self).__init__(action_set)

    def get_base_hex(self, context: Context) -> Hex:
        curr_tank = context.get_curr_tank()
        max_weight, best_base_hex = -1, curr_tank.position
        for b in Map().base:
            weight = self.eval_hex(context, b)
            if weight > max_weight:
                max_weight, best_base_hex = weight, b
        return best_base_hex

    def get_best_hex_around(self, context: Context) -> Hex:
        curr_tank = context.get_curr_tank()
        hexes_range = Map().get_hexes_in_range(curr_tank.position, curr_tank.sp)
        max_weight, best_hex = self.eval_possible_hexes(context, hexes_range)
        return best_hex

    def get_best_hex(self, context: Context, goal: Hex, use_range: bool = False) -> Hex:
        curr_tank = context.get_curr_tank()

        # is goal inside min range? need to move away
        min_range = curr_tank.get_range_min()
        if use_range and Hex.distance(curr_tank.position, goal) < min_range:
            # hexes from which tank can shoot goal
            hexes_in_range = Astar.get_in_range_from(goal, curr_tank.position, min_range, curr_tank.sp)
            if len(hexes_in_range) > 0:
                max_weight, best_hex = self.eval_possible_hexes(context, hexes_in_range)
                return best_hex
            else:
                # not enough sp or all hexes are occupied, get where possible
                hexes_range = Map().get_hexes_in_range(curr_tank.position, curr_tank.sp)
                max_weight, best_hex = self.eval_possible_hexes(context, hexes_range)
                return best_hex

        # tank is outside of range
        path = Astar.find_path(curr_tank.position, goal)
        max_weight, best_hex = self.eval_path(context, path, goal, use_range)

        return best_hex

    def eval_path(self, context: Context, path: List[Hex], goal, use_range: bool) -> (float, Hex):
        curr_tank = context.get_curr_tank()
        if use_range:
            min_range = curr_tank.get_range_min()
            path = path[min_range:]  # slicing so destination is in range
        # last path hex is curr_tank.position (path is reversed)
        furthest_index = len(path) - curr_tank.sp if len(path) >= curr_tank.sp else 0
        # slice to get hexes where tank can move based on sp
        path = path[furthest_index:]

        # add hexes that are equally distant from the origin to widen possible choices
        all_possible_paths = []
        for h in path:
            all_possible_paths.extend(self.explore_with_same_dist(h, [h], curr_tank.position, goal))
        return self.eval_possible_hexes(context, all_possible_paths)

    def eval_possible_hexes(self, context: Context, hexes: List[Hex]) -> (float, Hex):
        curr_tank = context.get_curr_tank()
        max_weight, best_hex = 0, curr_tank.position
        for h in hexes:
            weight = self.eval_hex(context, h)
            if weight > max_weight:
                max_weight, best_hex = weight, h
        return max_weight, best_hex

    def eval_hex(self, context: Context, h: Hex) -> float:
        if h not in Map().vehicles:
            context.desired_hex = h
            return self.pick_action(context)[1]
        return 0

    def explore_with_same_dist(self, h: Hex, hexes: List[Hex], origin: Hex, destination: Hex) -> List[Hex]:
        o = Hex.distance(h, origin)
        d = Hex.distance(h, destination)
        for n in Map().get_free_neighbours(h):
            n_o = Hex.distance(n, origin)
            n_d = Hex.distance(n, destination)
            if n not in hexes and n_o == o and n_d == d and Map().hex_is_free(n):
                hexes.append(n)
                self.explore_with_same_dist(n, hexes, origin, destination)
        return hexes
