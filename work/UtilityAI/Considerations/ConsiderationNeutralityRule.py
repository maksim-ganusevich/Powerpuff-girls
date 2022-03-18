from . import Consideration
from work.UtilityAI import Context
from work.GameState import GameState


class ConsiderationNeutralityRule(Consideration):

    @staticmethod
    def check_rule(player_id: int, target_owner_id: int) -> bool:
        id_all_players = list(GameState().attack_matrix.keys())
        id_all_players.remove(str(player_id))
        id_all_players.remove(str(target_owner_id))
        id_third_player = id_all_players[0]
        target_attacked_me = player_id in GameState().attack_matrix[str(target_owner_id)]
        target_was_attacked_by_third = target_owner_id in GameState().attack_matrix[id_third_player]
        rule_active = target_attacked_me or not target_was_attacked_by_third
        return rule_active

    def score(self, context: Context) -> float:
        rule_active = self.check_rule(context.player.id, context.get_target().owner)
        if self.curve:
            return self.eval(rule_active)
        return rule_active
