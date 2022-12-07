import dataclasses
import math
from decimal import Decimal
from typing import List

from practice_interval.interval_lib import Interval
from practice_interval.newton_method.one_dim.intersection_tools import intersection
from practice_interval.newton_method.one_dim.one_dim_class import NewtonComputations
from practice_interval.newton_method.one_dim.slope_module.elementary_functions import triplet_cos, triplet_sin
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet


class Func:
    def __init__(self, str_repr: str, f):
        self.str_repr = str_repr
        self.f = f

    def __call__(self, x):
        return self.f(x)

    def __str__(self):
        return self.str_repr

    def __repr__(self):
        return self.str_repr


@dataclasses.dataclass
class Pair:
    '''
    Элементы кусочно заданных функций

    f: Func - функция, принимающая triplet или decimal

    constraint: Interval - интервал, на котором определена f
    '''
    f: Func
    constraint: List[Interval]


class Piecewise:

    def __init__(self, pairs: List[Pair]):
        self.pairs = pairs
        self.repository = []

    def run_with_slope(self, primary_interval: Interval):
        for p in self.pairs:
            for sub_interval in p.constraint:
                intersection_result = intersection(sub_interval, primary_interval)
                if intersection_result is not None:
                    n = NewtonComputations(p.f, p.f, 0, intersection_result, eps=1e-5)
                    n.run_slope()
                    if len(n.common_base) > 0:
                        self.repository.append(n.common_base.copy())
                    # n.common_base.clear()
        print(f"COMMON REPO: {self.repository}")


# p: List[Pair] = [
#     Pair(
#         Func("f1", lambda x: triplet_cos(Triplet.from_number(5) * x) if isinstance(x, Triplet) else math.cos(5 * x)),
#         Interval(["-Infinity", 3 / 2 * math.pi])
#     ),
#     Pair(
#         Func("f2", lambda x: triplet_cos(x) if isinstance(x, Triplet) else math.cos(x)),
#         Interval(["Infinity", 3 / 2 * math.pi])
#     )
# ]


p: List[Pair] = [
    Pair(
        Func("f1", lambda x: -x + Triplet.from_number(4) if isinstance(x, Triplet) else -x + 4),
        [Interval(["-Infinity", 3])]
    ),
    Pair(
        Func("f2", lambda x: Triplet.from_number(Decimal(- 8 / 9)) * x ** 2 + Triplet.from_number(
            8) * x - Triplet.from_number(17) if isinstance(x, Triplet) else Decimal((-8 / 9)) * x ** 2 + 8 * x - 17),
        [Interval([3, 6])]
    ),
    Pair(
        Func("f1", lambda x: x - Triplet.from_number(5) if isinstance(x, Triplet) else x - 5),
        [Interval([6, "Infinity"])]
    )
]

# p: List[Pair] = [
#     Pair(
#         Func("f1", lambda x: triplet_cos(Triplet.from_number(5) * x) if isinstance(x, Triplet) else math.cos(5 * x)),
#         [Interval([3 / 2 * math.pi, 5 / 2 * math.pi])]
#     ),
#     Pair(
#         Func("f2", lambda x: triplet_cos(x) if isinstance(x, Triplet) else math.cos(x)),
#         [Interval(["-Infinity", 3 / 2 * math.pi]),  Interval(["Infinity", 5 / 2 * math.pi])]
#     )
# ]

# p: List[Pair] = [
#     Pair(
#         Func("f1", lambda x: triplet_sin(Triplet.from_number(5) * x) + Triplet.from_number(2) if isinstance(x, Triplet) else math.sin(5 * x) + 2),
#         [Interval(["-Infinity", math.pi])]
#     ),
#     Pair(
#         Func("f2", lambda x: Triplet.from_number(5) * triplet_sin(x) + Triplet.from_number(2) if isinstance(x, Triplet) else 5 * math.sin(x) + 2),
#         [Interval(["Infinity", math.pi])]
#     )
# ]


piec = Piecewise(p)
primary = Interval([-10, 10])
piec.run_with_slope(primary)
