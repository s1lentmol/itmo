import math


# 1) f1(x)= e^x + x^2 - 2
# 2) f2(x)= x^3 + 4.81x^2 - 17.37x + 5.38
# 4) f3(x)= cos(x) - x
# 5) f4(x)= sin(x) - x/2

def f1(x):
    return math.exp(x) + x * x - 2


def f2(x):
    return x ** 3 + 4.81 * x ** 2 - 17.37 * x + 5.38


def f3(x):
    return math.cos(x) - x


def f4(x):
    return math.sin(x) - x / 2


# Итерационные функции

def g1(x):
    # f1(x)= e^x + x^2 -2=0 => e^x = 2 - x^2 => x= ln(2 - x^2)
    return math.log(2 - x * x) if (2 - x * x) > 0 else x


def g2(x):
    # f2(x)= x^3 + 4.81x^2 -17.37x +5.38=0 => x = (x^3 + 4.81x^2 + 5.38)/17.37
    return (x*x*x + 4.81 * x*x + 5.38) / 17.37


def g3(x):
    # f3(x)= cos(x)-x=0 => x= cos(x)
    return math.cos(x)


def g4(x):
    # f4(x)= sin(x)-x/2=0 => x= 2*sin(x)
    return 2 * math.sin(x)


# Cистемы
#
# 1) F_system1:
#    F1(x,y)= sin(y)+2x-2
#    F2(x,y)= y + cos(x-1) - 0.7
#
# 2) F_system2:
#    F1(x,y)= x^2 + y^2 - 4
#    F2(x,y)= x - y - 1
def F_system1(x, y):
    return [
        math.sin(y) + 2 * x - 2,
        y + math.cos(x - 1) - 0.7
    ]


def J_system1(x, y):
    return [
        [2, math.cos(y)],
        [-math.sin(x - 1), 1]
    ]


def F_system2(x, y):
    return [
        x * x + y * y - 4,
        x - y - 1
    ]


def J_system2(x, y):
    return [
        [2 * x, 2 * y],
        [1, -1]
    ]
