from typing import Any, Dict, List
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QKeySequence
import keyboard


class CeleryGlobalHotkey(QObject):
    pressed = Signal()
    def __init__(self, parent: QObject=None):
        super(CeleryGlobalHotkey, self).__init__(parent)
        self.hotkey = None
    
    def register_hotkey(self, ksequence: QKeySequence):
        kstr = self.keyseq2pynput(ksequence)
        if self.hotkey is not None:
            self.unregister_hotkey()
        self.hotkey = keyboard.add_hotkey(kstr, self.pressed.emit, args=(), suppress=True, trigger_on_release=True)

    def unregister_hotkey(self):
        keyboard.remove_hotkey(self.hotkey)
        self.hotkey = None

    def keyseq2pynput(self, ksequence: QKeySequence) -> str:
        hotkey = ksequence.toString().lower()
        return hotkey


KeyModifiersMap = {
    Qt.Key_Control: "Ctrl",
    Qt.Key_Shift: "Shift",
    Qt.Key_Alt: "Alt",
    Qt.Key_Meta: "Meta"
}
KeyCodeMap = {
    Qt.Key_A: "A",
    Qt.Key_B: "B",
    Qt.Key_C: "C",
    Qt.Key_D: "D",
    Qt.Key_E: "E",
    Qt.Key_F: "F",
    Qt.Key_G: "G",
    Qt.Key_H: "H",
    Qt.Key_I: "I",
    Qt.Key_J: "J",
    Qt.Key_K: "K",
    Qt.Key_L: "L",
    Qt.Key_M: "M",
    Qt.Key_N: "N",
    Qt.Key_O: "O",
    Qt.Key_P: "P",
    Qt.Key_Q: "Q",
    Qt.Key_R: "R",
    Qt.Key_S: "S",
    Qt.Key_T: "T",
    Qt.Key_U: "U",
    Qt.Key_V: "V",
    Qt.Key_W: "W",
    Qt.Key_X: "X",
    Qt.Key_Y: "Y",
    Qt.Key_Z: "Z",
    Qt.Key_1: "1",
    Qt.Key_2: "2",
    Qt.Key_3: "3",
    Qt.Key_4: "4",
    Qt.Key_5: "5",
    Qt.Key_6: "6",
    Qt.Key_7: "7",
    Qt.Key_8: "8",
    Qt.Key_9: "9",
    Qt.Key_0: "0",
    Qt.Key_F1: "F1",
    Qt.Key_F2: "F2",
    Qt.Key_F3: "F3",
    Qt.Key_F4: "F4",
    Qt.Key_F5: "F5",
    Qt.Key_F6: "F6",
    Qt.Key_F7: "F7",
    Qt.Key_F8: "F8",
    Qt.Key_F9: "F9",
    Qt.Key_F10: "F10",
    Qt.Key_F11: "F11",
    Qt.Key_F12: "F12",
}