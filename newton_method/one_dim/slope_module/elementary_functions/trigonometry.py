import math
from decimal import Decimal

from practice_interval.interval_lib import Interval
from practice_interval.newton_method.one_dim.slope_module.slope_evaluators import evaluate_slope_otherwise_internal, evaluate_slope_otherwise_outer
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet


def triplet_sin(triplet: Triplet) -> Triplet:
    """
    Вычисление синуса от тройки объектов [Triplet]

    :param triplet:
    :return: Triplet
    """
    # slope = evaluate_slope_otherwise_internal(internal_triplet_range=triplet.interval,
    #                                           internal_triplet_at_c=triplet.point,
    #                                           outer_triplet_range=triplet.interval.sin(triplet.interval),
    #                                           outer_triplet_at_c=triplet.point.sin(triplet.point)
    #                                           )

    # slope = evaluate_slope_otherwise_outer(internal_triplet_range=triplet.interval,
    #                                           internal_triplet_at_c=triplet.point,
    #                                           outer_triplet_range=triplet.interval.sin(triplet.interval),
    #                                           outer_triplet_at_c=triplet.point.sin(triplet.point)
    #                                           )
    #

    return Triplet(
        value_at_c=triplet.point.sin(triplet.point),
        slope=triplet.interval.cos(triplet.interval) * triplet.slope,
        # slope=slope * triplet.slope,
        # slope=triplet.slope * Interval([-8.9, 8.9]),
        interval=triplet.interval.sin(triplet.interval)
    )


def triplet_cos(triplet: Triplet) -> Triplet:
    """
      Вычисление косинуса от тройки объектов [Triplet]

      :param triplet:
      :return: Triplet
      """
    # slope = evaluate_slope_otherwise_internal(internal_triplet_range=triplet.interval,
    #                                           internal_triplet_at_c=triplet.point,
    #                                           outer_triplet_range=triplet.interval.cos(triplet.interval),
    #                                           outer_triplet_at_c=triplet.point.cos(triplet.point))

    return Triplet(
        value_at_c=triplet.point.cos(triplet.point),
        slope=-triplet.interval.sin(triplet.interval) * triplet.slope,
        interval=triplet.interval.cos(triplet.interval)
    )
