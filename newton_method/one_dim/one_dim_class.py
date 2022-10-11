import math
from math import sin
from sys import setrecursionlimit


setrecursionlimit(20000)


from practice_interval.interval_lib import *
from intersection_tools import intersection


class IntervalExtensionFunction:
    def __init__(self, f):
        self.f = f

    def __call__(self, argument: Interval):
        return self.f(argument)


class NewtonIntervalIterationProcess:


    def __init__(self, f, func_ext, first_der, primary_interval: Interval, domain, eps: float):

        """ Одномерный метод Ньютона в интервальном виде
             Параметры:

                f - одномерная функция в аналитическом виде (lambda-выражение) \n
                first_der - первая производная f (lambda-выражение) \n
                domain - хранилище данных (внутренняя переменная) \n
                primary_value - начальное приближение \n
                precision - точность вычислений \n
             """


        self.f = f
        self.func_ext = func_ext
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
                    newt_iter = mid - Decimal(float(self.f(float(mid)))) * i
                    t = NewtonIntervalIterationProcess(self.f,
                                                       self.func_ext,
                                                       self.der,
                                                       intersection(result, newt_iter),
                                                       self.domain,
                                                       eps=self.eps)
                    t.start()
                break
            else:

                # в обычной ситуации действуем по привычному алгоритму
                newt_iter = mid - Decimal(float(self.f(float(mid)))) / self.der(result)
                # чтобы не допустить попадание None в массив результатов, добавляем данное условие
                if intersection(result, newt_iter) is None:
                    if result.width() <= self.eps and Interval([0,0]).isIn(self.func_ext(result)):
                        print("Add!")
                        self.domain.common_base.append(result)
                    break

                result = intersection(result, newt_iter)

                if result.width() <= self.eps and Interval([0, 0]).isIn(self.func_ext(result)):
                    self.domain.common_base.append(result)
                    break
        # else:
        #     if result is not None:
        #         if result.width() <= self.eps and Interval([0, 0]).isIn(self.func_ext(result)):
        #             if len(self.domain.common_base) == 0:
        #                 self.domain.common_base.append(result)
        #             for item in self.domain.common_base:
        #                 if abs(item[0] - result[0]) > 1e-1:
        #                     self.domain.common_base.append(result)
        #                     return




# аккумулирующий класс с хранилищем результатов итерационных процессов
class NewtonComputations:

    common_base = []

    def __init__(self, f, func_ext, first_der, primary_interval: Interval, eps: float):
        self.f = f
        self.func_ext = func_ext
        self.der = IntervalExtensionFunction(first_der)
        self.primary_interval = primary_interval
        self.eps = eps

    def run(self):
        nip = NewtonIntervalIterationProcess(self.f, self.func_ext, self.der, self.primary_interval, self, self.eps)
        nip.start()
