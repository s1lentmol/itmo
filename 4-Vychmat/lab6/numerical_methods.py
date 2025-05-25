import math


def get_equations():
    return [
        ("y' = y", lambda x, y: y, lambda x, x0, y0: y0 * math.exp(x - x0)),
        ("y' = x + y", lambda x, y: x + y,
         lambda x, x0, y0: -(x + 1) + (y0 + x0 + 1) * math.exp(x - x0)),
        ("y' = x * y", lambda x, y: x * y,
         lambda x, x0, y0: y0 * math.exp((x ** 2 - x0 ** 2) / 2)),
        ("y' = sin(x) - y", lambda x, y: math.sin(x) - y,
         lambda x, x0, y0: 0.5 * (math.sin(x) - math.cos(x)) + \
                           (y0 - 0.5 * (math.sin(x0) - math.cos(x0))) * math.exp(-(x - x0))),
        ("y' = y*(1 - y)", lambda x, y: y * (1 - y),
         lambda x, x0, y0: 1 / (1 + ((1 - y0) / y0) * math.exp(-(x - x0))))
    ]


def euler(f, x0, y0, xn, h):
    n = max(int((xn - x0) / h), 0)
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [y0]
    for i in range(n):
        try:
            ys.append(ys[i] + h * f(xs[i], ys[i]))
        except Exception:
            ys.append(float('nan'))
    return xs, ys


def improved_euler(f, x0, y0, xn, h):
    n = max(int((xn - x0) / h), 0)
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [y0]
    for i in range(n):
        try:
            k1 = f(xs[i], ys[i])
            y_temp = ys[i] + h * k1
            k2 = f(xs[i + 1], y_temp)
            ys.append(ys[i] + h * (k1 + k2) / 2)
        except Exception:
            ys.append(float('nan'))
    return xs, ys


def milne(f, x0, y0, xn, h):
    n = max(int((xn - x0) / h), 0)
    if n < 3:
        raise ValueError("Недостаточно шагов для метода Милна")
    xs = [x0 + i * h for i in range(n + 1)]
    _, ys0 = improved_euler(f, x0, y0, x0 + 3 * h, h)
    ys = ys0[:]
    for i in range(3, n):
        try:
            f_i3 = f(xs[i - 3], ys[i - 3])
            f_i2 = f(xs[i - 2], ys[i - 2])
            f_i1 = f(xs[i - 1], ys[i - 1])
            f_i = f(xs[i], ys[i])
            y_pred = ys[i - 3] + (4 * h / 3) * (2 * f_i - f_i1 + 2 * f_i2)
            f_pred = f(xs[i + 1], y_pred)
            y_corr = ys[i - 1] + (h / 3) * (f_pred + 4 * f_i + f_i1)
            ys.append(y_corr)
        except Exception:
            ys.append(float('nan'))
    return xs, ys


def runge_error(_, ys_h, f, x0, y0, xn, h, method='euler'):
    try:
        if method == 'euler':
            _, ys_h2 = euler(f, x0, y0, xn, h / 2)
            p = 1
        else:
            _, ys_h2 = improved_euler(f, x0, y0, xn, h / 2)
            p = 2
        err = []
        for i, y in enumerate(ys_h):
            err.append(abs((ys_h2[2 * i] - y) / (2 ** p - 1)))
        return err
    except Exception:
        return [float('nan')] * len(ys_h)


def exact_solution(exact, x0, y0, xn, h):
    n = max(int((xn - x0) / h), 0)
    xs = [x0 + i * h for i in range(n + 1)]
    ys = []
    for x in xs:
        try:
            ys.append(exact(x, x0, y0))
        except Exception:
            ys.append(float('nan'))
    return xs, ys
