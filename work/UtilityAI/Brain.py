from work.UtilityAI.Actions import *
from work.UtilityAI.Reasoners import *
from work.UtilityAI.Considerations import *
from .Context import Context
from .Curve import Curve, CurveRules
from work import Map


# Combining reasoners, actions and considerations
class Brain:

    def __init__(self):
        self.reasoner_target = None
        self.reasoner = None

    def init_reasoners(self):
        # action to select the best target
        act_target = ActionTarget([ConsiderationTargetHealth(Curve.linear_quadratic,
                                                             CurveRules(m=4, k=2, inverse=True)),
                                   ConsiderationTargetDistance(Curve.linear_quadratic,
                                                               CurveRules(m=Map.map_size*2, k=0.2, inverse=True)),
                                   ConsiderationNeutralityRule()])
        self.reasoner_target = ReasonerGetTarget([act_target])

        # actions for the main reasoner
        act_shoot = ActionShoot([ConsiderationTargetHealth(Curve.linear_quadratic,
                                                           CurveRules(m=4, k=2, inverse=True)),
                                 ConsiderationTargetInRange(),
                                 ConsiderationNeutralityRule()])
        act_capture_base = ActionCaptureBase([ConsiderationBaseDistance(Curve.linear_quadratic,
                                                                        CurveRules(m=Map.map_size+1, k=0.5, inverse=True))])
        self.reasoner = Reasoner([act_shoot, act_capture_base])

    # picking the best action and executing it
    def act(self, context: Context) -> None:
        target_index = self.reasoner_target.get_target_index(context)
        context.target_index = target_index
        best_action, weight = self.reasoner.pick_action(context)
        best_action.execute(context)
