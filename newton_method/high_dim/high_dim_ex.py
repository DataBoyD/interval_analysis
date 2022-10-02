import decimal
import numpy as np
from practice_interval.interval_lib import *
from high_dim_class import HightDimensionalIntervalNewtonProcess


f = lambda x: np.array([
    [x[0][0] ** 2 + x[1][0] ** 2 - Decimal(0.25)],
    [x[0][0] - x[1][0] ** 3],
])


jacobian = lambda x: np.array([
    [2 * x[0][0], 2 * x[1][0]],
    [1, -3 * x[1][0] ** 2],

])

x_0_0 = Interval([Decimal(-0.5), Decimal(-(1e-10))])
x_0_0.setprecision(40)
x_0_1 = Interval([Decimal(-0.8),  Decimal(-(1e-10))])
x_0_1.setprecision(40)

x_0 = np.array([
    x_0_0,
    x_0_1,
]).reshape(-1, 1)


hdNewt = HightDimensionalIntervalNewtonProcess(f, jacobian, x_0, precision=1e-21)
hdNewt.start()


x_0_0 = Interval([Decimal(0.05), Decimal(0.2)])
x_0_0.setprecision(40)
x_0_1 = Interval([Decimal(0.4),  Decimal((.55))])
x_0_1.setprecision(40)

x_0 = np.array([
    x_0_0,
    x_0_1,
]).reshape(-1, 1)


hdNewt = HightDimensionalIntervalNewtonProcess(f, jacobian, x_0)
hdNewt.start()






