import numpy as np


def compute_S_rms(phi_vals, y):
    S = np.sum((phi_vals - y) ** 2)
    rms = np.sqrt(S / len(y))
    return S, rms


# 1. Линейная функция: phi(x) = a*x + b
def linear_fit(x, y):
    n = len(x)
    Sx = np.sum(x)
    Sy = np.sum(y)
    Sxx = np.sum(x * x)
    Sxy = np.sum(x * y)
    denom = n * Sxx - Sx ** 2
    if denom == 0:
        raise Exception("Деление на ноль при вычислении коэффициентов линейной модели.")
    a = (n * Sxy - Sx * Sy) / denom
    b = (Sy - a * Sx) / n
    phi_vals = a * x + b
    S, rms = compute_S_rms(phi_vals, y)
    return {"coefficients": [a, b], "S": S, "rms": rms, "phi": phi_vals,
            "phi_func": lambda x_val: a * x_val + b}


# 2. Квадратичная функция: phi(x) = a*x^2 + b*x + c
def quadratic_fit(x, y):
    n = len(x)
    S0 = n
    Sx = np.sum(x)
    Sx2 = np.sum(x ** 2)
    Sx3 = np.sum(x ** 3)
    Sx4 = np.sum(x ** 4)
    Sy = np.sum(y)
    Sxy = np.sum(x * y)
    Sx2y = np.sum(x ** 2 * y)
    # Система нормальных уравнений:
    # [Sx4  Sx3  Sx2] [a] = [Sx2y]
    # [Sx3  Sx2  Sx ] [b]   [Sxy ]
    # [Sx2  Sx   S0 ] [c]   [Sy  ]
    A = np.array([[Sx4, Sx3, Sx2],
                  [Sx3, Sx2, Sx],
                  [Sx2, Sx, S0]])
    B = np.array([Sx2y, Sxy, Sy])
    coeffs = np.linalg.solve(A, B)
    phi_vals = coeffs[0] * x ** 2 + coeffs[1] * x + coeffs[2]
    S, rms = compute_S_rms(phi_vals, y)
    return {"coefficients": coeffs.tolist(), "S": S, "rms": rms, "phi": phi_vals,
            "phi_func": lambda x_val: coeffs[0] * x_val ** 2 + coeffs[1] * x_val + coeffs[2]}


# 3. Кубическая функция: phi(x) = a*x^3 + b*x^2 + c*x + d
def cubic_fit(x, y):
    n = len(x)
    S0 = n
    Sx = np.sum(x)
    Sx2 = np.sum(x ** 2)
    Sx3 = np.sum(x ** 3)
    Sx4 = np.sum(x ** 4)
    Sx5 = np.sum(x ** 5)
    Sx6 = np.sum(x ** 6)
    Sy = np.sum(y)
    Sxy = np.sum(x * y)
    Sx2y = np.sum(x ** 2 * y)
    Sx3y = np.sum(x ** 3 * y)
    # Система нормальных уравнений 4x4
    A = np.array([[Sx6, Sx5, Sx4, Sx3],
                  [Sx5, Sx4, Sx3, Sx2],
                  [Sx4, Sx3, Sx2, Sx],
                  [Sx3, Sx2, Sx, S0]])
    B = np.array([Sx3y, Sx2y, Sxy, Sy])
    coeffs = np.linalg.solve(A, B)
    phi_vals = coeffs[0] * x ** 3 + coeffs[1] * x ** 2 + coeffs[2] * x + coeffs[3]
    S, rms = compute_S_rms(phi_vals, y)
    return {"coefficients": coeffs.tolist(), "S": S, "rms": rms, "phi": phi_vals,
            "phi_func": lambda x_val: coeffs[0] * x_val ** 3 + coeffs[1] * x_val ** 2 + coeffs[2] * x_val + coeffs[3]}


# 4. Экспоненциальная функция: phi(x) = A * exp(B * x)
# Для y>0 используем линеаризацию: ln(y) = ln(A) + B*x
def exp_fit(x, y):
    if np.any(y <= 0):
        raise Exception("Экспоненциальная аппроксимация требует y > 0.")
    # Применяем преобразование: Y = ln(y)
    Y = np.log(y)
    # Решаем линейную модель: Y = B*x + lnA
    n = len(x)
    Sx = np.sum(x)
    SY = np.sum(Y)
    Sxx = np.sum(x * x)
    SxY = np.sum(x * Y)
    denom = n * Sxx - Sx ** 2
    if denom == 0:
        raise Exception("Деление на ноль при экспоненциальной аппроксимации.")
    B = (n * SxY - Sx * SY) / denom
    lnA = (SY - B * Sx) / n
    A = np.exp(lnA)
    phi_vals = A * np.exp(B * x)
    S, rms = compute_S_rms(phi_vals, y)
    return {"coefficients": [A, B], "S": S, "rms": rms, "phi": phi_vals,
            "phi_func": lambda x_val: A * np.exp(B * x_val)}


# 5. Логарифмическая функция: phi(x) = A + B * ln(x)  (x > 0)
def log_fit(x, y):
    if np.any(x <= 0):
        raise Exception("Логарифмическая аппроксимация требует x > 0.")
    U = np.log(x)
    n = len(x)
    SU = np.sum(U)
    Sy = np.sum(y)
    SUU = np.sum(U * U)
    SUy = np.sum(U * y)
    denom = n * SUU - SU ** 2
    if denom == 0:
        raise Exception("Деление на ноль при логарифмической аппроксимации.")
    B = (n * SUy - SU * Sy) / denom
    A = (Sy - B * SU) / n
    phi_vals = A + B * np.log(x)
    S, rms = compute_S_rms(phi_vals, y)
    return {"coefficients": [A, B], "S": S, "rms": rms, "phi": phi_vals,
            "phi_func": lambda x_val: A + B * np.log(x_val)}


# 6. Степенная функция: phi(x) = A * x^B  (x > 0, y > 0)
def power_fit(x, y):
    if np.any(x <= 0) or np.any(y <= 0):
        raise Exception("Степенная аппроксимация требует x > 0 и y > 0.")
    U = np.log(x)
    V = np.log(y)
    n = len(x)
    SU = np.sum(U)
    SV = np.sum(V)
    SUU = np.sum(U * U)
    SUV = np.sum(U * V)
    denom = n * SUU - SU ** 2
    if denom == 0:
        raise Exception("Деление на ноль при степенной аппроксимации.")
    B = (n * SUV - SU * SV) / denom
    lnA = (SV - B * SU) / n
    A = np.exp(lnA)
    phi_vals = A * x ** B
    S, rms = compute_S_rms(phi_vals, y)
    return {"coefficients": [A, B], "S": S, "rms": rms, "phi": phi_vals,
            "phi_func": lambda x_val: A * x_val ** B}
