import math
from decimal import Decimal

from slope_module.elementary_functions import triplet_sin, triplet_sqrt, triplet_cos, triplet_exp, triplet_log
from slope_module.elementary_functions.signum import triplet_signum
from interval_lib import Interval
from newton_method.one_dim.intersection_tools import intersection
from slope_module.triplet_entity import Triplet


# from  import Triplet


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

        print(f"Initial interval S = {self.S}")

        # проводим тест на монотонность
        # формируем массив slope по-новому. Вычисляем наклон относительно обоих концов интервала

        # относительно левого
        t_left = Triplet(interval=self.S, value_at_c=Interval.valueToInterval(self.S[0]), slope=1)
        t_left: Triplet = self.f(t_left)
        print(f"Left side slope on initial interval S = {t_left}")

        # относительно правого
        t_right = Triplet(interval=self.S, value_at_c=Interval.valueToInterval(self.S[1]), slope=1)
        t_right: Triplet = self.f(t_right)
        print(f"Right side slope on initial interval S = {t_right}")

        slope = Interval([t_left.slope[0], t_right.slope[1]])
        print(f"H_slope on initial data = {slope}")

        if self.monotonicity_test(slope) != True:
            return self.f_tilde, self.x_tilde

        # определяем нижние границы
        lb_down = self.f(self.S[0])
        lb_up = self.f(self.S[1])

        print(f"Initial lb_ and  lb^ = {lb_down} and {lb_up}")

        # проводим GradTest для получения нового интервала x
        x = self.grad_test(self.S, lb_down, lb_up, self.f_tilde, g=slope)
        print(f"Initial X based on S after GradTest = {x}")

        # переопределяем f_cap и lb
        f_cap = lb_up = lb_down = self.f_tilde
        print(f"f_cap = {f_cap}, lb_up = {lb_up}, lb_down = {lb_down}")

        # определяем минорирующую оценку f_z_min
        # t = Triplet(interval=x, value_at_c=Interval.valueToInterval(self.middle_of_interval(x)), slope=1)
        # t: Triplet = self.f(t)

        t_left = Triplet(interval=x, value_at_c=Interval.valueToInterval(x[0]), slope=1)
        t_left: Triplet = self.f(t_left)
        print(f"Left side slope on initial interval X = {t_left}")

        t_right = Triplet(interval=x, value_at_c=Interval.valueToInterval(x[1]), slope=1)
        t_right: Triplet = self.f(t_right)
        print(f"Right side slope on initial interval X = {t_right}")

        slope = [t_left.slope[0], t_right.slope[1]]

        print(f"H_slope on initial X = {slope}")

        f_z_min = self.define_f_z(self.define_lower_boundary(lb_down, lb_up, x, slope), t_left.interval[0])
        print(f"f_z min = {f_z_min}")
        # выполняем алгоритм отбора
        if x.width() < self.eps:
            self.Q.append([x, f_cap, f_z_min])
            print(f"Add to Q three objects = {[x, f_cap, f_z_min]}")
        else:
            self.L.append([x, f_cap, f_z_min])
            print(f"Add to L three objects = {[x, f_cap, f_z_min]}")

        print("\n\n\nMain loop is started\n\n\n")
        while len(self.L) > 0:
            # print("L: ", self.L)
            # сортируем массив L по неубыванию Fz_i
            self.L.sort(key=lambda x: x[2], reverse=False)
            # выбираем один элемент из L с наименьшим Fz_i
            x, f_cap, f_z_min = self.L.pop(0)
            # x, f_cap, f_z_min = self.L[0]
            print(f"Take from L three objects = {[x, f_cap, f_z_min]}")

            # снова проводим тест на монотонность
            # t = Triplet(interval=x, value_at_c=Interval.valueToInterval(self.middle_of_interval(x)), slope=1)
            # t: Triplet = self.f(t)

            t_left = Triplet(interval=x, value_at_c=Interval.valueToInterval(x[0]), slope=1)
            t_left: Triplet = self.f(t_left)
            print(f"Left side slope on initial interval X = {t_left}")

            t_right = Triplet(interval=x, value_at_c=Interval.valueToInterval(x[1]), slope=1)
            t_right: Triplet = self.f(t_right)
            print(f"Right side slope on initial interval X = {t_right}")

            # slope = [t_left.slope[0], t_right.slope[1]]
            slope = Interval([t_left.slope[0], t_right.slope[1]])
            print(f"H_slope on initial X = {slope}")

            if self.monotonicity_test(slope):
                # ищем середину интервала x
                mid = self.middle_of_interval(x)
                print(f"NEW MID FOR X={x}")
                if self.f(mid) < self.f_tilde:
                    self.f_tilde = self.f(mid)
                    print(f"f_tilde={self.f_tilde}")
                    # self.x_tilde = mid
                    self.cut_off_test()

                # делим исходный интервал на два других x_1 и x_2
                x_1, x_2 = Interval([x[0], mid]), Interval([mid, x[1]])
                print(f"x1={x_1}, x2={x_2}")

                # определяем новые lb для каждого интервала по алгоритму
                lb_x_1_down, lb_x_1_up, lb_x_2_down, lb_x_2_up = [None] * 4
                lb_x_1_down = lb_x_2_up = f_cap
                lb_x_1_up = lb_x_2_down = self.f(mid)

                print(f"lb1_down={lb_x_1_down}, lb1_up={lb_x_1_up}")
                print(f"lb2_down={lb_x_2_down}, lb2_up={lb_x_2_up}")

                # lb_x_1_down = self.f(x_1[0])
                # lb_x_1_up = self.f(x_1[1])
                #
                # lb_x_2_down = self.f(x_2[0])
                # lb_x_2_up = self.f(x_2[1])
                print("\n\n\n\nx1 boundary\n\n\n\n")
                print(f"x1 = {x_1}")

                # проводим GradTest для x_1
                x_1 = self.grad_test(x_1, lb_x_1_down, lb_x_1_up, self.f_tilde, slope)
                print(f"x1 after grad test = {x_1}")
                if x_1:
                    # print("X1= ", x_1, " WIDTH = ", x_1.width())

                    # определяем новые lb для x_1
                    lb_x_1_down = lb_x_1_up = f_cap_x_1 = self.f_tilde
                    # f_cap_x_1 = self.f_tilde
                    print(f"lb1_down={lb_x_1_down}, lb1_up={lb_x_1_up}")

                    t_1 = Triplet(interval=x_1, value_at_c=Interval.valueToInterval(x_1[1]),
                                  slope=1)
                    t_1: Triplet = self.f(t_1)

                    #
                    # t_1_right = Triplet(interval=x_1, value_at_c=Interval.valueToInterval(x_1[1]), slope=1)
                    # t_1_right: Triplet = self.f(t_1_right)

                    # slope = Interval([t_1_left.slope[0], t_1_right.slope[1]])

                    if x_1.width() > 0:

                        # lb_x_1_down = self.f(x_1[0])
                        # lb_x_1_up = self.f(x_1[1])

                        f_z_min_x_1 = self.define_f_z(self.define_lower_boundary(lb_x_1_down, lb_x_1_up, x_1, slope),
                                                      t_1.interval[0])
                        print(f"fx min on x1 = {f_z_min_x_1}")
                        if f_z_min_x_1 < self.f_tilde:
                            # self.f_tilde = f_z_min_x_1
                            if x_1.width() < self.eps:

                                # if self.monotonicity_test(t_1.slope):
                                    self.Q.append([x_1, f_cap_x_1, f_z_min_x_1])
                                    print(f"Add to Q three objects = {[x_1, f_cap_x_1, f_z_min_x_1]}")

                            else:
                                # print("MIN ON X1= ", f_z_min_x_1)
                                # if self.monotonicity_test(t_1.slope):
                                    self.L.append([x_1, f_cap_x_1, f_z_min_x_1])
                                    print(f"Add to L three objects = {[x_1, f_cap_x_1, f_z_min_x_1]}")
                print("\n\n\n\nx2 boundary\n\n\n\n")
                print(f"x2 = {x_2}")
                x_2 = self.grad_test(x_2, lb_x_2_down, lb_x_2_up, self.f_tilde, slope)
                print(f"x2 after GradTest = {x_2}")
                if x_2:
                    # print("X2= ", x_2, " WIDTH = ", x_2.width())

                    # f_cap_x_2 = self.f_tilde
                    lb_x_2_down = lb_x_2_up = f_cap_x_2 = self.f_tilde
                    print(f"lb2_down={lb_x_2_down}, lb2_up={lb_x_2_up}")


                    t_2 = Triplet(interval=x_2, value_at_c=Interval.valueToInterval(x_2[1]), slope=1)
                    t_2: Triplet = self.f(t_2)
                    # t_2_left = Triplet(interval=x_2, value_at_c=Interval.valueToInterval(self.middle_of_interval(x_2)),
                    #                    slope=1)
                    # t_2_left: Triplet = self.f(t_2_left)

                    # t_2_right = Triplet(interval=x_2, value_at_c=Interval.valueToInterval(x_2[1]), slope=1)
                    # t_2_right: Triplet = self.f(t_2_right)
                    #
                    # slope = Interval([t_2_left.slope[0], t_2_right.slope[1]])

                    if x_2.width() > 0:
                        # lb_x_2_down = self.f(x_2[0])
                        # lb_x_2_up = self.f(x_2[1])
                        f_z_min_x_2 = self.define_f_z(self.define_lower_boundary(lb_x_2_down, lb_x_2_up, x_2, slope),
                                                      t_2.interval[0])
                        print(f"fx min on x2 = {f_z_min_x_2}")

                        if f_z_min_x_2 < self.f_tilde:
                            # self.f_tilde = f_z_min_x_2
                            if x_2.width() < self.eps:
                                # if self.monotonicity_test(t_2.slope):
                                    self.Q.append([x_2, f_cap_x_2, f_z_min_x_2])
                                    print(f"Add to Q three objects = {[x_2, f_cap_x_2, f_z_min_x_2]}")

                            else:
                                # print("MIN ON X2= ", f_z_min_x_2)
                                # if self.monotonicity_test(t_2.slope):
                                    self.L.append([x_2, f_cap_x_2, f_z_min_x_2])
                                    print(f"Add to L three objects = {[x_2, f_cap_x_2, f_z_min_x_2]}")

            else:
                continue
                # if len(self.Q) > 0:

                # return self.Q, self.f_tilde
            # else:
            #     return self.x_tilde, self.f_tilde

            # if len(self.Q) > 0:
        return self.Q, self.f_tilde
        # else:
        #     return self.x_tilde, self.f_tilde

    @staticmethod
    def monotonicity_test(x):
        ''' **Тест на монотонность** '''

        print(f"M TEST: {Interval.valueToInterval(0).isIn(x)}")
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
        # l1 = max(
        #     lb_down,
        #     lb_up + slope[1] * (x[0] - x[1])
        # )
        # l2 = max(
        #     lb_up,
        #     lb_down + slope[0] * (x[1] - x[0])
        # )
        # return min(l1, l2)

        # return (2*slope[0]*lb_down + slope[1]*lb_up - slope[0]*lb_up + slope[0]*slope[1]*(x[1]-x[0]))/(slope[0]+slope[1])

        return (lb_down * slope[1] - lb_up * slope[0]) / (slope[1] - slope[0]) + (x[1] - x[0]) * (
                slope[0] * slope[1]) / (slope[1] - slope[0])

    @staticmethod
    def define_f_z(z, f_min):
        print("MINIMUM SEARCH: ", z, f_min)
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


