from typing import Any, Dict, List
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QKeySequence
from PyHotKey import manager as hotkManager, Key

hotkManager.setLogPath("log/hotkey.log")
# hotkManager.logger = 1


class CeleryGlobalHotkey(QObject):
    pressed = Signal()

    def __init__(self, parent: QObject = None):
        super(CeleryGlobalHotkey, self).__init__(parent)
        self.hotkey = None

    def register_hotkey(self, ksequence: QKeySequence):
        kstr = self.keyseq2pynput(ksequence)
        if self.hotkey is not None:
            self.unregister_hotkey()
        self.hotkey = hotkManager.RegisterHotKey(
            lambda args: self.pressed.emit(),
            self.keyseq2keylist(kstr),
            count=1,
            args=(),
        )

    def unregister_hotkey(self):
        hotkManager.UnregisterHotKey(self.hotkey)
        self.hotkey = None

    def keyseq2pynput(self, ksequence: QKeySequence) -> str:
        hotkey = ksequence.toString().lower()
        return hotkey

    def keyseq2keylist(self, kseq: str):
        keyseq = [k.lower() for k in kseq.split("+")]
        if len(keyseq) <= 1:
            raise ValueError(f"key sequence error: {kseq}")
        modifiers = [KeyModifiersMap[s] for s in keyseq[:-1]]
        return [*modifiers, keyseq[-1]]


KeyModifiersMap = {
    "ctrl": Key.ctrl_l,
    "shift": Key.shift,
    "alt": Key.alt_l,
    "meta": Key.cmd,
    "cmd": Key.cmd,
}
