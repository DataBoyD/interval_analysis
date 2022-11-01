import math

from practice_interval.interval_lib import *
from practice_interval.newton_method.one_dim.slope_module.slope_evaluators import evaluate_slope_otherwise_outer, \
    evaluate_slope_otherwise_internal
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_function_representation import Function
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_interval_extension import IntervalExtension


class Triplet:

    """
    Класс реализующий тройку объектов и пересчёт параметров

    (область значений, значение в точке, интервальный скос)
    """

    def __init__(self, interval, value_at_c, slope, f=None):
        self.interval = interval
        self.point = value_at_c
        self.slope = slope
        self.f = f

    @classmethod
    def from_number(cls, point: Decimal):
        return Triplet(Interval.valueToInterval(point), Interval.valueToInterval(point), Interval.valueToInterval(0))

    def __str__(self):
        return f"Triplet<interval={self.interval}, point={self.point}, slope={self.slope}>"

    def __add__(self, other):
        return Triplet(
            interval=self.interval + other.interval,
            value_at_c=self.point + other.point,
            slope=self.slope + other.slope
        )

    def __sub__(self, other):
        return Triplet(
            interval=self.interval - other.interval,
            value_at_c=self.point - other.point,
            slope=self.slope - other.slope
        )

    def __mul__(self, other):
        return Triplet(
            interval=self.interval * other.interval,
            value_at_c=self.point * other.point,
            slope=self.interval * other.slope + other.point * self.slope
        )

    def __pow__(self, power, modulo=None):
        t = self
        for i in range(power - 1):
            t *= self
        return t

    def __truediv__(self, other):
        if isinstance(other, Triplet):
            return Triplet(
                interval=self.interval / other.interval,
                value_at_c=self.point / other.point,
                slope=(self.slope - self.point / other.point * other.slope) / other.interval
            )

    def __neg__(self):
        return Triplet(
            interval=-self.interval,
            value_at_c=-self.point,
            slope=-self.slope
        )

    def __abs__(self):

        slope = Interval([
            (abs(self.interval[0]) - abs(self.point[0])) / (self.interval[0] - self.point[0]),
            (abs(self.interval[1]) - abs(self.point[1])) / (self.interval[1] - self.point[1])
        ])

        return Triplet(
            interval=Interval.abs(self.interval),
            value_at_c=Interval.abs(self.point),
            slope=slope * self.slope,
        )





