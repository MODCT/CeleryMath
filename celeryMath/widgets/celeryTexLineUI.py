# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'celeryTexLine.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from CeleryMath.widgets.celeryLineEdit import CeleryLineEdit
import celeryMath_rc


class Ui_CeleryTexLine(object):
    def setupUi(self, CeleryTexLine):
        if not CeleryTexLine.objectName():
            CeleryTexLine.setObjectName("CeleryTexLine")
        CeleryTexLine.resize(691, 51)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CeleryTexLine.sizePolicy().hasHeightForWidth())
        CeleryTexLine.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies(["MiSans Demibold"])
        font.setPointSize(10)
        CeleryTexLine.setFont(font)
        CeleryTexLine.setStyleSheet(
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
            "QLineEdit::focus\n"
            "{\n"
            "	border: 1px solid #55aaff;\n"
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
            "}"
        )
        self.gridLayout = QGridLayout(CeleryTexLine)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ledit_tex = CeleryLineEdit(CeleryTexLine)
        self.ledit_tex.setObjectName("ledit_tex")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ledit_tex.sizePolicy().hasHeightForWidth())
        self.ledit_tex.setSizePolicy(sizePolicy1)
        self.ledit_tex.setMinimumSize(QSize(30, 30))
        font1 = QFont()
        font1.setFamilies(["MiSans"])
        font1.setPointSize(10)
        self.ledit_tex.setFont(font1)
        self.ledit_tex.setClearButtonEnabled(False)

        self.horizontalLayout_2.addWidget(self.ledit_tex)

        self.btn_info = QPushButton(CeleryTexLine)
        self.btn_info.setObjectName("btn_info")
        self.btn_info.setStyleSheet("QPushButton{\n" "	width: auto;\n" "}")

        self.horizontalLayout_2.addWidget(self.btn_info)

        self.btn_copy = QPushButton(CeleryTexLine)
        self.btn_copy.setObjectName("btn_copy")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_copy.sizePolicy().hasHeightForWidth())
        self.btn_copy.setSizePolicy(sizePolicy2)
        self.btn_copy.setMinimumSize(QSize(0, 0))
        self.btn_copy.setFont(font)
        self.btn_copy.setStyleSheet("QPushButton{\n" "	width: 25px;\n" "}")
        icon = QIcon()
        icon.addFile(
            ":/icon/icons/content_copy_FILL0_wght400_GRAD0_opsz48.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.btn_copy.setIcon(icon)
        self.btn_copy.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.btn_copy)

        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(CeleryTexLine)

        QMetaObject.connectSlotsByName(CeleryTexLine)

    # setupUi

    def retranslateUi(self, CeleryTexLine):
        CeleryTexLine.setWindowTitle(
            QCoreApplication.translate("CeleryTexLine", "Form", None)
        )
        self.btn_info.setText(QCoreApplication.translate("CeleryTexLine", "0%", None))
        # if QT_CONFIG(statustip)
        self.btn_copy.setStatusTip(
            QCoreApplication.translate("CeleryTexLine", "Copy", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(whatsthis)
        self.btn_copy.setWhatsThis(
            QCoreApplication.translate("CeleryTexLine", "Copy", None)
        )
        # endif // QT_CONFIG(whatsthis)
        self.btn_copy.setText("")

    # retranslateUi
