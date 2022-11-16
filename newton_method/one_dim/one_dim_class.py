import math
from math import sin
from sys import setrecursionlimit
from decimal import Decimal




from practice_interval.interval_lib import *
from intersection_tools import intersection
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet

setrecursionlimit(20000)

#TODO: если середина непредставима (ошибки округления),
# то необходимо использовать 'интервалозначную' середину



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

            print(result.width())
            # print(f"RESULT: {result}\n"
            #       f"WIDTH: {result.width()}\n"
            #       f"EPS: {self.eps}")

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
                    if result.width() <= self.eps and Interval([0, 0]).isIn(self.func_ext(result)):
                        self.domain.common_base.append(result)
                    break

                result = intersection(result, newt_iter)

                if result.width() <= self.eps and Interval([0, 0]).isIn(self.func_ext(result)):
                    self.domain.common_base.append(result)
                    break

    # def start_with_slope(self):
    #
    #     result = self.primary_interval
    #
    #     # сам итерационный процесс
    #     while result != None and result.width() > self.eps:
    #         # print(f"RESULT: {result}\n"
    #         #       f"WIDTH: {result.width()}\n"
    #         #       f"EPS: {self.eps}")
    #
    #         # вычисляем середину интервала $$\Tilde{x}$$
    #         mid = (result[0] + result[1]) / 2
    #         print("MID: ", mid)
    #
    #         triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
    #         print("TRIPLE: ", triplet )
    #
    #         # вычисляем обратный интервал к первой производной
    #         division = 1 / self.f(triplet).slope
    #
    #         # Если содержится нуль, то интервал распадается на два луча
    #         if isinstance(division, list):
    #
    #             # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
    #             for i in division:
    #                 newt_iter = mid - self.f(mid) * i
    #                 print("NEWT OPER: ", newt_iter)
    #
    #                 # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) * i
    #
    #                 t = NewtonIntervalIterationProcess(self.f,
    #                                                    self.func_ext,
    #                                                    self.der,
    #                                                    intersection(result, newt_iter),
    #                                                    self.domain,
    #                                                    eps=self.eps)
    #                 t.start_with_slope()
    #             break
    #         else:
    #
    #             # в обычной ситуации действуем по привычному алгоритму
    #             triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
    #             newt_iter = mid - self.f(mid) / self.f(triplet).slope
    #             print("TRIPLE: ", triplet)
    #             print("NEWT OPER: ", newt_iter)
    #             # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) / self.f(triplet).slope
    #
    #             # чтобы не допустить попадание None в массив результатов, добавляем данное условие
    #             if intersection(result, newt_iter) is None:
    #                 if result.width() <= self.eps:
    #                     self.domain.common_base.append(result)
    #                 break
    #
    #             result = intersection(result, newt_iter)
    #             print("RESULT: ", result)
    #             if result.width() <= self.eps:
    #                 self.domain.common_base.append(result)
    #                 break
    # new version --------------------------------------
    def start_with_slope(self):

        result = self.primary_interval

        # сам итерационный процесс
        while result != None and result.width() > self.eps:

            print(result.width())

            # print(f"RESULT: {result}\n"
            #       f"WIDTH: {result.width()}\n"
            #       f"EPS: {self.eps}")

            # вычисляем середину интервала $$\Tilde{x}$$
            mid = (result[0] + result[1]) / 2
            # print("MID: ", mid)

            triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
            print("TRIPLE: ", triplet)

            if isinstance(self.f(triplet), list):
                for tr in self.f(triplet):
                    # вычисляем обратный интервал к первой производной
                    division = 1 / tr.slope

                    # Если содержится нуль, то интервал распадается на два луча
                    if isinstance(division, list):

                        # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
                        for i in division:
                            newt_iter = mid - self.f(mid) * i
                            # print("NEWT OPER: ", newt_iter)

                            # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) * i
                            print("Вложенность")

                            t = NewtonIntervalIterationProcess(self.f,
                                                               self.func_ext,
                                                               self.der,
                                                               intersection(result, newt_iter),
                                                               self.domain,
                                                               eps=self.eps)
                            t.start_with_slope()
                        print(
                            "Stop!!!!!!!!!!!!!!!!!!"
                        )
                        break
                    else:

                        # в обычной ситуации действуем по привычному алгоритму
                        triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
                        newt_iter = mid - self.f(mid) / self.f(triplet)[0].slope
                        # print("TRIPLE: ", triplet)
                        # print("NEWT OPER: ", newt_iter)
                        # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) / self.f(triplet).slope

                        # чтобы не допустить попадание None в массив результатов, добавляем данное условие
                        if intersection(result, newt_iter) is None:
                            if result.width() <= self.eps:
                                self.domain.common_base.append(result)
                            break

                        result = intersection(result, newt_iter)
                        if result.width() <= self.eps:
                            print("RESULT: ", result)
                            self.domain.common_base.append(result)
                            break
            else:

                # вычисляем обратный интервал к первой производной
                division = 1 / self.f(triplet).slope

                # Если содержится нуль, то интервал распадается на два луча
                if isinstance(division, list):

                    # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
                    for i in division:
                        newt_iter = mid - self.f(mid) * i
                        print("NEWT OPER: ", newt_iter)

                        # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) * i

                        t = NewtonIntervalIterationProcess(self.f,
                                                           self.func_ext,
                                                           self.der,
                                                           intersection(result, newt_iter),
                                                           self.domain,
                                                           eps=self.eps)
                        t.start_with_slope()
                    break
                else:

                    # в обычной ситуации действуем по привычному алгоритму
                    triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
                    newt_iter = mid - self.f(mid) / self.f(triplet).slope
                    print("TRIPLE: ", triplet)
                    print("NEWT OPER: ", newt_iter)
                    # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) / self.f(triplet).slope

                    # чтобы не допустить попадание None в массив результатов, добавляем данное условие
                    if intersection(result, newt_iter) is None:
                        if result.width() <= self.eps:
                            self.domain.common_base.append(result)
                        break

                    result = intersection(result, newt_iter)
                    print("RESULT: ", result)
                    if result.width() <= self.eps:
                        self.domain.common_base.append(result)
                        break


# аккумулирующий класс с хранилищем результатов итерационных процессов
class NewtonComputations:

    # common_base = []

    def __init__(self, f, func_ext, first_der, primary_interval: Interval, eps: float):
        self.f = f
        self.func_ext = func_ext
        self.der = IntervalExtensionFunction(first_der)
        self.primary_interval = primary_interval
        self.eps = eps
        self.common_base = []

    def run_slope(self):
        nip = NewtonIntervalIterationProcess(self.f, self.func_ext, self.der, self.primary_interval, self, self.eps)
        nip.start_with_slope()

    def run(self):
        nip = NewtonIntervalIterationProcess(self.f, self.func_ext, self.der, self.primary_interval, self, self.eps)
        nip.start()

