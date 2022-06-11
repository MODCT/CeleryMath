from typing import Any, Dict, List, Union
from PySide6.QtCore import QSettings, Slot, QUrl, QThread, Signal, QObject, QTimer, Qt
from PySide6.QtCore import QRegularExpression as QRegExp
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)
from PySide6.QtGui import QPixmap, QClipboard, QKeySequence, QKeyEvent, QCloseEvent
from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator

# from PySide6.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PIL import Image
import keyboard
import os

from .celeryLatexUI import Ui_MainWindow
from .dialogSettings import DialogSettings
from .celeryScreenShotWidget import CeleryScreenShotWidget
from .logger import get_logger
from .celeryThread import CeleryInferThread
from .lib.models.model import LatexModelONNX, get_model
from .lib.utils.config import Config


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
    tempe: float = 0.2
    logger = get_logger("celeryLatex")
    conf: Config = Config("conf/conf.json")
    model: LatexModelONNX = None

    def __init__(self, parent=None):
        super(CeleryLatex, self).__init__(parent)
        self.setupUi(self)
        self.clipboard = QClipboard(self)
        self.snip_widget = CeleryScreenShotWidget(self)
        self.settings_dialog = DialogSettings(conf=self.conf)

        self.init_settings()
        self.init_signals()

    def init_settings(self):
        self.render_web("\star Welcome \star")
        # try:
        self.tempe: float = self.conf.temperature
        # except Exception as e:
        #     self.logger.error(f"init settings error: {e}")
        self.update_model()
        self.btn_snip.setText(f"Screenshot({self.conf.snip_hotkey})")

    def init_signals(self):
        self.ledit_tex1.textEdited.connect(self.ledit_val_changed)
        self.ledit_tex2.textEdited.connect(self.ledit_val_changed)
        self.btn_copy1.clicked.connect(self.btn_copy1_clicked)
        self.btn_copy2.clicked.connect(self.btn_copy2_clicked)
        self.spinbox_tempe.valueChanged.connect(self.tempe_changed)
        self.btn_settings.clicked.connect(self.btn_settings_clicked)
        self.btn_snip.clicked.connect(self.btn_screenshot_clicked)
        self.settings_dialog.hotkey_sc.pressed.connect(self.btn_screenshot_clicked)
        self.settings_dialog.conf_updated.connect(self.on_conf_updated)

    def show_model_error_box(self):
        QMessageBox(
            QMessageBox.Icon.Warning,
            "Warning",
            "Please set correct path first!",
            buttons=QMessageBox.StandardButton.Ok,
            parent=self,
        ).exec()

    def update_model(self):
        if (
            os.path.exists(self.conf.encoder_path)
            and os.path.exists(self.conf.decoder_path)
            and os.path.exists(self.conf.tokenizer_path)
        ):
            self.model = get_model(self.conf)
        else:
            self.show_model_error_box()

    def on_conf_updated(self, conf: Config):
        self.conf = conf
        self.logger.debug(f"conf updated with: {self.conf.json}")
        self.update_model()
        self.btn_snip.setText(f"Screenshot({self.conf.snip_hotkey})")

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

    def btn_settings_clicked(self):
        self.settings_dialog.show()

    def tempe_changed(self, d: float):
        self.tempe = d

    def btn_screenshot_clicked(self):
        if self.model is None:
            self.show_model_error_box()
            return
        self.logger.debug(f"taking screenshot")
        # self.hide()
        self.showMinimized()
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

    def on_sc_returned(self, img: Union[Image.Image, None] = None):
        if img is None:
            return
        self.showNormal()
        self.logger.debug(f"screen shot finished")
        self.infer_thread = CeleryInferThread(img, self.model)
        self.infer_thread.finished.connect(self.on_infer_finished)
        self.infer_thread.finished.connect(self.infer_thread.deleteLater)
        self.infer_thread.start()
        # res = self.predict(img)
        # self.on_infer_finished(res)
        self.webTexView.setHtml("<h1>Loading...</h1>")

    def keyPressEvent(self, event: QKeyEvent):
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent):
        event.accept()

    def closeEvent(self, event: QCloseEvent):
        try:
            keyboard.remove_all_hotkeys()
        except Exception as e:
            self.logger.error(f"unregister snip hotkey error: {e}")
        event.accept()