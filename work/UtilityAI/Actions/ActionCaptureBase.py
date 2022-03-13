from typing import List

from ..Considerations.Consideration import Consideration
from work.UtilityAI.Context import Context
from .Action import Action
from work.Map import Map
from work.GameState import GameState


class ActionCaptureBase(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionCaptureBase, self).__init__(considerations)

    def score(self, context: Context) -> float:
        context.desired_hex = Map().base[0]
        return super(ActionCaptureBase, self).score(context)

    def execute(self, context: Context) -> None:
        curr_tank = context.get_curr_tank()
        base_hex = context.path_reasoner.get_base_hex(context)

        prev_pos = curr_tank.position
        best_hex = context.path_reasoner.get_best_hex(context, base_hex)
        if curr_tank.move(best_hex):
            Map().update_vehicle(prev_pos, curr_tank.position)
            # update info for visualisation
            GameState().vehicles[str(curr_tank.id)]["position"] = curr_tank.position.convert_to_dict()
            context.player.move(curr_tank.id, curr_tank.position)
