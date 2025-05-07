# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
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
    QSlider, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

from qfit.widgets.validated_line_edits import (IntLineEdit, MultiStatesLineEdit, PositiveFloatLineEdit)
from . import resources_rc

class Ui_settingsWidget(object):
    def setupUi(self, settingsWidget):
        if not settingsWidget.objectName():
            settingsWidget.setObjectName(u"settingsWidget")
        settingsWidget.resize(390, 470)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settingsWidget.sizePolicy().hasHeightForWidth())
        settingsWidget.setSizePolicy(sizePolicy)
        settingsWidget.setMinimumSize(QSize(390, 470))
        settingsWidget.setMaximumSize(QSize(390, 470))
        settingsWidget.setStyleSheet(u"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QWidget {\n"
"	font-family: \"Roboto Medium\";\n"
"	border: 2px solid #171717; \n"
"	border-radius: 5px;\n"
"	background-color: #2F2F2F;\n"
"}\n"
"\n"
"QLabel {\n"
"	color: rgb(170, 170, 170);\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"/* LINE EDIT */\n"
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
"QSlider::groove:horizo"
                        "ntal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: #38363B;\n"
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
"QSlider::handle:vertical"
                        ":hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"\n"
"QSlider::handle:vertical:pressed {\n"
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
"QSpinBox::up-arrow "
                        "{\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    image: url(:/icons/svg/plus.svg) 1;\n"
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
"")
        self.gridLayout_3 = QGridLayout(settingsWidget)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(12, 12, 12, -1)
        self.verticalSpacer_3 = QSpacerItem(5, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 1, 1, 1, 1)

        self.tabWidget = QTabWidget(settingsWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setMinimumSize(QSize(0, 430))
        self.tabWidget.setMaximumSize(QSize(16777215, 430))
        self.tabWidget.setStyleSheet(u"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that\n"
"    it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"    background: #171717;\n"
"	border: 2px solid #171717;\n"
"    border-bottom-color: #2F2F2F; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 7px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	background: #2F2F2F;\n"
"	border: 2px solid #171717;\n"
"    border-bottom-color: #2F2F2F; /* same as pane color */\n"
"	font: 14px \"Roboto Medium\";\n"
"    color: #DBBCFB;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"	font: 14px \"Roboto Medium\";\n"
"    color: #797979;\n"
"}\n"
"\n"
"QWidget {\n"
"	font-family: \"Roboto Medium\";\n"
"	background-color: #2F2F2F;\n"
"	border: 0px black;\n"
"}\n"
"\n"
"/* LINE EDIT */\n"
"QLineEdit {\n"
"	color: rgb(170, "
                        "170, 170);\n"
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
" 	border-radius: 11px;\n"
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
"/* COMBOBOX */\n"
"QComboBox {\n"
"	color: rgb(170, 170, 170);\n"
"	background-color: #171717;\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	pad"
                        "ding-left: 10px;\n"
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
"	image: url(:/icons/svg/arrow-down-2F2F2F.svg);\n"
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
"}")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.visualTab = QWidget()
        self.visualTab.setObjectName(u"visualTab")
        self.verticalLayout = QVBoxLayout(self.visualTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.visualTabContainerWidget = QWidget(self.visualTab)
        self.visualTabContainerWidget.setObjectName(u"visualTabContainerWidget")
        self.visualTabContainerWidget.setMinimumSize(QSize(0, 360))
        self.visualTabContainerWidget.setMaximumSize(QSize(16777215, 430))
        self.gridLayout_2 = QGridLayout(self.visualTabContainerWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 5, 0, 0)
        self.rangeSliderMin = QSlider(self.visualTabContainerWidget)
        self.rangeSliderMin.setObjectName(u"rangeSliderMin")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.rangeSliderMin.sizePolicy().hasHeightForWidth())
        self.rangeSliderMin.setSizePolicy(sizePolicy2)
        self.rangeSliderMin.setMinimumSize(QSize(207, 18))
        self.rangeSliderMin.setMaximumSize(QSize(207, 16777215))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.rangeSliderMin, 3, 0, 1, 1)

        self.rangeSliderMax = QSlider(self.visualTabContainerWidget)
        self.rangeSliderMax.setObjectName(u"rangeSliderMax")
        sizePolicy2.setHeightForWidth(self.rangeSliderMax.sizePolicy().hasHeightForWidth())
        self.rangeSliderMax.setSizePolicy(sizePolicy2)
        self.rangeSliderMax.setMinimumSize(QSize(207, 18))
        self.rangeSliderMax.setMaximumSize(QSize(207, 16777215))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout_2.addWidget(self.rangeSliderMax, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 7, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.filterQFrame = QFrame(self.visualTabContainerWidget)
        self.filterQFrame.setObjectName(u"filterQFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.filterQFrame.sizePolicy().hasHeightForWidth())
        self.filterQFrame.setSizePolicy(sizePolicy3)
        self.filterQFrame.setMinimumSize(QSize(0, 0))
        self.filterQFrame.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_12 = QVBoxLayout(self.filterQFrame)
        self.verticalLayout_12.setSpacing(15)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.waveletCheckBox = QCheckBox(self.filterQFrame)
        self.waveletCheckBox.setObjectName(u"waveletCheckBox")
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
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


        self.gridLayout_2.addWidget(self.filterQFrame, 8, 0, 1, 1)

        self.colorComboBox = QComboBox(self.visualTabContainerWidget)
        icon = QIcon()
        icon.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon, u"PuOr")
        icon1 = QIcon()
        icon1.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon1, u"RdYlBu")
        icon2 = QIcon()
        icon2.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon2, u"bwr")
        icon3 = QIcon()
        icon3.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon3, u"viridis")
        icon4 = QIcon()
        icon4.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon4, u"cividis")
        icon5 = QIcon()
        icon5.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon5, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy2.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy2)
        self.colorComboBox.setMinimumSize(QSize(250, 30))
        self.colorComboBox.setMaximumSize(QSize(250, 30))
