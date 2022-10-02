import math
from math import sin


from practice_interval.interval_lib import *
from intersection_tools import intersection


class IntervalExtensionFunction:
    def __init__(self, f):
        self.f = f

    def __call__(self, argument: Interval):
        return self.f(argument)


class NewtonIntervalIterationProcess:

    def __init__(self, f, first_der, primary_interval: Interval, domain, eps: float = 1e-20):
        self.f = f
        self.der = first_der
        self.primary_interval = primary_interval
        self.eps = eps
        self.domain = domain

    def start(self):
        result = self.primary_interval

        # сам итерационный процесс
        while result != None and result.width() > self.eps:

            # вычисляем середину интервала $$\Tilde{x}$$
            mid = (result[0] + result[1]) / 2

            # вычисляем обратный интервал к первой производной
            division = 1 / self.der(result)

            # Если содержится нуль, то интервал распадается на два луча
            if isinstance(division, list):

                # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
                for i in division:
                    newt_iter = mid - self.f(mid) * i
                    t = NewtonIntervalIterationProcess(self.f, self.der, intersection(result, newt_iter), self.domain)
                    t.start()
                break
            else:

                # в обычной ситуации действуем по привычному алгоритму
                newt_iter = mid - self.f(mid) / self.der(result)
                # чтобы не допустить попадание None в массив результатов, добавляем данное условие
                if intersection(result, newt_iter) is None:
                    break

                result = intersection(result, newt_iter)

                if result.width() <= self.eps:
                    self.domain.common_base.append(result)


# аккумулирующий класс с хранилищем результатов итерационных процессов
class NewtonComputations:

    common_base = []

    def __init__(self, f, first_der, primary_interval: Interval, eps: float = 1e-20):
        self.f = f
        self.der = IntervalExtensionFunction(first_der)
        self.primary_interval = primary_interval
        self.eps = eps

    def run(self):
        nip = NewtonIntervalIterationProcess(self.f, self.der, self.primary_interval, self, self.eps)
        nip.start()
