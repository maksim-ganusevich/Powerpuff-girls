from typing import List
from . import Action
from ..Considerations import Consideration
from work.UtilityAI import Context


class ActionShoot(Action):

    def __init__(self, considerations: List[Consideration]):
        super(ActionShoot, self).__init__(considerations)

    def execute(self, context: Context) -> None:
        curr_tank = context.get_curr_tank()
        target = context.get_target()
        shooting_pos = curr_tank.get_shoot_pos(target.position)
        context.player.shoot(curr_tank.id, shooting_pos)
        curr_tank.shoot(target)
