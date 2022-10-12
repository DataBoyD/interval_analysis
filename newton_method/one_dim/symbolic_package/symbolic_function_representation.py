from decimal import Decimal
import math
from sympy import *
from sympy.abc import x
from sympy.utilities.lambdify import implemented_function

class Function:

    def __init__(self, f):
        f = str(f)
        self.f = lambda x: eval(f)

    def __call__(self, x):
        return self.f(x)

