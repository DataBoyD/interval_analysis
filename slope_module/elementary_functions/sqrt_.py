from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet


def triplet_sqrt(triplet: Triplet):
    """
      Вычисление квадратного корня от тройки объектов [Triplet]

      :param triplet:
      :return: Triplet
      """
    return Triplet(
        value_at_c=triplet.point ** 0.5,
        interval=triplet.interval ** 0.5,
        slope=triplet.slope / (triplet.point ** 0.5 + triplet.interval ** 0.5)
    )