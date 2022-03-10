from . import Consideration
from work.UtilityAI import Context
from work.Hexagon import Hex


class ConsiderationTargetDistance(Consideration):

    def score(self, context: Context) -> float:
        distance = Hex.distance(context.get_curr_tank().position, context.get_target().position)
        return self.eval(distance)
