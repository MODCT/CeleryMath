# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'celeryMathUI.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QVBoxLayout, QWidget)

from src.widgets.celeryImageView import CeleryImageView
import celeryMath_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(764, 556)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icon/icons/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QMainWindow\n"
"{\n"
"	background-color: rgb(239, 246, 252);\n"
"}\n"
"\n"
"QPushButton,\n"
"QDoubleSpinBox,\n"
"QLineEdit\n"
"{\n"
"	border: 1px solid #000000;\n"
"	border-radius: 6px;\n"
"	padding: 3px;\n"
"	height: 25px;\n"
"	font-size: 10pt;\n"
"	color: #000000;\n"
"}\n"
"\n"
"QGroupBox\n"
"{\n"
"	border: 1px solid #000000;\n"
"	border-radius: 6px;\n"
"	padding: 3px;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"	background-color: #d3e0f3;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton::hover\n"
"{\n"
"	background-color: #d6e3f7;\n"
"}\n"
"\n"
"QPushButton::pressed\n"
"{\n"
"	background-color: #a2aec0;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.splitter_tex_img = QSplitter(self.groupBox)
        self.splitter_tex_img.setObjectName(u"splitter_tex_img")
        self.splitter_tex_img.setOrientation(Qt.Vertical)
        self.splitter_tex_img.setOpaqueResize(True)
        self.splitter_tex_img.setHandleWidth(3)
        self.splitter_tex_img.setChildrenCollapsible(True)
        self.imview_original = CeleryImageView(self.splitter_tex_img)
        self.imview_original.setObjectName(u"imview_original")
        font1 = QFont()
        font1.setFamilies([u"MiSans Demibold"])
        self.imview_original.setFont(font1)
        self.imview_original.setStyleSheet(u"border: none;")
        self.splitter_tex_img.addWidget(self.imview_original)
        self.webTexView = QWebEngineView(self.splitter_tex_img)
        self.webTexView.setObjectName(u"webTexView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webTexView.sizePolicy().hasHeightForWidth())
        self.webTexView.setSizePolicy(sizePolicy)
        self.webTexView.setMinimumSize(QSize(0, 80))
        self.webTexView.setFont(font1)
        self.webTexView.setStyleSheet(u"")
        self.webTexView.setUrl(QUrl(u"about:blank"))
        self.splitter_tex_img.addWidget(self.webTexView)

        self.gridLayout.addWidget(self.splitter_tex_img, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.ledit_tex1 = QLineEdit(self.centralwidget)
        self.ledit_tex1.setObjectName(u"ledit_tex1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ledit_tex1.sizePolicy().hasHeightForWidth())
        self.ledit_tex1.setSizePolicy(sizePolicy1)
        self.ledit_tex1.setMinimumSize(QSize(30, 30))
        font2 = QFont()
        font2.setFamilies([u"MiSans"])
        font2.setPointSize(10)
        self.ledit_tex1.setFont(font2)
        self.ledit_tex1.setClearButtonEnabled(False)

        self.horizontalLayout_2.addWidget(self.ledit_tex1)

        self.btn_copy1 = QPushButton(self.centralwidget)
        self.btn_copy1.setObjectName(u"btn_copy1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_copy1.sizePolicy().hasHeightForWidth())
        self.btn_copy1.setSizePolicy(sizePolicy2)
        self.btn_copy1.setMinimumSize(QSize(0, 0))
        font3 = QFont()
        font3.setFamilies([u"MiSans Demibold"])
        font3.setPointSize(10)
        self.btn_copy1.setFont(font3)
        self.btn_copy1.setStyleSheet(u"QPushButton{\n"
"	width: 25px;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/content_copy_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_copy1.setIcon(icon1)
        self.btn_copy1.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.btn_copy1)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.ledit_tex2 = QLineEdit(self.centralwidget)
        self.ledit_tex2.setObjectName(u"ledit_tex2")
        sizePolicy1.setHeightForWidth(self.ledit_tex2.sizePolicy().hasHeightForWidth())
        self.ledit_tex2.setSizePolicy(sizePolicy1)
        self.ledit_tex2.setMinimumSize(QSize(0, 30))
        self.ledit_tex2.setFont(font2)

        self.horizontalLayout_3.addWidget(self.ledit_tex2)

        self.btn_copy2 = QPushButton(self.centralwidget)
        self.btn_copy2.setObjectName(u"btn_copy2")
        sizePolicy2.setHeightForWidth(self.btn_copy2.sizePolicy().hasHeightForWidth())
        self.btn_copy2.setSizePolicy(sizePolicy2)
        self.btn_copy2.setMinimumSize(QSize(0, 30))
        self.btn_copy2.setFont(font3)
        self.btn_copy2.setStyleSheet(u"QPushButton{\n"
"	width: 25px;\n"
"}")
        self.btn_copy2.setIcon(icon1)
        self.btn_copy2.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.btn_copy2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.setFont(font3)
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/thermometer_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon2.addFile(u":/icon/icons/thermometer_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon2.addFile(u":/icon/icons/thermometer_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.pushButton)

        self.spinbox_tempe = QDoubleSpinBox(self.centralwidget)
        self.spinbox_tempe.setObjectName(u"spinbox_tempe")
        self.spinbox_tempe.setFont(font3)
        self.spinbox_tempe.setStyleSheet(u"QDoubleSpinBox\n"
"{\n"
"	border: none;\n"
"}")
        self.spinbox_tempe.setMaximum(10.000000000000000)
        self.spinbox_tempe.setSingleStep(0.010000000000000)
        self.spinbox_tempe.setValue(0.200000000000000)

        self.horizontalLayout.addWidget(self.spinbox_tempe)

        self.btn_settings = QPushButton(self.centralwidget)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setFont(font3)
        self.btn_settings.setStyleSheet(u"QPushButton{\n"
"	width: 25px;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icons/settings_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_settings.setIcon(icon3)
        self.btn_settings.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btn_settings)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btn_snip = QPushButton(self.centralwidget)
        self.btn_snip.setObjectName(u"btn_snip")
        self.btn_snip.setFont(font3)
        self.btn_snip.setStyleSheet(u"QPushButton{\n"
"	\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icon/icons/screenshot_monitor_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_snip.setIcon(icon4)
        self.btn_snip.setIconSize(QSize(25, 25))

        self.verticalLayout.addWidget(self.btn_snip)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CeleryMath", None))
        self.groupBox.setTitle("")
#if QT_CONFIG(statustip)
        self.btn_copy1.setStatusTip(QCoreApplication.translate("MainWindow", u"Copy", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_copy1.setWhatsThis(QCoreApplication.translate("MainWindow", u"Copy", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_copy1.setText("")
#if QT_CONFIG(statustip)
        self.btn_copy2.setStatusTip(QCoreApplication.translate("MainWindow", u"Copy", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_copy2.setWhatsThis(QCoreApplication.translate("MainWindow", u"Copy", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_copy2.setText("")
#if QT_CONFIG(whatsthis)
        self.pushButton.setWhatsThis(QCoreApplication.translate("MainWindow", u"Temperature", None))
#endif // QT_CONFIG(whatsthis)
        self.pushButton.setText("")
#if QT_CONFIG(statustip)
        self.spinbox_tempe.setStatusTip(QCoreApplication.translate("MainWindow", u"Temprature", None))
#endif // QT_CONFIG(statustip)
        self.spinbox_tempe.setPrefix("")
#if QT_CONFIG(statustip)
        self.btn_settings.setStatusTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_settings.setWhatsThis(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_settings.setText("")
#if QT_CONFIG(statustip)
        self.btn_snip.setStatusTip(QCoreApplication.translate("MainWindow", u"Screenshot", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_snip.setWhatsThis(QCoreApplication.translate("MainWindow", u"Screenshot", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_snip.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
    # retranslateUi

