import math


# Parameters that define a curve shape
class CurveRules:
    def __init__(self, m: float = 1, k: float = 1, b: float = 0, a: float = 1, inverse: bool = False):
        self.m = m
        self.k = k
        self.b = b
        self.a = a
        self.inverse = inverse


class Curve:

    @staticmethod
    def clamp01(value: float) -> float:
        return max(min(value, 1), 0)

    @staticmethod
    def linear_quadratic(x: float, rules: CurveRules) -> float:
        val = (x / rules.m) ** rules.k + rules.b
        return val if not rules.inverse else 1 - val

    @staticmethod
    def logistic(x: float, rules: CurveRules) -> float:
        e = math.exp(1)
        val = 1 / (1 + math.exp(-rules.k*(4*e*(x-rules.m)-2*e))) / rules.a + rules.b
        return val if not rules.inverse else 1 - val

    @staticmethod
    def sin(x: float, rules: CurveRules) -> float:
        val = math.sin(x * math.pi * rules.k + rules.b)
        return val if not rules.inverse else 1 - val

    @staticmethod
    def boolean(x: float, rules: CurveRules) -> float:
        return 1 if x < rules.m else 0

    @staticmethod
    def exponential(x: float, rules: CurveRules) -> float:
        val = (1 - (x - rules.m)**2) / rules.k + rules.b
        return val if not rules.inverse else 1 - val
