# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_visual.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_visualSettingsWidget(object):
    def setupUi(self, visualSettingsWidget):
        if not visualSettingsWidget.objectName():
            visualSettingsWidget.setObjectName(u"visualSettingsWidget")
        visualSettingsWidget.resize(375, 433)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(visualSettingsWidget.sizePolicy().hasHeightForWidth())
        visualSettingsWidget.setSizePolicy(sizePolicy)
        visualSettingsWidget.setMinimumSize(QSize(375, 0))
        visualSettingsWidget.setMaximumSize(QSize(375, 16777215))
        visualSettingsWidget.setStyleSheet(u"QMainWindow {\n"
"	background-color: #5F5F5F;\n"
"}\n"
"\n"
"QFrame {\n"
"	background-color: #5F5F5F;\n"
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
"	background-color: rgb(47, 47, 47);\n"
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
" 	bor"
                        "der-radius: 11px;\n"
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
"	background-c"
                        "olor: #38363B;\n"
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
"QSlider::handle:vertic"
                        "al:pressed {\n"
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
""
                        "}\n"
"\n"
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
"	image: url(:/icons/svg/arrow-dow"
                        "n-2F2F2F.svg);\n"
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
        self.gridLayout = QGridLayout(visualSettingsWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(-1)
        self.label_3 = QLabel(visualSettingsWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 1, 1, 1)

        self.label_39 = QLabel(visualSettingsWidget)
        self.label_39.setObjectName(u"label_39")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy1)
        self.label_39.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_39, 9, 0, 1, 1)

        self.bgndSubtractQFrame = QFrame(visualSettingsWidget)
        self.bgndSubtractQFrame.setObjectName(u"bgndSubtractQFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth())
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy2)
        self.bgndSubtractQFrame.setMinimumSize(QSize(207, 0))
        self.bgndSubtractQFrame.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout_7 = QVBoxLayout(self.bgndSubtractQFrame)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        sizePolicy.setHeightForWidth(self.bgndSubtractXCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractXCheckBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        self.bgndSubtractXCheckBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip(u"Background subtraction along X")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setText(u"Along X axis")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.verticalLayout_7.addWidget(self.bgndSubtractXCheckBox)

        self.bgndSubtractYCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractYCheckBox.setObjectName(u"bgndSubtractYCheckBox")
        sizePolicy.setHeightForWidth(self.bgndSubtractYCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractYCheckBox.setSizePolicy(sizePolicy)
        self.bgndSubtractYCheckBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText(u"Along Y axis")
        self.bgndSubtractYCheckBox.setTristate(False)

        self.verticalLayout_7.addWidget(self.bgndSubtractYCheckBox)


        self.gridLayout.addWidget(self.bgndSubtractQFrame, 7, 0, 1, 1)

        self.label_2 = QLabel(visualSettingsWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)

        self.visualSettingsCloseButton = QPushButton(visualSettingsWidget)
        self.visualSettingsCloseButton.setObjectName(u"visualSettingsCloseButton")
        sizePolicy.setHeightForWidth(self.visualSettingsCloseButton.sizePolicy().hasHeightForWidth())
        self.visualSettingsCloseButton.setSizePolicy(sizePolicy)
        self.visualSettingsCloseButton.setMinimumSize(QSize(25, 0))
        self.visualSettingsCloseButton.setMaximumSize(QSize(25, 16777215))
        self.visualSettingsCloseButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/svg/cross.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.visualSettingsCloseButton.setIcon(icon)
        self.visualSettingsCloseButton.setIconSize(QSize(30, 30))

        self.gridLayout.addWidget(self.visualSettingsCloseButton, 0, 3, 1, 1)

        self.filterQFrame = QFrame(visualSettingsWidget)
        self.filterQFrame.setObjectName(u"filterQFrame")
        sizePolicy2.setHeightForWidth(self.filterQFrame.sizePolicy().hasHeightForWidth())
        self.filterQFrame.setSizePolicy(sizePolicy2)
        self.filterQFrame.setMinimumSize(QSize(0, 0))
        self.filterQFrame.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_12 = QVBoxLayout(self.filterQFrame)
        self.verticalLayout_12.setSpacing(15)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.waveletCheckBox = QCheckBox(self.filterQFrame)
        self.waveletCheckBox.setObjectName(u"waveletCheckBox")
        self.waveletCheckBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.waveletCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.waveletCheckBox.setText(u"Denoise")

        self.verticalLayout_12.addWidget(self.waveletCheckBox)

        self.edgeFilterCheckBox = QCheckBox(self.filterQFrame)
        self.edgeFilterCheckBox.setObjectName(u"edgeFilterCheckBox")
        self.edgeFilterCheckBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setText(u"Edge")

        self.verticalLayout_12.addWidget(self.edgeFilterCheckBox)

        self.topHatCheckBox = QCheckBox(self.filterQFrame)
        self.topHatCheckBox.setObjectName(u"topHatCheckBox")
        self.topHatCheckBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.topHatCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.topHatCheckBox.setText(u"Top-hat")

        self.verticalLayout_12.addWidget(self.topHatCheckBox)


        self.gridLayout.addWidget(self.filterQFrame, 10, 0, 1, 1)

        self.colorComboBox = QComboBox(visualSettingsWidget)
        icon1 = QIcon()
        icon1.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon1, u"PuOr")
        icon2 = QIcon()
        icon2.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon2, u"RdYlBu")
        icon3 = QIcon()
        icon3.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon3, u"bwr")
        icon4 = QIcon()
        icon4.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon4, u"viridis")
        icon5 = QIcon()
        icon5.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon5, u"cividis")
        icon6 = QIcon()
        icon6.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon6, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy)
        self.colorComboBox.setMinimumSize(QSize(250, 30))
        self.colorComboBox.setMaximumSize(QSize(250, 30))
