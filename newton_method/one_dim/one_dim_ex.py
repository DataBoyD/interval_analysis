import datetime
from decimal import Decimal
import math
from typing import List

from sympy import *
from sympy.abc import x
from sympy.utilities.lambdify import implemented_function

from one_dim_class import NewtonComputations
from practice_interval.csv_adapter.csv_writer import NewtonRecord, CSVWriter
from practice_interval.interval_lib import Interval
from practice_interval.newton_method.one_dim.slope_module.elementary_functions.signum import triplet_signum
from practice_interval.newton_method.one_dim.slope_module.triplet_entity import Triplet
from practice_interval.newton_method.one_dim.slope_module.elementary_functions import triplet_sin, triplet_cos, \
    triplet_exp, triplet_log, triplet_sqrt
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_interval_extension import IntervalExtension
from practice_interval.newton_method.one_dim.symbolic_package.symbolic_function_representation import Function
from intersection_tools import intersection
f = lambda x: x ** 2 + 2 * x * Decimal(math.sin(x)) - 4
der_f = lambda x: 2 * x + 2 * x.sin(x) + 2 * x * x.cos(x)

a = Interval([-20, 10])
a.setprecision(40)

# n = NewtonComputations(f, der_f, a)
# n.run()

# print(n.common_base)


f = lambda x: x ** 2 + 2 * x * Decimal(math.sin(x)) - 4
der_f = lambda x: 2 * x + 2 * x.sin(x) + 2 * x * x.cos(x)

# a = Interval([-3, 4])
# a = Interval([-3, 7])
a = Interval([-8, 7])
a.setprecision(20)

# n = NewtonComputations(f, der_f, a)
# n.run()

# print(n.common_base)


# a = Interval([-.39, .39])
# a = Interval([-12, -9])
# a = Interval([math.pi + 0.1, 2 * math.pi - 0.1])
# a = Interval([math.pi + 0.1, 2 * math.pi - 0.1])
# a = Interval([-20, 12])
# a = Interval([-11, 10])
# a.setprecision(5)

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

# F = [
# #     ((x + 1) ** 3) / (x ** 2) - 7.1,
# #     # (x+sin(x))*exp(-x**2) + 0.8,
# #     # sum([k * cos(x * (k + 1) + k) for k in range(0, 6)]) + 12,
# #     #
#     x ** (0.5) * (sin(x)) ** 2,
#
#     # -sum([k * sin(x * (k + 1) + k) for k in range(1, 6)]) + 3,
#     # -sum([cos(x * (k + 1)) for k in range(1, 6)]),
# #     # ((x + 1) ** 3) / (x ** 2) - 7.1,
# #     # cos(x) + 2*cos(2*x)*exp(-x)
# #     (x ** 2 - 5 * x + 6) / (x ** 2 + 1) - 0.5,
# #     -exp(sin(3 * x)) + 1
#
#
# ]


# PATH = "csv_adapter/tests"
#
# writer = CSVWriter(path=f"{PATH}/{datetime.datetime.now()}.csv")
# # writer = CSVWriter(path=f"{datetime.datetime.now()}.csv")
# NewtonRecordJournal: List[NewtonRecord] = []

F = [
    #     ((x + 1) ** 3) / (x ** 2) - 7.1,
    #     # (x+sin(x))*exp(-x**2) + 0.8,
    #     # sum([k * cos(x * (k + 1) + k) for k in range(0, 6)]) + 12,
    #     #
    #     x ** (0.5) * (sin(x)) ** 2,

    # -sum([k * sin(x * (k + 1) + k) for k in range(1, 6)]) + 3,
    # -sum([cos(x * (k + 1)) for k in range(1, 6)]),
    ((x + 1) ** 3) / (x ** 2) - 7.1,
    #     # cos(x) + 2*cos(2*x)*exp(-x)
    (x ** 2 - 5 * x + 6) / (x ** 2 + 1) - 0.5,
    #     -exp(sin(3 * x)) + 1

]


# def print_result(f, primary: Interval):
#     # Проблема состояла в неоптимальном интервальном расширении производной!!!
#     der = diff(f, x).simplify()
#     print("DERIVATIVE: ", der)
#     # print(0 in a)
#     func = Function(f)
#     der_f = IntervalExtension(der)
#     f_ext = IntervalExtension(f)
#     n = NewtonComputations(func, f_ext, der_f, primary, eps=1e-5)
#     n.common_base.clear()
#     n.run()
#     rec = NewtonRecord(
#         str(f),
#         str(der),
#         a,
#         1e-5,
#         ""
#     )
#
#     if len(n.common_base) != 0:
#         base = sorted(n.common_base, key=lambda x: x[0])
#         print(base)
#         print()
#         roots = "\n".join([str(r) for r in base])
#         rec.roots = roots
#
#     NewtonRecordJournal.append(rec)


