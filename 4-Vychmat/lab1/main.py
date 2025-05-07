import numpy as np


def parse_number(s):
    return float(s.replace(',', '.'))


def gauss_elimination(A, b):
    n = len(A)
    A = [row[:] for row in A]  # Квадратная матрица коэффициентов
    b = b[:]  # Вектор свободных членов
    swap_count = 0  # Количество перестановок строк, чтобы понять знак определителя

    # Прямой ход
    for k in range(n):
        # Выбор главного элемента по столбцу k
        max_row = k
        max_val = abs(A[k][k])
        for i in range(k + 1, n):
            if abs(A[i][k]) > max_val:
                max_val = abs(A[i][k])
                max_row = i
        if abs(A[max_row][k]) < 1e-50:
            raise ValueError("Матрица вырождена (нулевой главный элемент)!")

        # Меняем строки
        if max_row != k:
            A[k], A[max_row] = A[max_row], A[k]
            b[k], b[max_row] = b[max_row], b[k]
            swap_count += 1

        # Обнуление элементов столбца k ниже диагонали
        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            A[i][k] = 0.0
            for j in range(k + 1, n):
                A[i][j] -= factor * A[k][j]
            b[i] -= factor * b[k]

    det = 1.0
    for i in range(n):
        det *= A[i][i]
    det *= (-1) ** swap_count

    # Обратный ход
    x = [0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = 0.0
        for j in range(i + 1, n):
            sum_ax += A[i][j] * x[j]
        x[i] = (b[i] - sum_ax) / A[i][i]

    return {"x": x, "A": A, "det": det}


def main():
    print("Выберите способ ввода коэффициентов:")
    print(" 1 - Ввод с клавиатуры")
    print(" 2 - Чтение из файла")
    mode = input("Введите 1 или 2: ").strip()

    if mode == "1":
        try:
            n = int(input("Введите размерность матрицы (n <= 20): "))
        except ValueError:
            print("Некорректное значение размерности!")
            return
        if n > 20 or n <= 0:
            print("Размерность матрицы должна быть в диапазоне 1..20")
            return

        print("Введите коэффициенты матрицы A построчно, разделяя элементы пробелами:")
        A = []
        for i in range(n):
            row_str = input(f"Строка {i + 1}: ").split()
            if len(row_str) != n:
                print(f"Ошибка: необходимо ввести ровно {n} коэффициентов!")
                return
            try:
                row = [parse_number(x) for x in row_str]
            except ValueError:
                print("Ошибка преобразования строки в число!")
                return
            A.append(row)

        b_str = input("Введите столбец свободных членов B (через пробел): ").split()
        if len(b_str) != n:
            print(f"Ошибка: необходимо ввести ровно {n} свободных членов!")
            return
        try:
            b = [parse_number(x) for x in b_str]
        except ValueError:
            print("Ошибка преобразования строки в число!")
            return

    elif mode == "2":
        filename = input("Введите имя файла: ").strip()
        try:
            with open(filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
            n = int(lines[0])
            if n > 20 or n <= 0:
                print("Размерность матрицы должна быть в диапазоне 1..20")
                return
            if len(lines) != n + 2:
                print("Неверный формат файла!")
                return
            A = []
            for i in range(1, n + 1):
                row_str = lines[i].split()
                if len(row_str) != n:
                    print(f"Ошибка: в строке {i} должно быть {n} коэффициентов!")
                    return
                row = [parse_number(x) for x in row_str]
                A.append(row)
            b = [parse_number(x) for x in lines[n + 1].split()]
            if len(b) != n:
                print("Ошибка: количество свободных членов не совпадает с размерностью матрицы!")
                return
        except Exception as e:
            print("Ошибка при чтении файла:", e)
            return
    else:
        print("Неверный выбор ввода!")
        return

    A_orig = [row[:] for row in A]
    b_orig = b[:]

    try:
        result = gauss_elimination(A, b)
        x = result["x"]
        A_triangular = result["A"]
        det = result["det"]
    except Exception as e:
        print("Ошибка при решении системы:", e)
        return

    # Вычисление вектора невязок: r = A_orig * x - b_orig
    residuals = []
    for i in range(len(A_orig)):
        s = sum(A_orig[i][j] * x[j] for j in range(len(A_orig)))
        residuals.append(s - b_orig[i])

    # Решение системы с использованием библиотеки NumPy
    A_np = np.array(A_orig, dtype=float)
    b_np = np.array(b_orig, dtype=float)
    try:
        x_np = np.linalg.solve(A_np, b_np)
        det_np = np.linalg.det(A_np)
    except Exception as e:
        print("Ошибка в решении системы с помощью библиотеки NumPy:", e)
        x_np = None
        det_np = None

    # Вывод результатов
    print("\n--- Результаты решения ---\n")
    print("Треугольная матрица (после прямого хода, с преобразованным столбцом B):")
    for i in range(n):
        row_str = ""
        for j in range(n):
            row_str += f"{A_triangular[i][j]: 10.10f} "
        row_str += "| " + f"{b[i]: 10.10f}"
        print(row_str)

    print("\nВектор неизвестных (метод Гаусса):")
    for i in range(n):
        print(f"  x{i + 1} = {x[i]: .10f}")

    print("\nВектор невязок (метод Гаусса):")
    for i in range(n):
        print(f"  r{i + 1} = {residuals[i]: .10e}")

    print("\nРешение с использованием библиотеки NumPy:")
    if x_np is not None:
        for i in range(n):
            print(f"  x{i + 1} = {x_np[i]: .10f}")

    print("\nОпределитель матрицы (метод Гаусса):")
    print(f"  det = {det: .10f}")
    print("Определитель матрицы (numpy.linalg.det):")
    if det_np is not None:
        print(f"  det = {det_np: .10f}")


if __name__ == "__main__":
    main()