# bb = BranchAndBoundAlgorithm(f=Func("|x-2| * x + sin(x) - 1", lambda x: abs(x-Triplet.from_number(2)) * x + triplet_sin(x) - Triplet.from_number(1) if isinstance(x, Triplet) else abs(Decimal(x-2)) * x + Decimal(math.sin(x) - 1)),
#                              s=Interval([1.2,5]),
#                              eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("|x-1|sin(x) - 1", lambda x: abs(x-Triplet.from_number(1))*triplet_sin(x) - Triplet.from_number(1) if isinstance(x, Triplet) else abs(x-1)*Decimal(math.sin(x)) - Decimal(1)),
#                              s=Interval([0.2, 7]),
#                              eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("x^3-2x^2+1",
#                                     lambda x: x ** 3 - Triplet.from_number(2) * x ** 2 + Triplet.from_number(
#                                         1) if isinstance(x, Triplet) else x ** 3 - 2 * x ** 2 + 1),
#                              s=Interval([.2, 50]),
#                              eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("2x^2+1",
#                                     lambda x: Triplet.from_number(2) * x ** 2 + Triplet.from_number(
#                                         1) if isinstance(x, Triplet) else  2 * x ** 2 + 1),
#                              s=Interval([-1, 5.3]),
#                              eps=1e-4)

