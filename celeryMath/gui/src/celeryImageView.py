"""
Description: Image View Widget
Author: Rainyl
Date: 2022-08-14 11:32:21
LastEditTime: 2022-08-14 15:56:43
"""
from PySide6.QtCore import Qt, QRectF, QSizeF, QPointF
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene


class CeleryImageView(QGraphicsView):
    def __init__(self, parent=None):
        super(CeleryImageView, self).__init__(parent=parent)
        self.setCursor(Qt.OpenHandCursor)
        self.setBackground(Qt.white)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setCacheMode(self.CacheBackground)
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self.im_item = QGraphicsPixmapItem()
        self.im_item.setFlags(
            QGraphicsPixmapItem.ItemIsFocusable | QGraphicsPixmapItem.ItemIsMovable
        )
        self.im_scene = QGraphicsScene(self)
        self.setScene(self.im_scene)
        self.im_scene.addItem(self.im_item)

        self.pixmap = None
        self._ds = 0.1

    def setBackground(self, color: QColor):
        self.setBackgroundBrush(color)

    def setPixmap(self, pixmap: QPixmap):
        self.pixmap = pixmap
        self.im_item.setPixmap(self.pixmap)
        self.im_item.update()
        self.setSceneDims()
        self.fitInView(
            QRectF(self.im_item.pos(), QSizeF(self.pixmap.size())),
            Qt.KeepAspectRatio,
        )
        self.update()

    def setSceneDims(self):
        if self.pixmap is None:
            return
        rect = QRectF(QPointF(0, 0), QPointF(self.pixmap.width(), self.pixmap.height()))
        self.setSceneRect(rect)

    def fitInView(self, rect: QRectF, flags=Qt.IgnoreAspectRatio):
        if not self.scene() or rect.isNull():
            return
        unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewRect = self.viewport().rect()
        sceneRect = self.transform().mapRect(rect)
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        if flags == Qt.KeepAspectRatio:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        self.scale(x_ratio, y_ratio)
        self.centerOn(rect.center())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom(1 + self._ds)
        else:
            self.zoom(1 - self._ds)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.RightButton:
            if not self.pixmap is None:
                self.fitInView(
                    QRectF(self.im_item.pos(), QSizeF(self.pixmap.size())),
                    Qt.KeepAspectRatio,
                )
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
        return super().mouseReleaseEvent(event)

    def zoom(self, factor: float):
        _factor = (
            self.transform().scale(factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        )
        if _factor < 0.01 or _factor > 100:
            return
        self.scale(factor, factor)
