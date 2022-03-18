from . import Consideration
from work.UtilityAI import Context


# meant to lower ActionCaptureBase utility and raise Shooting if staying on spot anyway
class ConsiderationBaseStayingOnSpot(Consideration):
    def score(self, context: Context) -> float:
        curr_tank = context.get_curr_tank()
        base_hex = context.path_reasoner.get_base_hex(context)
        best_hex = context.path_reasoner.get_best_hex(context, base_hex)
        staying_on_spot = best_hex == curr_tank.position
        return self.eval(staying_on_spot)
