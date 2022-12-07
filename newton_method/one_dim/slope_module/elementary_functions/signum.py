from decimal import Decimal

from practice_interval.interval_lib import Interval
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet


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
        slope=signum_slope(triplet.slope)
    )


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


def signum_slope(sl):
    if isinstance(sl, Interval):
        if Interval.valueToInterval(0).isIn(sl):
            return Interval.valueToInterval(Decimal("Infinity"))
        else:
            return Interval.valueToInterval(0)

    if isinstance(sl, Decimal):
        if sl == 0:
            return Interval.valueToInterval(Decimal("Infinity"))
        else:
            return Interval.valueToInterval(0)

    if isinstance(sl, int):
        if sl == 0:
            return Interval.valueToInterval(Decimal("Infinity"))
        else:
            return Interval.valueToInterval(0)