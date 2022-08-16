from PySide6.QtCore import QThread, Signal
from PIL import Image

from .lib.models.model import LatexModelONNX


class CeleryInferThread(QThread):
    # from https://github.com/lukas-blecher/LaTeX-OCR/blob/main/pix2tex/gui.py, thanks
    finished = Signal(dict)

    def __init__(
        self,
        img: Image.Image,
        model: LatexModelONNX,
        temp: float = 0.2,
        method: str = "greedy",
    ):
        super().__init__()
        self.img: Image.Image = img
        self.model: LatexModelONNX = model
        self.temp = temp
        self.method = method

    def run(self):
        try:
            prediction = self.model(
                self.img,
                temperature=self.temp,
                method=self.method,
            )
            self.finished.emit({"status": True, "data": prediction})
        except Exception as e:
            import traceback

            traceback.print_exc()
            self.finished.emit({"status": False, "data": ""})
