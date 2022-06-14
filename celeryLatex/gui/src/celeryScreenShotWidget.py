# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'celeryScreenImageWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QPoint, QRect, Qt)
from PySide6.QtGui import (QBrush, QColor, QCursor, QKeyEvent,
    QMouseEvent, QPaintEvent, QPen, QPainter, QPixmap)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget, QMainWindow, QVBoxLayout, QGraphicsOpacityEffect)

from PIL import ImageGrab

from .logger import get_logger

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class CeleryScreenShotWidget(QMainWindow):
    logger = get_logger("screen_image")
    img_ltop = QPoint()
    img_rbot = QPoint()
    is_snipping = False
    def __init__(self, parent=None) -> None:
        super(CeleryScreenShotWidget, self).__init__()
        self.parent = parent
        self.setupUi()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        self.opacity_effect = QGraphicsOpacityEffect()

        # setting opacity level
        self.opacity_effect.setOpacity(0.3)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"screenShotWidget")
        self.resize(400, 300)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_image = QLabel(self)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setCursor(QCursor(Qt.CrossCursor))
        self.label_image.setText(u"")
        self.label_image.setGeometry(0, 0, 400, 300)
        self.gridLayout.addWidget(self.label_image, 0, 0, 1, 1)
    # setupUi

    def set_image(self):
        screens = QApplication.screens()
        self.logger.debug(screens)
        for screen in screens:
            rect = screen.geometry()
            scale = screen.devicePixelRatio()
            top_left, bot_right = rect.topLeft(), rect.bottomRight()
            x0, y0 = top_left.x(), top_left.y()
            x1, y1 = bot_right.x(), bot_right.y()
            self.move(x0, y0)
            self.resize(x1-x0, y1-y0)
            self.logger.debug(f"screen: [{screen}], geo: [{x0}, {y0}, {x1}, {y1}]")
            bbox = (int(x0*scale), int(y0*scale), int(x1*scale), int(y1*scale))
            img = ImageGrab.grab(bbox=bbox, all_screens=True)
            im = QPixmap(img.toqimage())
            self.label_image.setGeometry(x0, y0, x1-x0, y1-y0)
            self.label_image.setScaledContents(True)
            self.label_image.setPixmap(im)

    def reset_rect(self):
        self.img_ltop.setX(0)
        self.img_ltop.setY(0)
        self.img_rbot.setX(0)
        self.img_rbot.setY(0)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            QApplication.restoreOverrideCursor()
            self.reset_rect()
            self.close()
            self.parent.on_sc_returned()
        event.accept()

    def take_screenshot(self):
        self.is_snipping = True
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.set_image()
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        self.raise_()

    def mousePressEvent(self, event: QMouseEvent):
        self.img_ltop = event.pos()
        self.img_rbot = event.pos()
        # self.logger.debug(f"press: {self.img_ltop}")
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        self.img_rbot = event.pos()
        # self.logger.debug(f"move, {self.img_rbot}")
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # self.logger.debug(f"button: {event.button()}")
        if event.button() != Qt.MouseButton.LeftButton:
            self.reset_rect()
            self.close()
            self.parent.on_sc_returned()
            return
        self.logger.debug(f"release, {self.img_ltop}, {self.img_rbot}")
        self.is_snipping = False
        QApplication.restoreOverrideCursor()

        start = self.img_ltop
        end = self.img_rbot

        x0 = start.x()
        y0 = start.y()
        x1 = end.x()
        y1 = end.y()
        screen = QApplication.screenAt(end)
        scale = screen.devicePixelRatio()
        bbox = (int(x0*scale), int(y0*scale), int(x1*scale), int(y1*scale))

        self.repaint()
        QApplication.processEvents()
        img = ImageGrab.grab(bbox=bbox, all_screens=True)
        QApplication.processEvents()

        self.reset_rect()
        self.close()
        self.parent.on_sc_returned(img)

    def paintEvent(self, event: QPaintEvent):
        # self.logger.debug(f"paint, {self.is_snipping}",)
        if self.is_snipping:
            brushColor = "#b1d5c8"
            lw = 1
            opacity = 0.8
        else:
            brushColor = "#FFFFFF"
            lw = 1
            opacity = 1
        self.opacity_effect.setOpacity(opacity)
        self.label_image.setGraphicsEffect(self.opacity_effect)
        qp = QPainter(self)
        qp.setPen(QPen(QColor("#000000"), lw))
        qp.setBrush(QColor(brushColor))
        qp.drawRect(QRect(self.img_ltop, self.img_rbot))
