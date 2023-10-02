from typing import Any, Dict, List

from PyHotKey import Key, keyboard_manager as hotkey_manager
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QKeySequence


class CGlobalHotkey(QObject):
    pressed = Signal()

    def __init__(self, parent: QObject | None = None):
        super(CGlobalHotkey, self).__init__(parent)
        self.hotkey: int | None = None

    def register_hotkey(self, ksequence: QKeySequence):
        if self.hotkey is not None:
            self.unregister_hotkey()
        kstr = self.keyseq2pynput(ksequence)
        self.hotkey = hotkey_manager.register_hotkey(
            self.keyseq2KeyList(kstr),
            1,
            lambda: self.pressed.emit(),
        )

    def unregister_hotkey(self):
        hotkey_manager.unregister_hotkey_by_id(self.hotkey)
        self.hotkey = None

    @staticmethod
    def unregister_all_hotkey():
        hotkey_manager.unregister_all_hotkeys()

    def keyseq2KeyList(self, kseq: str) -> List[Key | str]:
        keystrs = [k.lower() for k in kseq.split("+")]
        keylist = [KeyModifiersMap.get(k, k) for k in keystrs]
        return keylist

    def keyseq2pynput(self, kseq: QKeySequence) -> str:
        hotkey = kseq.toString().lower()
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
