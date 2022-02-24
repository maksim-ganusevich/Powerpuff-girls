from typing import List
from ..Considerations.Consideration import Consideration
from work.UtilityAI.Context import Context
from .Action import Action
from work import Map
from work.GameState import Info


class ActionCaptureBase(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionCaptureBase, self).__init__(considerations)
        self.info = Info()

    def execute(self, context: Context) -> None:
        curr_tank = context.get_curr_tank()
        if curr_tank.position in Map.base:  # already capturing
            return
        base_hex = Map.get_free_base_hex()
        if base_hex:
            prev_pos = curr_tank.position
            if curr_tank.move(base_hex):
                Map.update_vehicle(prev_pos, curr_tank.position)
                # update info for visualisation
                self.info.vehicles[str(curr_tank.id)]["position"] = curr_tank.position.convert_to_dict()
                context.player.move(curr_tank.id, curr_tank.position)
                print('update tank')
