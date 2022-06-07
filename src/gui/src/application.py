from PySide6.QtCore import QSettings, Slot, QUrl, QThread, Signal, QObject, QTimer
from PySide6.QtCore import QRegularExpression as QRegExp
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QSplashScreen, QButtonGroup
from PySide6.QtGui import QPixmap, QClipboard, QKeySequence
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
# from PySide6.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PIL import Image

from .celeryLatexUI import Ui_MainWindow
from .logger import get_logger


class CeleryLatex(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CeleryLatex, self).__init__(parent)
        self.clipboard = QClipboard(self)
        self.logger = get_logger("celeryLatex")
        self.tempe: float = 0.2
        self.default_snip_shortcut = QKeySequence("Ctrl+Alt+S")

        self.setupUi(self)
        self.init_signals()

    def init_signals(self):
        self.btn_copy1.clicked.connect(self.btn_copy1_clicked)
        self.btn_copy2.clicked.connect(self.btn_copy2_clicked)
        self.spinbox_tempe.valueChanged.connect(self.tempe_changed)
        self.btn_rec_hotkey.clicked.connect(self.hotkey_changed)
        self.btn_hotkey_reset.clicked.connect(self.reset_hotkey)
        self.btn_snip.clicked.connect(self.btn_screenshot_clicked)
        self.btn_snip.setShortcut(self.default_snip_shortcut)
    
    def btn_copy1_clicked(self):
        txt = self.ledit_tex1.text()
        if txt:
            self.clipboard.setText(txt, QClipboard.Clipboard)
            self.logger.debug(f"copy to clipboard: {txt}")
        return
    
    def btn_copy2_clicked(self):
        txt = self.ledit_tex2.text()
        if txt:
            self.clipboard.setText(txt, QClipboard.Clipboard)
            self.logger.debug(f"copy to clipboard: {txt}")
        return

    def tempe_changed(self, d: float):
        self.tempe = d

    def reset_hotkey(self):
        ...

    def hotkey_changed(self):
        ...

    def btn_screenshot_clicked(self):
        self.logger.debug(f"take screenshot clicked")

    def predict(self, img: Image):
        ...
