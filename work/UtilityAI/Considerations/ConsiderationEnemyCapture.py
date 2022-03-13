from . import Consideration
from work.UtilityAI import Context
from work.GameState import GameState


class ConsiderationEnemyCapture(Consideration):
    def score(self, context: Context) -> float:
        enemy_capture_max = 0
        for val in GameState().win_points.values():
            capture_points = val["capture"]
            if capture_points > enemy_capture_max:
                enemy_capture_max = capture_points

        return self.eval(enemy_capture_max)
