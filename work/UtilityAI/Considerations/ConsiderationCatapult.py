from . import Consideration
from work.UtilityAI import Context
from work.GameState import GameState


class ConsiderationCatapult(Consideration):
    def score(self, context: Context) -> float:
        # max catapults used
        if len(GameState().catapult_usage) >= GameState().max_catapult_usage:
            return 0
        return self.eval(context.get_curr_tank().shoot_range_bonus)
