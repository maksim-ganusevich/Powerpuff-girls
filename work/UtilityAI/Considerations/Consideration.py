from typing import Callable
from abc import ABC, abstractmethod
from work.UtilityAI import Context
from work.UtilityAI.Curve import Curve, CurveRules


# Considers a single piece of game info (health, dist, base, etc.)
class Consideration(ABC):

    def __init__(self, curve: Callable[[float, CurveRules], float] = None, rules: CurveRules = None):
        self.curve = curve
        self.rules = rules

    # scores the input in range [0,1]. Considers how good is the input for the action
    # 0 - bad, 1 - good
    @abstractmethod
    def score(self, context: Context) -> float:
        pass

    # evaluates utility based on response curve
    def eval(self, value: float) -> float:
        return Curve.clamp01(self.curve(value, self.rules)) if self.curve else value
