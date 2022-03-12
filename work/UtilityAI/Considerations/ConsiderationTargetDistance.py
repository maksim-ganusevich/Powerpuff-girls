from . import Consideration
from work.UtilityAI import Context
from work.Hexagon import Hex


class ConsiderationTargetDistance(Consideration):

    def score(self, context: Context) -> float:
        distance = Hex.distance(context.get_curr_tank().position, context.get_target().position)
        if self.rules.m == 1:  # use firing range if nothing is set
            self.rules.m = context.get_curr_tank().get_range_max()
        return self.eval(distance)
