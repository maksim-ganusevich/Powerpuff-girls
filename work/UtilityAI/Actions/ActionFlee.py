from typing import List
from . import Action
from ..Considerations import Consideration
from work.UtilityAI import Context
from work.Map import Map


class ActionFlee(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionFlee, self).__init__(considerations)

    def execute(self, context: Context) -> None:
        curr_tank = context.get_curr_tank()
        hexes_range = Map().get_hexes_in_range(curr_tank.position, curr_tank.sp)
        max_weight, best_hex = context.path_reasoner.eval_possible_hexes(context, hexes_range)
        return best_hex
