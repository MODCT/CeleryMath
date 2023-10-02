from PySide6.QtCore import Signal
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog

from ..lib.utils.config import Config
from ..utils import CGlobalHotkey
from ..utils.logger import CeleryLogger
from .CDialogSettingsUI import Ui_CDialogSettings


class CDialogSettings(QDialog, Ui_CDialogSettings):
    _default_sc_hotkey_ = QKeySequence("Ctrl+Alt+S")
    logger = CeleryLogger("dialog_settings")
    conf_updated = Signal(Config)
    snip_hotkey: QKeySequence | None = None
    last_open_path: str = "."

    def __init__(self, conf: Config, parent=None) -> None:
        super(CDialogSettings, self).__init__(parent)
        self.setupUi(self)
        self.hotkey_sc = CGlobalHotkey(self)

        self.conf = conf
        self.update_settings()

        self.btn_tokenizer_path.clicked.connect(self.btn_tokenizer_path_clicked)
        self.btn_encoder_path.clicked.connect(self.btn_encoer_path_clicked)
        self.btn_decoder_path.clicked.connect(self.btn_decoder_path_clicked)
        self.btn_hotkey_reset.clicked.connect(self.btn_hotk_reset_clicked)
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.clicked.connect(self.save_settings)
        self.kseq_screenshot.editingFinished.connect(self.update_hotkey)
        self.cbox_device.currentIndexChanged.connect(self.update_device)

    def update_settings(self):
        self.ledit_tokenizer_path.setText(self.conf.tokenizer_path)
        self.ledit_encoder_path.setText(self.conf.encoder_path)
        self.ledit_decoder_path.setText(self.conf.decoder_path)
        device = 1 if self.conf.device == "cuda" else 0
        self.cbox_device.setCurrentIndex(device)

        sh = self.conf.snip_hotkey
        self.snip_hotkey = QKeySequence(sh) if sh else self._default_sc_hotkey_
        self.kseq_screenshot.setKeySequence(self.snip_hotkey)
        self.update_hotkey()

    def update_device(self, idx: int):
        if idx == 0:
            self.conf.device = "cpu"
        elif idx == 1:
            self.conf.device = "cuda"
        else:
            return

    def btn_hotk_reset_clicked(self):
        self.kseq_screenshot.setKeySequence(self._default_sc_hotkey_)
        self.update_hotkey()

    def update_hotkey(self):
        self.snip_hotkey = self.kseq_screenshot.keySequence()
        self.hotkey_sc.register_hotkey(self.snip_hotkey)
        self.conf.snip_hotkey = self.snip_hotkey.toString()

    def btn_tokenizer_path_clicked(self):
        file_url: str
        file_url, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            self.last_open_path,
            "Json File(*.json)",
        )
        if not file_url:
            return
        self.conf.tokenizer_path = file_url
        self.ledit_tokenizer_path.setText(self.conf.tokenizer_path)

    def btn_encoer_path_clicked(self):
        file_url: str
        file_url, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            self.last_open_path,
            "ONNX Model(*.ONNX)",
        )
        if not file_url:
            return
        self.conf.encoder_path = file_url
        self.ledit_encoder_path.setText(self.conf.encoder_path)

    def btn_decoder_path_clicked(self):
        file_url: str
        file_url, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            self.last_open_path,
            "ONNX Model(*.ONNX)",
        )
        if not file_url:
            return
        self.conf.decoder_path = file_url
        self.ledit_decoder_path.setText(self.conf.decoder_path)

    def save_settings(self, button=None):
        if button == self.buttonBox.button(QDialogButtonBox.StandardButton.Apply):
            self.conf_updated.emit(self.conf)
            self.conf.save()

    @property
    def encoder(self):
        return self.conf.encoder_path

    @property
    def decoder(self):
        return self.conf.decoder_path

    @property
    def tokenizer(self):
        return self.conf.tokenizer_path
