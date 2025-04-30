import sys
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QTextEdit, QMessageBox,
                             QTableWidget, QTableWidgetItem, QGroupBox)
from PyQt5.QtCore import Qt
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from approx import (linear_fit, quadratic_fit, cubic_fit, exp_fit, log_fit, power_fit)
from data_manager import load_data_from_txt

# Функция форматирования числа: если abs(num) < 0.001, выводим "0"
def fmt(num):
    if abs(num) < 1e-3:
        return "0"
    else:
        return f"{num:.4f}"

# Функция формирования строки функции с подставленными коэффициентами
def function_str(model, coeffs):
    if model == "Линейная":
        a, b = coeffs
        return f"f(x) = {fmt(a)} * x + {fmt(b)}"
    elif model == "Квадратичная":
        a, b, c = coeffs
        return f"f(x) = {fmt(a)} * x² + {fmt(b)} * x + {fmt(c)}"
    elif model == "Кубическая":
        a, b, c, d = coeffs
        return f"f(x) = {fmt(a)} * x³ + {fmt(b)} * x² + {fmt(c)} * x + {fmt(d)}"
    elif model == "Экспоненциальная":
        A, B = coeffs
        return f"f(x) = {fmt(A)} * exp({fmt(B)} * x)"
    elif model == "Логарифмическая":
        A, B = coeffs
        return f"f(x) = {fmt(A)} + {fmt(B)} * ln(x)"
    elif model == "Степенная":
        A, B = coeffs
        return f"f(x) = {fmt(A)} * x^({fmt(B)})"
    else:
        return "Неизвестная модель"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аппроксимация данных методом наименьших квадратов")
        self.resize(1200, 800)
        self.data_loaded = False
        self.x = None
        self.y = None
        self.results = {}
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()  # Горизонтальный layout

        # Левая панель: управление, таблица входных данных и вывод результатов
        left_panel = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.load_file_btn = QPushButton("Загрузить из файла (TXT)")
        self.load_file_btn.clicked.connect(self.load_data_from_file)
        btn_layout.addWidget(self.load_file_btn)

        self.update_data_btn = QPushButton("Обновить данные")
        self.update_data_btn.clicked.connect(self.update_data_from_table)
        btn_layout.addWidget(self.update_data_btn)

        self.compute_btn = QPushButton("Вычислить аппроксимации")
        self.compute_btn.clicked.connect(self.compute_approximations)
        btn_layout.addWidget(self.compute_btn)

        self.save_btn = QPushButton("Сохранить результаты")
        self.save_btn.clicked.connect(self.save_results)
        btn_layout.addWidget(self.save_btn)

        left_panel.addLayout(btn_layout)

        input_group = QGroupBox("Входные данные (Формат: два столбца, разделенных пробелом: x и f(x))")
        input_layout = QVBoxLayout()
        self.input_table = QTableWidget(12, 2)
        self.input_table.setHorizontalHeaderLabels(["x", "f(x)"])
        self.input_table.horizontalHeader().setStretchLastSection(True)
        input_layout.addWidget(self.input_table)
        input_group.setLayout(input_layout)
        left_panel.addWidget(input_group)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("font: 12px;")
        left_panel.addWidget(self.output_text)

        # Правая панель: встроенный график
        right_panel = QVBoxLayout()
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        right_panel.addWidget(self.canvas)

        self.plot_btn = QPushButton("Построить графики")
        self.plot_btn.clicked.connect(self.plot_graphs)
        right_panel.addWidget(self.plot_btn)

        main_layout.addLayout(left_panel, stretch=3)
        main_layout.addLayout(right_panel, stretch=4)
        central_widget.setLayout(main_layout)

    def load_data_from_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите TXT-файл с данными", "",
                                                   "Text Files (*.txt);;Все файлы (*)", options=options)
        if file_name:
            try:
                self.x, self.y = load_data_from_txt(file_name)
                if len(self.x) < 8 or len(self.x) > 12:
                    QMessageBox.warning(self, "Ошибка", "Данные должны содержать от 8 до 12 точек.")
                    self.data_loaded = False
                else:
                    self.data_loaded = True
                    self.fill_table_with_data()
                    self.output_text.append(
                        f"<b>Данные успешно загружены из файла:</b> {file_name}<br>"
                        f"<b>Количество точек:</b> {len(self.x)}<br><hr>"
                    )
            except Exception as e:
                QMessageBox.critical(self, "Ошибка загрузки", str(e))
                self.data_loaded = False

    def fill_table_with_data(self):
        self.input_table.setRowCount(len(self.x))
        for i in range(len(self.x)):
            item_x = QTableWidgetItem(f"{self.x[i]}")
            item_fx = QTableWidgetItem(f"{self.y[i]}")
            item_x.setTextAlignment(Qt.AlignCenter)
            item_fx.setTextAlignment(Qt.AlignCenter)
            self.input_table.setItem(i, 0, item_x)
            self.input_table.setItem(i, 1, item_fx)
        self.input_table.resizeColumnsToContents()
        self.input_table.resizeRowsToContents()

    def update_data_from_table(self):
        xs = []
        ys = []
        for row in range(self.input_table.rowCount()):
            x_item = self.input_table.item(row, 0)
            y_item = self.input_table.item(row, 1)
            # Если хотя бы одна из ячеек отсутствует, пропускаем строку
            if x_item is None or y_item is None:
                continue
            x_str = x_item.text().strip().replace(',', '.')
            y_str = y_item.text().strip().replace(',', '.')
            # Пропускаем пустые строки
            if x_str == "" or y_str == "":
                continue
            try:
                x_val = float(x_str)
                y_val = float(y_str)
            except ValueError:
                QMessageBox.warning(self, "Ошибка ввода",
                    f"Некорректное число в строке {row+1}. Введите только числа (разделитель может быть запятой).")
                return  # Прерываем обновление, если обнаружен некорректный ввод
            xs.append(x_val)
            ys.append(y_val)
        if len(xs) < 8:
            QMessageBox.warning(self, "Ошибка", "В таблице должно быть не менее 8 корректных точек.")
            self.data_loaded = False
            return
        if len(xs) > 12:
            xs = xs[:12]
            ys = ys[:12]
        self.x, self.y = np.array(xs), np.array(ys)
        self.data_loaded = True
        self.output_text.append(
            f"<b>Данные успешно обновлены.</b><br>"
            f"<b>Количество точек:</b> {len(self.x)}<br><hr>"
        )

    def compute_approximations(self):
        if not self.data_loaded:
            QMessageBox.warning(self, "Внимание", "Сначала загрузите или обновите данные!")
            return
        self.results = {}
        S_total = np.sum((self.y - np.mean(self.y)) ** 2)

        def r2_message(r2):
            if r2 >= 0.9:
                return "Высокая степень детерминации."
            elif r2 >= 0.7:
                return "Средняя степень детерминации."
            else:
                return "Низкая степень детерминации."

        try:
            res_lin = linear_fit(self.x, self.y)
            res_lin['R2'] = 1 - res_lin['S'] / S_total
            corr_coef = np.corrcoef(self.x, self.y)[0, 1]
            res_lin['pearson'] = corr_coef
            res_lin['message'] = r2_message(res_lin['R2'])
            self.results['Линейная'] = res_lin
        except Exception as e:
            self.results['Линейная'] = {'error': str(e)}

        try:
            res_quad = quadratic_fit(self.x, self.y)
            res_quad['R2'] = 1 - res_quad['S'] / S_total
            res_quad['message'] = r2_message(res_quad['R2'])
            self.results['Квадратичная'] = res_quad
        except Exception as e:
            self.results['Квадратичная'] = {'error': str(e)}

        try:
            res_cubic = cubic_fit(self.x, self.y)
            res_cubic['R2'] = 1 - res_cubic['S'] / S_total
            res_cubic['message'] = r2_message(res_cubic['R2'])
            self.results['Кубическая'] = res_cubic
        except Exception as e:
            self.results['Кубическая'] = {'error': str(e)}

        try:
            res_exp = exp_fit(self.x, self.y)
            res_exp['R2'] = 1 - res_exp['S'] / S_total
            res_exp['message'] = r2_message(res_exp['R2'])
            self.results['Экспоненциальная'] = res_exp
        except Exception as e:
            self.results['Экспоненциальная'] = {'error': str(e)}

        if np.any(self.x <= 0):
            self.results['Логарифмическая'] = {'error': 'x должны быть > 0 для логарифмической аппроксимации.'}
        else:
            try:
                res_log = log_fit(self.x, self.y)
                res_log['R2'] = 1 - res_log['S'] / S_total
                res_log['message'] = r2_message(res_log['R2'])
                self.results['Логарифмическая'] = res_log
            except Exception as e:
                self.results['Логарифмическая'] = {'error': str(e)}

        if np.any(self.x <= 0) or np.any(self.y <= 0):
            self.results['Степенная'] = {'error': 'x и f(x) должны быть > 0 для степенной аппроксимации.'}
        else:
            try:
                res_power = power_fit(self.x, self.y)
                res_power['R2'] = 1 - res_power['S'] / S_total
                res_power['message'] = r2_message(res_power['R2'])
                self.results['Степенная'] = res_power
            except Exception as e:
                self.results['Степенная'] = {'error': str(e)}

        self.display_results()

    def display_results(self):
        result_str = "<h3>Результаты аппроксимации:</h3>"
        best_model = None
        best_rms = float('inf')
        for key, res in self.results.items():
            result_str += f"<b>Модель: {key}</b><br>"
            if 'error' in res:
                result_str += f"&nbsp;&nbsp;Ошибка: {res['error']}<br><br>"
            else:
                # Формируем вид функции с подставленными коэффициентами
                func_str = function_str(key, res['coefficients'])
                if key == "Линейная":
                    result_str += f"&nbsp;&nbsp;<b>Коэффициент корреляции Пирсона:</b> {res['pearson']:.3f}<br>"
                result_str += f"&nbsp;&nbsp;<b>Функция:</b> {func_str}<br>"
                result_str += f"&nbsp;&nbsp;<b>S (сумма квадратов ошибок):</b> {res['S']:.3f}<br>"
                result_str += f"&nbsp;&nbsp;<b>СКО:</b> {res['rms']:.3f}<br>"
                result_str += f"&nbsp;&nbsp;<b>Коэффициент детерминации R²:</b> {res['R2']:.3f}<br>"
                result_str += f"&nbsp;&nbsp;<b>Заключение:</b> {res['message']}<br><br>"
                if res['rms'] < best_rms:
                    best_rms = res['rms']
                    best_model = key
        if best_model is not None:
            result_str += f"<h4>Наилучшая аппроксимирующая функция: {best_model}</h4>"
        self.output_text.setHtml(result_str)

    def plot_graphs(self):
        if not self.data_loaded or not self.results:
            QMessageBox.warning(self, "Внимание", "Сначала загрузите данные и выполните вычисления!")
            return

        self.ax.clear()
        self.ax.scatter(self.x, self.y, color='black', label='Исходные данные')

        margin_x = 0.1 * (max(self.x) - min(self.x))
        margin_y = 0.1 * (max(self.y) - min(self.y)) if max(self.y) != min(self.y) else 1.0
        self.ax.set_xlim(min(self.x) - margin_x, max(self.x) + margin_x)
        self.ax.set_ylim(min(self.y) - margin_y, max(self.y) + margin_y)

        self.ax.axhline(0, color='gray', linewidth=0.8, linestyle='--')
        self.ax.axvline(0, color='gray', linewidth=0.8, linestyle='--')

        x_range = np.linspace(min(self.x) - margin_x, max(self.x) + margin_x, 300)
        for key, res in self.results.items():
            if 'error' in res:
                continue
            phi = res['phi_func'](x_range)
            self.ax.plot(x_range, phi, label=key)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title("Аппроксимация данных")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()

    def save_results(self):
        if self.output_text.toPlainText().strip() == "":
            QMessageBox.warning(self, "Внимание", "Нет результатов для сохранения.")
            return
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "",
                                                   "Text Files (*.txt);;HTML Files (*.html);;Все файлы (*)",
                                                   options=options)
        if file_name:
            try:
                if self.x is not None and self.y is not None:
                    input_data_txt = "Входные данные:\n"
                    for i in range(len(self.x)):
                        input_data_txt += f"  x[{i}]: {self.x[i]}, f(x)[{i}]: {self.y[i]}\n"
                    input_data_html = "<h3>Входные данные:</h3><table border='1' cellspacing='0' cellpadding='4'><tr><th>x</th><th>f(x)</th></tr>"
                    for i in range(len(self.x)):
                        input_data_html += f"<tr><td>{self.x[i]}</td><td>{self.y[i]}</td></tr>"
                    input_data_html += "</table><br>"
                else:
                    input_data_txt = ""
                    input_data_html = ""

                if file_name.lower().endswith(".txt"):
                    content = input_data_txt + "\n" + self.output_text.toPlainText()
                else:
                    content = input_data_html + self.output_text.toHtml()
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(content)
                QMessageBox.information(self, "Сохранение", "Результаты успешно сохранены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка сохранения", str(e))

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
