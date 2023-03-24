import math
from decimal import Decimal

from interval_lib import Interval
from slope_module.triplet_entity import Triplet


# from practice_interval.interval_lib import Interval
# from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet


def triplet_signum(triplet: Triplet):
    """
      Вычисление функции знака от тройки объектов [Triplet]

      :param triplet:
      :return: Triplet
      """
    return Triplet(
        value_at_c=signum_for_undefined_value(triplet.point),
        interval=signum_for_undefined_value(triplet.interval),
        # slope=Interval.valueToInterval(0)
        slope=signum_slope(triplet) * triplet.slope
    )


# def triplet_signum(triplet: Triplet):
#     """
#       Вычисление функции знака от тройки объектов [Triplet]
#
#       :param triplet:
#       :return: Triplet
#       """
#
#     return Triplet(
#         value_at_c=sigma(triplet.point),
#         interval=signum_for_undefined_value(triplet.interval),
#         slope=(sigma(triplet.slope)) * (1 - sigma(triplet.slope))
#         # slope=(1+signum(triplet.slope)) * (1 - signum(triplet.slope))
#     )


def sigma(x):
    prec = 1e9
    if isinstance(x, Decimal):
        return Decimal(2 / (1 + math.exp(-Decimal(prec) * x)) - 1)
    if isinstance(x, Interval):
        return 2 / (1 + Interval.exp(-prec * x)) - 1
    if isinstance(x, int):
        return Decimal(2 / (1 + math.exp(-prec * x)) - 1)
    if isinstance(x, float):
        return Decimal(2 / (1 + math.exp(-prec * x)) - 1)
    print("WOW", x)


def signum(x):
    prec = 50
    if isinstance(x, Decimal):
        return Decimal(math.exp(prec * x) - (math.exp(-prec * x))) / Decimal(math.exp(prec * x) + (math.exp(-prec * x)))
    if isinstance(x, Interval):
        return (Interval.exp(prec * x) - (Interval.exp(-prec * x))) / (
                Interval.exp(prec * x) + (Interval.exp(-prec * x)))
    if isinstance(x, int):
        return Decimal(math.exp(prec * x) - (math.exp(-prec * x))) / Decimal(math.exp(prec * x) + (math.exp(-prec * x)))
    if isinstance(x, float):
        return Decimal(math.exp(prec * x) - (math.exp(-prec * x))) / Decimal(math.exp(prec * x) + (math.exp(-prec * x)))


def signum_for_undefined_value(value_at_c: Decimal | Interval):
    if isinstance(value_at_c, Decimal):
        if value_at_c == 0:
            return Interval.valueToInterval(0)
        elif value_at_c < 0:
            return Interval.valueToInterval(-1)
        else:
            return Interval.valueToInterval(1)

    if isinstance(value_at_c, Interval):
        if value_at_c[0] == value_at_c[1] == 0:
            return Interval.valueToInterval(0)
        elif value_at_c[0] > 0 and value_at_c[1] > 0:
            return Interval.valueToInterval(1)
        elif value_at_c[0] < 0 and value_at_c[1] < 0:
            return Interval.valueToInterval(-1)
        else:
            return Interval([-1, 1])


def signum_slope(t):
    if t.interval[0] == t.interval[1]:

        return Interval([1/abs(t.interval[0]), "Infinity"])

    mid = (t.interval[0] + t.interval[1]) / 2

    if t.interval[0] < 0:
        if mid > 0:
            left = (-2) / (t.interval[0] - mid)
        else:
            left = 0
    else:
        if mid > 0:
            left = 0
        else:
            left = 2 / (t.interval[0] - mid)

    if t.interval[1] < 0:
        if mid > 0:
            right = (-2) / (t.interval[1] - mid)
        else:
            right = 0
    else:
        if mid > 0:
            right = 0
        else:
            right = 2 / (t.interval[1] - mid)

    if mid > 0:
        zero = 1 / mid
    else:
        zero = -1 / mid

    # print(f"\n\nINTERVAL: {t.interval}\n\nLEFT: {left}\nRIGHT: {right}\nZERO: {zero}\n\n")

    return Interval([min(left, right, zero), max(left, right, zero)])

    # if isinstance(sl, Decimal):
    #     if sl == 0:
    #         return Interval.valueToInterval(Decimal("Infinity"))
    #     else:
    #         return Interval.valueToInterval(0)
    #
    # if isinstance(sl, int):
    #     if sl == 0:
    #         return Interval.valueToInterval(Decimal("Infinity"))
    #     else:
    #         return Interval.valueToInterval(0)