#if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(150, 20))
        self.colorComboBox.setFrame(False)

        self.gridLayout_2.addWidget(self.colorComboBox, 2, 0, 1, 2)

        self.label_39 = QLabel(self.visualTabContainerWidget)
        self.label_39.setObjectName(u"label_39")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_39.sizePolicy().hasHeightForWidth())
        self.label_39.setSizePolicy(sizePolicy4)
        self.label_39.setStyleSheet(u"font-size: 13px")

        self.gridLayout_2.addWidget(self.label_39, 7, 0, 1, 1)

        self.label_2 = QLabel(self.visualTabContainerWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 3, 1, 1, 1)

        self.label_38 = QLabel(self.visualTabContainerWidget)
        self.label_38.setObjectName(u"label_38")
        sizePolicy4.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy4)
        self.label_38.setStyleSheet(u"font-size: 13px")

        self.gridLayout_2.addWidget(self.label_38, 5, 0, 1, 1)

        self.label_3 = QLabel(self.visualTabContainerWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 4, 1, 1, 1)

        self.label_40 = QLabel(self.visualTabContainerWidget)
        self.label_40.setObjectName(u"label_40")
        sizePolicy4.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy4)
        self.label_40.setStyleSheet(u"font-size: 13px")

        self.gridLayout_2.addWidget(self.label_40, 1, 0, 1, 1)

        self.logScaleCheckBox = QCheckBox(self.visualTabContainerWidget)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        self.logScaleCheckBox.setFont(font)
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText(u"Log")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout_2.addWidget(self.logScaleCheckBox, 2, 2, 1, 1)

        self.bgndSubtractQFrame = QFrame(self.visualTabContainerWidget)
        self.bgndSubtractQFrame.setObjectName(u"bgndSubtractQFrame")
        sizePolicy3.setHeightForWidth(self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth())
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy3)
        self.bgndSubtractQFrame.setMinimumSize(QSize(207, 0))
        self.bgndSubtractQFrame.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout_7 = QVBoxLayout(self.bgndSubtractQFrame)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        sizePolicy2.setHeightForWidth(self.bgndSubtractXCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractXCheckBox.setSizePolicy(sizePolicy2)
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
        sizePolicy2.setHeightForWidth(self.bgndSubtractYCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractYCheckBox.setSizePolicy(sizePolicy2)
        self.bgndSubtractYCheckBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText(u"Along Y axis")
        self.bgndSubtractYCheckBox.setTristate(False)

        self.verticalLayout_7.addWidget(self.bgndSubtractYCheckBox)


        self.gridLayout_2.addWidget(self.bgndSubtractQFrame, 6, 0, 1, 1)


        self.verticalLayout.addWidget(self.visualTabContainerWidget)

        self.tabWidget.addTab(self.visualTab, "")
        self.spectrumTab = QWidget()
        self.spectrumTab.setObjectName(u"spectrumTab")
        self.verticalLayout_3 = QVBoxLayout(self.spectrumTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.spectrumTabContainerWidget = QWidget(self.spectrumTab)
        self.spectrumTabContainerWidget.setObjectName(u"spectrumTabContainerWidget")
        self.spectrumTabContainerWidget.setMinimumSize(QSize(0, 360))
        self.spectrumTabContainerWidget.setMaximumSize(QSize(16777215, 430))
        self.gridLayout = QGridLayout(self.spectrumTabContainerWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 5, 0, 0)
        self.subsysComboBox = QComboBox(self.spectrumTabContainerWidget)
        self.subsysComboBox.setObjectName(u"subsysComboBox")
        sizePolicy2.setHeightForWidth(self.subsysComboBox.sizePolicy().hasHeightForWidth())
        self.subsysComboBox.setSizePolicy(sizePolicy2)
        self.subsysComboBox.setMinimumSize(QSize(170, 30))
        self.subsysComboBox.setMaximumSize(QSize(16777215, 30))
        self.subsysComboBox.setStyleSheet(u"")
        self.subsysComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.gridLayout.addWidget(self.subsysComboBox, 1, 1, 1, 2)

        self.pointsAddLineEdit = IntLineEdit(self.spectrumTabContainerWidget)
        self.pointsAddLineEdit.setObjectName(u"pointsAddLineEdit")
        sizePolicy2.setHeightForWidth(self.pointsAddLineEdit.sizePolicy().hasHeightForWidth())
        self.pointsAddLineEdit.setSizePolicy(sizePolicy2)
        self.pointsAddLineEdit.setMinimumSize(QSize(170, 30))
        self.pointsAddLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.pointsAddLineEdit, 5, 1, 1, 2)

        self.prefitPhotonSpinBox = QSpinBox(self.spectrumTabContainerWidget)
        self.prefitPhotonSpinBox.setObjectName(u"prefitPhotonSpinBox")
        sizePolicy2.setHeightForWidth(self.prefitPhotonSpinBox.sizePolicy().hasHeightForWidth())
        self.prefitPhotonSpinBox.setSizePolicy(sizePolicy2)
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

        self.gridLayout.addWidget(self.prefitPhotonSpinBox, 7, 1, 1, 1)

        self.numCPUsLineEdit = IntLineEdit(self.spectrumTabContainerWidget)
        self.numCPUsLineEdit.setObjectName(u"numCPUsLineEdit")
        sizePolicy2.setHeightForWidth(self.numCPUsLineEdit.sizePolicy().hasHeightForWidth())
        self.numCPUsLineEdit.setSizePolicy(sizePolicy2)
        self.numCPUsLineEdit.setMinimumSize(QSize(170, 30))

        self.gridLayout.addWidget(self.numCPUsLineEdit, 6, 1, 1, 1)

        self.label = QLabel(self.spectrumTabContainerWidget)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_44 = QLabel(self.spectrumTabContainerWidget)
        self.label_44.setObjectName(u"label_44")
        sizePolicy2.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy2)
        self.label_44.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_44, 1, 0, 1, 1)

        self.label_5 = QLabel(self.spectrumTabContainerWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(170)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy5)
        self.label_5.setMinimumSize(QSize(170, 0))
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-size: 10pt;\n"
"}")
        self.label_5.setWordWrap(True)

        self.gridLayout.addWidget(self.label_5, 3, 1, 1, 1)

        self.label_6 = QLabel(self.spectrumTabContainerWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 1)

        self.label_33 = QLabel(self.spectrumTabContainerWidget)
        self.label_33.setObjectName(u"label_33")
        sizePolicy2.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy2)
        self.label_33.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_33, 7, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 115, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 9, 0, 1, 1)

        self.label_4 = QLabel(self.spectrumTabContainerWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)

        self.label_42 = QLabel(self.spectrumTabContainerWidget)
        self.label_42.setObjectName(u"label_42")
        sizePolicy2.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy2)
        self.label_42.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_42, 4, 0, 1, 1)

        self.label_43 = QLabel(self.spectrumTabContainerWidget)
        self.label_43.setObjectName(u"label_43")
        sizePolicy2.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy2)
        self.label_43.setStyleSheet(u"font-size: 13px")

        self.gridLayout.addWidget(self.label_43, 5, 0, 1, 1)

        self.evalsCountLineEdit = IntLineEdit(self.spectrumTabContainerWidget)
        self.evalsCountLineEdit.setObjectName(u"evalsCountLineEdit")
        sizePolicy2.setHeightForWidth(self.evalsCountLineEdit.sizePolicy().hasHeightForWidth())
        self.evalsCountLineEdit.setSizePolicy(sizePolicy2)
        self.evalsCountLineEdit.setMinimumSize(QSize(170, 30))
        self.evalsCountLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.evalsCountLineEdit, 4, 1, 1, 2)

        self.initStateLineEdit = MultiStatesLineEdit(self.spectrumTabContainerWidget)
        self.initStateLineEdit.setObjectName(u"initStateLineEdit")
        sizePolicy2.setHeightForWidth(self.initStateLineEdit.sizePolicy().hasHeightForWidth())
        self.initStateLineEdit.setSizePolicy(sizePolicy2)
        self.initStateLineEdit.setMinimumSize(QSize(170, 30))
        self.initStateLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.initStateLineEdit, 2, 1, 1, 2)

        self.numericalSpectrumSettingsHelpPushButton = QPushButton(self.spectrumTabContainerWidget)
        self.numericalSpectrumSettingsHelpPushButton.setObjectName(u"numericalSpectrumSettingsHelpPushButton")
        sizePolicy2.setHeightForWidth(self.numericalSpectrumSettingsHelpPushButton.sizePolicy().hasHeightForWidth())
        self.numericalSpectrumSettingsHelpPushButton.setSizePolicy(sizePolicy2)
        self.numericalSpectrumSettingsHelpPushButton.setMinimumSize(QSize(0, 0))
        self.numericalSpectrumSettingsHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icons/svg/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.numericalSpectrumSettingsHelpPushButton.setIcon(icon6)
        self.numericalSpectrumSettingsHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout.addWidget(self.numericalSpectrumSettingsHelpPushButton, 8, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.spectrumTabContainerWidget)

        self.tabWidget.addTab(self.spectrumTab, "")
        self.fitTab = QWidget()
        self.fitTab.setObjectName(u"fitTab")
        self.verticalLayout_2 = QVBoxLayout(self.fitTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.fitTabContainerWidget = QWidget(self.fitTab)
        self.fitTabContainerWidget.setObjectName(u"fitTabContainerWidget")
        self.fitTabContainerWidget.setMinimumSize(QSize(0, 360))
        self.fitTabContainerWidget.setMaximumSize(QSize(16777215, 430))
        self.gridLayout_4 = QGridLayout(self.fitTabContainerWidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 5, 0, 0)
        self.tolLineEdit = PositiveFloatLineEdit(self.fitTabContainerWidget)
        self.tolLineEdit.setObjectName(u"tolLineEdit")
        sizePolicy2.setHeightForWidth(self.tolLineEdit.sizePolicy().hasHeightForWidth())
        self.tolLineEdit.setSizePolicy(sizePolicy2)
        self.tolLineEdit.setMinimumSize(QSize(170, 30))
        self.tolLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_4.addWidget(self.tolLineEdit, 1, 1, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 240, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 2, 0, 1, 1)

        self.label_47 = QLabel(self.fitTabContainerWidget)
        self.label_47.setObjectName(u"label_47")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy6)
        self.label_47.setStyleSheet(u"font-size: 13px")

        self.gridLayout_4.addWidget(self.label_47, 0, 0, 1, 1)

        self.optimizerComboBox = QComboBox(self.fitTabContainerWidget)
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.setObjectName(u"optimizerComboBox")
        sizePolicy2.setHeightForWidth(self.optimizerComboBox.sizePolicy().hasHeightForWidth())
        self.optimizerComboBox.setSizePolicy(sizePolicy2)
        self.optimizerComboBox.setMinimumSize(QSize(170, 30))
        self.optimizerComboBox.setMaximumSize(QSize(16777213, 30))

        self.gridLayout_4.addWidget(self.optimizerComboBox, 0, 1, 1, 1)

        self.label_8 = QLabel(self.fitTabContainerWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy6.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy6)
        self.label_8.setMinimumSize(QSize(0, 0))
        self.label_8.setStyleSheet(u"font-size: 13px")

        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.fitTabContainerWidget)

        self.tabWidget.addTab(self.fitTab, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 2, 1)

        self.settingsCloseButton = QPushButton(settingsWidget)
        self.settingsCloseButton.setObjectName(u"settingsCloseButton")
        sizePolicy2.setHeightForWidth(self.settingsCloseButton.sizePolicy().hasHeightForWidth())
        self.settingsCloseButton.setSizePolicy(sizePolicy2)
        self.settingsCloseButton.setMinimumSize(QSize(25, 0))
        self.settingsCloseButton.setMaximumSize(QSize(25, 16777215))
        self.settingsCloseButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/icons/svg/cross.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsCloseButton.setIcon(icon7)
        self.settingsCloseButton.setIconSize(QSize(30, 30))

        self.gridLayout_3.addWidget(self.settingsCloseButton, 0, 1, 1, 1)


        self.retranslateUi(settingsWidget)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(settingsWidget)
    # setupUi

    def retranslateUi(self, settingsWidget):
        settingsWidget.setWindowTitle(QCoreApplication.translate("settingsWidget", u"Form", None))

        self.colorComboBox.setCurrentText(QCoreApplication.translate("settingsWidget", u"PuOr", None))
        self.label_39.setText(QCoreApplication.translate("settingsWidget", u"FILTERS", None))
        self.label_2.setText(QCoreApplication.translate("settingsWidget", u"MIN", None))
        self.label_38.setText(QCoreApplication.translate("settingsWidget", u"BACKGROUND SUBTRACT", None))
        self.label_3.setText(QCoreApplication.translate("settingsWidget", u"MAX", None))
        self.label_40.setText(QCoreApplication.translate("settingsWidget", u"COLORING", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.visualTab), QCoreApplication.translate("settingsWidget", u"VISUAL", None))
        self.pointsAddLineEdit.setText(QCoreApplication.translate("settingsWidget", u"10", None))
        self.pointsAddLineEdit.setPlaceholderText(QCoreApplication.translate("settingsWidget", u"# of x value for spectrum sweep", None))
        self.numCPUsLineEdit.setText(QCoreApplication.translate("settingsWidget", u"1", None))
        self.label.setText(QCoreApplication.translate("settingsWidget", u"INITIAL STATE", None))
        self.label_44.setText(QCoreApplication.translate("settingsWidget", u"TRANSITIONS", None))
        self.label_5.setText(QCoreApplication.translate("settingsWidget", u"* For multiple initial-state indices: separate indices by \";\"", None))
        self.label_6.setText(QCoreApplication.translate("settingsWidget", u"HELP", None))
        self.label_33.setText(QCoreApplication.translate("settingsWidget", u"PHOTONS", None))
        self.label_4.setText(QCoreApplication.translate("settingsWidget", u"CORES TO USE", None))
        self.label_42.setText(QCoreApplication.translate("settingsWidget", u"EVALS COUNT", None))
        self.label_43.setText(QCoreApplication.translate("settingsWidget", u"POINTS ADDED", None))
        self.evalsCountLineEdit.setText(QCoreApplication.translate("settingsWidget", u"20", None))
        self.initStateLineEdit.setPlaceholderText(QCoreApplication.translate("settingsWidget", u"dressed or bare indices", None))
        self.numericalSpectrumSettingsHelpPushButton.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spectrumTab), QCoreApplication.translate("settingsWidget", u"SPECTRUM", None))
        self.tolLineEdit.setStyleSheet(QCoreApplication.translate("settingsWidget", u"font-size: 13px", None))
        self.tolLineEdit.setText(QCoreApplication.translate("settingsWidget", u"1e-6", None))
        self.label_47.setText(QCoreApplication.translate("settingsWidget", u"OPTIMIZER", None))
        self.optimizerComboBox.setItemText(0, QCoreApplication.translate("settingsWidget", u"L-BFGS-B", None))
        self.optimizerComboBox.setItemText(1, QCoreApplication.translate("settingsWidget", u"Nelder-Mead", None))
        self.optimizerComboBox.setItemText(2, QCoreApplication.translate("settingsWidget", u"Powell", None))
        self.optimizerComboBox.setItemText(3, QCoreApplication.translate("settingsWidget", u"shgo", None))
        self.optimizerComboBox.setItemText(4, QCoreApplication.translate("settingsWidget", u"differential evolution", None))

        self.optimizerComboBox.setStyleSheet(QCoreApplication.translate("settingsWidget", u"font-size: 13px", None))
        self.label_8.setText(QCoreApplication.translate("settingsWidget", u"TOLERANCE", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fitTab), QCoreApplication.translate("settingsWidget", u"FIT", None))
        self.settingsCloseButton.setText("")
    # retranslateUi

