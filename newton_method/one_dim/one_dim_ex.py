from decimal import Decimal
import math
from sympy import *
from sympy.abc import x
from sympy.utilities.lambdify import implemented_function

from one_dim_class import NewtonComputations
from practice_interval.interval_lib import Interval
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_interval_extension import IntervalExtension
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_function_representation import Function

f = lambda x: x ** 2 + 2 * x * Decimal(math.sin(x)) - 4
der_f = lambda x: 2 * x + 2 * x.sin(x) + 2 * x * x.cos(x)

a = Interval([-10, 10])
a.setprecision(40)

# n = NewtonComputations(f, der_f, a)
# n.run()

# print(n.common_base)


f = lambda x: x ** 2 + 2 * x * Decimal(math.sin(x)) - 4
der_f = lambda x: 2 * x + 2 * x.sin(x) + 2 * x * x.cos(x)

a = Interval([1, 7])
a.setprecision(25)


# n = NewtonComputations(f, der_f, a)
# n.run()

# print(n.common_base)





a = Interval([-3,2])
a.setprecision(40)

x = Symbol('x')
# f = (-0.5 * x ** 2) * log(x) + 5
# f = (-x ** (0.5)) * sin(x) + 1
# f = (-exp(-x)) * sin(2 * pi * x) + 1
# f = x * sin(x) + sin(10 * x / 3) + log(x) - 0.84 * x + 1.3
# f = x + sin(5 * x)
# f = -x * sin(x) + 5
# f = sin(x) * cos(x) - 1.5 * (sin(x)) ** 2 + 1.2
# f = 2 * cos(x) + cos(2 * x) + 5
# f = 2 * sin(x) * exp(-x)
# f = (3 * x - 1.4) * sin(18 * x) + 1.7
# error!!!
# f = ((x + 1) ** 3) / (x ** 2) - 7.1

# f = exp(sin(3 * x))
# f = sum([k * cos(x * (k + 1) + k) for k in range(0, 6)]) + 12
#
# f = 2 * (x - 3) ** 2 - exp(x / 2) + 5
# f = x**(0.5)*(sin(x))**2

# f = -exp(sin(x)) + 4
# f = cos(x) - sin(5 * x) + 1
# f = -x-sin(3*x)+1.6
# f = cos(x)+2*cos(2*x)*exp(-x)
# f = -sum([k * sin(x * (k + 1) + k) for k in range(1, 6)]) + 3
# f = -sum([cos(x * (k + 1)) for k in range(1, 6)])
# f = log(3*x)*log(2*x) - 1
# f = -exp(-x)*sin(2*pi*x)+0.5
# error!!!
# f = (x**2-5*x+6)/(x**2 + 1) - 0.5
# f = (x+sin(x))*exp(-x**2) + 0.8

# f = -x + sin(3*x)+1

F = [

    (-0.5 * x ** 2) * log(x) + 5,
    (-x ** (0.5)) * sin(x) + 1,
    (-exp(-x)) * sin(2 * pi * x) + 1,
    x * sin(x) + sin(10 * x / 3) + log(x) - 0.84 * x + 1.3,
    x + sin(5 * x),
    -x * sin(x) + 5,
    sin(x) * cos(x) - 1.5 * (sin(x)) ** 2 + 1.2,
    2 * cos(x) + cos(2 * x) + 5,
    2 * sin(x) * exp(-x),
    (3 * x - 1.4) * sin(18 * x) + 1.7,
    exp(sin(3 * x)),
    sum([k * cos(x * (k + 1) + k) for k in range(0, 6)]) + 12,
    2 * (x - 3) ** 2 - exp(x / 2) + 5,
    x ** (0.5) * (sin(x)) ** 2,
    -exp(sin(x)) + 4,
    cos(x) - sin(5 * x) + 1,
    -x - sin(3 * x) + 1.6,
    cos(x) + 2 * cos(2 * x) * exp(-x),
    -sum([k * sin(x * (k + 1) + k) for k in range(1, 6)]) + 3,
    -sum([cos(x * (k + 1)) for k in range(1, 6)]),
    log(3 * x) * log(2 * x) - 1,
    -exp(-x) * sin(2 * pi * x) + 0.5,
    (x + sin(x)) * exp(-x ** 2) + 0.8,
    - x + sin(3 * x) + 1,
    -exp(sin(3 * x)) + 1,
    ((x + 1) ** 3) / (x ** 2) - 7.1,

    # -exp(sin(3*x))+1
    # f = (x+sin(x))*exp(-x**2) + 0.8  # r!!!
    # f = (x**2-5*x+6)/(x**2 + 1) - 0.5
    # f = (x+sin(x))*exp(-x**2) + 0.8

    # f = -x + sin(3*x)+1
]
# F = [
#     # ((x + 1) ** 3) / (x ** 2) - 7.1,
#     # (x+sin(x))*exp(-x**2) + 0.8,
#     # (x ** 2 - 5 * x + 6) / (x ** 2 + 1) - 0.5
#     -exp(sin(3 * x)) + 1
#
# ]

F = [
#     ((x + 1) ** 3) / (x ** 2) - 7.1,
#     # (x+sin(x))*exp(-x**2) + 0.8,
#     # sum([k * cos(x * (k + 1) + k) for k in range(0, 6)]) + 12,
#     #
    -sum([k * sin(x * (k + 1) + k) for k in range(1, 6)]) + 3,
    -sum([cos(x * (k + 1)) for k in range(1, 6)]),
#     # ((x + 1) ** 3) / (x ** 2) - 7.1,
#     # cos(x) + 2*cos(2*x)*exp(-x)
    (x ** 2 - 5 * x + 6) / (x ** 2 + 1) - 0.5,
    -exp(sin(3 * x)) + 1


]


def print_result(f, primary: Interval):
    # Проблема состояла в неоптимальном интервальном расширении производной!!!
    der = diff(f, x).simplify()
    print("DERIVATIVE: ", der)
    # print(0 in a)
    func = Function(f)
    der_f = IntervalExtension(der)
    f_ext = IntervalExtension(f)
    n = NewtonComputations(func, f_ext, der_f, primary, eps=1e-5)
    n.common_base.clear()
    n.run()
    if len(n.common_base) != 0:
        print(sorted(n.common_base, key=lambda x: x[0]))
        print()


for idx, f in enumerate(F):
    print(f"Функция #{idx + 1}: {f}")
    print_result(f, a)
    print()


