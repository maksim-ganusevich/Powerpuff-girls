from . import Consideration
from work.UtilityAI import Context


class ConsiderationTargetHealth(Consideration):

    def score(self, context: Context) -> float:
        target = context.get_target()
        return self.eval(target.hp)
