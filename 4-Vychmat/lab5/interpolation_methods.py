def lagrange(xs, ys, x0):
    n = len(xs)
    result = 0.0
    for i in range(n):
        term = ys[i]
        for j in range(n):
            if i != j:
                term *= (x0 - xs[j]) / (xs[i] - xs[j])
        result += term
    return result


def newton_divided(xs, ys, x0):
    n = len(xs)
    coef = ys.copy()
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (xs[i] - xs[i - j])
    result = coef[n - 1]
    for k in range(n - 2, -1, -1):
        result = result * (x0 - xs[k]) + coef[k]
    return result


def compute_finite_diff_table(ys):
    table = [ys.copy()]
    for level in range(1, len(ys)):
        prev = table[level - 1]
        curr = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        table.append(curr)
    return table


def newton_finite(xs, ys, x0):
    if len(xs) < 2:
        raise ValueError('Недостаточно точек для конечных разностей')
    h = xs[1] - xs[0]
    diff = compute_finite_diff_table(ys)
    s = (x0 - xs[0]) / h
    result = ys[0]
    prod = 1.0
    for i in range(1, len(ys)):
        prod *= (s - (i - 1)) / i
        result += prod * diff[i][0]
    return result