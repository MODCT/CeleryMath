from typing import Any, Dict, List, Union
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QGridLayout,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QPixmap, QClipboard, QKeyEvent, QCloseEvent

from PIL import Image
from PyHotKey import manager as hotkManager
import os
import re

from .celeryMathUI import Ui_MainWindow
from .widgets.dialogSettings import DialogSettings
from .widgets.celeryScreenShotWidget import CeleryScreenShotWidget
from .widgets.celeryTexLinesWidget import CeleryTexLineWidget, CeleryTexDispWidget
from .utils.logger import CeleryLogger
from .celeryThread import CeleryInferThread
from .lib.models.model import LatexModelONNX, get_model
from .lib.utils.config import Config


class CeleryMath(QMainWindow, Ui_MainWindow):
    tempe: float = 0.2
    logger = CeleryLogger("celeryMath")
    conf: Config = Config("conf/conf.json")
    model: LatexModelONNX = None
    img: Image.Image = None
    crt_tex: str = ""

    def __init__(self, parent=None):
        super(CeleryMath, self).__init__(parent)
        self.setupUi(self)
        self.clipboard = QClipboard(self)
        self.snip_widget = CeleryScreenShotWidget(self)
        self.settings_dialog = DialogSettings(conf=self.conf)

        self.init_settings()
        self.init_signals()
        self.init_ui()

    def init_settings(self):
        self.webTexView.load(QUrl("qrc:/html/index.html"))

        self.tempe: float = self.conf.temperature
        self.update_model()
        self.btn_snip.setText(f"Screenshot({self.conf.snip_hotkey})")

    def init_signals(self):
        # self.ledit_tex1.textEdited.connect(self.ledit_val_changed)
        # self.ledit_tex2.textEdited.connect(self.ledit_val_changed)
        # self.btn_copy1.clicked.connect(self.btn_copy1_clicked)
        # self.btn_copy2.clicked.connect(self.btn_copy2_clicked)
        self.spinbox_tempe.valueChanged.connect(self.tempe_changed)
        self.btn_settings.clicked.connect(self.btn_settings_clicked)
        self.btn_snip.clicked.connect(self.btn_screenshot_clicked)
        self.settings_dialog.hotkey_sc.pressed.connect(self.btn_screenshot_clicked)
        self.settings_dialog.conf_updated.connect(self.on_conf_updated)
        self.splitter_tex_img.splitterMoved.connect(self.on_splitter_tex_img_moved)

    def init_ui(self):
        self.splitter_tex_img.setStretchFactor(0, 1)
        self.splitter_tex_img.setStretchFactor(1, 2)
        self.splitter_tex_group.setStretchFactor(0, 3)
        self.splitter_tex_group.setStretchFactor(1, 2)
        self.update_tex_lines([""])

    def update_tex_lines(self, tex: List[str]):
        self.scroll_layout = QVBoxLayout()
        self.scroll_tex_lines_contents = QWidget()
        for t in tex:
            texline = CeleryTexLineWidget(text=t, clipboard=self.clipboard)
            texline.ledit_tex.textEdited.connect(self.ledit_val_changed)
            texline.ledit_tex.focussed.connect(self.render_tex)
            self.scroll_layout.addWidget(texline)
        self.scroll_layout.setContentsMargins(3, 6, 3, 6)
        self.scroll_layout.setSpacing(8)
        self.scroll_tex_lines_contents.setLayout(self.scroll_layout)
        self.scroll_tex_lines.setWidget(self.scroll_tex_lines_contents)

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

    def on_splitter_tex_img_moved(self, pos: int, idx: int):
        self.set_original_img(self.img)

    def on_conf_updated(self, conf: Config):
        self.conf = conf
        self.logger.debug(f"conf updated with: {self.conf.json}")
        self.update_model()
        self.btn_snip.setText(f"Screenshot({self.conf.snip_hotkey})")

    def ledit_val_changed(self, v: str):
        v = v.replace("$", "").replace("\[", "").replace("\]", "")
        self.render_tex(v)

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

    def render_tex(self, s: str):
        if len(s) == 0:
            return
        js = rf"""updateMath("$${re.escape(s)}$$");"""
        self.webTexView.page().runJavaScript(js)

    def on_infer_finished(self, tex: Union[List[List[str]], str, Dict[str, Any]]):
        if isinstance(tex, dict):
            if tex["status"]:
                tex: Union[List[List[str]], str] = tex["data"]
        if isinstance(tex, list):
            tex = tex[0]
        msg = "\n".join(tex)
        self.logger.debug(f"prediction: \n{msg}")
        self.crt_tex = tex[0]
        self.render_tex(self.crt_tex)

        self.update_tex_lines(tex)
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
        self.render_tex("\mathrm{Loading...}")
        # res = self.predict(img)
        # self.on_infer_finished(res)
        self.img = img
        self.set_original_img(img)

    def set_original_img(self, img: Union[Image.Image, QPixmap] = None):
        if img is None:
            return
        if isinstance(img, Image.Image):
            img = img.toqpixmap()
        self.imview_original.setPixmap(img)

    def keyPressEvent(self, event: QKeyEvent):
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent):
        event.accept()

    def closeEvent(self, event: QCloseEvent):
        try:
            # keyboard.remove_all_hotkeys()
            hotkManager.unregister_all()
            self.settings_dialog.hotkey_sc.unregister_hotkey()
        except Exception as e:
            self.logger.error(f"unregister snip hotkey error: {e}")
        event.accept()
