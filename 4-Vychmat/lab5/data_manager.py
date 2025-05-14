import math


def load_from_file(path):
    xs, ys = [], []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            x_str, y_str = parts
            x = float(x_str.replace(',', '.'))
            y = float(y_str.replace(',', '.'))
            xs.append(x)
            ys.append(y)
    if len(xs) < 2:
        raise ValueError('Недостаточно точек в файле')
    return xs, ys


def generate_data(f_str, a, b, n):
    xs = [a + i * (b - a) / (n - 1) for i in range(n)]
    if f_str == 'sin(x)':
        ys = [math.sin(x) for x in xs]
    elif f_str == 'cos(x)':
        ys = [math.cos(x) for x in xs]
    elif f_str == 'exp(x)':
        ys = [math.exp(x) for x in xs]
    elif f_str == 'x^2':
        ys = [x ** 2 for x in xs]
    else:
        raise ValueError(f'Неизвестная функция: {f_str}')
    return xs, ys
