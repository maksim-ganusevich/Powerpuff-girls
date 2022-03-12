from . import Consideration
from work.UtilityAI import Context


class ConsiderationTargetInRange(Consideration):
    def score(self, context: Context) -> float:
        in_range = context.get_target().position in context.get_curr_tank().get_firing_range()
        return self.eval(in_range)
