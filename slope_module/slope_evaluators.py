# from practice_interval.interval_lib import Interval
from interval_lib import Interval


def evaluate_slope_otherwise_internal(internal_triplet_range,
                                      internal_triplet_at_c,
                                      outer_triplet_range,
                                      outer_triplet_at_c: Interval) -> Interval:
    """
      Вычисление интервального скоса для вогнутой функции

      :param internal_triplet_range:
      :param internal_triplet_at_c:
      :param outer_triplet_range:
      :param outer_triplet_at_c:
      :return: Interval


      """
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
                                   outer_triplet_at_c: Interval) -> Interval:
    """
    Вычисление интервального скоса для выпуклой функции

    :param internal_triplet_range:
    :param internal_triplet_at_c:
    :param outer_triplet_range:
    :param outer_triplet_at_c:
    :return: Interval


    """
    if internal_triplet_range[0] != internal_triplet_at_c[0] and internal_triplet_range[1] != internal_triplet_at_c[1]:
        return Interval([
            (outer_triplet_range[0] - outer_triplet_at_c[0]) / (internal_triplet_range[0] - internal_triplet_at_c[0]),
            (outer_triplet_range[1] - outer_triplet_at_c[1]) / (internal_triplet_range[1] - internal_triplet_at_c[1])

        ])
    # else:
    #     return outer_triplet_range
        # possible returning result
        # return 1 / internal_triplet_range
