import math


# Parameters that define a curve shape
class CurveRules:
    def __init__(self, m: float = 1, k: float = 1, inverse: bool = False):
        self.m = m
        self.k = k
        self.inverse = inverse


class Curve:

    @staticmethod
    def clamp01(value: float) -> float:
        return max(min(value, 1), 0)

    @staticmethod
    def linear_quadratic(x: float, rules: CurveRules) -> float:
        val = (x / rules.m) ** rules.k
        return val if not rules.inverse else 1 - val

    @staticmethod
    def logistic(x: float, rules: CurveRules) -> float:
        val = 1 / (1 + math.exp(-x))
        return val if not rules.inverse else 1 - val
