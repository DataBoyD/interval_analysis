import math

from practice_interval.interval_lib import *
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_function_representation import Function
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_interval_extension import IntervalExtension


class Triplet:

    def __init__(self, interval, value_at_c, slope):
        self.interval = interval
        self.point = value_at_c
        self.slope = slope

    @classmethod
    def from_number(cls, point: Decimal):
        return Triplet(Interval.valueToInterval(point), Interval.valueToInterval(point), 0)

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
            value_at_c=-self.interval,
            slope=-self.slope
        )


def triplet_sin(triplet: Triplet) -> Triplet:
    slope = evaluate_slope_otherwise_internal(internal_triplet_range=triplet.interval,
                                              internal_triplet_at_c=triplet.point,
                                              outer_triplet_range=triplet.interval.sin(triplet.interval),
                                              outer_triplet_at_c=triplet.point.sin(triplet.point))


    # if isinstance(triplet.slope, Interval):
    #     slope = triplet.slope.cos(triplet.slope) * triplet.slope
    # else:
    #     slope = math.cos(triplet.slope) * triplet.slope

    return Triplet(
        value_at_c=triplet.point.sin(triplet.point),
        slope=slope * triplet.slope,
        interval=triplet.interval.sin(triplet.interval)
    )


def triplet_cos(triplet: Triplet) -> Triplet:
    slope = evaluate_slope_otherwise_internal(internal_triplet_range=triplet.interval,
                                              internal_triplet_at_c=triplet.point,
                                              outer_triplet_range=triplet.interval.cos(triplet.interval),
                                              outer_triplet_at_c=triplet.point.cos(triplet.point))
    # if isinstance(triplet.slope, Interval):
    #     slope = -triplet.slope.sin(triplet.slope) * triplet.slope
    # else:
    #     slope = -math.sin(triplet.slope) * triplet.slope

    return Triplet(
        value_at_c=triplet.point.cos(triplet.point),
        slope=slope * triplet.slope,
        interval=triplet.interval.cos(triplet.interval)
    )


def triplet_exp(triplet: Triplet):
    slope = evaluate_slope_otherwise_outer(internal_triplet_range=triplet.interval,
                                           internal_triplet_at_c=triplet.point,
                                           outer_triplet_range=triplet.interval.exp(triplet.interval),
                                           outer_triplet_at_c=triplet.point.exp(triplet.point)
                                           )
    # print("triplet: ", triplet)
    # print("SLOPE: ", slope)
    return Triplet(
        value_at_c=triplet.point.exp(triplet.point),
        slope=slope * triplet.slope,
        interval=triplet.interval.exp(triplet.interval)
    )


def triplet_log(triplet: Triplet):
    slope = evaluate_slope_otherwise_internal(internal_triplet_range=triplet.interval,
                                              internal_triplet_at_c=triplet.point,
                                              outer_triplet_range=triplet.interval.ln(triplet.interval),
                                              outer_triplet_at_c=triplet.point.ln(triplet.point)
                                              )
    # print("triplet: ", triplet)
    # print("SLOPE: ", slope)
    return Triplet(
        value_at_c=triplet.point.ln(triplet.point),
        slope=slope * triplet.slope,
        interval=triplet.interval.ln(triplet.interval)
    )


def evaluate_slope_otherwise_internal(internal_triplet_range,
                                      internal_triplet_at_c,
                                      outer_triplet_range,
                                      outer_triplet_at_c: Interval):
    if internal_triplet_range[0] != internal_triplet_at_c[0] and internal_triplet_range[1] != internal_triplet_at_c[1]:
        return Interval([
            (outer_triplet_range[0] - outer_triplet_at_c[0]) / (internal_triplet_range[0] - internal_triplet_at_c[0]),
            (outer_triplet_range[1] - outer_triplet_at_c[1]) / (internal_triplet_range[1] - internal_triplet_at_c[1])

        ])
    else:
        # return outer_triplet_range
        # possible returning result
        return 1 / internal_triplet_range


def evaluate_slope_otherwise_outer(internal_triplet_range,
                                   internal_triplet_at_c,
                                   outer_triplet_range,
                                   outer_triplet_at_c: Interval):
    if internal_triplet_range[0] != internal_triplet_at_c[0] and internal_triplet_range[1] != internal_triplet_at_c[1]:
        return Interval([
            (outer_triplet_range[0] - outer_triplet_at_c[0]) / (internal_triplet_range[0] - internal_triplet_at_c[0]),
            (outer_triplet_range[1] - outer_triplet_at_c[1]) / (internal_triplet_range[1] - internal_triplet_at_c[1])

        ])
    else:
        return outer_triplet_range
        # possible returning result
        # return 1 / internal_triplet_range
