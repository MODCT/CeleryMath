import sys

from PySide6.QtWidgets import QApplication

from src.application import CeleryMath
from src.lib.utils.utils import seed_everything


def main():
    app = QApplication(sys.argv)
    mainWindow = CeleryMath()
    # mainWindow.flashSplash()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    seed_everything(241)
    main()
