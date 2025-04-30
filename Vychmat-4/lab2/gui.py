import json

import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox, QGridLayout, QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from functions import (
    f1, f2, f3, f4,
    g1, g2, g3, g4,
    F_system1, J_system1,
    F_system2, J_system2
)
from numerical_methods import NumericalMethods


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Вычислительная математика - лаб2")
        self.resize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)

        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Метод половинного деления",
            "Метод секущих",
            "Метод простой итерации",
            "Метод Ньютона - для систем"
        ])

        self.function_combo = QComboBox()
        self.function_combo.addItems([
            "f1(x)=e^x + x^2 - 2 = 0",
            "f2(x)=x^3 + 4.81x^2 -17.37x+5.38 = 0",
            "f3(x)=cos(x) - x = 0",
            "f4(x)=sin(x) - x/2 = 0",
            "Система 1: sin(y)+2x-2 = 0, y+cos(x-1)-0.7 = 0",
            "Система 2: x^2+y^2-4 = 0, x-y-1 = 0"
        ])

        # Поля ввода
        self.label_a = QLabel("a:")
        self.edit_a = QLineEdit("0,0")
        self.label_b = QLabel("b:")
        self.edit_b = QLineEdit("2,0")
        self.label_x0 = QLabel("x0:")
        self.edit_x0 = QLineEdit("1,0")
        self.label_x1 = QLabel("x1:")
        self.edit_x1 = QLineEdit("2,0")
        self.label_tol = QLabel("tol:")
        self.edit_tol = QLineEdit("1e-6")

        # Кнопки
        self.solve_button = QPushButton("Вычислить")
        self.solve_button.clicked.connect(self.on_solve_clicked)
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        self.save_button = QPushButton("Сохранить результат")
        self.save_button.clicked.connect(self.save_result)
        self.format_button = QPushButton("Формат JSON")
        self.format_button.clicked.connect(self.show_json_format)
        self.result_label = QLabel("Результат:")

        input_layout = QGridLayout()
        input_layout.addWidget(QLabel("Метод:"), 0, 0)
        input_layout.addWidget(self.method_combo, 0, 1, 1, 2)
        input_layout.addWidget(QLabel("Функция / Система:"), 1, 0)
        input_layout.addWidget(self.function_combo, 1, 1, 1, 2)
        input_layout.addWidget(self.label_a, 2, 0)
        input_layout.addWidget(self.edit_a, 2, 1)
        input_layout.addWidget(self.label_b, 2, 2)
        input_layout.addWidget(self.edit_b, 2, 3)
        input_layout.addWidget(self.label_x0, 3, 0)
        input_layout.addWidget(self.edit_x0, 3, 1)
        input_layout.addWidget(self.label_x1, 3, 2)
        input_layout.addWidget(self.edit_x1, 3, 3)
        input_layout.addWidget(self.label_tol, 4, 0)
        input_layout.addWidget(self.edit_tol, 4, 1)
        input_layout.addWidget(self.solve_button, 5, 0, 1, 4)
        input_layout.addWidget(self.result_label, 6, 0, 1, 4)
        input_layout.addWidget(self.load_button, 7, 0, 1, 2)
        input_layout.addWidget(self.save_button, 7, 2, 1, 2)
        input_layout.addWidget(self.format_button, 8, 0, 1, 4)

        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addLayout(input_layout)
        layout.addLayout(left_layout)
        layout.addWidget(self.canvas)
        central_widget.setLayout(layout)

        self.method_combo.currentIndexChanged.connect(self.update_input_fields)
        self.function_combo.currentIndexChanged.connect(self.update_input_fields)
        self.update_input_fields()

    def update_input_fields(self):
        func_index = self.function_combo.currentIndex()
        is_system = (func_index >= 4)
        model = self.method_combo.model()
        for i in range(self.method_combo.count()):
            text = self.method_combo.itemText(i)
            if text == "Метод Ньютона - для систем":
                if is_system:
                    model.item(i).setEnabled(True)
                else:
                    model.item(i).setEnabled(False)
                    if self.method_combo.currentIndex() == i:
                        self.method_combo.setCurrentIndex(0)
        if is_system:
            self.method_combo.setCurrentIndex(3)
            self.method_combo.setEnabled(False)
            method_index = 3
        else:
            self.method_combo.setEnabled(True)
            method_index = self.method_combo.currentIndex()
        if method_index == 0:
            self.edit_a.setEnabled(True)
            self.edit_b.setEnabled(True)
            self.edit_x0.setEnabled(False)
            self.edit_x1.setEnabled(False)
        elif method_index == 1:
            self.edit_a.setEnabled(False)
            self.edit_b.setEnabled(False)
            self.edit_x0.setEnabled(True)
            self.edit_x1.setEnabled(True)
        elif method_index == 2:
            self.edit_a.setEnabled(False)
            self.edit_b.setEnabled(False)
            self.edit_x0.setEnabled(True)
            self.edit_x1.setEnabled(False)
        else:
            self.edit_a.setEnabled(False)
            self.edit_b.setEnabled(False)
            self.edit_x0.setEnabled(True)
            self.edit_x1.setEnabled(True)

    def parse_input(self, line_edit):
        return float(line_edit.text().strip().replace(',', '.'))

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл с входными данными", "",
                                                  "JSON Files (*.json);;Text Files (*.txt);;Все файлы (*)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
                return
            if "a" in data:
                self.edit_a.setText(str(data["a"]))
            if "b" in data:
                self.edit_b.setText(str(data["b"]))
            if "x0" in data:
                self.edit_x0.setText(str(data["x0"]))
            if "x1" in data:
                self.edit_x1.setText(str(data["x1"]))
            if "tol" in data:
                self.edit_tol.setText(str(data["tol"]))
            if "function_index" in data:
                idx = int(data["function_index"])
                if 0 <= idx < self.function_combo.count():
                    self.function_combo.setCurrentIndex(idx)
            if "method_index" in data:
                idx = int(data["method_index"])
                if 0 <= idx < self.method_combo.count():
                    self.method_combo.setCurrentIndex(idx)

    def save_result(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить результат", "",
                                                  "Text Files (*.txt);;Все файлы (*)")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("Результаты вычислений:\n")
                    f.write(self.result_label.text() + "\n\n")
                    f.write("Входные данные:\n")
                    f.write(f"Функция / Система: {self.function_combo.currentText()}\n")
                    f.write(f"Метод: {self.method_combo.currentText()}\n")
                    f.write(f"a: {self.edit_a.text()}\n")
                    f.write(f"b: {self.edit_b.text()}\n")
                    f.write(f"x0: {self.edit_x0.text()}\n")
                    f.write(f"x1: {self.edit_x1.text()}\n")
                    f.write(f"tol: {self.edit_tol.text()}\n")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def show_json_format(self):
        example_json = (
            '{\n'
            '  "a": "0,0",\n'
            '  "b": "2,0",\n'
            '  "x0": "1,0",\n'
            '  "x1": "2,0",\n'
            '  "tol": "1e-6",\n'
            '  "function_index": 0,\n'
            '  "method_index": 0\n'
            '}'
        )
        description = (
                "Пример формата входного JSON файла:\n\n"
                + example_json +
                "\n\nОписание полей:\n"
                "- a, b – границы интервала (для метода половинного деления, причем a должно быть меньше b).\n"
                "- x0, x1 – начальные приближения (для методов секущих, простой итерации, Ньютона).\n"
                "- tol – точность вычисления.\n"
                "- function_index – индекс функции/системы (0..3 для уравнений, 4..5 для систем).\n"
                "- method_index – индекс метода (0: половинное деление, 1: секущих, 2: простая итерация, 3: Ньютона).\n"
                "При выборе системы method_index игнорируется и автоматически становится 3."
        )
        QMessageBox.information(self, "Формат JSON", description)

    def on_solve_clicked(self):
        method_index = self.method_combo.currentIndex()
        func_index = self.function_combo.currentIndex()

        try:
            tol = self.parse_input(self.edit_tol)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверно задана точность.")
            return

        self.canvas.axes.clear()
        self.canvas.axes.grid(True)
        # Определяем, какую функцию/систему решаем
        if func_index == 0:
            f, g, name = (f1, g1, "f1(x)=e^x + x^2 - 2")
        elif func_index == 1:
            f, g, name = (f2, g2, "f2(x)=x^3 + 4.81x^2 -17.37x+5.38")
        elif func_index == 2:
            f, g, name = (f3, g3, "f3(x)=cos(x) - x")
        elif func_index == 3:
            f, g, name = (f4, g4, "f4(x)=sin(x) - x/2")
        elif func_index == 4:
            f, g, name = (None, None, "Система 1: sin(y)+2x-2, y+cos(x-1)-0.7")
        else:
            f, g, name = (None, None, "Система 2: x^2+y^2-4, x-y-1")

        is_system = (func_index >= 4)

        if method_index == 0:  # Метод половинного деления
            if is_system:
                QMessageBox.warning(self, "Ошибка", "Метод половинного деления не применим к системе.")
                return
            try:
                a = self.parse_input(self.edit_a)
                b = self.parse_input(self.edit_b)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверно заданы границы a и b.")
                return
            if a >= b:
                QMessageBox.warning(self, "Ошибка", "Граница a должна быть меньше b.")
                return
            try:
                root, froot, iters = NumericalMethods.bisection(f, a, b, tol)
                self.result_label.setText(f"Результат: x={root:.6g}, f(x)={froot:.6g}, итераций={iters}")
                margin = 0.5 * (b - a)
                xs = np.linspace(a - margin, b + margin, 500)
                ys = [f(xx) for xx in xs]
                self.canvas.axes.plot(xs, ys, label=name)
                self.canvas.axes.axhline(0, color='black', linewidth=0.8)
                self.canvas.axes.plot(root, froot, 'ro', label="Найденный корень")
                self.canvas.axes.legend()
                self.canvas.draw()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))
                return

        elif method_index == 1:  # Метод секущих
            if is_system:
                QMessageBox.warning(self, "Ошибка", "Метод секущих не применим к системе.")
                return
            try:
                x0 = self.parse_input(self.edit_x0)
                x1 = self.parse_input(self.edit_x1)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверно заданы начальные приближения x0, x1.")
                return
            try:
                root, froot, iters = NumericalMethods.secant(f, x0, x1, tol)
                self.result_label.setText(f"Результат: x={root:.6g}, f(x)={froot:.6g}, итераций={iters}")
                margin = 0.5 * max(abs(x0 - root), abs(x1 - root))
                left = min(x0, x1, root) - margin
                right = max(x0, x1, root) + margin
                xs = np.linspace(left, right, 500)
                ys = [f(xx) for xx in xs]
                self.canvas.axes.plot(xs, ys, label=name)
                self.canvas.axes.axhline(0, color='black', linewidth=0.8)
                self.canvas.axes.plot(root, froot, 'ro', label="Найденный корень")
                self.canvas.axes.legend()
                self.canvas.draw()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))
                return

        elif method_index == 2:  # Метод простой итерации
            if is_system:
                QMessageBox.warning(self, "Ошибка", "Метод простой итерации не применим к системе.")
                return
            try:
                x0 = self.parse_input(self.edit_x0)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверно задано начальное приближение x0.")
                return
            # Если выбрана f1, проверяем, что |x0| < sqrt(2) для корректности g1(x)=ln(2-x^2)
            if func_index == 0:
                if x0 ** 2 >= 2:
                    QMessageBox.warning(self, "Ошибка",
                                        "Для метода простой итерации с f1(x)=e^x+x^2-2 начальное приближение должно удовлетворять |x0| < √2 ≈ 1.414.")
                    return

            try:
                root, err, iters = NumericalMethods.simple_iteration(g, x0, tol)
                self.result_label.setText(f"Результат: x={root:.6g}, f(x)={f(root):.6g}, итераций={iters}")
                margin = 0.5 * abs(root - x0)
                left = min(x0, root) - margin
                right = max(x0, root) + margin
                xs = np.linspace(left, right, 500)
                ys = [f(xx) for xx in xs]
                self.canvas.axes.plot(xs, ys, label=name)
                self.canvas.axes.axhline(0, color='black', linewidth=0.8)
                self.canvas.axes.plot(root, f(root), 'ro', label="Найденный корень")
                self.canvas.axes.legend()
                self.canvas.draw()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))
                return

        else:  # Метод Ньютона - для систем
            if not is_system:
                QMessageBox.warning(self, "Ошибка", "Метод Ньютона для систем применим только к выбранной системе.")
                return
            try:
                x0 = self.parse_input(self.edit_x0)
                y0 = self.parse_input(self.edit_x1)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Неверно заданы начальные приближения x0, y0.")
                return
            if func_index == 4:
                F, J = F_system1, J_system1
            else:
                F, J = F_system2, J_system2
            try:
                sol, iters, errors = NumericalMethods.newton_system(F, J, (x0, y0), tol)
                x_sol, y_sol = sol
                error_vector = errors[-1] if errors else np.array([0, 0])
                error_str = f"({error_vector[0]:.3g}, {error_vector[1]:.3g})"
                f_values = F(x_sol, y_sol)
                check_str = f"Проверка: |F1(x,y)| = {abs(f_values[0]):.3g}, |F2(x,y)| = {abs(f_values[1]):.3g}"
                self.result_label.setText(
                    f"Результат: (x,y)=({x_sol:.6g}, {y_sol:.6g}), итераций={iters}\nПогрешности: {error_str}\n{check_str}"
                )
                dx = 5
                num_points = 300
                X = np.linspace(x_sol - dx, x_sol + dx, num_points)
                Y = np.linspace(y_sol - dx, y_sol + dx, num_points)
                Xgrid, Ygrid = np.meshgrid(X, Y)
                if func_index == 4:
                    F1_vals = np.sin(Ygrid) + 2 * Xgrid - 2
                    F2_vals = Ygrid + np.cos(Xgrid - 1) - 0.7
                else:
                    F1_vals = Xgrid ** 2 + Ygrid ** 2 - 4
                    F2_vals = Xgrid - Ygrid - 1
                self.canvas.axes.contour(Xgrid, Ygrid, F1_vals, levels=[0], colors='blue')
                self.canvas.axes.contour(Xgrid, Ygrid, F2_vals, levels=[0], colors='red')
                self.canvas.axes.plot(x_sol, y_sol, 'ko', label="Решение системы")
                self.canvas.axes.set_xlabel("x")
                self.canvas.axes.set_ylabel("y")
                self.canvas.axes.set_xlim(x_sol - dx, x_sol + dx)
                self.canvas.axes.set_ylim(y_sol - dx, y_sol + dx)
                self.canvas.axes.legend()
                self.canvas.draw()
            except ValueError as e:
                QMessageBox.warning(self, "Ошибка", str(e))
                return
