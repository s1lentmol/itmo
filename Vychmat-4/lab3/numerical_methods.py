def left_rectangles(f, a, b, n):
    h = (b - a) / n
    x = a
    s = 0.0
    for _ in range(n):
        s += f(x)
        x += h
    return s * h


def right_rectangles(f, a, b, n):
    h = (b - a) / n
    x = a + h
    s = 0.0
    for _ in range(n):
        s += f(x)
        x += h
    return s * h


def mid_rectangles(f, a, b, n):
    h = (b - a) / n
    x = a + 0.5 * h
    s = 0.0
    for _ in range(n):
        s += f(x)
        x += h
    return s * h


def trapezoid(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        x = a + i * h
        s += f(x)
    return s * h


def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1  # корректировка, если n нечётно
    h = (b - a) / n
    s = f(a) + f(b)
    for k in range(1, n):
        x = a + k * h
        if k % 2 == 1:
            s += 4 * f(x)
        else:
            s += 2 * f(x)
    return s * h / 3


def runge_rule(method, f, a, b, eps, p, n_init=4):
    n = n_init
    I_n = method(f, a, b, n)

    while True:
        n2 = 2 * n
        I_n2 = method(f, a, b, n2)
        error_est = abs(I_n2 - I_n) / (2 ** p - 1)

        if error_est < eps:
            return I_n2, n2
        else:
            n = n2
            I_n = I_n2