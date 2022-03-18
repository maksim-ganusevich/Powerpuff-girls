from typing import List
from work.UtilityAI.Actions import Action
from work.UtilityAI import Context
from ..Actions.ActionShoot import ActionShoot
from . import Reasoner


# Only interested in shoot action for determining neutrality rule
class ReasonerShoot(Reasoner):

    def __init__(self, action_set: List[Action]):
        super(ReasonerShoot, self).__init__(action_set)

    # returns shooting action and
    def pick_action_shoot(self, context: Context) -> (Action, str):
        action, max_score = (None, -1)
        for a in self.action_set:
            score = a.score(context)
            if isinstance(a, ActionShoot) and score == 0:
                return None, ""
            if score > max_score:
                action = a
                max_score = score

        if not isinstance(action, ActionShoot):
            return None, ""

        return action, context.get_target().owner
