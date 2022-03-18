from typing import List

from ..Considerations.Consideration import Consideration
from work.UtilityAI.Context import Context
from .Action import Action
from work.Map import Map
from work.GameState import GameState
from work.Hexagon import Hex


class ActionFreeTheWay(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionFreeTheWay, self).__init__(considerations)

    def score(self, context: Context) -> float:
        context.desired_hex = Map().base[0]
        return super(ActionFreeTheWay, self).score(context)

    def execute(self, context: Context) -> None:
        curr_tank = context.get_curr_tank()

        # find hexes closer to spawn
        hexes_closer_to_spawn = []
        curr_to_spawn_dist = Hex.distance(curr_tank.position, curr_tank.spawn_position)
        for n in Map().get_free_neighbours(curr_tank.position):
            if Hex.distance(n, curr_tank.spawn_position) < curr_to_spawn_dist:
                hexes_closer_to_spawn.append(n)

        prev_pos = curr_tank.position
        weight, best_hex = context.path_reasoner.eval_possible_hexes(context, hexes_closer_to_spawn)
        if curr_tank.move(best_hex):
            Map().update_vehicle(prev_pos, curr_tank.position)
            # update info for visualisation
            GameState().vehicles[str(curr_tank.id)]["position"] = curr_tank.position.convert_to_dict()
            context.player.move(curr_tank.id, curr_tank.position)
