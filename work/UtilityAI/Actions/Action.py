from typing import List
from abc import ABC, abstractmethod
from ..Considerations.Consideration import Consideration
from work.UtilityAI.Context import Context


class Action(ABC):
    def __init__(self, considerations: List[Consideration]):
        # list of considerations define how likely the action will be picked
        self.considerations = considerations

    # calculates utility score for the action based on all considerations
    def score(self, context: Context) -> float:
        result = 1
        modification_factor = 1 - (1 / len(self.considerations))
        for c in self.considerations:
            score = c.score(context)
            make_up_value = (1 - score) * modification_factor
            final_score = score + (make_up_value * score)
            result *= final_score
        return result

    # game action that is being considered
    @abstractmethod
    def execute(self, context: Context) -> None:
        pass
