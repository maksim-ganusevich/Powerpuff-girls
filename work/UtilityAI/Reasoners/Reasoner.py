from typing import List
from work.UtilityAI.Actions import Action
from work.UtilityAI import Context


# Responsible for evaluating every action and picking the best one
class Reasoner:

    def __init__(self, action_set: List[Action]):
        self.action_set = action_set

    def pick_action(self, context: Context) -> (Action, float):
        action, max_score = (None, -1)
        for a in self.action_set:
            score = a.score(context)
            if score > max_score:
                action = a
                max_score = score
        return action, max_score
