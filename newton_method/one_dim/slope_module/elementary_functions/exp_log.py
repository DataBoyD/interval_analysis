from practice_interval.newton_method.one_dim.slope_module.slope_evaluators import evaluate_slope_otherwise_outer, \
    evaluate_slope_otherwise_internal
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet


def triplet_exp(triplet: Triplet):
    """
      Вычисление показательной функции от тройки объектов [Triplet]

      :param triplet:
      :return: Triplet
      """
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
    """
      Вычисление натурального логарифма от тройки объектов [Triplet]

      :param triplet:
      :return: Triplet
      """
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

