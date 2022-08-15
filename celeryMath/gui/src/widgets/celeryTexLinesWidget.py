'''
Description: 
Author: Rainyl
Date: 2022-08-15 21:26:29
LastEditTime: 2022-08-15 23:26:36
'''
from typing import Callable, List
from PySide6.QtGui import QClipboard
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from .celeryTexLineUI import Ui_CeleryTexLine

class CeleryTexLineWidget(QWidget, Ui_CeleryTexLine):
    def __init__(self, parent=None, text: str=None, clipboard: QClipboard=None) -> None:
        super(CeleryTexLineWidget, self).__init__(parent=parent)
        self.setupUi(self)

        self.clipboard = QClipboard(self) if clipboard is None else clipboard

        if not text is None:
            self.ledit_tex.setText(text)
        
        self.setup_signals()

    def setup_signals(self):
        self.btn_copy.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        txt = self.ledit_tex.text()
        if txt:
            self.clipboard.setText(txt, QClipboard.Clipboard)


class CeleryTexDispWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super(CeleryTexDispWidget, self).__init__(parent)

        self.scroll_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

    def add_lines(self, lines: List[str], slot: Callable=None):
        for line in lines:
            tex_line = CeleryTexLineWidget(text=line)
            if not slot is None:
                tex_line.ledit_tex.textEdited.connect(slot)
            self.scroll_layout.addWidget(tex_line)
