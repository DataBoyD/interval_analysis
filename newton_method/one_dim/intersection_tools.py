from practice_interval.interval_lib import Interval


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



