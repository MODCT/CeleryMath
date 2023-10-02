# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'celeryScreenImageWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from typing import List

import numpy as np
from PIL import ImageGrab, Image, ImageOps
from pynput.mouse import Controller as MouseController
from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import (
    QColor,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from ..utils.logger import CeleryLogger

QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)


class CScreenShotWidget(QMainWindow):
    logger = CeleryLogger("screen_image")
    draw_ltop = QPoint()
    draw_rbot = QPoint()
    img_ltop = (0, 0)
    img_rbot = (0, 0)
    is_snipping = False

    def __init__(self, parent=None) -> None:
        super(CScreenShotWidget, self).__init__()
        self.parent = parent  # type: ignore

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.mouse = MouseController()

    def set_image(self):
        screens = QApplication.screens()
        xs: List[int] = []
        ys: List[int] = []
        for screen in screens:
            rect = screen.geometry()
            scale = screen.devicePixelRatio()
            top_left, bot_right = rect.topLeft(), rect.bottomRight()
            x0, y0 = top_left.x(), top_left.y()
            x1, y1 = bot_right.x(), bot_right.y()
            xs.extend([x0, x1])
            ys.extend([y0, y1])
            self.logger.debug(
                f"screen: [{screen}], scale: [{scale}] geo: [{x0}, {y0}, {x1}, {y1}]"
            )
        tl_x, tl_y = min(xs), min(ys)
        rb_x, rb_y = max(xs), max(ys)
        new_size = (rb_x - tl_x, rb_y - tl_y)
        self.move(tl_x, tl_y)
        # self.logger.debug(f"moved to {tl_x}, {tl_y}")
        self.resize(new_size[0], new_size[1])
        # self.logger.debug(
        #     f"resized to {new_size}",
        # )

    def reset_rect(self):
        self.draw_ltop = QPoint()
        self.draw_rbot = QPoint()
        self.img_ltop = (0, 0)
        self.img_rbot = (0, 0)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.is_snipping = False
            QApplication.restoreOverrideCursor()
            self.reset_rect()
            self.close()
            self.parent.on_sc_returned()
        event.accept()

    def take_screenshot(self):
        self.is_snipping = True
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        self.set_image()
        self.show()
        self.setWindowState(
            self.windowState() & ~Qt.WindowState.WindowMinimized
            | Qt.WindowState.WindowActive
        )
        self.activateWindow()
        self.raise_()

    def post_process_img(self, img: Image.Image):
        # convert dark ground image to white
        img = img.convert("L")
        colors = sorted(
            img.getcolors(img.height * img.width),
            key=lambda c: c[0],
            reverse=True,
        )
        bg = colors[0][1]
        if bg < 200:
            img_array = np.array(img, dtype=np.float32)
            img_array += bg
            img_array[img_array <= bg * 2 + np.random.randint(5, 50)] = 0
            img = Image.fromarray(img_array.astype(np.uint8), mode="L")
            img = ImageOps.invert(img)
        return img

    def mousePressEvent(self, event: QMouseEvent):
        self.draw_ltop = event.pos()
        self.draw_rbot = event.pos()
        self.img_ltop = self.mouse.position
        self.img_rbot = self.img_ltop
        # self.logger.debug(f"press: {self.img_ltop}")
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.draw_rbot = event.pos()
        self.img_rbot = self.mouse.position
        # self.logger.debug(f"move, {self.img_rbot}")
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # self.logger.debug(f"button: {event.button()}")
        self.is_snipping = False
        if event.button() != Qt.MouseButton.LeftButton:
            self.reset_rect()
            self.close()
            self.parent.on_sc_returned()
            return
        self.logger.debug(f"release, {self.img_ltop}, {self.img_rbot}")

        bbox = (*self.img_ltop, *self.img_rbot)
        # self.logger.debug(f"bbox: {bbox}")

        self.repaint()
        QApplication.processEvents()
        img = ImageGrab.grab(bbox=bbox, all_screens=True)  # type: ignore
        QApplication.processEvents()

        self.reset_rect()
        self.close()
        self.parent.on_sc_returned(self.post_process_img(img))

    def paintEvent(self, event: QPaintEvent):
        if self.is_snipping:
            brushColor = "#b1d5c8"
            lw = 1
            opacity = 0.2
        else:
            brushColor = "#FFFFFF"
            lw = 1
            opacity = 0.0
        self.setWindowOpacity(opacity)
        qp = QPainter(self)
        qp.setPen(QPen(QColor("#000000"), lw))
        qp.setBrush(QColor(brushColor))
        qp.drawRect(QRect(self.draw_ltop, self.draw_rbot))