#if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(150, 20))
        self.colorComboBox.setFrame(False)

        self.gridLayout.addWidget(self.colorComboBox, 2, 0, 1, 2)

        self.logScaleCheckBox = QCheckBox(visualSettingsWidget)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        self.logScaleCheckBox.setFont(font)
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText(u"Log")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout.addWidget(self.logScaleCheckBox, 2, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(25, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 11, 0, 1, 1)

        self.rangeSliderMin = QSlider(visualSettingsWidget)
        self.rangeSliderMin.setObjectName(u"rangeSliderMin")
        sizePolicy.setHeightForWidth(self.rangeSliderMin.sizePolicy().hasHeightForWidth())
        self.rangeSliderMin.setSizePolicy(sizePolicy)
        self.rangeSliderMin.setMinimumSize(QSize(207, 18))
        self.rangeSliderMin.setMaximumSize(QSize(207, 16777215))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.rangeSliderMin, 3, 0, 1, 1)

        self.label_38 = QLabel(visualSettingsWidget)
        self.label_38.setObjectName(u"label_38")
        sizePolicy1.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy1)
        self.label_38.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_38, 6, 0, 1, 1)

        self.rangeSliderMax = QSlider(visualSettingsWidget)
        self.rangeSliderMax.setObjectName(u"rangeSliderMax")
        sizePolicy.setHeightForWidth(self.rangeSliderMax.sizePolicy().hasHeightForWidth())
        self.rangeSliderMax.setSizePolicy(sizePolicy)
        self.rangeSliderMax.setMinimumSize(QSize(207, 18))
        self.rangeSliderMax.setMaximumSize(QSize(207, 16777215))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.rangeSliderMax, 4, 0, 1, 1)

        self.label_4 = QLabel(visualSettingsWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(True)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(0, 23))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setWeight(QFont.Light)
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size:16px;")
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_4.setMargin(0)
        self.label_4.setIndent(0)

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 2)

        self.label_40 = QLabel(visualSettingsWidget)
        self.label_40.setObjectName(u"label_40")
        sizePolicy1.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy1)
        self.label_40.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_40, 1, 0, 1, 1)


        self.retranslateUi(visualSettingsWidget)

        QMetaObject.connectSlotsByName(visualSettingsWidget)
    # setupUi

    def retranslateUi(self, visualSettingsWidget):
        visualSettingsWidget.setWindowTitle(QCoreApplication.translate("visualSettingsWidget", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("visualSettingsWidget", u"MAX", None))
        self.label_39.setText(QCoreApplication.translate("visualSettingsWidget", u"FILTERS", None))
        self.label_2.setText(QCoreApplication.translate("visualSettingsWidget", u"MIN", None))
        self.visualSettingsCloseButton.setText("")

        self.colorComboBox.setCurrentText(QCoreApplication.translate("visualSettingsWidget", u"PuOr", None))
        self.label_38.setText(QCoreApplication.translate("visualSettingsWidget", u"BACKGROUND SUBTRACT", None))
        self.label_4.setText(QCoreApplication.translate("visualSettingsWidget", u"SETTINGS: VISUAL", None))
        self.label_40.setText(QCoreApplication.translate("visualSettingsWidget", u"COLORING", None))
    # retranslateUi

