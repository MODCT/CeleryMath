import os
from typing import Any, Dict, List, Tuple, Union, Optional, ClassVar

from ziamath.zmath import Latex
from ziafont.config import config as zf_config
from PIL import Image
from PySide6.QtCore import Qt, Slot, QByteArray
from PySide6.QtGui import QClipboard, QCloseEvent, QKeyEvent, QPixmap, QImage
from PySide6.QtWidgets import (
    QButtonGroup,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from .CeleryMathUI import Ui_MainWindow
from .CeleryThread import CeleryInferThread
from .lib import LatexModelONNX, get_model, Config
from .utils import CRadioButtonType, CeleryLogger
from .widgets import CScreenShotWidget, CTexLineWidget, CDialogSettings

# ensure ziamath to construct svg with better compatibility
# TODO: It's not an elegant implementation, plan to modify the ziamath library
zf_config.svg2 = False


class CeleryMath(QMainWindow, Ui_MainWindow):
    welcome_txt = r"\star CeleryMath \quad by \quad Rainyl@MODCT \star"
    logger = CeleryLogger("CeleryMath")
    conf: Config = Config("conf/conf.json")

    def __init__(self, parent=None):
        super(CeleryMath, self).__init__(parent)
        self.setupUi(self)
        self.model: LatexModelONNX  # inference model
        self.img: Image.Image | None = None  # current image
        self.clipboard = QClipboard(self)
        self.snip_widget = CScreenShotWidget(self)
        self.settings_dialog = CDialogSettings(conf=self.conf)

        self.init_ui()
        self.init_signals()
        self.init_settings()

    def init_settings(self):
        self.render_tex(self.welcome_txt)

        self.update_model()
        self.spbox_beam_width.setValue(self.conf.beam_width)
        self.spinbox_tempe.setValue(self.conf.temperature)
        self.btn_snip.setText(f"Screenshot({self.conf.snip_hotkey})")
        if self.conf.search_method == "beam":
            self.rdbtn_beam.setChecked(True)

    def init_signals(self):
        self.cmbox_sampling.currentIndexChanged.connect(self.on_sampling_changed)
        self.spinbox_tempe.valueChanged.connect(self.tempe_changed)
        self.spbox_beam_width.valueChanged.connect(self.on_spbox_beam_width_changed)
        self.btn_settings.clicked.connect(self.btn_settings_clicked)
        self.btn_snip.clicked.connect(self.btn_screenshot_clicked)
        self.settings_dialog.hotkey_sc.pressed.connect(self.btn_screenshot_clicked)
        self.settings_dialog.conf_updated.connect(self.on_conf_updated)
        self.splitter_tex_img.splitterMoved.connect(self.on_splitter_tex_img_moved)

        self.btngrp_greedy_beam = QButtonGroup(self)
        self.btngrp_greedy_beam.addButton(
            self.rdbtn_greedy, CRadioButtonType.GREEDY.value
        )
        self.btngrp_greedy_beam.addButton(self.rdbtn_beam, CRadioButtonType.BEAM.value)
        self.btngrp_greedy_beam.buttonClicked.connect(self.on_greedy_beam_clicked)

    def init_ui(self):
        self.splitter_tex_img.setSizes([100, 100])
        self.splitter_tex_img.setStretchFactor(0, 1)
        self.splitter_tex_img.setStretchFactor(1, 2)
        self.splitter_tex_group.setStretchFactor(0, 3)
        self.splitter_tex_group.setStretchFactor(1, 2)
        self.update_tex_lines([("", 0)])

    ###############################################################################
    # Slots
    ###############################################################################
    def on_greedy_beam_clicked(self):
        if self.btngrp_greedy_beam.checkedId() == CRadioButtonType.GREEDY.value:
            self.conf.search_method = "greedy"
            self.conf.save()
        elif self.btngrp_greedy_beam.checkedId() == CRadioButtonType.BEAM.value:
            self.conf.search_method = "beam"
            self.conf.save()
        else:
            return

    def on_spbox_beam_width_changed(self, bw: int):
        self.conf.beam_width = bw
        self.conf.save()

    def on_sampling_changed(self, idx: int):
        if idx == 0:
            self.conf.sampling = "nucleus"
        elif idx == 1:
            self.conf.sampling = "random"
        else:
            self.logger.warning(f"sampling method {idx} not supported")
        self.conf.save()

    def on_splitter_tex_img_moved(self, pos: int, idx: int):
        self.set_original_img(self.img)

    def on_conf_updated(self, conf: Config):
        self.conf = conf
        self.logger.debug(f"conf updated with: {self.conf.json}")
        self.update_model()
        self.btn_snip.setText(f"Screenshot({self.conf.snip_hotkey})")

    @Slot(str)
    def ledit_val_changed(self, v: str):
        v = v.replace("$", "").replace(r"\[", "").replace(r"\]", "")
        self.render_tex(v)

    @Slot()
    def btn_settings_clicked(self):
        self.settings_dialog.show()

    @Slot(float)
    def tempe_changed(self, d: float):
        self.conf.temperature = d
        self.conf.save()

    @Slot()
    def btn_screenshot_clicked(self):
        if self.model is None:
            self.show_model_error_box()
            return
        self.logger.debug("taking screenshot")
        # self.hide()
        self.showMinimized()
        self.snip_widget.take_screenshot()

    ########################################################################
    # Functions
    ########################################################################
    def update_tex_lines(self, tex: List[Tuple[str, float]]):
        self.scroll_layout = QVBoxLayout()
        self.scroll_tex_lines_contents = QWidget()
        for t in tex:
            texline = CTexLineWidget(text=t[0], prob=t[1], clipboard=self.clipboard)
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

    def update_model_config(self):
        self.model.temperature = self.conf.temperature
        self.model.p_n = 0.95
        self.model.beam_width = self.conf.beam_width
        self.model.sampling = self.conf.sampling
        self.model.search_method = self.conf.search_method

    def predict(self, img: Image.Image):
        self.update_model_config()
        try:
            res = self.model(img)
        except Exception as e:
            self.logger.critical(f"prediction error: {e}")
            res = None
        return res

    def render_tex(self, s: str):
        if len(s) == 0:
            return
        try:
            svg = Latex(s).svg()
            self.tex_view.load(QByteArray.fromStdString(svg))
            self.tex_view.renderer().setAspectRatioMode(
                Qt.AspectRatioMode.KeepAspectRatio,
            )
        except Exception as e:
            self.tex_view.load(QByteArray.fromStdString(f"{e}"))
            self.logger.error(f"render failed: {e}")

    def on_sc_returned(self, img: Union[Image.Image, None] = None):
        if img is None:
            return
        self.showNormal()
        self.logger.debug("screen shot finished")
        self.update_model_config()
        self.infer_thread = CeleryInferThread(img, self.model)
        self.logger.info(f"inference starting with:\n{str(self.conf)}")
        self.infer_thread.finished.connect(self.on_infer_finished)
        self.infer_thread.finished.connect(self.infer_thread.deleteLater)
        self.infer_thread.start()
        self.render_tex(r"\quad \small Loading... \quad")

        # DEBUG
        # res = self.predict(img)
        # self.on_infer_finished(res)

        self.img = img
        self.set_original_img(img)

    def on_infer_finished(self, tex: Dict[str, List[List[Tuple[str, float]]] | str]):
        tex_res_0: List[List[Tuple[str, float]]] = []  # (B, BW, (str, float))
        self.logger.debug(tex)
        if isinstance(tex, dict):
            if tex["status"]:
                tex_res_0: List[List[Tuple[str, float]]] = tex["data"]  # type: ignore
            else:
                self.render_tex("Prediction Error!")
                self.logger.error(
                    f"error occured during inference, result is:{tex['data']}"
                )
                return
        else:
            self.render_tex("Prediction Error!")
            self.logger.error(f"prediction error, result is:{tex}")
            return
        tex_res = tex_res_0[0]
        self.logger.debug(f"prediction: \n{tex_res}")
        self.render_tex(tex_res[0][0])

        self.update_tex_lines(tex_res)
        self.setWindowState(
            self.windowState() & ~Qt.WindowState.WindowMinimized
            | Qt.WindowState.WindowActive
        )
        self.activateWindow()

    def set_original_img(self, img: Image.Image | QPixmap | None | QPixmap = None):
        if img is None:
            return
        img_qpixmap: QPixmap
        if isinstance(img, Image.Image):
            img_qpixmap = img.toqpixmap()
        else:
            img_qpixmap = img
        self.imview_original.setPixmap(img_qpixmap)

    #############################################################################
    # Life Cycle
    #############################################################################
    def keyPressEvent(self, event: QKeyEvent):
        event.accept()

    def keyReleaseEvent(self, event: QKeyEvent):
        event.accept()

    def closeEvent(self, event: QCloseEvent):
        try:
            self.settings_dialog.hotkey_sc.unregister_hotkey()
        except Exception as e:
            self.logger.error(f"unregister snip hotkey error: {e}")
        event.accept()
