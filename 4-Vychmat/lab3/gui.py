from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox
)

from functions import FUNCTIONS_DATA
from numerical_methods import (
    left_rectangles, right_rectangles, mid_rectangles,
    trapezoid, simpson, runge_rule
)


def parse_float(text: str) -> float:
    text_dot = text.replace(',', '.')
    return float(text_dot)


class IntegrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вычислительная математика - лаб 3")
        self.init_ui()

    def init_ui(self):
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 1. Выбор функции
        self.func_label = QLabel("Выберите функцию")
        layout.addWidget(self.func_label)

        self.func_combo = QComboBox()
        for expression in FUNCTIONS_DATA.keys():
            self.func_combo.addItem(expression)
        layout.addWidget(self.func_combo)

        # 2. Ввод пределов интегрирования
        bounds_layout = QHBoxLayout()
        self.a_edit = QLineEdit()
        self.a_edit.setPlaceholderText("нижний предел")
        self.b_edit = QLineEdit()
        self.b_edit.setPlaceholderText("верхний предел")
        bounds_layout.addWidget(QLabel("a ="))
        bounds_layout.addWidget(self.a_edit)
        bounds_layout.addWidget(QLabel("b ="))
        bounds_layout.addWidget(self.b_edit)
        layout.addLayout(bounds_layout)

        # 3. Ввод точности
        self.eps_edit = QLineEdit()
        self.eps_edit.setPlaceholderText("Точность (например 0,0001)")
        layout.addWidget(QLabel("Точность вычисления:"))
        layout.addWidget(self.eps_edit)

        # 4. Выбор метода
        self.method_label = QLabel("Выберите метод:")
        layout.addWidget(self.method_label)

        self.method_combo = QComboBox()
        self.method_combo.addItem("Левых прямоугольников")
        self.method_combo.addItem("Правых прямоугольников")
        self.method_combo.addItem("Средних прямоугольников")
        self.method_combo.addItem("Трапеций")
        self.method_combo.addItem("Симпсона")
        layout.addWidget(self.method_combo)

        # 5. Кнопка "Вычислить"
        self.calc_button = QPushButton("Вычислить")
        self.calc_button.clicked.connect(self.on_calculate)
        layout.addWidget(self.calc_button)

        # 6. Метка вывода результата
        self.result_label = QLabel("Результат:")
        layout.addWidget(self.result_label)

    def on_calculate(self):
        try:
            a = parse_float(self.a_edit.text())
            b = parse_float(self.b_edit.text())
            eps = parse_float(self.eps_edit.text())
        except ValueError:
            self.result_label.setText("Ошибка ввода! Пожалуйста, введите числовые значения.")
            return

        if a >= b:
            self.result_label.setText("Ошибка: a должно быть меньше b.")
            return

        expression = self.func_combo.currentText()
        f, F = FUNCTIONS_DATA[expression]

        if expression == "ln(x+1)":
            if a <= -1 or b <= -1:
                self.result_label.setText("Ошибка: для функции ln(x+1) допустимы только значения x > -1.")
                return

        method_name = self.method_combo.currentText()
        if method_name == "Левые прямоугольники":
            method_func = left_rectangles
            p = 2
        elif method_name == "Правые прямоугольники":
            method_func = right_rectangles
            p = 2
        elif method_name == "Средние прямоугольники":
            method_func = mid_rectangles
            p = 2
        elif method_name == "Трапеции":
            method_func = trapezoid
            p = 2
        else:
            method_func = simpson
            p = 4

        try:
            exact_value = F(b) - F(a)
        except ValueError as e:
            self.result_label.setText("Ошибка вычисления точного значения интеграла: " + str(e))
            return

        I_approx, final_n = runge_rule(method_func, f, a, b, eps, p, n_init=4)

        result_str = (
            f"<b>Метод:</b> {method_name}<br>"
            f"<b>Выбранная функция:</b> {expression}<br>"
            f"<b>Точное значение интеграла:</b> {exact_value:.8f}<br>"
            f"<b>Приближённое значение:</b> {I_approx:.8f}<br>"
            f"<b>Число разбиений n:</b> {final_n}"
        )
        self.result_label.setText(result_str)
