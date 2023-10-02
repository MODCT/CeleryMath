# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CeleryMathUI.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QMainWindow,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QSplitter, QStatusBar,
    QVBoxLayout, QWidget)

from CeleryMath.widgets.CImageView import CImageView
import CeleryMath_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(660, 493)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icon/icons/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QMainWindow,\n"
"QScrollArea #scroll_tex_lines_contents\n"
"{\n"
"	background-color: rgb(239, 246, 252);\n"
"}\n"
"\n"
"QPushButton,\n"
"QSpinBox,\n"
"QDoubleSpinBox,\n"
"QLineEdit,\n"
"QScrollArea\n"
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
"\n"
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
"}\n"
"\n"
"QRadioButton\n"
"{\n"
"	height: 25px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    width:16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"QRadioButton::indicator::unchecked\n"
"{\n"
"   image: url(:/icon/icons/radio_button_unchecked_FILL0_wght400_GRAD0_opsz48.svg);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:hove"
                        "r\n"
"{\n"
"image: url(:/icon/icons/radio_button_unchecked_hover_FILL0_wght400_GRAD0_opsz48.svg);\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked:pressed\n"
"{\n"
"\n"
"}\n"
"\n"
"QRadioButton::indicator::checked \n"
"{\n"
"    image: url(:/icon/icons/radio_button_checked_FILL0_wght400_GRAD0_opsz48.svg);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover \n"
"{\n"
"image: url(:/icon/icons/radio_button_checked_hover_FILL0_wght400_GRAD0_opsz48.svg);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:pressed \n"
"{\n"
"\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.splitter_tex_group = QSplitter(self.centralwidget)
        self.splitter_tex_group.setObjectName(u"splitter_tex_group")
        self.splitter_tex_group.setOrientation(Qt.Vertical)
        self.groupBox = QGroupBox(self.splitter_tex_group)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"QGroupBox #imview_original\n"
