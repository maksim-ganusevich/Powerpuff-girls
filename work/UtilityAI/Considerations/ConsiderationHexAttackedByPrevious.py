from . import Consideration
from work.UtilityAI import Context
from .ConsiderationHexAttacked import ConsiderationHexAttacked

"""
If we have a list of players [0, 1, 2], and players move in order 0->1->2->0...
then it's better to be attacked by a player on a previous turn. 
(if we play as 2, then better be attacked by 1 rather than 0)
This is related to neutrality rule. """


class ConsiderationHexAttackedByPrevious(Consideration):
    def score(self, context: Context) -> float:
        enemy_previous_turn = False
        enemy_on_previous_turn = ConsiderationHexAttacked.enemy_on_previous_turn(context.player.id)
        for enemy in context.enemy_tanks:
            if context.desired_hex in enemy.get_firing_range():
                enemy_previous_turn = enemy.owner == enemy_on_previous_turn
                if enemy_previous_turn:
                    break
        return self.eval(enemy_previous_turn)
