from decimal import Decimal

import numpy as np

from practice_interval.interval_lib import Interval


def intersection(a: Interval, b: Interval):

    if isinstance(a, np.ndarray):
        a = a[0]
    if isinstance(b, np.ndarray):
        b = b[0]


    A_boundary = max(a[0], b[0])
    B_boundary = min(a[1], b[1])

    if A_boundary <= B_boundary:
        return Interval([A_boundary, B_boundary])
    else:
        return None

