import math
from math import sin
from sys import setrecursionlimit
from decimal import Decimal

from practice_interval.interval_lib import *
from intersection_tools import intersection
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet

setrecursionlimit(20000)


# TODO: если середина непредставима (ошибки округления),
# то необходимо использовать 'интервалозначную' середину


class IntervalExtensionFunction:
    def __init__(self, f):
        self.f = f

    def __call__(self, argument: Interval):
        return self.f(argument)


class NewtonIntervalIterationProcess:

    def __init__(self, f, func_ext, first_der, primary_interval: Interval, domain, eps: float, int_level):

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
        self.level = int_level

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

    def start_with_slope(self):

        result = self.primary_interval
        # self.domain.iter_tools += 4 * self.level * " " + f"{result}\n"

        # сам итерационный процесс
        while result != None and result.width() > self.eps:
            # print("Промежуточный результат: ", result)

            # вычисляем середину интервала $$\Tilde{x}$$
            mid = (result[0] + result[1]) / 2
            # print("MID: ", mid)

            triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
            # print("TRIPLE: ", triplet)

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
                            # print("Вложенность")
                            # print(f"Из {result}")
                            self.domain.iter_tools += 4 * (
                                    self.level + 1) * " " + f"Из {result}\n"

                            self.domain.iter_tools += 4 * (
                                    self.level + 1) * " " + f"{intersection(result, newt_iter)}\n"
                            result_iter = intersection(newt_iter, result)
                            # if result_iter is not None and result_iter.width() <= self.eps and Interval.valueToInterval(
                            #         0).isIn(self.f(result_iter)):
                            #     print("Добавили при вложенности: ", result_iter, result_iter.width())
                            #     self.domain.common_base.append(result_iter)
                            #
                            # else:

                            t = NewtonIntervalIterationProcess(self.f,
                                                               self.func_ext,
                                                               self.der,
                                                               result_iter,
                                                               self.domain,
                                                               eps=self.eps,
                                                               int_level=self.level + 1)

                            t.start_with_slope()

                        break
                    else:

                        # в обычной ситуации действуем по привычному алгоритму
                        triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
                        newt_iter = mid - self.f(mid) / self.f(triplet)[0].slope

                        # чтобы не допустить попадание None в массив результатов, добавляем данное условие
                        if intersection(result, newt_iter) is None:
                            if result.width() <= self.eps:
                                self.domain.common_base.append(result)
                            break

                        # self.domain.iter_tools += f"{intersection(result, newt_iter)}\n"
                        self.domain.iter_tools += 4 * (self.level) * " " + f"{intersection(result, newt_iter)}\n"

                        result = intersection(result, newt_iter)
                        if result.width() <= self.eps:
                            # print("RESULT: ", result)
                            self.domain.common_base.append(result)
                            break
            else:

                # вычисляем обратный интервал к первой производной
                division = 1 / self.f(triplet).slope

                # Если содержится нуль, то интервал распадается на два луча

                if isinstance(division, list):

                    # for i in division:
                    #     newt_iter = mid - self.f(mid) * i
                    #     self.domain.iter_tools += 4 * (self.level + 1) * "-" + f" {intersection(result, newt_iter)}\n"
                    #     # self.domain.iter_tools += f"    {intersection(result, newt_iter)}\n"

                    # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
                    for i in division:
                        newt_iter = mid - self.f(mid) * i
                        # print("NEWT OPER: ", newt_iter)

                        # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) * i
                        self.domain.iter_tools += 4 * (
                                self.level + 1) * " " + f"Из {result}\n"

                        self.domain.iter_tools += 4 * (self.level + 1) * " " + f"{intersection(result, newt_iter)}\n"
                        result_iter = intersection(result, newt_iter)
                        # # if result_iter is not None and result_iter.width() <= self.eps and Interval.valueToInterval(0).isIn(self.func_ext(result_iter)):
                        # #     print("Добавили при вложенности: ", result_iter, result_iter.width())
                        # #     self.domain.common_base.append(result_iter)
                        #
                        # else:

                        t = NewtonIntervalIterationProcess(self.f,
                                                               self.func_ext,
                                                               self.der,
                                                               result_iter,
                                                               self.domain,
                                                               eps=self.eps,
                                                               int_level=self.level + 1)

                        t.start_with_slope()

                    break
                else:

                    # в обычной ситуации действуем по привычному алгоритму
                    triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
                    newt_iter = mid - self.f(mid) / self.f(triplet).slope
                    # print("TRIPLE: ", triplet)
                    # print("NEWT OPER: ", newt_iter)
                    # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) / self.f(triplet).slope

                    # чтобы не допустить попадание None в массив результатов, добавляем данное условие
                    if intersection(result, newt_iter) is None:
                        if result.width() <= self.eps:
                            # print(result)
                            self.domain.common_base.append(result)
                        break
                    # self.domain.iter_tools += f"{intersection(result, newt_iter)}\n"
                    self.domain.iter_tools += 4 * (self.level) * " " + f"{intersection(result, newt_iter)}\n"

                    result = intersection(result, newt_iter)
                    # print("RESULT: ", result)
                    if result.width() <= self.eps:
                        # print(result)
                        self.domain.common_base.append(result)
                        break
        # else:
        #     if result is not None:
        #         self.domain.common_base.append(result)

    # def start_with_slope(self):
    #
    #     result = self.primary_interval
    #     # iter_tool.append(result)
    #
    #     # сам итерационный процесс
    #     while result != None and result.width() > self.eps:
    #
    #         # вычисляем середину интервала $$\Tilde{x}$$
    #         mid = (result[0] + result[1]) / 2
    #         # print("MID: ", mid)
    #         iteration_result = []
    #
    #         triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
    #         print("TRIPLE: ", triplet)
    #
    #         if isinstance(self.f(triplet), list):
    #             # iteration_result = []
    #             for tr in self.f(triplet):
    #                 # вычисляем обратный интервал к первой производной
    #                 division = 1 / tr.slope
    #
    #                 # Если содержится нуль, то интервал распадается на два луча
    #                 if isinstance(division, list):
    #
    #                     # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
    #                     for i in division:
    #                         newt_iter = mid - self.f(mid) * i
    #                         if intersection(result, newt_iter) is not None:
    #                             iteration_result.append(intersection(result, newt_iter))
    #                 else:
    #
    #                     # в обычной ситуации действуем по привычному алгоритму
    #                     triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
    #                     newt_iter = mid - self.f(mid) / self.f(triplet)[0].slope
    #
    #                     iteration_result.append(intersection(result, newt_iter))
    #
    #             ###################################
    #             for tr in self.f(triplet):
    #                 # вычисляем обратный интервал к первой производной
    #                 division = 1 / tr.slope
    #
    #                 # Если содержится нуль, то интервал распадается на два луча
    #                 if isinstance(division, list):
    #
    #                     # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
    #                     for i in division:
    #                         newt_iter = mid - self.f(mid) * i
    #                         # print("NEWT OPER: ", newt_iter)
    #
    #                         # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) * i
    #                         print("Вложенность")
    #
    #                         t = NewtonIntervalIterationProcess(self.f,
    #                                                            self.func_ext,
    #                                                            self.der,
    #                                                            intersection(result, newt_iter),
    #                                                            self.domain,
    #                                                            eps=self.eps)
    #                         t.start_with_slope()
    #                     print(
    #                         "Stop!!!!!!!!!!!!!!!!!!"
    #                     )
    #                     break
    #                 else:
    #
    #                     # в обычной ситуации действуем по привычному алгоритму
    #                     triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
    #                     newt_iter = mid - self.f(mid) / self.f(triplet)[0].slope
    #                     # print("TRIPLE: ", triplet)
    #                     # print("NEWT OPER: ", newt_iter)
    #                     # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) / self.f(triplet).slope
    #
    #                     # чтобы не допустить попадание None в массив результатов, добавляем данное условие
    #                     if intersection(result, newt_iter) is None:
    #                         if result.width() <= self.eps:
    #                             self.domain.common_base.append(result)
    #                         break
    #
    #                     result = intersection(result, newt_iter)
    #                     if result.width() <= self.eps:
    #                         print("RESULT: ", result)
    #                         self.domain.common_base.append(result)
    #                         break
    #         else:
    #
    #             # вычисляем обратный интервал к первой производной
    #             division = 1 / self.f(triplet).slope
    #
    #             # Если содержится нуль, то интервал распадается на два луча
    #             if isinstance(division, list):
    #
    #                 for i in division:
    #                     newt_iter = mid - self.f(mid) * i
    #                     if intersection(result, newt_iter) is not None:
    #                         iteration_result.append(intersection(result, newt_iter))
    #
    #                 # обрабатываем каждый луч отдельно (запускаем для них отдельные итерационные процессы)
    #                 for i in division:
    #                     newt_iter = mid - self.f(mid) * i
    #                     print("NEWT OPER: ", newt_iter)
    #
    #                     # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) * i
    #
    #                     t = NewtonIntervalIterationProcess(self.f,
    #                                                        self.func_ext,
    #                                                        self.der,
    #                                                        intersection(result, newt_iter),
    #                                                        self.domain,
    #                                                        eps=self.eps)
    #                     t.start_with_slope()
    #                 break
    #             else:
    #
    #                 # в обычной ситуации действуем по привычному алгоритму
    #                 triplet = Triplet(interval=result, value_at_c=Interval.valueToInterval(mid), slope=1)
    #                 newt_iter = mid - self.f(mid) / self.f(triplet).slope
    #                 print("TRIPLE: ", triplet)
    #                 print("NEWT OPER: ", newt_iter)
    #                 # newt_iter = Interval.valueToInterval(mid) - self.f(Interval.valueToInterval(mid)) / self.f(triplet).slope
    #
    #                 # чтобы не допустить попадание None в массив результатов, добавляем данное условие
    #                 if intersection(result, newt_iter) is None:
    #                     if result.width() <= self.eps:
    #                         self.domain.common_base.append(result)
    #                     break
    #
    #                 result = intersection(result, newt_iter)
    #                 print("RESULT: ", result)
    #                 if result.width() <= self.eps:
    #                     self.domain.common_base.append(result)
    #                     break


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
        self.iter_tools = ""

    def run_slope(self):
        nip = NewtonIntervalIterationProcess(self.f, self.func_ext, self.der, self.primary_interval, self, self.eps, 0)
        nip.start_with_slope()
        # print(self.primary_interval)
        print(self.iter_tools)

    def run(self):
        nip = NewtonIntervalIterationProcess(self.f, self.func_ext, self.der, self.primary_interval, self, self.eps, 0)
        nip.start()
