# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'celeryLatexUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)
# from . import celeryLatex_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(508, 356)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.webTexView = QWebEngineView(self.centralwidget)
        self.webTexView.setObjectName(u"webTexView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webTexView.sizePolicy().hasHeightForWidth())
        self.webTexView.setSizePolicy(sizePolicy)
        self.webTexView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout.addWidget(self.webTexView)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ledit_tex1 = QLineEdit(self.centralwidget)
        self.ledit_tex1.setObjectName(u"ledit_tex1")

        self.horizontalLayout_2.addWidget(self.ledit_tex1)

        self.btn_copy1 = QPushButton(self.centralwidget)
        self.btn_copy1.setObjectName(u"btn_copy1")

        self.horizontalLayout_2.addWidget(self.btn_copy1)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ledit_tex2 = QLineEdit(self.centralwidget)
        self.ledit_tex2.setObjectName(u"ledit_tex2")

        self.horizontalLayout_3.addWidget(self.ledit_tex2)

        self.btn_copy2 = QPushButton(self.centralwidget)
        self.btn_copy2.setObjectName(u"btn_copy2")

        self.horizontalLayout_3.addWidget(self.btn_copy2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_tempe = QLabel(self.centralwidget)
        self.label_tempe.setObjectName(u"label_tempe")

        self.horizontalLayout.addWidget(self.label_tempe)

        self.spinbox_tempe = QDoubleSpinBox(self.centralwidget)
        self.spinbox_tempe.setObjectName(u"spinbox_tempe")
        self.spinbox_tempe.setMaximum(10.000000000000000)
        self.spinbox_tempe.setSingleStep(0.010000000000000)
        self.spinbox_tempe.setValue(0.200000000000000)

        self.horizontalLayout.addWidget(self.spinbox_tempe)

        self.label_hotkey = QLabel(self.centralwidget)
        self.label_hotkey.setObjectName(u"label_hotkey")

        self.horizontalLayout.addWidget(self.label_hotkey)

        self.btn_rec_hotkey = QPushButton(self.centralwidget)
        self.btn_rec_hotkey.setObjectName(u"btn_rec_hotkey")
        self.btn_rec_hotkey.setEnabled(True)

        self.horizontalLayout.addWidget(self.btn_rec_hotkey)

        self.btn_hotkey_reset = QPushButton(self.centralwidget)
        self.btn_hotkey_reset.setObjectName(u"btn_hotkey_reset")

        self.horizontalLayout.addWidget(self.btn_hotkey_reset)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btn_snip = QPushButton(self.centralwidget)
        self.btn_snip.setObjectName(u"btn_snip")

        self.verticalLayout.addWidget(self.btn_snip)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CeleryLatex", None))
        self.btn_copy1.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.btn_copy2.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.label_tempe.setText(QCoreApplication.translate("MainWindow", u"Temperature:", None))
        self.spinbox_tempe.setPrefix("")
        self.label_hotkey.setText(QCoreApplication.translate("MainWindow", u"HotKey:", None))
        self.btn_rec_hotkey.setText(QCoreApplication.translate("MainWindow", u"Ctrl+Alt+S", None))
        self.btn_hotkey_reset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.btn_snip.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
#if QT_CONFIG(shortcut)
        self.btn_snip.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Alt+S", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

