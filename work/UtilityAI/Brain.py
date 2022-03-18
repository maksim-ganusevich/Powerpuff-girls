from work.UtilityAI.Actions import *
from work.UtilityAI.Reasoners import *
from work.UtilityAI.Considerations import *
from .Context import Context
from .Curve import Curve, CurveRules
from work.Map import Map
from work.Tanks import *
from work.Hexagon import Hex
from work.GameState import GameState


# Combining reasoners, actions and considerations
class Brain:

    def __init__(self):
        self.light_reasoners = None
        self.medium_reasoners = None
        self.heavy_reasoners = None
        self.spg_reasoners = None
        self.at_spg_reasoners = None
        self.path_reasoner = None
        self.simple_reasoner = None

    def init_reasoners(self) -> None:
        self.light_reasoners = self.get_light_reasoners()
        self.medium_reasoners = self.get_medium_reasoners()
        self.heavy_reasoners = self.get_heavy_reasoners()
        self.spg_reasoners = self.get_spg_reasoners()
        self.at_spg_reasoners = self.get_at_spg_reasoners()
        self.simple_reasoner = self.get_stupid_reasoner()

        # action that evaluates hexes
        act_path = ActionPath([
            ConsiderationHexAttacked(Curve.linear_quadratic),
            ConsiderationHexDistance(Curve.linear_quadratic, CurveRules(m=4, b=0.01)),
            ConsiderationHexBlockingTeammate(Curve.linear_quadratic, CurveRules(m=10, inverse=True)),
            ConsiderationHexAttackedByPrevious(Curve.linear_quadratic, CurveRules(m=5, b=0.8)),
            ConsiderationHexType()
        ])
        self.path_reasoner = ReasonerPath([act_path])

    @staticmethod
    def get_stupid_reasoner() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.linear_quadratic, CurveRules(m=Map().size * 2, k=0.2, inverse=True)),
            ConsiderationNeutralityRule()
        ])
        reasoner_target = ReasonerGetTarget([act_target])

        # actions for the main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(),
            ConsiderationNeutralityRule()
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationHexDistance(Curve.linear_quadratic, CurveRules(m=Map().size + 1, k=0.5, inverse=True))
        ])

        reasoner = Reasoner([act_shoot, act_capture_base])
        return reasoner, reasoner_target

    @staticmethod
    def get_light_reasoners() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(m=5, k=-0.2)),
            ConsiderationNeutralityRule(Curve.linear_quadratic, CurveRules(m=2, b=0.3)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1.7, b=0.2))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.1)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.2, a=1.9, inverse=True)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-0.3, b=-0.3, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.4, a=1.9)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-1, b=0.3)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0.7, k=0.1, inverse=True)),
            ConsiderationBaseStayingOnSpot(Curve.linear_quadratic, CurveRules(m=1.05, inverse=True))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            # ConsiderationTargetDistance(Curve.exponential, CurveRules(k=1.3, b=-0.3)),  # m is set based on firing range
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(inverse=True)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=-0.2, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.05, b=-0.05)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.3, m=-0.1, b=-0.05, inverse=True))
        ])
        act_catapult = ActionCatapult([
            ConsiderationHexDistance(Curve.logistic, CurveRules(m=3, k=0.2, inverse=True)),
            ConsiderationCatapult(Curve.linear_quadratic, CurveRules(inverse=True)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.3, m=0.2, b=-0.2, inverse=True))
        ])

        return (Reasoner([act_shoot, act_capture_base]),
                ReasonerGetTarget([act_target]))

    @staticmethod
    def get_medium_reasoners() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(m=5, k=-0.2)),
            ConsiderationNeutralityRule(Curve.linear_quadratic, CurveRules(m=1.6, b=0.2)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1.7, b=0.2))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.9, k=0.1)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.2, a=1.9, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.4, a=1.9)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-1, b=-0.05)),
            ConsiderationBaseStayingOnSpot(Curve.linear_quadratic, CurveRules(m=1.05, inverse=True))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            # ConsiderationTargetDistance(Curve.exponential, CurveRules(k=1.3, b=-0.3)),  # m is set based on firing range
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.2, m=0.2, b=-0.3, inverse=True)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-0.1, b=-0.05, inverse=True))
        ])
        act_repair = ActionLightRepair([
            ConsiderationMyHealth(Curve.linear_quadratic, CurveRules(b=-1, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=1.5, k=0.1, inverse=True)),
            ConsiderationHexDistance(Curve.linear_quadratic, CurveRules(m=Map().size, inverse=True)),
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=1.1, k=0.2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=2, k=1, b=0.3, inverse=True)),
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=0.7, k=0.4, b=-1))
        ])
        act_catapult = ActionCatapult([
            ConsiderationHexDistance(Curve.logistic, CurveRules(m=2, k=0.2, inverse=True)),
            ConsiderationCatapult(Curve.linear_quadratic, CurveRules(inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=2, k=1, b=0.3, inverse=True)),
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=0.7, k=0.4, b=-1)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=1.5, k=0.1, inverse=True)),
        ])

        return (Reasoner([act_shoot, act_capture_base]),
                ReasonerGetTarget([act_target]))

    @staticmethod
    def get_heavy_reasoners() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(m=5, k=-0.2)),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1.7, b=0.2))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.1)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.2, a=1.9, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.2, a=1.9)),
            ConsiderationBaseStayingOnSpot(Curve.linear_quadratic, CurveRules(m=1.05, inverse=True))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(k=0.5)),  # m is set based on firing range
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.2, m=0.2, b=-0.3, inverse=True))
        ])
        act_repair = ActionHardRepair([
            ConsiderationMyHealth(Curve.linear_quadratic, CurveRules(m=2, b=-0.5, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=1.5, k=0.2, inverse=True)),
            ConsiderationHexDistance(Curve.linear_quadratic, CurveRules(m=Map().size, inverse=True)),
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=1.1, k=0.2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=2, k=1, b=0.3, inverse=True)),
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=0.7, k=0.4, b=-1))
        ])

        return (Reasoner([act_shoot, act_capture_base, act_repair]),
                ReasonerGetTarget([act_target]))

    @staticmethod
    def get_spg_reasoners() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.linear_quadratic, CurveRules(m=Map().size * 2, k=0.2, inverse=True)),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1, b=0.1))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.1))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationHexDistance(Curve.sin, CurveRules(b=0.01, k=0.005))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            # m in TargetDistance is set based on firing range
            ConsiderationTargetDistance(Curve.exponential, CurveRules(k=1.3, b=0.1, inverse=True))
        ])
        act_free_the_way = ActionFreeTheWay([
            ConsiderationBlockingWay(Curve.linear_quadratic, CurveRules(m=1.2)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=-2.5, b=1)),
            ConsiderationTargetBaseCapture(Curve.linear_quadratic, CurveRules(k=0.1)),
            ConsiderationAttacked(Curve.linear_quadratic, CurveRules(m=2.4, b=0.6))
        ])
        act_flee = ActionFlee([
            ConsiderationAttacked(Curve.logistic, CurveRules(k=1, b=0.2, a=1.5)),
            ConsiderationNowhereToRun(Curve.linear_quadratic, CurveRules(inverse=True))
        ])

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target, act_free_the_way, act_flee]),
                ReasonerGetTarget([act_target]))

    @staticmethod
    def get_at_spg_reasoners() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(m=5, k=-0.2)),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1.7, b=0.2))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.1)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.2, a=1.9, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.3, b=0.2, a=1.9)),
            ConsiderationBaseStayingOnSpot(Curve.linear_quadratic, CurveRules(m=1.05, inverse=True))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(k=0.5)),  # m is set based on firing range
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.2, m=0.2, b=-0.3, inverse=True))
        ])
        act_repair = ActionHardRepair([
            ConsiderationMyHealth(Curve.linear_quadratic, CurveRules(m=1.2, b=-0.6, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=1.5, k=0.2, inverse=True)),
            ConsiderationHexDistance(Curve.linear_quadratic, CurveRules(m=Map().size, inverse=True)),
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=1.1, k=0.2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=2, k=1, b=0.3, inverse=True)),
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=0.7, k=0.4, b=-1))
        ])
        act_free_the_way = ActionFreeTheWay([
            ConsiderationBlockingWay(Curve.linear_quadratic, CurveRules(m=1.2)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=-2.5, b=1)),
            ConsiderationTargetBaseCapture(Curve.linear_quadratic, CurveRules(k=0.1)),
            ConsiderationAttacked(Curve.linear_quadratic, CurveRules(m=2.4, b=0.6))
        ])

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target, act_repair, act_free_the_way]),
                ReasonerGetTarget([act_target]))

    @staticmethod
    def get_empty_reasoners() -> (Reasoner, Reasoner):
        # used to freeze any team
        return Reasoner([]), ReasonerGetTarget([])

    def get_reasoner(self, tank_type: str) -> (Reasoner, Reasoner):
        reasoners = {
            repr(LightTank): self.light_reasoners,
            repr(MediumTank): self.medium_reasoners,
            repr(HeavyTank): self.heavy_reasoners,
            repr(SPG): self.spg_reasoners,
            repr(AtSPG): self.at_spg_reasoners
        }
        return reasoners[tank_type]

    def think(self, context: Context) -> None:
        """
        Firstly we got to check if any tank is going to shoot, therefore changing neutrality rule.
        After attack matrix is updated, other tanks know for sure if they are protected by neutrality rule
        and can safely move on certain hexes.
        """

        if not context.path_reasoner:
            context.path_reasoner = self.path_reasoner

        for i in range(len(context.player.tanks)):
            context.update_curr_tank_index(i)
            reasoner_main, reasoner_target = self.get_reasoner(repr(type(context.get_curr_tank())))

            shoot_reasoner = ReasonerShoot(reasoner_main.action_set)

            target_index = reasoner_target.get_target_index(context)
            context.target_index = target_index

            # ask for target id that current tank wants to shoot
            best_action, target_id_we_want_to_shoot = shoot_reasoner.pick_action_shoot(context)
            if target_id_we_want_to_shoot:
                # update attack matrix for neutrality rule
                GameState().attack_matrix[str(context.player.id)].append(target_id_we_want_to_shoot)

        # flag for considerations to use neutrality rule
        GameState().attack_matrix_corrected = True

    # executing all best actions
    def act(self, context: Context) -> None:
        for i in range(len(context.player.tanks)):
            context.update_curr_tank_index(i)
            reasoner_main, reasoner_target = self.get_reasoner(repr(type(context.get_curr_tank())))

            target_index = reasoner_target.get_target_index(context)
            context.target_index = target_index
            best_action, weight = reasoner_main.pick_action(context)

            if best_action:
                self.print_action_info(context, best_action)
                best_action.execute(context)

    @staticmethod
    def print_action_info(context: Context, best_action):
        print()
        print("curr: " + repr(type(context.get_curr_tank())))
        print("target: " + repr(type(context.get_target())) + " id: " + str(context.get_target().owner))
        print("distance: " + str(Hex.distance(context.get_curr_tank().position, context.get_target().position)))
        print("Range: " + str(context.get_curr_tank().shoot_range_max) + " bonus: " + str(
            context.get_curr_tank().shoot_range_bonus))
        print("Action: " + repr(type(best_action)))
        print("Attack matrix: " + str(GameState().attack_matrix))
        print("Curr turn: " + str(GameState().current_turn))
        print()
