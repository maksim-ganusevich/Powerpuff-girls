from . import Consideration
from work.UtilityAI import Context
from work.Hexagon import Hex


class ConsiderationHexDistance(Consideration):
    def score(self, context: Context) -> float:
        if not context.desired_hex:
            return 0
        dist = Hex.distance(context.get_curr_tank().position, context.desired_hex)
        return self.eval(dist)
