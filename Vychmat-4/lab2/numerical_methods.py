import numpy as np


class NumericalMethods:
    @staticmethod
    def bisection(f, a, b, tol=1e-6):
        fa = f(a)
        fb = f(b)
        if fa * fb > 0:
            raise ValueError("На концах отрезка функция не меняет знак. Возможно, нет корня или их несколько.")
        iteration = 0
        while iteration < 100:
            iteration += 1
            c = (a + b) / 2.0
            fc = f(c)
            if abs(fc) < tol or abs(b - a) < tol:
                return c, fc, iteration
            if fa * fc < 0:
                b = c
                fb = fc
            else:
                a = c
                fa = fc
        return (a + b) / 2.0, f((a + b) / 2.0), iteration

    @staticmethod
    def secant(f, x0, x1, tol=1e-6):
        f0 = f(x0)
        f1 = f(x1)
        iteration = 0
        for i in range(100):
            iteration += 1
            if abs(f1 - f0) < 1e-14:
                raise ValueError("Разность f(x1) и f(x0) слишком мала, деление на 0.")
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
            f2 = f(x2)
            if abs(f2) < tol:
                return x2, f2, iteration
            x0, x1 = x1, x2
            f0, f1 = f1, f2
        return x2, f2, iteration

    @staticmethod
    def simple_iteration(g, x0, tol=1e-6, h=1e-5):
        derivative = (g(x0 + h) - g(x0 - h)) / (2 * h)
        if abs(derivative) >= 1:
            raise ValueError(f"Достаточное условие сходимости не выполнено: |g'(x0)| = {abs(derivative):.3f} ≥ 1.")
        iteration = 0
        x_current = x0
        for i in range(100):
            iteration += 1
            x_next = g(x_current)
            if abs(x_next - x_current) < tol:
                return x_next, abs(x_next - x_current), iteration
            x_current = x_next
        return x_current, abs(g(x_current) - x_current), iteration

    @staticmethod
    def newton_system(F, J, xy0, eps=1e-6):
        x, y = xy0
        errors = []
        for iteration in range(1, 101):
            f_val = np.array(F(x, y), dtype=float)
            j_val = np.array(J(x, y), dtype=float)
            try:
                delta = np.linalg.solve(j_val, -f_val)
            except np.linalg.LinAlgError:
                raise ValueError("Матрица Якоби является вырожденной (детерминант равен 0).")
            errors.append(np.abs(delta))
            if np.max(np.abs(delta)) < eps:
                x += delta[0]
                y += delta[1]
                return (x, y), iteration, errors
            x += delta[0]
            y += delta[1]
        return (x, y), 100, errors
