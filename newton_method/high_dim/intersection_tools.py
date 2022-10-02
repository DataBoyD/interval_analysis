from decimal import Decimal

import numpy as np

from practice_interval.interval_lib import Interval


def intersection(a: Interval, b: Interval):

    if isinstance(a, np.ndarray):
        a = a[0]
    if isinstance(b, np.ndarray):
        b = b[0]

    # проверка на отсутствие пересечения интервалов
    if (Decimal(a[1]) < Decimal(b[0]) and Decimal(a[1]) < Decimal(b[1])) or\
            (Decimal(b[1]) < Decimal(a[0]) and Decimal(b[1]) < Decimal(a[1])):
        return None

    # проверка на нормальное пересечение
    if Decimal(a[0]) < Decimal(b[0]) and Decimal(a[1]) < Decimal(b[1]):
        return Interval([b[0], a[1]])

    # проверка на нормальное пересечение №2
    if Decimal(b[0]) < Decimal(a[0]) and Decimal(b[1]) < Decimal(a[1]):
        return Interval([a[0], b[1]])

    # проверка на вложенность
    if a.isIn(b):
        return a

    # проверка на вложенность №2
    if b.isIn(a):
        return b

    if a == b:
        return a