# class Func:
#     def __init__(self, str_repr: str, f):
#         self.str_repr = str_repr
#         self.f = f
#
#     def __call__(self, x):
#         return self.f(x)
#
#     def __str__(self):
#         return self.str_repr
#
#     def __repr__(self):
#         return self.str_repr


# for idx, f in enumerate(F):
#     print(f"Функция #{idx + 1}: {str(f)}")
#     print_result(f, a)
#     # print_result_slope(f, a)
#     # fff = lambda x: ((x + 1) ** 3) / (x ** 2) - 7.1
#     # print(fff(Decimal(1)))

def sigma_oper(arr):
    result = arr[0]
    for i in range(1, len(arr)):
        result = result + arr[i]
    return result


def f1(x):
    if isinstance(x, Triplet):
        return sigma_oper(
            [Triplet.from_number(k) * triplet_cos(Triplet.from_number(k + 1) * x + Triplet.from_number(k)) for k in
             range(0, 6)]) + Triplet.from_number(12)
    else:
        return sigma_oper([k * Decimal(math.cos(x * (k + 1) + k)) for k in range(0, 6)]) + 12


def f2(x):
    if isinstance(x, Triplet):
        if x.interval.sin(x.interval)[0] > x.interval.cos(x.interval)[1]:
            return triplet_sin(x)
        else:
            return triplet_cos(x)
    else:
        if math.sin(x) > math.cos(x):
            return math.sin(x)
        else:
            return math.cos(x)


# def f3(x):
#
#     if isinstance(x, Triplet):
#         result = []
#         if x.interval[1] <= 1:
#             result.append(x ** 2 + Triplet.from_number(0.5))
#         elif x.interval[1] <= 3 and x.interval[0] > 1:
#             result.append(Triplet.from_number(5) * triplet_sin(Triplet.from_number(2*math.pi) * x) + Triplet.from_number(1.5))
#         else:
#             result.append(x - Triplet.from_number(5))
#         return result
#     else:
#         result = []
#         if x <= 1:
#             return x ** 2 + Decimal(0.5)
#         elif x <= 3 and x > 1:
#             return 5*Decimal(math.sin(2*pi*x)) + Decimal(1.5)
#         elif x > 3:
#              return x - Decimal(5)

def f4(x):
    if isinstance(x, Triplet):
        result = []
        first_condition = Interval(["-Infinity", math.pi * 3 / 2])
        if intersection(x.interval, first_condition):
            mid = (intersection(x.interval, first_condition)[0] + intersection(x.interval, first_condition)[1]) / 2
            result.append(triplet_cos(Triplet.from_number(5) * Triplet(
                interval=intersection(x.interval, first_condition),
                value_at_c=Interval.valueToInterval(mid),
                slope=1
            )))
        if intersection(x.interval, Interval(["Infinity", math.pi * 3 / 2+1e-2])):
            mid = (intersection(x.interval, first_condition)[0] + intersection(x.interval, first_condition)[1]) / 2
            result.append(triplet_cos(Triplet(
                interval=intersection(x.interval, first_condition),
                value_at_c=Interval.valueToInterval(mid),
                slope=1
            )))
        return result
    else:
        if x <= 3 * math.pi / 2:
            return math.cos(5 * x)
        else:
            return math.cos(x)

def f5_1(x):
    if isinstance(x, Triplet):
        # result = []
        first_condition = Interval(["-Infinity", 2])
        if intersection(x.interval, first_condition):
            # mid = (x.interval[0] + x.interval[1]) / 2
            mid = (intersection(x.interval, first_condition)[0] + intersection(x.interval, first_condition)[1]) / 2
            return Triplet.from_number(2) * Triplet(
                interval=intersection(x.interval, first_condition),
                value_at_c=Interval.valueToInterval(mid),
                slope=1
            ) - Triplet.from_number(1)
    else:
        if x <= 2:
            return 2*x - 1

def f5_2(x):
    if isinstance(x, Triplet):
        first_condition = Interval(["Infinity", 2])
        if intersection(x.interval, Interval(["Infinity", 2])):
            mid = (intersection(x.interval, first_condition)[0] + intersection(x.interval, first_condition)[1]) / 2
            return -Triplet(
                interval=intersection(x.interval, first_condition),
                value_at_c=Interval.valueToInterval(mid),
                slope=1
            ) + Triplet.from_number(5)
    else:
        if x >= 2:
            return -x + 5
class Func:
    def __init__(self, str_repr: str, f):
        self.str_repr = str_repr
        self.f = f

    def __call__(self, x):
        print(x, self.f(x))
        return self.f(x)

    def __str__(self):
        return self.str_repr

    def __repr__(self):
        return self.str_repr

