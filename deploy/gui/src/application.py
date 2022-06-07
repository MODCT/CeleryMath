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
        self.init_signals()

    def init_signals(self):
        self.btn_copy1.clicked.connect(self.btn_copy1_clicked)
        self.btn_copy2.clicked.connect(self.btn_copy2_clicked)
        self.spinbox_tempe.valueChanged.connect(self.tempe_changed)
        self.btn_rec_hotkey.clicked.connect(self.hotkey_changed)
        self.btn_hotkey_reset.clicked.connect(self.reset_hotkey)
        self.btn_snip.clicked.connect(self.btn_screenshot_clicked)
    
    def btn_copy1_clicked(self):
        ...
    
    def btn_copy2_clicked(self):
        ...

    def copy_to_clipboard(self):
        ...

    def tempe_changed(self):
        ...
    
    def reset_hotkey(self):
        ...

    def hotkey_changed(self):
        ...

    def btn_screenshot_clicked(self):
        ...

    
