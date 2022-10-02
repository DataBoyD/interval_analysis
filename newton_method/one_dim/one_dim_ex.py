from decimal import Decimal
import math

from one_dim_class import NewtonComputations
from practice_interval.interval_lib import Interval

f = lambda x: x ** 2 + 2 * x * Decimal(math.sin(x)) - 4
der_f = lambda x: 2 * x + 2 * x.sin(x) + 2 * x * x.cos(x)


a = Interval([-2, 2])
a.setprecision(40)

n = NewtonComputations(f, der_f, a)
n.run()

print(n.common_base)


