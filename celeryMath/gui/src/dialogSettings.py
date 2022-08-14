from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QDialog, QFileDialog, QDialogButtonBox

from .celeryGlobalHotkey import CeleryGlobalHotkey
from .dialogSettingUI import Ui_diaglog_settings
from .logger import CeleryLogger
from .lib.utils.config import Config


class DialogSettings(QDialog, Ui_diaglog_settings):
    _default_sc_hotkey_ = QKeySequence("Ctrl+Alt+S")
    logger = CeleryLogger("dialog_settings")
    conf_updated = Signal(Config)
    snip_hotkey: QKeySequence = None

    def __init__(self, conf: Config, parent=None) -> None:
        super(DialogSettings, self).__init__(parent)
        self.setupUi(self)
        self.hotkey_sc = CeleryGlobalHotkey(self)

        self.conf = conf
        self.update_settings(
            t=self.conf.tokenizer_path,
            e=self.conf.encoder_path,
            d=self.conf.decoder_path,
            sh=self.conf.snip_hotkey,
        )

        self.btn_tokenizer_path.clicked.connect(self.btn_tokenizer_path_clicked)
        self.btn_encoder_path.clicked.connect(self.btn_encoer_path_clicked)
        self.btn_decoder_path.clicked.connect(self.btn_decoder_path_clicked)
        self.btn_hotkey_reset.clicked.connect(self.btn_hotk_reset_clicked)
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.clicked.connect(self.save_settings)
        self.kseq_screenshot.editingFinished.connect(self.update_hotkey)

    def update_settings(self, t="", e="", d="", sh=""):
        self.conf.tokenizer_path = t or self.conf.tokenizer_path
        self.conf.encoder_path = e or self.conf.encoder_path
        self.conf.decoder_path = d or self.conf.decoder_path
        self.ledit_tokenizer_path.setText(self.conf.tokenizer_path)
        self.ledit_encoder_path.setText(self.conf.encoder_path)
        self.ledit_decoder_path.setText(self.conf.decoder_path)

        self.snip_hotkey = QKeySequence(sh) if sh else self._default_sc_hotkey_
        self.kseq_screenshot.setKeySequence(self.snip_hotkey)
        self.update_hotkey()

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
            self, "Select File", ".", "Json File(*.json)"
        )
        if not file_url:
            return
        self.conf.tokenizer_path = file_url
        self.ledit_tokenizer_path.setText(self.conf.tokenizer_path)

    def btn_encoer_path_clicked(self):
        file_url: str
        file_url, _ = QFileDialog.getOpenFileName(
            self, "Select File", ".", "ONNX Model(*.ONNX)"
        )
        if not file_url:
            return
        self.conf.encoder_path = file_url
        self.ledit_encoder_path.setText(self.conf.encoder_path)

    def btn_decoder_path_clicked(self):
        file_url: str
        file_url, _ = QFileDialog.getOpenFileName(
            self, "Select File", ".", "ONNX Model(*.ONNX)"
        )
        if not file_url:
            return
        self.conf.decoder_path = file_url
        self.ledit_decoder_path.setText(self.conf.decoder_path)

    def save_settings(self, button=None):
        if button == self.buttonBox.button(QDialogButtonBox.Apply):
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
