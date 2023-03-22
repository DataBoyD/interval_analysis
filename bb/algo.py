import math
from decimal import Decimal

from elementary_functions import triplet_sin, triplet_sqrt, triplet_cos, triplet_exp, triplet_log
from elementary_functions.signum import triplet_signum
from practice_interval.interval_lib import Interval
from practice_interval.newton_method.one_dim.intersection_tools import intersection
from triplet_entity import Triplet


class BranchAndBoundAlgorithm:

    def __init__(self, f, s: Interval, eps: float):
        self.f = f
        self.S = s
        self.eps = eps
        self.L = []
        self.Q = []
        self.x_tilde = None
        self.f_tilde = None

        # инициализируем f~ и x~
        if f(s[0]) < f(s[1]):
            self.x_tilde = s[0]
            self.f_tilde = f(s[0])
        else:
            self.x_tilde = s[1]
            self.f_tilde = f(s[1])

    def run(self):

        # проводим тест на монотонность
        t_init = Triplet(interval=self.S, value_at_c=Interval.valueToInterval(self.middle_of_interval(self.S)), slope=1)
        t_init: Triplet = self.f(t_init)

        if self.monotonicity_test(t_init.slope) != True:
            return self.f_tilde, self.x_tilde

        # определяем нижние границы
        lb_down = self.f(self.S[0])
        lb_up = self.f(self.S[1])

        # проводим GradTest для получения нового интервала x
        x = self.grad_test(self.S, lb_down, lb_up, self.f_tilde, g=t_init.slope)

        # переопределяем f_cap и lb
        f_cap = lb_up = lb_down = self.f_tilde

        # определяем минорирующую оценку f_z_min
        t = Triplet(interval=x, value_at_c=Interval.valueToInterval(self.middle_of_interval(x)), slope=1)
        t: Triplet = self.f(t)

        f_z_min = self.define_f_z(self.define_lower_boundary(lb_down, lb_up, x, t.slope), t.interval[0])

        # выполняем алгоритм отбора
        if x.width() < self.eps:
            self.Q.append([x, f_cap, f_z_min])
        else:
            self.L.append([x, f_cap, f_z_min])

        while len(self.L) > 0:
            print("L: ", self.L)
            # сортируем массив L по неубыванию Fz_i
            self.L.sort(key=lambda x: x[2])
            # выбираем один элемент из L с наименьшим Fz_i
            x, f_cap, f_z_min = self.L.pop(0)
            # x, f_cap, f_z_min = self.L[0]

            # снова проводим тест на монотонность
            t = Triplet(interval=x, value_at_c=Interval.valueToInterval(self.middle_of_interval(x)), slope=1)
            t: Triplet = self.f(t)
            if self.monotonicity_test(t.slope):
                # ищем середину интервала x
                mid = self.middle_of_interval(x)
                if self.f(mid) < self.f_tilde:
                    self.f_tilde = self.f(mid)
                    self.x_tilde = mid
                    self.cut_off_test()

                # делим исходный интервал на два других x_1 и x_2
                x_1, x_2 = Interval([x[0], mid]), Interval([mid, x[1]])

                # определяем новые lb для каждого интервала по алгоритму
                lb_x_1_down, lb_x_1_up, lb_x_2_down, lb_x_2_up = [None] * 4
                lb_x_1_down = lb_x_2_up = f_cap
                lb_x_1_up = lb_x_2_down = self.f(mid)

                # проводим GradTest для x_1
                x_1 = self.grad_test(x_1, lb_x_1_down, lb_x_1_up, self.f_tilde, t.slope)
                if x_1:
                    print("X1= ", x_1, " WIDTH = ", x_1.width())

                    # определяем новые lb для x_1
                    lb_x_1_down = lb_x_1_up = f_cap_x_1 = self.f_tilde

                    t_1 = Triplet(interval=x_1, value_at_c=Interval.valueToInterval(self.middle_of_interval(x_1)), slope=1)
                    t_1: Triplet = self.f(t_1)

                    if x_1.width() > 0:
                        f_z_min_x_1 = self.define_f_z(self.define_lower_boundary(lb_x_1_down, lb_x_1_up, x_1, t.slope), t_1.interval[0])
                        if f_z_min_x_1 < self.f_tilde:
                            # self.f_tilde = f_z_min_x_1
                            if x_1.width() < self.eps:
                                self.Q.append([x_1, f_cap_x_1, f_z_min_x_1])
                            else:
                                print("MIN ON X1= ", f_z_min_x_1)
                                self.L.append([x_1, f_cap_x_1, f_z_min_x_1])
                x_2 = self.grad_test(x_2, lb_x_2_down, lb_x_2_up, self.f_tilde, t.slope)
                if x_2:
                    print("X2= ", x_2, " WIDTH = ", x_2.width())

                    lb_x_2_down = lb_x_2_up = f_cap_x_2 = self.f_tilde

                    t_2 = Triplet(interval=x_2, value_at_c=Interval.valueToInterval(self.middle_of_interval(x_2)), slope=1)
                    t_2: Triplet = self.f(t_2)

                    if x_2.width() > 0:
                        f_z_min_x_2 = self.define_f_z(self.define_lower_boundary(lb_x_2_down, lb_x_2_up, x_2, t.slope), t_2.interval[0])
                        if f_z_min_x_2 < self.f_tilde:
                            # self.f_tilde = f_z_min_x_2
                            if x_2.width() < self.eps:
                                self.Q.append([x_2, f_cap_x_2, f_z_min_x_2])
                            else:
                                print("MIN ON X2= ", f_z_min_x_2)
                                self.L.append([x_2, f_cap_x_2, f_z_min_x_2])
            else:
                # if len(self.Q) > 0:
                    return self.Q, self.f_tilde
                # else:
                #     return self.x_tilde, self.f_tilde

        # if len(self.Q) > 0:
            return self.Q, self.f_tilde
        # else:
        #     return self.x_tilde, self.f_tilde

    @staticmethod
    def monotonicity_test(x):
        ''' **Тест на монотонность** '''
        return Interval.valueToInterval(0).isIn(x)

    @staticmethod
    def grad_test(x, lb_down, lb_up, f_tilda_value, g):
        '''**тест на наклоны**'''
        result = x
        if lb_down > f_tilda_value:
            v_right = Interval([x[0] - (lb_down - f_tilda_value) / g[0], "Infinity"])
            result = intersection(v_right, x)
        if result is not None and result.width() > 0 and lb_up > f_tilda_value:
            v_left = Interval(["-Infinity", x[1] - (lb_up - f_tilda_value) / g[1]])
            result = intersection(v_left, result)
        print(f"NEW X = {result}")
        return result

    def define_lower_boundary(self, lb_down, lb_up, x, slope):
        '''**определение нижней границы**'''
        l1 = max(
            lb_down,
            lb_up + slope[1] * (x[0] - x[1])
        )
        l2 = max(
            lb_up,
            lb_down + slope[0] * (x[1] - x[0])
        )
        return min(l1, l2)

        # return (lb_down * slope[1] - lb_up * slope[0]) / slope.width() + x.width() * (slope[0] * slope[1])/(slope.width())

    @staticmethod
    def define_f_z(z, f_min):
        return max(f_min, z)

    def cut_off_test(self):
        print("I am here: ", self.L, [len(i) for i in self.L])
        print(f"BEFORE CUT TEST len(L)={len(self.L)}")
        for elem in self.L:
            if elem[2] > self.f_tilde:
                self.L.remove(elem)

        print(f"AFTER CUT TEST len(L)={len(self.L)}")

        for elem in self.Q:
            if elem[2] > self.f_tilde:
                self.Q.remove(elem)

    @staticmethod
    def middle_of_interval(x: Interval):
        return (x[0] + x[1]) / 2

