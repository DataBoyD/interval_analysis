from practice_interval.interval_lib import Interval


def intersection(a: Interval, b: Interval):

    A_boundary = max(a[0], b[0])
    B_boundary = min(a[1], b[1])

    if A_boundary <= B_boundary:
        return Interval([A_boundary, B_boundary])
    else:
        return None