# bb = BranchAndBoundAlgorithm(f=Func("sin(x)x",
#                                     lambda x: triplet_sin(x)*x if isinstance(x, Triplet) else  Decimal(math.sin(x))* x),
#                              s=Interval([-1, 2]),
#                              eps=1e-4)


# bb = BranchAndBoundAlgorithm(f=Func("x^{5}+2x^{3}+3\left(x-2\right)^{2}+7x^{5}-2",
#                                     lambda x: x ** 5 + Triplet.from_number(2) * x ** 3 + Triplet.from_number(3) * (
#                                                 x - Triplet.from_number(2)) ** 2 + Triplet.from_number(
#                                         7) * x ** 5 - Triplet.from_number(2) if isinstance(x,
#                                                                                            Triplet) else x ** 5 + 2 * x ** 3 + 3 * (
#                                                 x - 2) ** 2 + 7 * x ** 5 - 2),
#                              s=Interval([0.2, 7]),
#                              eps=1e-5)

bb = BranchAndBoundAlgorithm(f=Func("sqrt(x)*sin^2(x)", lambda x: triplet_sqrt(x)*triplet_sin(x)**2 if isinstance(x, Triplet) else Decimal(math.sqrt(x))*Decimal(math.sin(x)**2)),
                             s=Interval([0.2, 7]),
                             eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("2*sin(x)*e^(-x)", lambda x: Triplet.from_number(2)*triplet_sin(x)*triplet_exp(-x) if isinstance(x, Triplet) else 2*Decimal(math.sin(x))*Decimal(math.exp(-x))),
#                              s=Interval([0.5, 2]),
#                              eps=1e-6)

# bb = BranchAndBoundAlgorithm(f=Func("ln(3x)*ln(2x) - 1", lambda x: triplet_log(Triplet.from_number(3)*x)*triplet_log(Triplet.from_number(2)*x) - Triplet.from_number(1) if isinstance(x, Triplet) else Decimal(math.log(3*x)*math.log(2*x)) - Decimal(1)),
#                              s=Interval([0.2, 7]),
#                              eps=1e-5)

# bb = BranchAndBoundAlgorithm(f=Func("sqrt(x)*sin^2(x)", lambda x: Triplet.from_number(1)/(Triplet.from_number(2)*x) if isinstance(x, Triplet) else 1/(2*x)),
#                              s=Interval([0., 7]),
#                              eps=1e-3)

# bb = BranchAndBoundAlgorithm(f=Func("(x-3)^2-25", lambda x: ((x-Triplet.from_number(3))**2 - Triplet.from_number(25) if isinstance(x, Triplet) else (x-3)**2 - 25)),
#                              s=Interval([0, 6.1]),
#                              eps=1e-5)

print("RESULT: ", bb.run())