def my_abs(x):
    if isinstance(x, Interval):
        return x.abs(x)
    return abs(x)

F = [
    # Func("sign(x) * x + sin(x) - 1", lambda x: triplet_signum(x) * x + triplet_sin(x) - Triplet.from_number(1) if isinstance(x, Triplet) else  (my_abs(x) / x) * x + Decimal(math.sin(x) - 1)),
    # Func("x*sign(x)-x^2+sin(x)*sign(x)*cos(x)", lambda x: triplet_signum(x) * x - x ** 2 + triplet_sin(x)*triplet_signum(x)*triplet_cos(x) if isinstance(x, Triplet) else  (my_abs(x) / x) * x - x ** 2 + Decimal(Decimal(math.sin(x)*math.cos(x))*(my_abs(x) / x))),
    Func("cos(x^2)*sign(x-1)+x^2*sin(x)", lambda x: triplet_signum(x-Triplet.from_number(1)) * triplet_cos(x ** 2) + x ** 2 * triplet_sin(x) if isinstance(x, Triplet) else (my_abs(x-1) / (x-1)) * Decimal(math.cos(x**2)) + x ** 2 * Decimal(math.sin(x))),
    # Func("x*sign(x)*sin(x)-cos(x^2)*x", lambda x: triplet_signum(x) * x * triplet_sin(x) + triplet_cos(x**2)*x if isinstance(x, Triplet) else abs(x) * Decimal(math.sin(x)) + x*Decimal(math.cos(x**2))),
    # Func("sign(x) * x - sin(x) - 1", lambda x: (abs(x) / x) * x - triplet_sin(x) - Triplet.from_number(1) if isinstance(x, Triplet) else x * abs(x) / x - Decimal(math.sin(x)) - 1),
    # Func("(x+1)^3/x^2-7.1", lambda x: ((x + Triplet.from_number(1)) ** 3) / (x ** 2) - Triplet.from_number(7.1) if isinstance(x, Triplet) else ((x + Decimal(1)) ** 3) / (x ** 2) - Decimal(7.1)),
    # Func("(x^2-5x+6)/(x^2+1)-0.5", lambda x: (x ** 2 - Triplet.from_number(5) * x + Triplet.from_number(6)) / (x ** 2 + Triplet.from_number(1)) - Triplet.from_number(0.5) if isinstance(x, Triplet) else (x ** 2 - 5 * x + 6) / (x ** 2 + 1) - Decimal(0.5)),
    # lambda x: triplet_sin(x / Triplet.from_number(2)) - Triplet.from_number(0.5) if isinstance(x, Triplet) else math.sin(x / 2) - 0.5,
    # Func("-x+sin(3x)+1", lambda x: -x + triplet_sin(Triplet.from_number(3) * x) + Triplet.from_number(1) if isinstance(x, Triplet) else -x + Decimal(math.sin(3 * x)) + 1),
    # lambda x: triplet_sin(x) - Triplet.from_number(0.5) if isinstance(x, Triplet) else Decimal(math.sin(x)) - Decimal(0.5),
    # lambda x: x ** 3 - triplet_exp(Triplet.from_number(2) / x) if isinstance(x, Triplet) else x ** 3 - Decimal(math.exp(2 / x)),
    # Func("cos(x)-sin(5x)+1", lambda x: triplet_cos(x) - triplet_sin(Triplet.from_number(5) * x) + Triplet.from_number(1) if isinstance(x, Triplet) else Decimal(math.cos(x)) - Decimal(math.sin(5 * x)) + Decimal(1)),
    # Func("2(x-3)^2-e^(x/2)+5", lambda x: Triplet.from_number(2) * (x - Triplet.from_number(3)) ** 2 - triplet_exp(x / Triplet.from_number(2)) + Triplet.from_number(5) if isinstance(x, Triplet) else 2  * (x - 3) ** 2 - Decimal(math.exp(x / 2)) + 5),
    # Func("ln(3x)*ln(2x) - 1", lambda x: triplet_log(Triplet.from_number(3) * x) * triplet_log(Triplet.from_number(2) * x) - Triplet.from_number(1) if isinstance(x, Triplet) else math.log(3*x)*math.log(2*x) - 1),
    # lambda x: triplet_sqrt(Triplet.from_number(5) * x) - Triplet.from_number(1) if isinstance(x, Triplet) else math.sqrt(5 * x) - 1,
    # lambda x: triplet_cos(Triplet.from_number(5) * x) - Triplet.from_number(0.5) if isinstance(x, Triplet) else math.cos(5*x) - 0.5,
    # Func("x+sin(5x)", lambda x: x + triplet_sin(Triplet.from_number(5) * x) if isinstance(x, Triplet) else x + Decimal(math.sin(5*x))),
    # Func("2*sin(x)*exp(-x)", lambda x: Triplet.from_number(2) * triplet_sin(x) * triplet_exp(-x) if isinstance(x, Triplet) else 2 * math.sin(x) * math.exp(-x)),
    # lambda x: triplet_exp(x / Triplet.from_number(2)) - Triplet.from_number(2) * x if isinstance(x, Triplet) else Decimal(math.exp(x / 2)) - 2 * x,
    # Func("x*|sin(x)| + 6",lambda x: x * abs(triplet_sin(x)) + Triplet.from_number(6) if isinstance(x, Triplet) else x * abs(Decimal(math.sin(x))) + Decimal(6)),
    # Func("f2", lambda x: f2(x)),
    # Func("f4", lambda x: f4(x)),
    # Func("f5", lambda x: f5_1(x)),
    # Func("f5_2", lambda x: f5_2(x)),
    # Func("|x*sin(x)|-1.5", lambda x: abs(x * triplet_sin(x)) - Triplet.from_number(1.5) if isinstance(x, Triplet) else abs(x * Decimal(math.sin(x))) - Decimal(1.5)),
    # Func("-exp(sin(3x))+1", lambda x: -triplet_exp(triplet_sin(Triplet.from_number(3) * x)) + Triplet.from_number(1) if isinstance(x,Triplet) else -math.exp(math.sin(3 * x)) + 1),
    # Func("exp(x^2)-2", lambda x: triplet_exp(x ** 2) - Triplet.from_number(2) if isinstance(x,Triplet) else Decimal(math.exp(x ** 2)) - 2),
    # Func("2/100*x^2 - 3/100*exp(-20*(x-0.875)^2)", lambda x: Triplet.from_number(2/100)*x**2 - Triplet.from_number(3/100)*triplet_exp(-Triplet.from_number(20)*(x-Triplet.from_number(0.875))**2) if isinstance(x, Triplet) else Decimal((2/100))*x**2 - Decimal((3/100))*Decimal(math.exp(-20*(x-Decimal(0.875))**2))),
    # Func("sum([k * cos(x * (k + 1) + k) for k in range(0, 6)]) + 12)", lambda x: f1(x)),
    # Func("x^6-15x^4+27x^3+250", lambda x: x**6 - Triplet.from_number(15)*x**4 + Triplet.from_number(27)*x**3+Triplet.from_number(250) if isinstance(x,Triplet) else x**6 - 15 * x**4 + 27 * x**3 + 250),
]

