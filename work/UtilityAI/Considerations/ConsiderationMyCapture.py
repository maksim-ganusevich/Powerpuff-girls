from . import Consideration
from work.UtilityAI import Context
from work.Map import Map
from work.GameState import GameState


class ConsiderationMyCapture(Consideration):

    def score(self, context: Context) -> float:
        curr_tank = context.get_curr_tank()
        capture_points = 0
        if curr_tank.position in Map().base:
            capture_points = GameState().win_points[str(context.player.id)]["capture"]
        return self.eval(capture_points)
