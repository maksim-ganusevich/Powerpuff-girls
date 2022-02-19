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
        for c in self.considerations:
            result *= c.score(context)  # TODO compensate multiplication
        return result

    # game action that is being considered
    @abstractmethod
    def execute(self, context: Context) -> None:
        pass
