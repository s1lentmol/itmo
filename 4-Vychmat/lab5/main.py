import sys
from PyQt5.QtWidgets import QApplication, QWidget
from gui import setup_ui


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    setup_ui(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
