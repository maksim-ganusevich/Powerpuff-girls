from . import Consideration
from work.UtilityAI import Context


class ConsiderationTargetInRange(Consideration):

    @staticmethod
    def score(context: Context) -> float:
        if context.get_target().position not in context.get_curr_tank().get_firing_range():
            return 0  # eliminates shoot action
        return 1
