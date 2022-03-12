from . import Consideration
from work.UtilityAI import Context
from work.Map import Map
from work.Hexagon import Hex


class ConsiderationBaseDistance(Consideration):

    def score(self, context: Context) -> float:
        base_hex = Map().get_closest_in_list(context.get_curr_tank().position, Map().base)
        distance = Hex.distance(context.get_curr_tank().position, base_hex)
        return self.eval(distance)
