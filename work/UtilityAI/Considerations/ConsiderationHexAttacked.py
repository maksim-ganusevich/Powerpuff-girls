from . import Consideration
from work.UtilityAI import Context
from work.GameState import GameState
from ..Curve import CurveRules
from .ConsiderationNeutralityRule import ConsiderationNeutralityRule


class ConsiderationHexAttacked(Consideration):

    @staticmethod
    def count_attacking_enemies(context: Context, enemy_pl: dict) -> int:
        attacks_by_single_enemy = 0
        count = 0
        for enemy in context.enemy_tanks:
            if context.desired_hex in enemy.get_firing_range() and enemy.owner == enemy_pl["idx"]:
                count += 1
        if count > attacks_by_single_enemy:
            attacks_by_single_enemy = count
        return attacks_by_single_enemy

    @staticmethod
    def enemy_on_previous_turn(player_id: int) -> str:
        players = GameState().players
        for i in range(len(players)):
            if players[i] == player_id:
                return players[i-1]

    def score(self, context: Context) -> float:
        # how many enemy tanks attack desired hex
        most_attacks = 0
        for pl in GameState().players:
            if pl["idx"] != context.player.id:
                enemy_moved_previously = pl["idx"] == self.enemy_on_previous_turn(context.player.id)
                # if matrix corrected then we can safely use neutrality rule
                if GameState().attack_matrix_corrected:
                    # if rule active, enemy can attack us
                    neutral_rule = ConsiderationNeutralityRule.check_rule(pl["idx"], context.player.id)
                    if not neutral_rule and enemy_moved_previously:  # cannot attack us, so don't bother counting
                        continue

                count = self.count_attacking_enemies(context, pl)
                if count > most_attacks:
                    most_attacks = count

        # curve slope depends on curr hp
        self.rules = CurveRules(m=context.get_curr_tank().hp, inverse=True)
        return self.eval(most_attacks)
