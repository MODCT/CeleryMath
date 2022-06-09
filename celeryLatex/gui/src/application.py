from typing import Any, Dict, List, Union
from PySide6.QtCore import QSettings, Slot, QUrl, QThread, Signal, QObject, QTimer, Qt
from PySide6.QtCore import QRegularExpression as QRegExp
from PySide6.QtWidgets import (QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, 
    QSplashScreen, QButtonGroup, QApplication)
from PySide6.QtGui import QPixmap, QClipboard, QKeySequence, QKeyEvent, QCloseEvent
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
# from PySide6.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PIL import Image
import keyboard

from celeryLatex.gui.celeryLatexUI import Ui_MainWindow
from .celeryScreenShotWidget import CeleryScreenShotWidget
from .logger import get_logger
from .celeryThread import CeleryInferThread
from .celeryGlobalHotkey import CeleryGlobalHotkey, KeyCodeMap, KeyModifiersMap
from ...models.model import get_model
from ...utils.config import Config
from ...utils.utils import post_process, seed_everything

class CeleryLatex(QMainWindow, Ui_MainWindow):
    html_head = """
        <html><head><meta charset="utf-8">
        <meta name="viewport" content="width=device-width">
        <script id="MathJax-script" src="qrc:js/js/MathJax.js"></script>
        <script src="qrc:js/js/mathJaxConfig.js"></script>
        </head>"""
    html_body = """
        <body>
        <div id="equation" style="font-size:1em;">$${equation}$$</div>
        </body>"""
    html_end = """</html>"""
    default_snip_shortcut = QKeySequence("Ctrl+Alt+S")
    is_rec_hotkey = False
    rec_hotkeys = []
    keycode = KeyCodeMap
    modifiers = KeyModifiersMap
    def __init__(self, parent=None):
        super(CeleryLatex, self).__init__(parent)
        self.clipboard = QClipboard(self)
        self.logger = get_logger("celeryLatex")
        self.conf = Config("src/conf/conf.json")
        self.model = get_model(self.conf)
        self.hotkey_sc = CeleryGlobalHotkey(self)

        self.setupUi(self)
        self.init_signals()
        self.init_settings()
        self.snip_widget = CeleryScreenShotWidget(self)

    def init_settings(self):
        self.render_web("\star Welcome \star")
        # try:
        self.tempe: float = self.conf.temperature
        self.snip_shortcut = QKeySequence(self.conf.snip_hotkey) if self.conf.snip_hotkey else self.default_snip_shortcut
        self.hotkey_sc.register_hotkey(self.snip_shortcut)
        # except Exception as e:
        #     self.logger.error(f"init settings error: {e}")

    def init_signals(self):
        self.ledit_tex1.textEdited.connect(self.ledit_val_changed)
        self.ledit_tex2.textEdited.connect(self.ledit_val_changed)
        self.btn_copy1.clicked.connect(self.btn_copy1_clicked)
        self.btn_copy2.clicked.connect(self.btn_copy2_clicked)
        self.spinbox_tempe.valueChanged.connect(self.tempe_changed)
        self.btn_rec_hotkey.clicked.connect(self.hotkey_changed)
        self.btn_hotkey_reset.clicked.connect(self.reset_hotkey)
        self.btn_snip.clicked.connect(self.btn_screenshot_clicked)
        self.btn_snip.setShortcut(self.default_snip_shortcut)
        self.hotkey_sc.pressed.connect(self.btn_screenshot_clicked)

    def ledit_val_changed(self, v: str):
        v = v.replace("$", "").replace("\[", "").replace("\]", "")
        self.render_web(v)

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
        try:
            self.snip_shortcut = self.default_snip_shortcut
            self.hotkey_sc.register_hotkey(self.snip_shortcut)
            self.logger.debug(f"reset hotkey to {self.snip_shortcut.toString()}")
        except Exception as e:
            self.logger.error(f"reset snip hotkey error: {e}")

    def hotkey_changed(self):
        self.is_rec_hotkey = True
        self.btn_rec_hotkey.setEnabled(False)
        self.btn_rec_hotkey.setText("Press...")
        self.rec_hotkeys.clear()

    def record_hotkey(self, key):
        if key in self.modifiers and key not in self.rec_hotkeys:
            self.rec_hotkeys.append(key)
        if key in self.keycode:
            self.rec_hotkeys.append(key)
            self.logger.debug(f"self.rec_hotkeys: {self.rec_hotkeys}")
            self.is_rec_hotkey = False
            new_k_list = [*[self.modifiers[k] for k in self.rec_hotkeys[:-1]], self.keycode[self.rec_hotkeys[-1]]]
            new_keyseq = "+".join(new_k_list)
            self.snip_shortcut = QKeySequence(new_keyseq)
            self.logger.debug(f"newkey: {new_keyseq}, snip_shortcut: {self.snip_shortcut.toString()}")
            self.hotkey_sc.register_hotkey(self.snip_shortcut)
            self.btn_rec_hotkey.setText(new_keyseq)
            self.btn_rec_hotkey.setEnabled(True)
        if len(self.rec_hotkeys) > 4:
            self.logger.error(f"hotkey error, {self.rec_hotkeys}")

    def btn_screenshot_clicked(self):
        self.logger.debug(f"taking screenshot")
        self.hide()
        self.snip_widget.take_screenshot()

    def predict(self, img: Image.Image):
        res = self.model(img, temperature=self.tempe)
        return res

    def render_web(self, s: str):
        self.logger.debug(f"prediction: {s}")
        s = self.html_head + self.html_body.format(equation=s) + self.html_end
        self.webTexView.setHtml(s)

    def on_infer_finished(self, s: Union[List[str], str, Dict[str, Any]]):
        if isinstance(s, dict):
            if s["status"]:
                tex: Union[List, str] = s["data"]
                if isinstance(tex, list):
                    tex = "\n".join(tex)
        if isinstance(s, list):
            tex = "\n".join(s)
        self.render_web(tex)

        self.ledit_tex1.setText(f"${tex}$")
        self.ledit_tex2.setText(f"\[{tex}\]")
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def on_sc_returned(self, img: Union[Image.Image, None]):
        self.show()
        if img is None:
            return
        self.logger.debug(f"screen shot finished")
        self.infer_thread = CeleryInferThread(img, self.model)
        self.infer_thread.finished.connect(self.on_infer_finished)
        self.infer_thread.finished.connect(self.infer_thread.deleteLater)
        self.infer_thread.start()
        # res = self.predict(img)
        # self.on_infer_finished(res)
        self.webTexView.setHtml("<h1>Loading...</h1>")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.snip_widget.close()
            self.show()
        if self.is_rec_hotkey:
            self.logger.debug(f"key: {event.key()}")
            self.record_hotkey(event.key())
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent):
        if self.is_rec_hotkey:
            self.rec_hotkeys.clear()
        event.accept()

    def closeEvent(self, event: QCloseEvent):
        try:
            keyboard.remove_all_hotkeys()
        except Exception as e:
            self.logger.error(f"unregister snip hotkey error: {e}")
        event.accept()
