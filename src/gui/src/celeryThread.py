from PySide6.QtCore import QThread, Signal
from PIL import Image

from ...models.model import LatexModelONNX


class CeleryInferThread(QThread):
    # from https://github.com/lukas-blecher/LaTeX-OCR/blob/main/pix2tex/gui.py, thanks
    finished = Signal(dict)

    def __init__(self, img: Image.Image, model: LatexModelONNX):
        super().__init__()
        self.img: Image.Image = img
        self.model: LatexModelONNX = model

    def run(self):
        try:
            prediction = self.model(self.img)
            self.finished.emit({"status": True, "data": prediction})
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.finished.emit({"status": False, "data": ""})