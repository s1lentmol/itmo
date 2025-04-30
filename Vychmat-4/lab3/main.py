import sys
from PyQt5.QtWidgets import QApplication
from gui import IntegrationWindow


def main():
    app = QApplication(sys.argv)
    window = IntegrationWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
