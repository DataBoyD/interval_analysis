import numpy as np
import copy

from practice_interval.interval_lib import *
from practice_interval.newton_method.high_dim.matrix_inversion import MatrixInversion


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


class HightDimensionalIntervalNewtonProcess:

    def __init__(self, f, jacobian, primary_value, precision = 1e-15):
        self.f = f
        self.jacoby_matrix = jacobian
        self.primary_value = primary_value
        self.eps = precision

    def get_middle_point(self, point):
        result = []
        for d in point:
            result.append((d[0][0] + d[0][1]) / 2)
        return np.array(result).reshape(-1, 1)

    def intersect(self, result, newt_iter):
        new_array = []

        for i in range(result.shape[0]):
            new_array.append(intersection(result[i][0], newt_iter[i][0]))

        return np.array(new_array).reshape(-1, 1)

    def start(self):
        result = self.primary_value
        while any([elem[0] is None for elem in result]) is False and all([elem[0].width() >= self.eps for elem in result]):
            jacobian_inv = MatrixInversion(self.jacoby_matrix(result))
            mid = self.get_middle_point(result)
            newt_iter = mid - jacobian_inv() @ self.f(mid)
            if any([elem[0] is None for elem in self.intersect(result, newt_iter)]):
                    break
            result = self.intersect(result, newt_iter)
        print(result)
