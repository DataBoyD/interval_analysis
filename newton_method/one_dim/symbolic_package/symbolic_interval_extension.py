from decimal import Decimal
import math
from sympy import *
from sympy.abc import x
from sympy.utilities.lambdify import implemented_function

from practice_interval.interval_lib import Interval


class IntervalExtension:
    '''
    Класс для построения функции, принимающей в качестве аргумента интервал
    '''

    def __init__(self, f):
        self.f = f
        self.__evaluate_interval_expresion()

    def __evaluate_interval_expresion(self):
        s = str(self.f)
        s = s.replace("cos(", "x.cos(")
        s = s.replace("sin(", "x.sin(")
        s = s.replace("log(", "x.ln(")
        s = s.replace("exp(", "x.exp(")
        s = s.replace("pi", "Decimal(math.pi)")
        s = s.replace("sqrt(", "math.sqrt(")
        self.f = lambda x: eval(s)

    def __call__(self, x: Interval):
        return self.f(x)
