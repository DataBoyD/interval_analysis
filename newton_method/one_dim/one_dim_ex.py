import math
from math import sin


from practice_interval.interval_lib import *

i_1 = Interval([5, 500])
i_2 = Interval([1, 2])


def intersection(a: Interval, b: Interval):

    # проверка на отсутствие пересечения интервалов
    if (a[1] < b[0] and a[1] < b[1]) or (b[1] < a[0] and b[1] < a[1]):
        return None

    # проверка на нормальное пересечение
    if a[0] < b[0] and a[1] < b[1]:
        return Interval([b[0], a[1]])

    # проверка на нормальное пересечение №2
    if b[0] < a[0] and b[1] < a[1]:
        return Interval([a[0], b[1]])

    # проверка на вложенность
    if a.isIn(b):
        return a

    # проверка на вложенность №2
    if b.isIn(a):
        return b

    if a == b:
        print("case 7")

        return a

# case of equal boundaries
a = Interval([1, 2])
b = Interval([2, 4])

print(intersection(a, b))

# case of normal overlapping
a = Interval([3, 5])
b = Interval([2, 4])

print(intersection(a, b))


# case of internal interval
a = Interval([-2, 5])
b = Interval([1, 3])

print(intersection(a, b))

# case of empty overlapping
a = Interval([-200, -25])
b = Interval([-20, -2])

print(intersection(a, b))


# /////////////////////////////////////////////////////////////////////////////////////


class IntervalExtensionFunction:
    def __init__(self, f):
        self.f = f

    def __call__(self, argument: Interval):
        return self.f(argument)


class NewtonIntervalIterationProcess:

    def __init__(self, f, first_der, primary_interval: Interval, domain, eps: float = 1e-3):
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
                if result.width() < self.eps:
                    self.domain.common_base.append(result)


# аккумулирующий класс с хранилищем результатов итерационных процессов
class NewtonComputations:

    common_base = []

    def __init__(self, f, first_der, primary_interval: Interval, eps: float = 1e-29):
        self.f = f
        self.der = IntervalExtensionFunction(first_der)
        self.primary_interval = primary_interval
        self.eps = eps

    def run(self):
        nip = NewtonIntervalIterationProcess(self.f, self.der, self.primary_interval, self, self.eps)
        nip.start()


f = lambda x: x ** 67 - Decimal(0.5292992393494939439493444)
der_f = lambda x: 67 * x ** 66


# f = lambda x: x ** 2 + 2 * x + 1 - Decimal(math.sin(x ** 2))
# der_f = lambda x: 2 * x + 2 - 2 * x * x.cos(x)


a = Interval([-1, 1])
# print(der_f(a))
a.setprecision(40)


n = NewtonComputations(f, der_f, a, eps=1e-35)
n.run()


print(n.common_base)