"{\n"
"	border: none;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.splitter_tex_img = QSplitter(self.groupBox)
        self.splitter_tex_img.setObjectName(u"splitter_tex_img")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_tex_img.sizePolicy().hasHeightForWidth())
        self.splitter_tex_img.setSizePolicy(sizePolicy)
        self.splitter_tex_img.setOrientation(Qt.Vertical)
        self.imview_original = CImageView(self.splitter_tex_img)
        self.imview_original.setObjectName(u"imview_original")
        font1 = QFont()
        font1.setFamilies([u"MiSans Demibold"])
        self.imview_original.setFont(font1)
        self.splitter_tex_img.addWidget(self.imview_original)
        self.tex_view = QSvgWidget(self.splitter_tex_img)
        self.tex_view.setObjectName(u"tex_view")
        sizePolicy.setHeightForWidth(self.tex_view.sizePolicy().hasHeightForWidth())
        self.tex_view.setSizePolicy(sizePolicy)
        self.splitter_tex_img.addWidget(self.tex_view)

        self.verticalLayout.addWidget(self.splitter_tex_img)

        self.splitter_tex_group.addWidget(self.groupBox)
        self.scroll_tex_lines = QScrollArea(self.splitter_tex_group)
        self.scroll_tex_lines.setObjectName(u"scroll_tex_lines")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scroll_tex_lines.sizePolicy().hasHeightForWidth())
        self.scroll_tex_lines.setSizePolicy(sizePolicy1)
        self.scroll_tex_lines.setFrameShape(QFrame.StyledPanel)
        self.scroll_tex_lines.setWidgetResizable(True)
        self.scroll_tex_lines_contents = QWidget()
        self.scroll_tex_lines_contents.setObjectName(u"scroll_tex_lines_contents")
        self.scroll_tex_lines_contents.setGeometry(QRect(0, 0, 634, 69))
        self.gridLayout_2 = QGridLayout(self.scroll_tex_lines_contents)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scroll_tex_lines.setWidget(self.scroll_tex_lines_contents)
        self.splitter_tex_group.addWidget(self.scroll_tex_lines)

        self.gridLayout_3.addWidget(self.splitter_tex_group, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.rdbtn_greedy = QRadioButton(self.centralwidget)
        self.rdbtn_greedy.setObjectName(u"rdbtn_greedy")
        font2 = QFont()
        font2.setFamilies([u"MiSans Demibold"])
        font2.setPointSize(10)
        self.rdbtn_greedy.setFont(font2)
        self.rdbtn_greedy.setStyleSheet(u"")
        self.rdbtn_greedy.setChecked(True)

        self.horizontalLayout.addWidget(self.rdbtn_greedy)

        self.cmbox_sampling = QComboBox(self.centralwidget)
        self.cmbox_sampling.addItem("")
        self.cmbox_sampling.addItem("")
        self.cmbox_sampling.setObjectName(u"cmbox_sampling")
        font3 = QFont()
        font3.setFamilies([u"MiSans Demibold"])
        font3.setPointSize(9)
        self.cmbox_sampling.setFont(font3)
        self.cmbox_sampling.setStyleSheet(u"QComboBox\n"
"{\n"
"	border: none;\n"
"	border-radius: 6px;\n"
"	height: 30px;\n"
"	width: 55px;\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"	background-color: #d3e0f3;\n"
"	padding: 0;\n"
"	margin: 0;\n"
"	border: none;\n"
"}\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"	image: url(:/icon/icons/arrow_drop_down_FILL0_wght400_GRAD0_opsz48.svg);\n"
"	width: 90%;\n"
"}\n"
"\n"
"QComboBox::drop-down:pressed\n"
"{\n"
"	background-color: #a2aec0;\n"
"}\n"
"\n"
"QComboBox::item\n"
"{\n"
"	border: none;\n"
"}")

        self.horizontalLayout.addWidget(self.cmbox_sampling)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: rgb(255, 255, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icon/icons/thermometer_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/icon/icons/thermometer_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Disabled, QIcon.Off)
        icon1.addFile(u":/icon/icons/thermometer_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Disabled, QIcon.On)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.pushButton)

        self.spinbox_tempe = QDoubleSpinBox(self.centralwidget)
        self.spinbox_tempe.setObjectName(u"spinbox_tempe")
        self.spinbox_tempe.setFont(font2)
        self.spinbox_tempe.setStyleSheet(u"QDoubleSpinBox\n"
"{\n"
"	border: none;\n"
"	border-top-right-radius: 0px;\n"
"	border-bottom-right-radius: 0px;\n"
"	width: 20px;\n"
"}\n"
"\n"
"QDoubleSpinBox::up-button\n"
"{\n"
"	image: url(:/icon/icons/arrow_drop_up_FILL0_wght400_GRAD0_opsz48.svg);\n"
"	background-color: #d3e0f3;\n"
"	border-radius: 0 6px 0px 0;\n"
"	margin-bottom: 1px;\n"
"}\n"
"\n"
"QDoubleSpinBox::up-button::pressed\n"
"{\n"
"	\n"
"	background-color: #a2aec0;\n"
"}\n"
"\n"
"QDoubleSpinBox::down-button\n"
"{\n"
"	image: url(:/icon/icons/arrow_drop_down_FILL0_wght400_GRAD0_opsz48.svg);\n"
"	background-color: #d3e0f3;\n"
"	border-radius: 0 0px 6px 0;\n"
"	margin-top: 1px;\n"
"}\n"
"\n"
"QDoubleSpinBox::down-button::pressed\n"
"{\n"
"	background-color: #a2aec0;\n"
"}")
        self.spinbox_tempe.setMaximum(10.000000000000000)
        self.spinbox_tempe.setSingleStep(0.010000000000000)
        self.spinbox_tempe.setValue(0.200000000000000)

        self.horizontalLayout.addWidget(self.spinbox_tempe)

        self.btn_settings = QPushButton(self.centralwidget)
        self.btn_settings.setObjectName(u"btn_settings")
        self.btn_settings.setFont(font2)
        self.btn_settings.setStyleSheet(u"QPushButton{\n"
"	width: 25px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icon/icons/settings_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_settings.setIcon(icon2)
        self.btn_settings.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.btn_settings)

        self.spbox_beam_width = QSpinBox(self.centralwidget)
        self.spbox_beam_width.setObjectName(u"spbox_beam_width")
        self.spbox_beam_width.setFont(font2)
        self.spbox_beam_width.setStyleSheet(u"QSpinBox\n"
"{\n"
"	border: none;\n"
"	border-top-right-radius: 0px;\n"
"	border-bottom-right-radius: 0px;\n"
"	width: 20px;\n"
"}\n"
"\n"
"QSpinBox::up-button\n"
"{\n"
"	image: url(:/icon/icons/arrow_drop_up_FILL0_wght400_GRAD0_opsz48.svg);\n"
"	background-color: #d3e0f3;\n"
"	border-radius: 0 6px 0px 0;\n"
"	margin-bottom: 1px;\n"
"}\n"
"\n"
"QSpinBox::up-button::pressed\n"
"{\n"
"	\n"
"	background-color: #a2aec0;\n"
"}\n"
"\n"
"QSpinBox::down-button\n"
"{\n"
"	image: url(:/icon/icons/arrow_drop_down_FILL0_wght400_GRAD0_opsz48.svg);\n"
"	background-color: #d3e0f3;\n"
"	border-radius: 0 0px 6px 0;\n"
"	margin-top: 1px;\n"
"}\n"
"\n"
"QSpinBox::down-button::pressed\n"
"{\n"
"	background-color: #a2aec0;\n"
"}")
        self.spbox_beam_width.setMinimum(1)
        self.spbox_beam_width.setMaximum(20)
        self.spbox_beam_width.setValue(3)

        self.horizontalLayout.addWidget(self.spbox_beam_width)

        self.rdbtn_beam = QRadioButton(self.centralwidget)
        self.rdbtn_beam.setObjectName(u"rdbtn_beam")
        self.rdbtn_beam.setFont(font2)

        self.horizontalLayout.addWidget(self.rdbtn_beam)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.btn_snip = QPushButton(self.centralwidget)
        self.btn_snip.setObjectName(u"btn_snip")
        self.btn_snip.setFont(font2)
        self.btn_snip.setStyleSheet(u"QPushButton{\n"
"	\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icon/icons/screenshot_monitor_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_snip.setIcon(icon3)
        self.btn_snip.setIconSize(QSize(25, 25))

        self.gridLayout_3.addWidget(self.btn_snip, 2, 0, 1, 1)

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
        self.rdbtn_greedy.setStatusTip(QCoreApplication.translate("MainWindow", u"Greedy Search", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.rdbtn_greedy.setWhatsThis(QCoreApplication.translate("MainWindow", u"Greedy Search", None))
#endif // QT_CONFIG(whatsthis)
        self.rdbtn_greedy.setText(QCoreApplication.translate("MainWindow", u"Greedy", None))
        self.cmbox_sampling.setItemText(0, QCoreApplication.translate("MainWindow", u"Nucleus", None))
        self.cmbox_sampling.setItemText(1, QCoreApplication.translate("MainWindow", u"Random", None))

#if QT_CONFIG(statustip)
        self.cmbox_sampling.setStatusTip(QCoreApplication.translate("MainWindow", u"Sampling Method", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.cmbox_sampling.setWhatsThis(QCoreApplication.translate("MainWindow", u"Sampling Method", None))
#endif // QT_CONFIG(whatsthis)
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
        self.spbox_beam_width.setStatusTip(QCoreApplication.translate("MainWindow", u"Beam Width", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.spbox_beam_width.setWhatsThis(QCoreApplication.translate("MainWindow", u"Beam Width", None))
#endif // QT_CONFIG(whatsthis)
        self.spbox_beam_width.setSuffix("")
        self.spbox_beam_width.setPrefix(QCoreApplication.translate("MainWindow", u"BW: ", None))
#if QT_CONFIG(statustip)
        self.rdbtn_beam.setStatusTip(QCoreApplication.translate("MainWindow", u"Beam Search", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.rdbtn_beam.setWhatsThis(QCoreApplication.translate("MainWindow", u"Beam Search", None))
#endif // QT_CONFIG(whatsthis)
        self.rdbtn_beam.setText(QCoreApplication.translate("MainWindow", u"Beam", None))
#if QT_CONFIG(statustip)
        self.btn_snip.setStatusTip(QCoreApplication.translate("MainWindow", u"Screenshot", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_snip.setWhatsThis(QCoreApplication.translate("MainWindow", u"Screenshot", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_snip.setText(QCoreApplication.translate("MainWindow", u"Screenshot", None))
    # retranslateUi

