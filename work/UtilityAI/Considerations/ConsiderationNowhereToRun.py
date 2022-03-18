from . import Consideration
from work.UtilityAI import Context
from work.Map import Map


class ConsiderationNowhereToRun(Consideration):

    def score(self, context: Context) -> float:
        curr_tank = context.get_curr_tank()
        hexes_range = Map().get_hexes_in_range(curr_tank.position, curr_tank.sp)
        max_weight, best_hex = context.path_reasoner.eval_possible_hexes(context, hexes_range)
        nowhere_to_run = best_hex == curr_tank.position
        return self.eval(nowhere_to_run)