# PATH = "csv_adapter/tests/slope_tests"
#
# writer = CSVWriter(path=f"{PATH}/slope_{datetime.datetime.now()}.csv")
# # writer = CSVWriter(path=f"{datetime.datetime.now()}.csv")
# NewtonRecordJournal: List[NewtonRecord] = []


def print_result_slope(f, primary: Interval):
    # Проблема состояла в неоптимальном интервальном расширении производной!!!
    # der = diff(f, x).simplify()
    # print("DERIVATIVE: ", der)
    # print(0 in a)
    # func = Function(f)
    # der_f = IntervalExtension(der)
    # f_ext = IntervalExtension(f)

    n = NewtonComputations(f, f, der_f, primary, eps=1e-3)
    n.common_base.clear()
    n.run_slope()
    # rec = NewtonRecord(
    #     str(f),
    #     "slope mode",
    #     a,
    #     1e-5,
    #     ""
    # )

    if len(n.common_base) != 0:
        base = sorted(n.common_base, key=lambda x: x[0])
        roots = "\n".join([str(r) for r in base])
        print(roots)
        print()


        # rec.roots = roots

    # NewtonRecordJournal.append(rec)


#
for idx, f in enumerate(F):
    print(f"Функция #{idx + 1}: {str(f)}")
    # print_result(f, a)
    print_result_slope(f, a)
    # fff = lambda x: ((x + 1) ** 3) / (x ** 2) - 7.1
    # print(fff(Decimal(1)))

# writer.save(NewtonRecordJournal)

# mid = (a[0] + a[1]) / 2
# # print("MID: ", mid)
#
# triplet = Triplet(interval=a, value_at_c=Interval.valueToInterval(mid), slope=1)
# print(abs(triplet) / triplet)


# t1 = Triplet(interval=[Interval(['-Infinity', -0.2500000000]), Interval([0.1250000000, 'Infinity'])], value_at_c=Interval([31.2500000000, 31.2500000000]), slope=Interval(["-Infinity", 'Infinity']))
# t2 = Triplet(interval=Interval([7.0999999999, 7.1000000000]), value_at_c=Interval([7.0999999999, 7.1000000000]), slope=Interval([0E-10, 0E-10]))
# t1.interval[0] - t2.interval