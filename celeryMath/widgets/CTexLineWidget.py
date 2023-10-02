"""
Description: Tex line edit widget
Author: Rainyl
Date: 2022-08-15 21:26:29
LastEditTime: 2023-08-07 11:16:02
"""
from typing import Callable, List

from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from .CTexLineWidgetUI import Ui_CTexLine


class CTexLineWidget(QWidget, Ui_CTexLine):
    def __init__(
        self,
        parent=None,
        text: str | None = None,
        prob: float | None = None,
        clipboard: QClipboard | None = None,
    ):
        super(CTexLineWidget, self).__init__(parent)
        self.setupUi(self)

        self.clipboard = QClipboard(self) if clipboard is None else clipboard

        if text is not None:
            self.ledit_tex.setText(text)
        if prob is not None:
            self.btn_info.setText(f"{prob*100:.0f}%")

        self.setup_signals()

    def setup_signals(self):
        self.btn_copy.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        txt = self.ledit_tex.text()
        if txt:
            self.clipboard.setText(txt, QClipboard.Mode.Clipboard)


class CeleryTexDispWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super(CeleryTexDispWidget, self).__init__(parent)

        self.scroll_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

    def add_lines(self, lines: List[str], slot: Callable | None = None):
        for line in lines:
            tex_line = CTexLineWidget(text=line)
            if slot is not None:
                tex_line.ledit_tex.textEdited.connect(slot)
            self.scroll_layout.addWidget(tex_line)
