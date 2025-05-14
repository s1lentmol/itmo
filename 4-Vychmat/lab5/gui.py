from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, QComboBox)
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_manager import load_from_file, generate_data
from interpolation_methods import lagrange, newton_divided, newton_finite, compute_finite_diff_table


def setup_ui(window):
    window.setWindowTitle('Интерполяция')
    layout = QVBoxLayout(window)

    # Таблица входных данных
    table = QTableWidget(0, 2)
    table.setHorizontalHeaderLabels(['x', 'y'])
    table.setEditTriggers(QTableWidget.AllEditTriggers)  # Разрешить ввод
    layout.addWidget(table)

    btn_add_row = QPushButton('Добавить строку')
    btn_update = QPushButton('Обновить данные')
    btn_load = QPushButton('Загрузить из файла')
    row_ctrl = QHBoxLayout()
    row_ctrl.addWidget(btn_add_row)
    row_ctrl.addWidget(btn_update)
    row_ctrl.addWidget(btn_load)
    layout.addLayout(row_ctrl)

    # Генерация данных
    func_combo = QComboBox()
    func_combo.addItems(['sin(x)', 'cos(x)', 'exp(x)', 'x^2'])
    edit_start = QLineEdit('0')
    edit_end = QLineEdit('10')
    edit_num = QLineEdit('5')
    btn_generate = QPushButton('Сгенерировать')
    gen_layout = QHBoxLayout()
    gen_layout.addWidget(QLabel('Функция:'));
    gen_layout.addWidget(func_combo)
    gen_layout.addWidget(QLabel('Интервал от:'));
    gen_layout.addWidget(edit_start)
    gen_layout.addWidget(QLabel('до:'));
    gen_layout.addWidget(edit_end)
    gen_layout.addWidget(QLabel('Точек:'));
    gen_layout.addWidget(edit_num)
    gen_layout.addWidget(btn_generate)
    layout.addLayout(gen_layout)

    # Таблица конечных разностей
    diff_table = QTableWidget()
    layout.addWidget(QLabel('Таблица конечных разностей:'))
    layout.addWidget(diff_table)

    # Вычисление значения
    edit_x0 = QLineEdit()
    btn_eval = QPushButton('Вычислить')
    eval_layout = QHBoxLayout()
    eval_layout.addWidget(QLabel('x0:'));
    eval_layout.addWidget(edit_x0);
    eval_layout.addWidget(btn_eval)
    layout.addLayout(eval_layout)

    # Результаты
    result_label = QLabel('Результаты:')
    layout.addWidget(result_label)

    # График
    figure = Figure()
    canvas = FigureCanvas(figure)
    layout.addWidget(canvas)

    data = {'x': [], 'y': []}

    def update_data_table():
        table.setRowCount(len(data['x']))
        for i, (xi, yi) in enumerate(zip(data['x'], data['y'])):
            table.setItem(i, 0, QTableWidgetItem(f"{xi:.4f}"))
            table.setItem(i, 1, QTableWidgetItem(f"{yi:.4f}"))

    def load_table_data():
        xs, ys = [], []
        for i in range(table.rowCount()):
            try:
                xi = float(table.item(i, 0).text().replace(',', '.'))
                yi = float(table.item(i, 1).text().replace(',', '.'))
            except Exception:
                QMessageBox.warning(window, 'Ошибка', f'Некорректные данные в строке {i + 1}')
                return
            xs.append(xi);
            ys.append(yi)
        data['x'], data['y'] = xs, ys
        update_diff()

    def update_diff():
        if not data['y']: return
        diff = compute_finite_diff_table(data['y'])
        diff_table.clear()
        diff_table.setRowCount(len(diff))
        diff_table.setColumnCount(len(diff[0]))
        for i, row in enumerate(diff):
            for j, val in enumerate(row):
                diff_table.setItem(i, j, QTableWidgetItem(f"{val:.4f}"))

    def on_add_row():
        table.insertRow(table.rowCount())

    def on_load():
        path, _ = QFileDialog.getOpenFileName(window, 'Открыть файл', '', 'Text Files (*.txt)')
        if path:
            try:
                xs, ys = load_from_file(path)
                data['x'], data['y'] = xs, ys
                update_data_table()
                update_diff()
            except Exception as e:
                QMessageBox.warning(window, 'Ошибка', str(e))

    def on_generate():
        try:
            a = float(edit_start.text().replace(',', '.'))
            b = float(edit_end.text().replace(',', '.'))
            n = int(edit_num.text())
            xs, ys = generate_data(func_combo.currentText(), a, b, n)
            data['x'], data['y'] = xs, ys
            update_data_table()
            update_diff()
        except Exception as e:
            QMessageBox.warning(window, 'Ошибка', str(e))

    def on_eval():
        try:
            x0 = float(edit_x0.text().replace(',', '.'))
        except Exception:
            QMessageBox.warning(window, 'Ошибка', 'Введите корректное x0')
            return
        xs, ys = data['x'], data['y']
        if len(xs) < 2:
            QMessageBox.warning(window, 'Ошибка', 'Недостаточно данных')
            return
        try:
            r1 = lagrange(xs, ys, x0)
            r2 = newton_divided(xs, ys, x0)
            r3 = newton_finite(xs, ys, x0)
            result_label.setText(
                f'Результаты: Лагранж={r1:.4f}, Ньютон_раздел={r2:.4f}, Ньютон_конечн={r3:.4f}'
            )
            draw_plot()
        except Exception as e:
            QMessageBox.warning(window, 'Ошибка', str(e))

    def draw_plot():
        figure.clear()
        ax = figure.add_subplot(111)
        xs_arr = np.array(data['x'])
        ys_arr = np.array(data['y'])
        xx = np.linspace(min(xs_arr), max(xs_arr), 300)
        yy = [lagrange(data['x'], data['y'], xi) for xi in xx]
        ax.plot(xx, yy, label='Интерполяционный полином')
        ax.scatter(xs_arr, ys_arr, label='Узлы')
        ax.legend()
        canvas.draw()

    btn_add_row.clicked.connect(on_add_row)
    btn_update.clicked.connect(load_table_data)
    btn_load.clicked.connect(on_load)
    btn_generate.clicked.connect(on_generate)
    btn_eval.clicked.connect(on_eval)