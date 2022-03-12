from . import Consideration
from work.UtilityAI import Context


class ConsiderationTargetBaseCapture(Consideration):

    def score(self, context: Context) -> float:
        target = context.get_target()
        return self.eval(target.capture_points)
