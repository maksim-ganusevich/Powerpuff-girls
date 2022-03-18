from . import Consideration
from work.UtilityAI import Context
from work.Map import Map
from work.Hexagon import Hex
from .ConsiderationHexAttacked import ConsiderationHexAttacked
from ..Curve import Curve


class ConsiderationCaptureSafe(Consideration):
    def score(self, context: Context) -> float:
        # check for safe base hex to capture within speed points
        curr_tank = context.get_curr_tank()
        c = ConsiderationHexAttacked(Curve.linear_quadratic)
        # getting utility of the best base hex
        best_weight = 0.8  # default value if base not in reach
        for b in Map().base:
            if Hex.distance(curr_tank.position, b) <= curr_tank.sp:
                context.desired_hex = b
                weight = c.score(context)
                if weight > best_weight:
                    best_weight = weight

        return self.eval(best_weight)
