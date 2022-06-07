import sys

from PySide6.QtWidgets import QApplication

from .application import CeleryLatex


def main():
    app = QApplication(sys.argv)
    mainWindow = CeleryLatex()
    # mainWindow.flashSplash()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()