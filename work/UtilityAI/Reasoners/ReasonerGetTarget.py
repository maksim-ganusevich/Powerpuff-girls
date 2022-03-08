from typing import List
from . import Reasoner
from work.UtilityAI.Actions import Action
from work.UtilityAI import Context


# helper reasoner to retrieve a best target
class ReasonerGetTarget(Reasoner):

    def __init__(self, action_set: List[Action]):
        super(ReasonerGetTarget, self).__init__(action_set)

    def get_target_index(self, context: Context) -> int:
        max_weight, target_index = 0, 0
        # check weight of every enemy tank
        for i, tank in enumerate(context.enemy_tanks):
            context.target_index = i
            action, t_weight = self.pick_action(context)
            if t_weight > max_weight:  # remember tank with the best weight
                max_weight, target_index = t_weight, i

        return target_index
