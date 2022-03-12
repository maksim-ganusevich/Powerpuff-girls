from typing import List
from . import Action
from ..Considerations import Consideration


# acts as a container for hex considerations
class ActionPath(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionPath, self).__init__(considerations)

    def execute(self, context) -> None:
        pass
