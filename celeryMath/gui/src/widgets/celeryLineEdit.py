"""
Description: QLineEdit
Author: Rainyl
Date: 2022-08-15 23:59:41
LastEditTime: 2022-08-16 00:07:45
"""
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit


class CeleryLineEdit(QLineEdit):
    focussed = Signal(str)

    def __init__(self, parent=None):
        super(CeleryLineEdit, self).__init__(parent=parent)

    def focusInEvent(self, e) -> None:
        self.focussed.emit(self.text())
        return super().focusInEvent(e)
