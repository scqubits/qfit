# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_fit.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

from qfit.widgets.validated_line_edits import PositiveFloatLineEdit
from . import resources_rc

class Ui_fitSettingsWidget(object):
    def setupUi(self, fitSettingsWidget):
        if not fitSettingsWidget.objectName():
            fitSettingsWidget.setObjectName(u"fitSettingsWidget")
        fitSettingsWidget.setWindowModality(Qt.WindowModal)
        fitSettingsWidget.resize(375, 432)
        fitSettingsWidget.setMinimumSize(QSize(375, 0))
        fitSettingsWidget.setMaximumSize(QSize(484, 16777215))
        fitSettingsWidget.setStyleSheet(u"QWidget {\n"
"	background-color: #3F3F3F;\n"
"}\n"
"\n"
"QFrame {\n"
"	background-color: #3F3F3F;\n"
"}\n"
"\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QWidget {\n"
"	font-family: \"Roboto Medium\";\n"
"	background-color: #2F2F2F;\n"
"}\n"
"\n"
"QLabel {\n"
"	color: rgb(170, 170, 170);\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"/* LINE EDIT */\n"
"QLineEdit {\n"
"	color: rgb(170, 170, 170);\n"
"	background-color: #171717;\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 5px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox {\n"
"	color: #AAAAAA;\n"
"    spacing: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    border: 1px solid #DBBCFB;\n"
"	width: 20px;\n"
"	height: 20px;\n"
" 	border-radius: "
                        "11px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"	border: 1px solid #BE82FA;\n"
"   background: transparent;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"	border: 1px solid #BE82FA;\n"
"   background: transparent;\n"
"	image: url(:/icons/svg/check.svg);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton {\n"
"	color: #AAAAAA;\n"
"    spacing: 10px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 1px solid #DBBCFB;\n"
"	width: 20px;\n"
"	height: 20px;\n"
" 	border-radius: 11px;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"	border: 1px solid #BE82FA;\n"
"   background: transparent;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"	border: 1px solid #BE82FA;\n"
"   background: transparent;\n"
"	image: url(:/icons/svg/check.svg);\n"
"}\n"
"\n"
"\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: #38363"
                        "B;\n"
"}\n"
"\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: #3A393F;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: #BE82FA;\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: #C186FE;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: #A870E0;\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(85, 170, 255);\n"
"	border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"\n"
"QSlider::handle:vertical:pressed {"
                        "\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QGroupBox {\n"
"	border: 0;\n"
"	color: rgb(170, 170, 170);\n"
"	font: 57 10px \"Roboto Medium\";\n"
"}\n"
"\n"
"QSpinBox {\n"
"	background-color: transparent;\n"
"	color: rgb(170, 170, 170);\n"
"    padding-right: 5px; /* make room for the arrows */\n"
"    border-width: 3;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: right; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px; \n"
"	background-color: rgb(93,93,93);\n"
"    border-radius: 4px;\n"
"    border: 1px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: left; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px;\n"
"	background-color: rgb(93,93,93);\n"
"    border-radius: 4px;\n"
"    border: 1px;\n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    image: url(:/icons/svg/plus.svg) 1;\n"
"}\n"
"\n"
""
                        "QSpinBox::down-arrow {\n"
"    image: url(:/icons/svg/minus.svg) 1;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed {\n"
"    background-color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox {\n"
"	color: rgb(170, 170, 170);\n"
"	background-color: #171717;\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:hover{\n"
"	background-color: #171717;\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	background-color: #171717;\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
" }\n"
"QComboBox::drop-down:button {\n"
"	width: 25px; \n"
" }\n"
"\n"
"QComboBox::down-arrow{\n"
"	image: url(:/icons/svg/arrow-down-2F2F2F.sv"
                        "g);\n"
"	width: 12px;\n"
"	height: 9px;\n"
"}\n"
" \n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: #2F2F2F;\n"
"	padding: 5px;\n"
"	selection-background-color: #2F2F2F;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item{\n"
"    height: 50px;\n"
"}\n"
"\n"
"")
        self.gridLayout = QGridLayout(fitSettingsWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tolLineEdit = PositiveFloatLineEdit(fitSettingsWidget)
        self.tolLineEdit.setObjectName(u"tolLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tolLineEdit.sizePolicy().hasHeightForWidth())
        self.tolLineEdit.setSizePolicy(sizePolicy)
        self.tolLineEdit.setMinimumSize(QSize(170, 30))
        self.tolLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.tolLineEdit, 3, 2, 1, 1)

        self.optimizerComboBox = QComboBox(fitSettingsWidget)
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.setObjectName(u"optimizerComboBox")
        sizePolicy.setHeightForWidth(self.optimizerComboBox.sizePolicy().hasHeightForWidth())
        self.optimizerComboBox.setSizePolicy(sizePolicy)
        self.optimizerComboBox.setMinimumSize(QSize(170, 30))
        self.optimizerComboBox.setMaximumSize(QSize(16777213, 30))

        self.gridLayout.addWidget(self.optimizerComboBox, 2, 2, 1, 1)

        self.label_49 = QLabel(fitSettingsWidget)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_49, 5, 1, 1, 1)

        self.fitSettingsCloseButton = QPushButton(fitSettingsWidget)
        self.fitSettingsCloseButton.setObjectName(u"fitSettingsCloseButton")
        sizePolicy.setHeightForWidth(self.fitSettingsCloseButton.sizePolicy().hasHeightForWidth())
        self.fitSettingsCloseButton.setSizePolicy(sizePolicy)
        self.fitSettingsCloseButton.setMinimumSize(QSize(25, 0))
        self.fitSettingsCloseButton.setSizeIncrement(QSize(0, 0))
        self.fitSettingsCloseButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/svg/cross.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.fitSettingsCloseButton.setIcon(icon)
        self.fitSettingsCloseButton.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.fitSettingsCloseButton, 1, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(25, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 4, 1, 1)

        self.fitResultHelpPushButton = QPushButton(fitSettingsWidget)
        self.fitResultHelpPushButton.setObjectName(u"fitResultHelpPushButton")
        self.fitResultHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.fitResultHelpPushButton.setIcon(icon1)
        self.fitResultHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout.addWidget(self.fitResultHelpPushButton, 4, 3, 1, 1)

        self.label_47 = QLabel(fitSettingsWidget)
        self.label_47.setObjectName(u"label_47")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy1)
        self.label_47.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_47, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 1, 1, 1)

        self.label_45 = QLabel(fitSettingsWidget)
        self.label_45.setObjectName(u"label_45")
        sizePolicy.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy)
        self.label_45.setMinimumSize(QSize(0, 23))
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        font.setWeight(QFont.Light)
        font.setItalic(False)
        self.label_45.setFont(font)
        self.label_45.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size: 16px;")
        self.label_45.setIndent(-1)

        self.gridLayout.addWidget(self.label_45, 1, 1, 1, 2)

        self.statusTextLabel_2 = QLabel(fitSettingsWidget)
        self.statusTextLabel_2.setObjectName(u"statusTextLabel_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.statusTextLabel_2.sizePolicy().hasHeightForWidth())
        self.statusTextLabel_2.setSizePolicy(sizePolicy2)
        self.statusTextLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel_2.setWordWrap(True)
        self.statusTextLabel_2.setMargin(5)

        self.gridLayout.addWidget(self.statusTextLabel_2, 6, 1, 1, 4)

        self.label_8 = QLabel(fitSettingsWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setMinimumSize(QSize(0, 0))
        self.label_8.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_8, 3, 1, 1, 1)

        self.mseLabel_2 = QLabel(fitSettingsWidget)
        self.mseLabel_2.setObjectName(u"mseLabel_2")
        sizePolicy.setHeightForWidth(self.mseLabel_2.sizePolicy().hasHeightForWidth())
        self.mseLabel_2.setSizePolicy(sizePolicy)
        self.mseLabel_2.setMinimumSize(QSize(200, 0))
        self.mseLabel_2.setMaximumSize(QSize(200, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setBold(True)
        self.mseLabel_2.setFont(font1)
        self.mseLabel_2.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.mseLabel_2, 4, 1, 1, 1)


        self.retranslateUi(fitSettingsWidget)

        QMetaObject.connectSlotsByName(fitSettingsWidget)
    # setupUi

    def retranslateUi(self, fitSettingsWidget):
        self.tolLineEdit.setStyleSheet(QCoreApplication.translate("fitSettingsWidget", u"font-size: 13px", None))
        self.tolLineEdit.setText(QCoreApplication.translate("fitSettingsWidget", u"1e-6", None))
        self.optimizerComboBox.setItemText(0, QCoreApplication.translate("fitSettingsWidget", u"L-BFGS-B", None))
        self.optimizerComboBox.setItemText(1, QCoreApplication.translate("fitSettingsWidget", u"Nelder-Mead", None))
        self.optimizerComboBox.setItemText(2, QCoreApplication.translate("fitSettingsWidget", u"Powell", None))
        self.optimizerComboBox.setItemText(3, QCoreApplication.translate("fitSettingsWidget", u"shgo", None))
        self.optimizerComboBox.setItemText(4, QCoreApplication.translate("fitSettingsWidget", u"differential evolution", None))

        self.optimizerComboBox.setStyleSheet(QCoreApplication.translate("fitSettingsWidget", u"font-size: 13px", None))
        self.label_49.setText(QCoreApplication.translate("fitSettingsWidget", u"STATUS:", None))
        self.fitSettingsCloseButton.setText("")
        self.fitResultHelpPushButton.setText("")
        self.label_47.setText(QCoreApplication.translate("fitSettingsWidget", u"OPTIMIZER", None))
        self.label_45.setText(QCoreApplication.translate("fitSettingsWidget", u"SETTINGS: FIT", None))
        self.statusTextLabel_2.setText(QCoreApplication.translate("fitSettingsWidget", u"-", None))
        self.label_8.setText(QCoreApplication.translate("fitSettingsWidget", u"TOLERANCE", None))
        self.mseLabel_2.setText(QCoreApplication.translate("fitSettingsWidget", u"MSE:  - GHz\u00b2   (+0.00%)", None))
        pass
    # retranslateUi

