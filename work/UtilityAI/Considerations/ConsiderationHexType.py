from . import Consideration
from work.UtilityAI import Context
from work.Map import Map


class ConsiderationHexType(Consideration):
    def score(self, context: Context) -> float:
        desired_is_base = context.desired_hex in Map().base
        # base hex should always be more valuable
        if desired_is_base:
            return 1
        else:
            return 0.7
