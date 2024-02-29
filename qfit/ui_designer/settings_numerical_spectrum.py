# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_numerical_spectrum.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QWidget)

from qfit.widgets.validated_line_edits import (IntLineEdit, StateLineEdit)
from . import resources_rc

class Ui_numericalSpectrumSettingsWidget(object):
    def setupUi(self, numericalSpectrumSettingsWidget):
        if not numericalSpectrumSettingsWidget.objectName():
            numericalSpectrumSettingsWidget.setObjectName(u"numericalSpectrumSettingsWidget")
        numericalSpectrumSettingsWidget.resize(375, 432)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(numericalSpectrumSettingsWidget.sizePolicy().hasHeightForWidth())
        numericalSpectrumSettingsWidget.setSizePolicy(sizePolicy)
        numericalSpectrumSettingsWidget.setMinimumSize(QSize(375, 0))
        numericalSpectrumSettingsWidget.setMaximumSize(QSize(439, 16777215))
        numericalSpectrumSettingsWidget.setStyleSheet(u"QMainWindow {\n"
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
" 	border-radi"
                        "us: 11px;\n"
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
"	background-color: #3"
                        "8363B;\n"
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
"QSlider::handle:vertical:press"
                        "ed {\n"
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
        self.gridLayout = QGridLayout(numericalSpectrumSettingsWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.initStateLineEdit = StateLineEdit(numericalSpectrumSettingsWidget)
        self.initStateLineEdit.setObjectName(u"initStateLineEdit")
        sizePolicy.setHeightForWidth(self.initStateLineEdit.sizePolicy().hasHeightForWidth())
        self.initStateLineEdit.setSizePolicy(sizePolicy)
        self.initStateLineEdit.setMinimumSize(QSize(170, 30))
        self.initStateLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.initStateLineEdit, 6, 2, 2, 3)

        self.evalsCountLineEdit = IntLineEdit(numericalSpectrumSettingsWidget)
        self.evalsCountLineEdit.setObjectName(u"evalsCountLineEdit")
        sizePolicy.setHeightForWidth(self.evalsCountLineEdit.sizePolicy().hasHeightForWidth())
        self.evalsCountLineEdit.setSizePolicy(sizePolicy)
        self.evalsCountLineEdit.setMinimumSize(QSize(170, 30))
        self.evalsCountLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.evalsCountLineEdit, 8, 2, 1, 3)

        self.label_46 = QLabel(numericalSpectrumSettingsWidget)
        self.label_46.setObjectName(u"label_46")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy1)
        self.label_46.setMaximumSize(QSize(200, 16777215))
        self.label_46.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_46, 12, 1, 1, 1)

        self.numericalSpectrumSettingsHelpPushButton = QPushButton(numericalSpectrumSettingsWidget)
        self.numericalSpectrumSettingsHelpPushButton.setObjectName(u"numericalSpectrumSettingsHelpPushButton")
        sizePolicy.setHeightForWidth(self.numericalSpectrumSettingsHelpPushButton.sizePolicy().hasHeightForWidth())
        self.numericalSpectrumSettingsHelpPushButton.setSizePolicy(sizePolicy)
        self.numericalSpectrumSettingsHelpPushButton.setMinimumSize(QSize(0, 0))
        self.numericalSpectrumSettingsHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/svg/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.numericalSpectrumSettingsHelpPushButton.setIcon(icon)
        self.numericalSpectrumSettingsHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout.addWidget(self.numericalSpectrumSettingsHelpPushButton, 0, 4, 2, 1)

        self.pointsAddLineEdit = IntLineEdit(numericalSpectrumSettingsWidget)
        self.pointsAddLineEdit.setObjectName(u"pointsAddLineEdit")
        sizePolicy.setHeightForWidth(self.pointsAddLineEdit.sizePolicy().hasHeightForWidth())
        self.pointsAddLineEdit.setSizePolicy(sizePolicy)
        self.pointsAddLineEdit.setMinimumSize(QSize(170, 30))
        self.pointsAddLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.pointsAddLineEdit, 9, 2, 1, 3)

        self.label_42 = QLabel(numericalSpectrumSettingsWidget)
        self.label_42.setObjectName(u"label_42")
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)
        self.label_42.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_42, 8, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(25, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 5, 2, 1)

        self.numSpecSettingsCloseButton = QPushButton(numericalSpectrumSettingsWidget)
        self.numSpecSettingsCloseButton.setObjectName(u"numSpecSettingsCloseButton")
        sizePolicy.setHeightForWidth(self.numSpecSettingsCloseButton.sizePolicy().hasHeightForWidth())
        self.numSpecSettingsCloseButton.setSizePolicy(sizePolicy)
        self.numSpecSettingsCloseButton.setMinimumSize(QSize(25, 0))
        self.numSpecSettingsCloseButton.setMaximumSize(QSize(167777, 16777215))
        self.numSpecSettingsCloseButton.setSizeIncrement(QSize(45, 0))
        self.numSpecSettingsCloseButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/cross.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.numSpecSettingsCloseButton.setIcon(icon1)
        self.numSpecSettingsCloseButton.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.numSpecSettingsCloseButton, 0, 5, 3, 1)

        self.label_43 = QLabel(numericalSpectrumSettingsWidget)
        self.label_43.setObjectName(u"label_43")
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_43, 9, 1, 1, 1)

        self.label = QLabel(numericalSpectrumSettingsWidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label, 6, 1, 2, 1)

        self.label_33 = QLabel(numericalSpectrumSettingsWidget)
        self.label_33.setObjectName(u"label_33")
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_33, 10, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 14, 1, 1, 1)

        self.statusTextLabel = QLabel(numericalSpectrumSettingsWidget)
        self.statusTextLabel.setObjectName(u"statusTextLabel")
        self.statusTextLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel.setWordWrap(True)
        self.statusTextLabel.setMargin(5)

        self.gridLayout.addWidget(self.statusTextLabel, 13, 1, 1, 5)

        self.prefitPhotonSpinBox = QSpinBox(numericalSpectrumSettingsWidget)
        self.prefitPhotonSpinBox.setObjectName(u"prefitPhotonSpinBox")
        sizePolicy.setHeightForWidth(self.prefitPhotonSpinBox.sizePolicy().hasHeightForWidth())
        self.prefitPhotonSpinBox.setSizePolicy(sizePolicy)
        self.prefitPhotonSpinBox.setMinimumSize(QSize(96, 35))
        self.prefitPhotonSpinBox.setStyleSheet(u"QSpinBox {\n"
"    color: #FFFFFF;\n"
"    background-color: #2F2F2F;\n"
"	height: 28px;\n"
"    width: 28px; \n"
"    background-image: url(:/images/spin_box_bg_171717.svg) 1;\n"
"    background-repeat: no-repeat;\n"
"    background-position: center center;\n"
"    background-origin: content;\n"
"   /*padding: -5px 0px -14px 0px;*/\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: right; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px; \n"
"	background-color: #171717;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: left; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px;\n"
"	background-color: #171717;\n"
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
"QSpinBox::up-arrow:pressed {\n"
"  "
                        "  width: 20px;\n"
"    height: 20px;\n"
"    image: url(:/icons/svg/plus-pressed.svg) 1;\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/svg/minus.svg) 1;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow:pressed {\n"
"    image: url(:/icons/svg/minus-pressed.svg) 1;\n"
"    width: 20px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed {\n"
"    background-color: #262626;\n"
"}\n"
"\n"
"QSpinBox::down-button:pressed {\n"
"    background-color: #262626;\n"
"}")
        self.prefitPhotonSpinBox.setAlignment(Qt.AlignCenter)
        self.prefitPhotonSpinBox.setMinimum(1)

        self.gridLayout.addWidget(self.prefitPhotonSpinBox, 10, 2, 1, 2)

        self.numericalSpectrumSettingsLabel = QLabel(numericalSpectrumSettingsWidget)
        self.numericalSpectrumSettingsLabel.setObjectName(u"numericalSpectrumSettingsLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.numericalSpectrumSettingsLabel.sizePolicy().hasHeightForWidth())
        self.numericalSpectrumSettingsLabel.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        font.setWeight(QFont.Light)
        font.setItalic(False)
        self.numericalSpectrumSettingsLabel.setFont(font)
        self.numericalSpectrumSettingsLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size: 16px;")
        self.numericalSpectrumSettingsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.numericalSpectrumSettingsLabel, 1, 1, 1, 3)

        self.subsysComboBox = QComboBox(numericalSpectrumSettingsWidget)
        self.subsysComboBox.setObjectName(u"subsysComboBox")
        sizePolicy.setHeightForWidth(self.subsysComboBox.sizePolicy().hasHeightForWidth())
        self.subsysComboBox.setSizePolicy(sizePolicy)
        self.subsysComboBox.setMinimumSize(QSize(170, 30))
        self.subsysComboBox.setMaximumSize(QSize(16777215, 30))
        self.subsysComboBox.setStyleSheet(u"")
        self.subsysComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.gridLayout.addWidget(self.subsysComboBox, 3, 2, 2, 3)

        self.label_44 = QLabel(numericalSpectrumSettingsWidget)
        self.label_44.setObjectName(u"label_44")
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)
        self.label_44.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_44, 3, 1, 2, 1)

        self.mseLabel = QLabel(numericalSpectrumSettingsWidget)
        self.mseLabel.setObjectName(u"mseLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.mseLabel.sizePolicy().hasHeightForWidth())
        self.mseLabel.setSizePolicy(sizePolicy3)
        self.mseLabel.setMinimumSize(QSize(200, 0))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setBold(True)
        self.mseLabel.setFont(font1)
        self.mseLabel.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.mseLabel, 11, 1, 1, 1)

        self.prefitResultHelpPushButton = QPushButton(numericalSpectrumSettingsWidget)
        self.prefitResultHelpPushButton.setObjectName(u"prefitResultHelpPushButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.prefitResultHelpPushButton.sizePolicy().hasHeightForWidth())
        self.prefitResultHelpPushButton.setSizePolicy(sizePolicy4)
        self.prefitResultHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.prefitResultHelpPushButton.setIcon(icon)
        self.prefitResultHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout.addWidget(self.prefitResultHelpPushButton, 11, 4, 1, 1)


        self.retranslateUi(numericalSpectrumSettingsWidget)

        QMetaObject.connectSlotsByName(numericalSpectrumSettingsWidget)
    # setupUi

    def retranslateUi(self, numericalSpectrumSettingsWidget):
        numericalSpectrumSettingsWidget.setWindowTitle(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"Form", None))
        self.initStateLineEdit.setPlaceholderText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"dressed or bare label", None))
        self.evalsCountLineEdit.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"20", None))
        self.label_46.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"STATUS:", None))
        self.numericalSpectrumSettingsHelpPushButton.setText("")
        self.pointsAddLineEdit.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"10", None))
        self.pointsAddLineEdit.setPlaceholderText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"# of x value for spectrum sweep", None))
        self.label_42.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"EVALS COUNT", None))
        self.numSpecSettingsCloseButton.setText("")
        self.label_43.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"POINTS ADDED", None))
        self.label.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"INITIAL STATE", None))
        self.label_33.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"PHOTONS", None))
        self.statusTextLabel.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"-", None))
        self.numericalSpectrumSettingsLabel.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"SETTINGS: NUMERICAL SPECTRUM", None))
        self.label_44.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"TRANSITIONS", None))
        self.mseLabel.setText(QCoreApplication.translate("numericalSpectrumSettingsWidget", u"MSE:  - GHz\u00b2   (+0.00%)", None))
        self.prefitResultHelpPushButton.setText("")
    # retranslateUi

