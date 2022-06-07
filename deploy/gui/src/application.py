from .celeryLatexUI import Ui_MainWindow

from PySide6.QtCore import QSettings, Slot, QUrl, QThread, Signal, QObject, QTimer
from PySide6.QtCore import QRegularExpression as QRegExp
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QSplashScreen, QButtonGroup
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
# from PySide6.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class CeleryLatex(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CeleryLatex, self).__init__(parent)
        self.setupUi(self)
