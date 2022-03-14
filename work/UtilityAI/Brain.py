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
        self.at_spg_reasoners = self.get_heavy_reasoners()
        self.simple_reasoner = self.get_stupid_reasoner()

        # action to select the best hex
        act_path = ActionPath([
            ConsiderationHexAttacked(Curve.linear_quadratic),
            ConsiderationHexDistance(Curve.linear_quadratic, CurveRules(m=4, b=0.01)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=5, b=0.4))
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
            ConsiderationNeutralityRule(Curve.linear_quadratic, CurveRules(m=2, b=0.3, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1.7, b=0.2))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.1)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23, inverse=True)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-0.3, b=-0.3, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-1, b=0.3)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0.7, k=0.1, inverse=True))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            ConsiderationTargetDistance(Curve.exponential, CurveRules(k=1.3, b=-0.3)),  # m is set based on firing range
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(inverse=True)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.2, m=0.2, b=-0.3, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.1, k=0.05, b=-0.05)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.3, m=-0.1, b=-0.05, inverse=True))
        ])
        act_catapult = ActionCatapult([
            ConsiderationHexDistance(Curve.logistic, CurveRules(m=3, k=0.2, inverse=True)),
            ConsiderationCatapult(Curve.linear_quadratic, CurveRules(inverse=True)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.3, m=0.2, b=-0.2, inverse=True))
        ])

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target, act_catapult]),
                ReasonerGetTarget([act_target]))

    @staticmethod
    def get_medium_reasoners() -> (Reasoner, Reasoner):
        # action to select the best target
        act_target = ActionTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetDistance(Curve.logistic, CurveRules(m=5, k=-0.2)),
            ConsiderationNeutralityRule(Curve.linear_quadratic, CurveRules(m=1.8, b=0.4, inverse=True)),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=0, k=0.1)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules(m=1.7, b=0.2))
        ])

        # actions for main reasoner
        act_shoot = ActionShoot([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=2, inverse=True)),
            ConsiderationTargetInRange(Curve.linear_quadratic, CurveRules()),
            ConsiderationNeutralityRule(),
            ConsiderationTargetBaseCapture(Curve.logistic, CurveRules(m=-0.9, k=0.1)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23)),
            ConsiderationEnemyCapture(Curve.logistic, CurveRules(k=0.1, m=-1, b=-0.05))
        ])
        act_move_to_target = ActionMoveToTarget([
            ConsiderationTargetHealth(Curve.linear_quadratic, CurveRules(m=4, k=0.8, inverse=True)),
            ConsiderationTargetDistance(Curve.exponential, CurveRules(k=1.3, b=-0.3)),  # m is set based on firing range
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

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target, act_repair, act_catapult]),
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
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23, inverse=True))
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

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target, act_repair]),
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
            ConsiderationTargetDistance(Curve.exponential, CurveRules(k=1.3, b=-0.3))  # m is set based on firing range
        ])

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target]),
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
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23, inverse=True))
        ])
        act_capture_base = ActionCaptureBase([
            ConsiderationMyCapture(Curve.logistic, CurveRules(m=-0.8, k=0.05)),
            ConsiderationCaptureSafe(Curve.logistic, CurveRules(k=0.6, m=0.2, b=0.05)),
            ConsiderationAttacked(Curve.logistic, CurveRules(k=0.2, b=0.23, inverse=True))
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

        return (Reasoner([act_shoot, act_capture_base, act_move_to_target, act_repair]),
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

    # picking the best action and executing it
    def act(self, context: Context) -> None:
        if not context.path_reasoner:
            context.path_reasoner = self.path_reasoner
        reasoner_main, reasoner_target = self.get_reasoner(repr(type(context.get_curr_tank())))

        # if context.player.name == "Semen":
        #     reasoner_main, reasoner_target = self.get_empty_reasoners()
        if context.player.name != "Woody":
            reasoner_main, reasoner_target = self.get_stupid_reasoner()

        target_index = reasoner_target.get_target_index(context)
        context.target_index = target_index
        best_action, weight = reasoner_main.pick_action(context)
        if best_action:
            if context.player.name == "Woody":
                print()
                print("curr: " + repr(type(context.get_curr_tank())))
                print("target: " + repr(type(context.get_target())))
                print("distance: " + str(Hex.distance(context.get_curr_tank().position, context.get_target().position)))
                print("Range: " + str(context.get_curr_tank().shoot_range_max) + " bonus: " + str(
                    context.get_curr_tank().shoot_range_bonus))
                print("Action: " + repr(type(best_action)))
                print("Attack matrix: " + str(context.attack_matrix))
                print("Curr turn: " + str(GameState().current_turn))
                print()
            best_action.execute(context)
