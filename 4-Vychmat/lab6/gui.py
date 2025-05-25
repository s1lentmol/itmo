import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numerical_methods as nm



def create_ui():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('Численное решение ОДУ')
    central = QWidget()
    layout = QHBoxLayout()
    central.setLayout(layout)
    window.setCentralWidget(central)

    # Left panel: controls
    left = QWidget()
    left_layout = QVBoxLayout()
    left.setLayout(left_layout)
    layout.addWidget(left, 1)

    # Equation selector
    eq_selector = QComboBox()
    eqs = nm.get_equations()
    for desc, _, _ in eqs:
        eq_selector.addItem(desc)
    left_layout.addWidget(eq_selector)

    # Parameters table
    params_table = QTableWidget(5, 2)
    params_table.setHorizontalHeaderLabels(['Параметр', 'Значение'])
    names = ['x0', 'xn', 'y0', 'h', 'eps']
    for i, name in enumerate(names):
        params_table.setItem(i, 0, QTableWidgetItem(name))
        params_table.setItem(i, 1, QTableWidgetItem(''))
    left_layout.addWidget(params_table)

    # Update button
    update_btn = QPushButton('Обновить данные')
    left_layout.addWidget(update_btn)

    # Results table
    results_table = QTableWidget()
    left_layout.addWidget(results_table, 3)

    # Right panel: plot
    fig = Figure(figsize=(5, 4))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    layout.addWidget(canvas, 2)

    def on_update():
        try:
            # Read parameters
            p = {}
            for i, key in enumerate(names):
                item = params_table.item(i, 1)
                if item is None or not item.text():
                    raise ValueError(f'Пустое значение для параметра {names[i]}')
                val = item.text().replace(',', '.')
                p[key] = float(val)
            if p['h'] <= 0 or p['xn'] <= p['x0']:
                raise ValueError('Некорректные границы или шаг')

            # Unpack
            desc, f, exact = eqs[eq_selector.currentIndex()]
            x0, xn, y0, h, eps = p['x0'], p['xn'], p['y0'], p['h'], p['eps']

            # Numeric solutions
            xs_e, ys_e = nm.euler(f, x0, y0, xn, h)
            xs_ie, ys_ie = nm.improved_euler(f, x0, y0, xn, h)
            n = len(xs_e)

            # Exact solution
            try:
                xs_ex, ys_ex = nm.exact_solution(exact, x0, y0, xn, h)
            except Exception:
                xs_ex, ys_ex = xs_e, ys_e
                QMessageBox.warning(window, 'Предупреждение',
                                    'Не удалось вычислить точное решение. Используются численные значения.')
            if len(xs_ex) != n:
                xs_ex, ys_ex = xs_e, ys_e

            # Milne method
            try:
                xs_m, ys_m = nm.milne(f, x0, y0, xn, h)
            except Exception:
                xs_m, ys_m = xs_ex, ys_ex
                QMessageBox.warning(window, 'Предупреждение',
                                    'Ошибка метода Милна. Используется точное решение.')
            m = min(len(xs_m), n)
            xs_m, ys_m = xs_m[:m], ys_m[:m]

            # Compute errors
            err_e = nm.runge_error(None, ys_e, f, x0, y0, xn, h, method='euler')
            err_ie = nm.runge_error(None, ys_ie, f, x0, y0, xn, h, method='improved')
            err_e += [float('nan')] * (n - len(err_e))
            err_ie += [float('nan')] * (n - len(err_ie))
            err_m = [abs(ys_ex[i] - ys_m[i]) if i < m else float('nan') for i in range(n)]

            # Update table
            cols = ['x', 'Euler', 'ImpEuler', 'Milne', 'Exact', 'ErrEuler', 'ErrImp', 'ErrMilne']
            results_table.clear()
            results_table.setRowCount(n)
            results_table.setColumnCount(len(cols))
            results_table.setHorizontalHeaderLabels(cols)
            for i in range(n):
                vals = [
                    xs_e[i], ys_e[i], ys_ie[i],
                    ys_m[i] if i < m else float('nan'),
                    ys_ex[i], err_e[i], err_ie[i], err_m[i]
                ]
                for j, v in enumerate(vals):
                    text = f"{v:.3f}" if isinstance(v, float) else str(v)
                    results_table.setItem(i, j, QTableWidgetItem(text))

            # Plot
            ax.clear()
            ax.plot(xs_ex, ys_ex, label='Exact', color='black')
            ax.plot(xs_e, ys_e, '--', label='Euler')
            ax.plot(xs_ie, ys_ie, ':', label='ImpEuler')
            ax.plot(xs_m, ys_m, '-.', label='Milne')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()
            canvas.draw()

        except Exception as e:
            err_msg = f"Непредвиденная ошибка:\n{str(e)}"
            QMessageBox.critical(window, 'Ошибка', err_msg)
            return

    update_btn.clicked.connect(on_update)

    window.show()
    sys.exit(app.exec_())
