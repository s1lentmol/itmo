import math


def func_polynomial(x):
    """ f(x) = 2x^3 - 5x^2 + x - 1 """
    return 2 * x ** 3 - 5 * x ** 2 + x - 1


def func_trig(x):
    """ f(x) = sin(x) + cos(2x) """
    return math.sin(x) + math.cos(2 * x)


def func_log(x):
    """ f(x) = ln(x+1) """
    return math.log(x + 1)


def func_exponential(x):
    """ f(x) = e^(0.5*x) """
    return math.exp(0.5 * x)


def func_custom(x):
    """ f(x) = x^2*sin(x) - 3 """
    return x ** 2 * math.sin(x) - 3


# --- 2. Первообразные для точного вычисления интеграла ---
def F_polynomial(x):
    """
    F(x) = (2/4)x^4 - (5/3)x^3 + (x^2)/2 - x
         = 0.5*x^4 - (5/3)*x^3 + 0.5*x^2 - x
    """
    return 0.5 * x ** 4 - (5 / 3) * x ** 3 + 0.5 * x ** 2 - x


def F_trig(x):
    """
    F(x) = -cos(x) + (1/2)*sin(2x)
    """
    return -math.cos(x) + 0.5 * math.sin(2 * x)


def F_log(x):
    """
    F(x) = (x+1)*ln(x+1) - x
    """
    return (x + 1) * math.log(x + 1) - x


def F_exponential(x):
    """
    F(x) = 2*e^(0.5*x)
    """
    return 2 * math.exp(0.5 * x)


def F_custom(x):
    """
    F(x) = ∫( x^2*sin(x) - 3 ) dx
         = ∫ x^2*sin(x) dx - 3x
    Для x^2*sin(x):
       ∫ x^2 sin(x) dx = -x^2 cos(x) + 2x sin(x) + 2 cos(x)
    Итого:
       F(x) = [-x^2 cos(x) + 2x sin(x) + 2 cos(x)] - 3x
    """
    return (-x ** 2 * math.cos(x) + 2 * x * math.sin(x) + 2 * math.cos(x)) - 3 * x


FUNCTIONS_DATA = {
    "2x^3 - 5x^2 + x - 1": (func_polynomial, F_polynomial),
    "sin(x) + cos(2x)": (func_trig, F_trig),
    "ln(x+1)": (func_log, F_log),
    "e^(0.5*x)": (func_exponential, F_exponential),
    "x^2*sin(x) - 3": (func_custom, F_custom)
}
