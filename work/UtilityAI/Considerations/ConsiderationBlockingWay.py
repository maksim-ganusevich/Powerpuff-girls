from . import Consideration
from work.UtilityAI import Context
from work.Map import Map, DIRECTIONS
from work.Hexagon import Hex


class ConsiderationBlockingWay(Consideration):
    def score(self, context: Context) -> float:
        curr_tank = context.get_curr_tank()
        between_obstacles = False

        # check if tank is between two obstacles -> blocking the way
        for i in range(0, 3):
            direction = DIRECTIONS[i]
            left = curr_tank.position - direction
            right = curr_tank.position + direction
            if left in Map().obstacles and right in Map().obstacles:
                between_obstacles = True
                break

        if not between_obstacles:
            return 0

        # check for tanks behind which might want to move forward
        tank_behind = False
        neighbours = Map().get_free_neighbours(curr_tank.position)
        for t in context.player_tanks:
            # if t close and has speed points 1, meaning can't go through
            if t.position in neighbours and t.sp == 1:
                t_to_spawn_dist = Hex.distance(t.position, t.spawn_position)
                curr_to_spawn_dist = Hex.distance(curr_tank.position, curr_tank.spawn_position)
                # is curr further away from spawn than t?
                if curr_to_spawn_dist > t_to_spawn_dist:
                    tank_behind = True
                    break

        return self.eval(tank_behind)
