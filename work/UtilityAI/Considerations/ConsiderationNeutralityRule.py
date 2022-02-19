from .Consideration import Consideration
from work.UtilityAI.Context import Context


class ConsiderationNeutralityRule(Consideration):

    def score(self, context: Context) -> float:
        id_all_players = list(context.attack_matrix.keys())
        id_all_players.remove(str(context.player.id))
        id_all_players.remove(str(context.get_target().owner))
        id_third_player = id_all_players[0]
        target_attacked_me = context.player.id in context.attack_matrix[str(context.get_target().owner)]
        target_was_attacked_by_third = context.get_target().owner in context.attack_matrix[id_third_player]
        if target_attacked_me or not target_was_attacked_by_third:
            return 1
        return 0