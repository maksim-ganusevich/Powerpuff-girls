from typing import List
from work.UtilityAI.Considerations.Consideration import Consideration
from .Action import Action


# acts as a container for target considerations
class ActionTarget(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionTarget, self).__init__(considerations)

    def execute(self, context) -> None:
        pass
