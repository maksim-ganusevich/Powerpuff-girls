from . import Consideration
from work.UtilityAI import Context
from work.GameState import GameState
from ..Curve import CurveRules
from work.Map import Map


class ConsiderationHexCost(Consideration):
    def score(self, context: Context) -> float:
        attacks_by_single_enemy = 0
        for pl in GameState().players:
            count = 0
            for enemy in context.enemy_tanks:
                if context.desired_hex in enemy.get_firing_range() and enemy.owner == pl["idx"]:
                    count += 1
            if count > attacks_by_single_enemy:
                attacks_by_single_enemy = count
        # curve slope depends on curr hp
        self.rules = CurveRules(m=context.get_curr_tank().hp - 2, k=-0.2, b=-0.05)
        if context.desired_hex in Map().base:
            if context.get_curr_tank().position not in Map().base:
                self.rules.b = 0.03
            else:
                self.rules.b = 0.01
        return self.eval(attacks_by_single_enemy)
