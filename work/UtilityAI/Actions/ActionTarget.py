from typing import List
from . import Action
from ..Considerations import Consideration


# acts as a container for target considerations
class ActionTarget(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionTarget, self).__init__(considerations)

    def execute(self, context) -> None:
        pass
