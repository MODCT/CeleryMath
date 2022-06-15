# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialogSettingsUI.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QKeySequenceEdit, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_diaglog_settings(object):
    def setupUi(self, diaglog_settings):
        if not diaglog_settings.objectName():
            diaglog_settings.setObjectName(u"diaglog_settings")
        diaglog_settings.resize(400, 357)
        self.gridLayout_3 = QGridLayout(diaglog_settings)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(3)
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(diaglog_settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_hotkey = QLabel(self.groupBox_2)
        self.label_hotkey.setObjectName(u"label_hotkey")

        self.horizontalLayout.addWidget(self.label_hotkey)

        self.kseq_screenshot = QKeySequenceEdit(self.groupBox_2)
        self.kseq_screenshot.setObjectName(u"kseq_screenshot")

        self.horizontalLayout.addWidget(self.kseq_screenshot)

        self.btn_hotkey_reset = QPushButton(self.groupBox_2)
        self.btn_hotkey_reset.setObjectName(u"btn_hotkey_reset")

        self.horizontalLayout.addWidget(self.btn_hotkey_reset)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(diaglog_settings)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(6)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ledit_tokenizer_path = QLineEdit(self.groupBox)
        self.ledit_tokenizer_path.setObjectName(u"ledit_tokenizer_path")

        self.horizontalLayout_2.addWidget(self.ledit_tokenizer_path)

        self.btn_tokenizer_path = QPushButton(self.groupBox)
        self.btn_tokenizer_path.setObjectName(u"btn_tokenizer_path")
        self.btn_tokenizer_path.setFlat(False)

        self.horizontalLayout_2.addWidget(self.btn_tokenizer_path)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ledit_encoder_path = QLineEdit(self.groupBox)
        self.ledit_encoder_path.setObjectName(u"ledit_encoder_path")

        self.horizontalLayout_3.addWidget(self.ledit_encoder_path)

        self.btn_encoder_path = QPushButton(self.groupBox)
        self.btn_encoder_path.setObjectName(u"btn_encoder_path")

        self.horizontalLayout_3.addWidget(self.btn_encoder_path)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ledit_decoder_path = QLineEdit(self.groupBox)
        self.ledit_decoder_path.setObjectName(u"ledit_decoder_path")

        self.horizontalLayout_4.addWidget(self.ledit_decoder_path)

        self.btn_decoder_path = QPushButton(self.groupBox)
        self.btn_decoder_path.setObjectName(u"btn_decoder_path")

        self.horizontalLayout_4.addWidget(self.btn_decoder_path)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self.groupBox)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.textBrowser = QTextBrowser(self.groupBox_3)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_4.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_3, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 3)

        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(diaglog_settings)
        self.buttonBox.accepted.connect(diaglog_settings.accept)
        self.buttonBox.rejected.connect(diaglog_settings.reject)

        QMetaObject.connectSlotsByName(diaglog_settings)
    # setupUi

    def retranslateUi(self, diaglog_settings):
        diaglog_settings.setWindowTitle(QCoreApplication.translate("diaglog_settings", u"Settings", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("diaglog_settings", u"General", None))
        self.label_hotkey.setText(QCoreApplication.translate("diaglog_settings", u"HotKey:", None))
#if QT_CONFIG(tooltip)
        self.kseq_screenshot.setToolTip(QCoreApplication.translate("diaglog_settings", u"Click to change screenshot hotkey", None))
#endif // QT_CONFIG(tooltip)
        self.kseq_screenshot.setKeySequence(QCoreApplication.translate("diaglog_settings", u"Ctrl+Alt+S", None))
        self.btn_hotkey_reset.setText(QCoreApplication.translate("diaglog_settings", u"Reset", None))
        self.groupBox.setTitle(QCoreApplication.translate("diaglog_settings", u"Path Settings", None))
        self.label.setText(QCoreApplication.translate("diaglog_settings", u"Tokenizer:", None))
        self.btn_tokenizer_path.setText(QCoreApplication.translate("diaglog_settings", u"Browse", None))
        self.label_2.setText(QCoreApplication.translate("diaglog_settings", u"Encoder:", None))
        self.btn_encoder_path.setText(QCoreApplication.translate("diaglog_settings", u"Browse", None))
        self.label_3.setText(QCoreApplication.translate("diaglog_settings", u"Decoder:", None))
        self.btn_decoder_path.setText(QCoreApplication.translate("diaglog_settings", u"Browse", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("diaglog_settings", u"About", None))
        self.textBrowser.setMarkdown(QCoreApplication.translate("diaglog_settings", u"CeleryMath\n"
"\n"
"A Latex Equation OCR tool.\n"
"\n"
"Author: Rainyl\n"
"\n"
"", None))
        self.textBrowser.setHtml(QCoreApplication.translate("diaglog_settings", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CeleryMath</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">A Latex Equation OCR tool.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Author: Rainyl</span></p></b"
                        "ody></html>", None))
    # retranslateUi