class Func:
    def __init__(self, str_repr: str, f):
        self.str_repr = str_repr
        self.f = f

    def __call__(self, x):
        # print(x, self.f(x))
        return self.f(x)

    def __str__(self):
        return self.str_repr

    def __repr__(self):
        return self.str_repr
def my_abs(x):
    if x == 0:
        return 0
    return abs(x) / x

# bb = BranchAndBoundAlgorithm(f=Func("|x-2| * x + sin(x) - 1", lambda x: abs(triplet_sin(x)-Triplet.from_number(2)) * x ** 2 * triplet_cos(x) + triplet_sin(x) - Triplet.from_number(1) if isinstance(x, Triplet) else  abs(Decimal(math.sin(x))-2)*x**2*Decimal(math.cos(x)) + Decimal(math.sin(x) - 1)),
#                              s=Interval([1, 5]),
#                              eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("|x-2|sin(x) - 1", lambda x: abs(x-Triplet.from_number(2))*triplet_sin(x) - Triplet.from_number(1) if isinstance(x, Triplet) else  abs(x-2)*Decimal(math.sin(x)) - Decimal(1)),
#                              s=Interval([0.2, 7]),
#                              eps=1e-3)

# bb = BranchAndBoundAlgorithm(f=Func("x^2*sin(x)+1.6", lambda x: x**2*triplet_sin(x) + Triplet.from_number(1.6) if isinstance(x, Triplet) else x**2*Decimal(math.sin(x))  + Decimal(1.6)),
#                              s=Interval([0.2, 7]),
#                              eps=1e-3)

bb = BranchAndBoundAlgorithm(f=Func("sqrt(x)*sin^2(x)", lambda x: triplet_sqrt(x)*triplet_sin(x)**2 if isinstance(x, Triplet) else Decimal(math.sqrt(x))*Decimal(math.sin(x)**2)),
                             s=Interval([2, 3.5]),
                             eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("2*sin(x)*e^(-x)", lambda x: Triplet.from_number(2)*triplet_sin(x)*triplet_exp(-x) if isinstance(x, Triplet) else 2*Decimal(math.sin(x))*Decimal(math.exp(-x))),
#                              s=Interval([0.2, 7]),
#                              eps=1e-6)

# bb = BranchAndBoundAlgorithm(f=Func("ln(3x)*ln(2x) - 0.1", lambda x: triplet_log(Triplet.from_number(3)*x)*triplet_log(Triplet.from_number(2)*x) - Triplet.from_number(1) if isinstance(x, Triplet) else Decimal(math.log(3*x)*math.log(2*x)) - Decimal(1)),
#                              s=Interval([.2, 7]),
#                              eps=1e-3)

# bb = BranchAndBoundAlgorithm(f=Func("sqrt(x)*sin^2(x)", lambda x: 1/(2*x) if isinstance(x, Interval) else Decimal(math.sqrt(x))*Decimal(math.sin(x)**2)),
#                              s=Interval([0.2, 7]),
#                              eps=1e-3)

# bb = BranchAndBoundAlgorithm(f=Func("(x-2)^2+24", lambda x: ((x-Triplet.from_number(2))**2 + Triplet.from_number(24) if isinstance(x, Triplet) else (x-2)**2 + 24)),
#                              s=Interval([0.2, 3]),
#                              eps=1e-8)

print("RESULT: ", bb.run())