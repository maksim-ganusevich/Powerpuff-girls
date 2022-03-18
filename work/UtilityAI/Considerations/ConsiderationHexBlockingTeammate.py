from . import Consideration
from work.UtilityAI import Context
from work.Map import Map, CENTER
from work.Hexagon import Hex


# meant to discourage of standing in front of slow tanks by lowering hex utility
class ConsiderationHexBlockingTeammate(Consideration):
    def score(self, context: Context) -> float:
        curr_tank = context.get_curr_tank()

        in_front_of_slow = False
        for t in context.player_tanks:
            if t != curr_tank and t.sp == 1:  # friendly tank is slow
                neighbours = Map().get_free_neighbours(t.position)
                if context.desired_hex in neighbours:  # desired hex is close to friendly slow tank
                    # check if that hex is in front of slow tank
                    t_to_center_dist = Hex.distance(t.position, CENTER)
                    des_to_center_dist = Hex.distance(context.desired_hex, CENTER)
                    if des_to_center_dist < t_to_center_dist:
                        in_front_of_slow = True
                        break

        return self.eval(in_front_of_slow)
