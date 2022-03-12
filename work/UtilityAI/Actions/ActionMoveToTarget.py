from typing import List
from ..Considerations.Consideration import Consideration
from work.UtilityAI.Context import Context
from .Action import Action
from work.Map import Map
from work.GameState import GameState


class ActionMoveToTarget(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionMoveToTarget, self).__init__(considerations)

    def execute(self, context: Context) -> None:
        curr_tank = context.get_curr_tank()
        target = context.get_target()
        prev_pos = curr_tank.position
        best_hex = context.path_reasoner.get_best_hex(context, target.position, True)
        if curr_tank.move(best_hex):
            Map().update_vehicle(prev_pos, curr_tank.position)
            # update info for visualisation
            GameState().vehicles[str(curr_tank.id)]["position"] = curr_tank.position.convert_to_dict()
            context.player.move(curr_tank.id, curr_tank.position)
