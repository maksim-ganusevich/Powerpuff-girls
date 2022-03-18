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
        max_weight, best_hex = self.eval_path(context, goal)
        return best_hex

    def eval_path(self, context: Context, goal) -> (float, Hex):
        curr_tank = context.get_curr_tank()
        all_possible_paths = Astar.find_all_paths(curr_tank.position, goal, curr_tank.sp)
        max_weight, best_hex = self.eval_possible_hexes(context, all_possible_paths)
        return max_weight, best_hex

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
