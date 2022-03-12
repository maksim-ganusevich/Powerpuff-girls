from . import Consideration
from work.UtilityAI import Context


class ConsiderationMyHealth(Consideration):

    def score(self, context: Context) -> float:
        return self.eval(context.get_curr_tank().hp)
