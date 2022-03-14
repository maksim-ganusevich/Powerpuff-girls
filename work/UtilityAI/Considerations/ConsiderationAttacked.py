from . import Consideration
from work.UtilityAI import Context
from work.GameState import GameState
from ..Curve import CurveRules


class ConsiderationAttacked(Consideration):
    def score(self, context: Context) -> float:
        attacks_by_single_enemy = 0
        for pl in GameState().players:
            count = 0
            for enemy in context.enemy_tanks:
                if context.get_curr_tank().position in enemy.get_firing_range() and enemy.owner == pl["idx"]:
                    count += 1
            if count > attacks_by_single_enemy:
                attacks_by_single_enemy = count
        # curve slope depends on curr hp
        self.rules = CurveRules(m=context.get_curr_tank().hp-0.7, inverse=True)
        return self.eval(attacks_by_single_enemy)
