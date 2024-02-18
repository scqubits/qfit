# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_window.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

from qfit.views.calibration import CalibrationLineEdit
from qfit.widgets.data_extracting import (DataExtractingWidget, ListView)
from qfit.widgets.mpl_canvas import (MplFigureCanvas, MplNavButtons)
from qfit.widgets.validated_line_edits import (IntLineEdit, IntTupleLineEdit, PositiveFloatLineEdit, StateLineEdit)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1276, 926)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setMaximumSize(QSize(16777215, 16777190))
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        font.setPointSize(13)
        font.setWeight(QFont.Light)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(u"qfit")
        icon = QIcon()
        icon.addFile(u":/icons/svg/qfit-icon.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"	background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QFrame {\n"
"	background-color: rgb(18, 18, 18);\n"
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
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
""
                        "    background: rgb(85, 170, 255);\n"
"    min-width: 20px;\n"
"	border-radius: 5px\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 10px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius:"
                        " 0px;\n"
" }\n"
"\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"	border-radius: 5px\n"
" }\n"
"\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox {\n"
"	color: #AAAAAA;\n"
"    spacing: 10px;\n"
"    font-size: 14px"
                        ";\n"
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
"/* SLIDERS "
                        "*/\n"
"QSlider::groove:horizontal {\n"
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
""
                        "\n"
"QSlider::handle:vertical:hover {\n"
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
"	font: 57 10pt \"Roboto Medium\";\n"
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
"}"
                        "\n"
"\n"
"QSpinBox::up-arrow {\n"
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
"/* COMBOBOX */\n"
"QComboBox {\n"
"	color: rgb(170, 170, 170);\n"
"	background-color: #2F2F2F;\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:hover{\n"
"	background-color: #2F2F2F;\n"
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
"QCo"
                        "mboBox::drop-down:button {\n"
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
"}\n"
"\n"
"/*\n"
"QHeaderView::section{\n"
"	Background-color: rgb(39, 44, 54);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"*/\n"
"\n"
"L"
                        "istView\n"
"{\n"
"	selection-background-color: rgb(93, 93, 93);\n"
"	background: rgb(63,63,63);\n"
"	color: rgb(220,220,220);\n"
"}\n"
"\n"
"ListView::item:hover {\n"
"	 background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, \n"
"                                              stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}\n"
"\n"
"ListView::item:selected {\n"
"	 background: rgb(110, 110, 110);\n"
"}\n"
"")
        MainWindow.setIconSize(QSize(30, 30))
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.windowBodyFrame = QFrame(self.centralWidget)
        self.windowBodyFrame.setObjectName(u"windowBodyFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.windowBodyFrame.sizePolicy().hasHeightForWidth())
        self.windowBodyFrame.setSizePolicy(sizePolicy1)
        self.windowBodyFrame.setMinimumSize(QSize(120, 0))
        self.windowBodyFrame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(33,33,33);\n"
"}")
        self.gridLayout = QGridLayout(self.windowBodyFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.bottomStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.bottomStackedWidget.setObjectName(u"bottomStackedWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.bottomStackedWidget.sizePolicy().hasHeightForWidth())
        self.bottomStackedWidget.setSizePolicy(sizePolicy2)
        self.bottomStackedWidget.setMinimumSize(QSize(0, 220))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        self.bottomStackedWidget.setFont(font1)
        self.bottomStackedWidget.setStyleSheet(u"")
        self.bottomStackedWidget.setFrameShape(QFrame.NoFrame)
        self.bottomStackedWidget.setFrameShadow(QFrame.Raised)
        self.calibrationPage = QWidget()
        self.calibrationPage.setObjectName(u"calibrationPage")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.calibrationPage.sizePolicy().hasHeightForWidth())
        self.calibrationPage.setSizePolicy(sizePolicy3)
        self.horizontalLayout_4 = QHBoxLayout(self.calibrationPage)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 12, 0, 0)
        self.frame_2 = QFrame(self.calibrationPage)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.frame_2.setLineWidth(0)
        self.gridLayout_4 = QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_9, 1, 0, 1, 1)

        self.calibratedCheckBox = QPushButton(self.frame_2)
        self.calibratedCheckBox.setObjectName(u"calibratedCheckBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.calibratedCheckBox.sizePolicy().hasHeightForWidth())
        self.calibratedCheckBox.setSizePolicy(sizePolicy4)
        self.calibratedCheckBox.setMinimumSize(QSize(200, 40))
        self.calibratedCheckBox.setMaximumSize(QSize(200, 40))
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setKerning(False)
        self.calibratedCheckBox.setFont(font2)
        self.calibratedCheckBox.setStyleSheet(u"QPushButton {\n"
"color: #DBBCFB;\n"
"background-color: transparent;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton::checked {\n"
"background-color: transparent;\n"
"}\n"
"\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/toggle-off.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u":/icons/svg/toggle-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.calibratedCheckBox.setIcon(icon1)
        self.calibratedCheckBox.setIconSize(QSize(60, 50))
        self.calibratedCheckBox.setCheckable(True)

        self.gridLayout_4.addWidget(self.calibratedCheckBox, 0, 0, 1, 1)


        self.horizontalLayout_4.addWidget(self.frame_2)

        self.bottomStackedWidget.addWidget(self.calibrationPage)
        self.datapointsPage = QWidget()
        self.datapointsPage.setObjectName(u"datapointsPage")
        sizePolicy3.setHeightForWidth(self.datapointsPage.sizePolicy().hasHeightForWidth())
        self.datapointsPage.setSizePolicy(sizePolicy3)
        self.datapointsPage.setLayoutDirection(Qt.LeftToRight)
        self.datapointsPage.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(self.datapointsPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.frame_8 = QFrame(self.datapointsPage)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy1.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy1)
        self.frame_8.setStyleSheet(u"QPushButton {\n"
"	color: rgb(170, 170, 170);\n"
"	text-align: left;\n"
"	border: none;\n"
"}")
        self.gridLayout_5 = QGridLayout(self.frame_8)
#ifndef Q_OS_MAC
        self.gridLayout_5.setSpacing(-1)
#endif
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(20, 0, 0, 0)
        self.verticalSpacer_7 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_7, 6, 3, 1, 1)

        self.colorGridWidget = QWidget(self.frame_8)
        self.colorGridWidget.setObjectName(u"colorGridWidget")
        sizePolicy2.setHeightForWidth(self.colorGridWidget.sizePolicy().hasHeightForWidth())
        self.colorGridWidget.setSizePolicy(sizePolicy2)
        self.colorGridWidget.setMinimumSize(QSize(0, 0))
        self.colorGridWidget.setMaximumSize(QSize(1000000, 16777215))
        self.gridLayout_9 = QGridLayout(self.colorGridWidget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setHorizontalSpacing(-1)
        self.gridLayout_9.setVerticalSpacing(15)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.colorGridWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_9.addWidget(self.label_3, 5, 1, 1, 1)

        self.rangeSliderMin = QSlider(self.colorGridWidget)
        self.rangeSliderMin.setObjectName(u"rangeSliderMin")
        self.rangeSliderMin.setMinimumSize(QSize(0, 18))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMin, 3, 0, 1, 1)

        self.logScaleCheckBox = QCheckBox(self.colorGridWidget)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        self.logScaleCheckBox.setFont(font1)
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText(u"Log")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout_9.addWidget(self.logScaleCheckBox, 2, 0, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_12, 2, 1, 1, 1)

        self.rangeSliderMax = QSlider(self.colorGridWidget)
        self.rangeSliderMax.setObjectName(u"rangeSliderMax")
        self.rangeSliderMax.setMinimumSize(QSize(0, 18))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMax, 5, 0, 1, 1)

        self.label_2 = QLabel(self.colorGridWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_9.addWidget(self.label_2, 3, 1, 1, 1)

        self.colorComboBox = QComboBox(self.colorGridWidget)
        icon2 = QIcon()
        icon2.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon2, u"PuOr")
        icon3 = QIcon()
        icon3.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon3, u"RdYlBu")
        icon4 = QIcon()
        icon4.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon4, u"bwr")
        icon5 = QIcon()
        icon5.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon5, u"viridis")
        icon6 = QIcon()
        icon6.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon6, u"cividis")
        icon7 = QIcon()
        icon7.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon7, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy5)
        self.colorComboBox.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(150, 20))
        self.colorComboBox.setFrame(False)

        self.gridLayout_9.addWidget(self.colorComboBox, 1, 0, 1, 2)


        self.gridLayout_5.addWidget(self.colorGridWidget, 3, 0, 1, 1)

        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setMinimumSize(QSize(0, 23))
        font3 = QFont()
        font3.setFamilies([u"Roboto Medium"])
        font3.setWeight(QFont.Light)
        self.label_4.setFont(font3)
        self.label_4.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size:16px;")
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_4.setMargin(0)
        self.label_4.setIndent(0)

        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.frame_8)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy6)
        self.widget_2.setMinimumSize(QSize(300, 0))
        self.widget_2.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.widget_2)
#ifndef Q_OS_MAC
        self.verticalLayout_5.setSpacing(-1)
#endif
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bgndSubtractQFrame = QFrame(self.widget_2)
        self.bgndSubtractQFrame.setObjectName(u"bgndSubtractQFrame")
        sizePolicy2.setHeightForWidth(self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth())
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy2)
        self.bgndSubtractQFrame.setMinimumSize(QSize(330, 0))
        self.bgndSubtractQFrame.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout_7 = QVBoxLayout(self.bgndSubtractQFrame)
        self.verticalLayout_7.setSpacing(15)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        sizePolicy4.setHeightForWidth(self.bgndSubtractXCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractXCheckBox.setSizePolicy(sizePolicy4)
        self.bgndSubtractXCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip(u"Background subtraction along X")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setText(u"Along X axis")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.verticalLayout_7.addWidget(self.bgndSubtractXCheckBox)

        self.bgndSubtractYCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractYCheckBox.setObjectName(u"bgndSubtractYCheckBox")
        sizePolicy4.setHeightForWidth(self.bgndSubtractYCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractYCheckBox.setSizePolicy(sizePolicy4)
        self.bgndSubtractYCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText(u"Along Y axis")
        self.bgndSubtractYCheckBox.setTristate(False)

        self.verticalLayout_7.addWidget(self.bgndSubtractYCheckBox)


        self.verticalLayout_5.addWidget(self.bgndSubtractQFrame)

        self.label_39 = QLabel(self.widget_2)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setStyleSheet(u"font-size: 13px")

        self.verticalLayout_5.addWidget(self.label_39)

        self.filterQFrame = QFrame(self.widget_2)
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
        self.waveletCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.waveletCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.waveletCheckBox.setText(u"Denoise")

        self.verticalLayout_12.addWidget(self.waveletCheckBox)

        self.edgeFilterCheckBox = QCheckBox(self.filterQFrame)
        self.edgeFilterCheckBox.setObjectName(u"edgeFilterCheckBox")
        self.edgeFilterCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setText(u"Edge")

        self.verticalLayout_12.addWidget(self.edgeFilterCheckBox)

        self.topHatCheckBox = QCheckBox(self.filterQFrame)
        self.topHatCheckBox.setObjectName(u"topHatCheckBox")
        self.topHatCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.topHatCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.topHatCheckBox.setText(u"Top-hat")

        self.verticalLayout_12.addWidget(self.topHatCheckBox)


        self.verticalLayout_5.addWidget(self.filterQFrame)


        self.gridLayout_5.addWidget(self.widget_2, 3, 4, 3, 1)

        self.horizontalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_13, 5, 5, 1, 1)

        self.label_38 = QLabel(self.frame_8)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setStyleSheet(u"font-size: 13px")

        self.gridLayout_5.addWidget(self.label_38, 2, 4, 1, 1)

        self.widget = QWidget(self.frame_8)
        self.widget.setObjectName(u"widget")
        sizePolicy6.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy6)
        self.widget.setMinimumSize(QSize(300, 0))
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_5.addWidget(self.widget, 5, 0, 1, 1)

        self.label_40 = QLabel(self.frame_8)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setStyleSheet(u"font-size: 13px")

        self.gridLayout_5.addWidget(self.label_40, 2, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame_8)

        self.bottomStackedWidget.addWidget(self.datapointsPage)
        self.prefitPage = QWidget()
        self.prefitPage.setObjectName(u"prefitPage")
        sizePolicy3.setHeightForWidth(self.prefitPage.sizePolicy().hasHeightForWidth())
        self.prefitPage.setSizePolicy(sizePolicy3)
        self.horizontalLayout_9 = QHBoxLayout(self.prefitPage)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 12, 0, 0)
        self.frame_4 = QFrame(self.prefitPage)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(-1)
        self.gridLayout_3.setContentsMargins(20, 0, 20, 0)
        self.mseLabel = QLabel(self.frame_4)
        self.mseLabel.setObjectName(u"mseLabel")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.mseLabel.sizePolicy().hasHeightForWidth())
        self.mseLabel.setSizePolicy(sizePolicy7)
        self.mseLabel.setMinimumSize(QSize(200, 0))
        font4 = QFont()
        font4.setFamilies([u"Roboto Medium"])
        font4.setBold(True)
        self.mseLabel.setFont(font4)
        self.mseLabel.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.mseLabel, 3, 6, 1, 1)

        self.pointsAddLineEdit = IntLineEdit(self.frame_4)
        self.pointsAddLineEdit.setObjectName(u"pointsAddLineEdit")
        sizePolicy4.setHeightForWidth(self.pointsAddLineEdit.sizePolicy().hasHeightForWidth())
        self.pointsAddLineEdit.setSizePolicy(sizePolicy4)
        self.pointsAddLineEdit.setMinimumSize(QSize(170, 30))
        self.pointsAddLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_3.addWidget(self.pointsAddLineEdit, 6, 2, 1, 1)

        self.label_44 = QLabel(self.frame_4)
        self.label_44.setObjectName(u"label_44")
        sizePolicy7.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy7)
        self.label_44.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.label_44, 3, 0, 1, 1)

        self.label_43 = QLabel(self.frame_4)
        self.label_43.setObjectName(u"label_43")
        sizePolicy7.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy7)
        self.label_43.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.label_43, 6, 0, 1, 1)

        self.prefitResultHelpPushButton = QPushButton(self.frame_4)
        self.prefitResultHelpPushButton.setObjectName(u"prefitResultHelpPushButton")
        sizePolicy1.setHeightForWidth(self.prefitResultHelpPushButton.sizePolicy().hasHeightForWidth())
        self.prefitResultHelpPushButton.setSizePolicy(sizePolicy1)
        self.prefitResultHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icons/svg/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.prefitResultHelpPushButton.setIcon(icon8)
        self.prefitResultHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout_3.addWidget(self.prefitResultHelpPushButton, 3, 7, 1, 1)

        self.horizontalSpacer_32 = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_32, 3, 4, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 3, 10, 1, 1)

        self.label_33 = QLabel(self.frame_4)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.label_33, 7, 0, 1, 1)

        self.numericalSpectrumSettingsTitleWidget = QWidget(self.frame_4)
        self.numericalSpectrumSettingsTitleWidget.setObjectName(u"numericalSpectrumSettingsTitleWidget")
        self.horizontalLayout_6 = QHBoxLayout(self.numericalSpectrumSettingsTitleWidget)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 16, 0)
        self.numericalSpectrumSettingsLabel = QLabel(self.numericalSpectrumSettingsTitleWidget)
        self.numericalSpectrumSettingsLabel.setObjectName(u"numericalSpectrumSettingsLabel")
        sizePolicy5.setHeightForWidth(self.numericalSpectrumSettingsLabel.sizePolicy().hasHeightForWidth())
        self.numericalSpectrumSettingsLabel.setSizePolicy(sizePolicy5)
        font5 = QFont()
        font5.setFamilies([u"Roboto Medium"])
        font5.setWeight(QFont.Light)
        font5.setItalic(False)
        self.numericalSpectrumSettingsLabel.setFont(font5)
        self.numericalSpectrumSettingsLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size: 16px;")
        self.numericalSpectrumSettingsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.numericalSpectrumSettingsLabel)

        self.numericalSpectrumSettingsHelpPushButton = QPushButton(self.numericalSpectrumSettingsTitleWidget)
        self.numericalSpectrumSettingsHelpPushButton.setObjectName(u"numericalSpectrumSettingsHelpPushButton")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.numericalSpectrumSettingsHelpPushButton.sizePolicy().hasHeightForWidth())
        self.numericalSpectrumSettingsHelpPushButton.setSizePolicy(sizePolicy8)
        self.numericalSpectrumSettingsHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.numericalSpectrumSettingsHelpPushButton.setIcon(icon8)
        self.numericalSpectrumSettingsHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_6.addWidget(self.numericalSpectrumSettingsHelpPushButton)


        self.gridLayout_3.addWidget(self.numericalSpectrumSettingsTitleWidget, 0, 0, 1, 5)

        self.label_42 = QLabel(self.frame_4)
        self.label_42.setObjectName(u"label_42")
        sizePolicy7.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy7)
        self.label_42.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.label_42, 5, 0, 1, 1)

        self.subsysComboBox = QComboBox(self.frame_4)
        self.subsysComboBox.setObjectName(u"subsysComboBox")
        sizePolicy4.setHeightForWidth(self.subsysComboBox.sizePolicy().hasHeightForWidth())
        self.subsysComboBox.setSizePolicy(sizePolicy4)
        self.subsysComboBox.setMinimumSize(QSize(170, 30))
        self.subsysComboBox.setMaximumSize(QSize(16777215, 30))
        self.subsysComboBox.setStyleSheet(u"")
        self.subsysComboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.gridLayout_3.addWidget(self.subsysComboBox, 3, 2, 1, 2)

        self.initStateLineEdit = StateLineEdit(self.frame_4)
        self.initStateLineEdit.setObjectName(u"initStateLineEdit")
        sizePolicy4.setHeightForWidth(self.initStateLineEdit.sizePolicy().hasHeightForWidth())
        self.initStateLineEdit.setSizePolicy(sizePolicy4)
        self.initStateLineEdit.setMinimumSize(QSize(170, 30))
        self.initStateLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_3.addWidget(self.initStateLineEdit, 4, 2, 1, 1)

        self.evalsCountLineEdit = IntLineEdit(self.frame_4)
        self.evalsCountLineEdit.setObjectName(u"evalsCountLineEdit")
        sizePolicy4.setHeightForWidth(self.evalsCountLineEdit.sizePolicy().hasHeightForWidth())
        self.evalsCountLineEdit.setSizePolicy(sizePolicy4)
        self.evalsCountLineEdit.setMinimumSize(QSize(170, 30))
        self.evalsCountLineEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_3.addWidget(self.evalsCountLineEdit, 5, 2, 1, 2)

        self.label_46 = QLabel(self.frame_4)
        self.label_46.setObjectName(u"label_46")
        sizePolicy9 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy9)
        self.label_46.setMaximumSize(QSize(200, 16777215))
        self.label_46.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.label_46, 4, 6, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 8, 0, 1, 1)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        sizePolicy7.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy7)
        self.label.setStyleSheet(u"font-size: 13px")

        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 1)

        self.horizontalSpacer_33 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_33, 5, 1, 1, 1)

        self.prefitPhotonSpinBox = QSpinBox(self.frame_4)
        self.prefitPhotonSpinBox.setObjectName(u"prefitPhotonSpinBox")
        sizePolicy4.setHeightForWidth(self.prefitPhotonSpinBox.sizePolicy().hasHeightForWidth())
        self.prefitPhotonSpinBox.setSizePolicy(sizePolicy4)
        self.prefitPhotonSpinBox.setMinimumSize(QSize(96, 35))
        self.prefitPhotonSpinBox.setStyleSheet(u"QSpinBox {\n"
"    color: #FFFFFF;\n"
"    background-color: #212121;\n"
"	height: 28px;\n"
"    width: 28px; \n"
"    background-image: url(:/images/spin_box_bg.svg) 1;\n"
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
"	background-color: #2F2F2F;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: left; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px;\n"
"	background-color: #2F2F2F;\n"
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
"    width"
                        ": 20px;\n"
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

        self.gridLayout_3.addWidget(self.prefitPhotonSpinBox, 7, 2, 1, 1)

        self.statusTextLabel = QLabel(self.frame_4)
        self.statusTextLabel.setObjectName(u"statusTextLabel")
        self.statusTextLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel.setWordWrap(True)
        self.statusTextLabel.setMargin(5)

        self.gridLayout_3.addWidget(self.statusTextLabel, 5, 6, 1, 5)


        self.horizontalLayout_9.addWidget(self.frame_4)

        self.bottomStackedWidget.addWidget(self.prefitPage)
        self.fitPage = QWidget()
        self.fitPage.setObjectName(u"fitPage")
        sizePolicy3.setHeightForWidth(self.fitPage.sizePolicy().hasHeightForWidth())
        self.fitPage.setSizePolicy(sizePolicy3)
        self.horizontalLayout_10 = QHBoxLayout(self.fitPage)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, -1, 0, 0)
        self.frame_5 = QFrame(self.fitPage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy1.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy1)
        self.frame_5.setFont(font3)
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(0)
        self.gridLayout_6.setVerticalSpacing(-1)
        self.gridLayout_6.setContentsMargins(20, 0, 20, 0)
        self.verticalSpacer_10 = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_6.addItem(self.verticalSpacer_10, 3, 0, 1, 1)

        self.mseLabel_2 = QLabel(self.frame_5)
        self.mseLabel_2.setObjectName(u"mseLabel_2")
        sizePolicy4.setHeightForWidth(self.mseLabel_2.sizePolicy().hasHeightForWidth())
        self.mseLabel_2.setSizePolicy(sizePolicy4)
        self.mseLabel_2.setMinimumSize(QSize(200, 0))
        self.mseLabel_2.setMaximumSize(QSize(200, 16777215))
        self.mseLabel_2.setFont(font4)
        self.mseLabel_2.setStyleSheet(u"font-size: 13px")

        self.gridLayout_6.addWidget(self.mseLabel_2, 1, 7, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        sizePolicy7.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy7)
        self.label_8.setMinimumSize(QSize(0, 0))
        self.label_8.setStyleSheet(u"font-size: 13px")

        self.gridLayout_6.addWidget(self.label_8, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(60, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_7, 1, 5, 1, 1)

        self.tolLineEdit = PositiveFloatLineEdit(self.frame_5)
        self.tolLineEdit.setObjectName(u"tolLineEdit")
        sizePolicy4.setHeightForWidth(self.tolLineEdit.sizePolicy().hasHeightForWidth())
        self.tolLineEdit.setSizePolicy(sizePolicy4)
        self.tolLineEdit.setMinimumSize(QSize(170, 30))
        self.tolLineEdit.setMaximumSize(QSize(16777215, 28))

        self.gridLayout_6.addWidget(self.tolLineEdit, 2, 2, 1, 1)

        self.label_47 = QLabel(self.frame_5)
        self.label_47.setObjectName(u"label_47")
        sizePolicy7.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy7)
        self.label_47.setStyleSheet(u"font-size: 13px")

        self.gridLayout_6.addWidget(self.label_47, 1, 0, 1, 1)

        self.label_45 = QLabel(self.frame_5)
        self.label_45.setObjectName(u"label_45")
        sizePolicy5.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy5)
        self.label_45.setMinimumSize(QSize(0, 23))
        self.label_45.setFont(font5)
        self.label_45.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size: 16px;")
        self.label_45.setIndent(-1)

        self.gridLayout_6.addWidget(self.label_45, 0, 0, 1, 3)

        self.label_49 = QLabel(self.frame_5)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setStyleSheet(u"font-size: 13px")

        self.gridLayout_6.addWidget(self.label_49, 4, 0, 1, 1)

        self.optimizerComboBox = QComboBox(self.frame_5)
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.setObjectName(u"optimizerComboBox")
        sizePolicy4.setHeightForWidth(self.optimizerComboBox.sizePolicy().hasHeightForWidth())
        self.optimizerComboBox.setSizePolicy(sizePolicy4)
        self.optimizerComboBox.setMinimumSize(QSize(170, 30))
        self.optimizerComboBox.setMaximumSize(QSize(16777213, 28))

        self.gridLayout_6.addWidget(self.optimizerComboBox, 1, 2, 1, 1)

        self.fitResultHelpPushButton = QPushButton(self.frame_5)
        self.fitResultHelpPushButton.setObjectName(u"fitResultHelpPushButton")
        self.fitResultHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.fitResultHelpPushButton.setIcon(icon8)
        self.fitResultHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout_6.addWidget(self.fitResultHelpPushButton, 1, 8, 1, 1)

        self.horizontalSpacer_34 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_34, 1, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_9, 1, 9, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.statusTextLabel_2 = QLabel(self.frame_5)
        self.statusTextLabel_2.setObjectName(u"statusTextLabel_2")
        sizePolicy3.setHeightForWidth(self.statusTextLabel_2.sizePolicy().hasHeightForWidth())
        self.statusTextLabel_2.setSizePolicy(sizePolicy3)
        self.statusTextLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel_2.setWordWrap(True)
        self.statusTextLabel_2.setMargin(5)

        self.gridLayout_6.addWidget(self.statusTextLabel_2, 5, 0, 1, 10)


        self.horizontalLayout_10.addWidget(self.frame_5)

        self.bottomStackedWidget.addWidget(self.fitPage)

        self.gridLayout.addWidget(self.bottomStackedWidget, 2, 3, 1, 1)

        self.menu_frame = QFrame(self.windowBodyFrame)
        self.menu_frame.setObjectName(u"menu_frame")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy10)
        self.menu_frame.setMinimumSize(QSize(190, 0))
        self.menu_frame.setMaximumSize(QSize(190, 16777215))
        self.menu_frame.setStyleSheet(u"QFrame {\n"
"	color: white;\n"
"	background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"\n"
"QPushButton:checked {	\n"
"	color: rgb(190, 130, 250);\n"
"}")
        self.menu_frame.setFrameShape(QFrame.NoFrame)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.menu_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(37, 0, 20, 0)
        self.modeFitButton = QPushButton(self.menu_frame)
        self.modeFitButton.setObjectName(u"modeFitButton")
        self.modeFitButton.setMinimumSize(QSize(120, 70))
        self.modeFitButton.setMaximumSize(QSize(120, 70))
        self.modeFitButton.setFont(font3)
        self.modeFitButton.setStyleSheet(u"font-size: 16px;")
        icon9 = QIcon()
        icon9.addFile(u":/icons/svg/cil-speedometer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeFitButton.setIcon(icon9)
        self.modeFitButton.setIconSize(QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeFitButton, 5, 0, 1, 1)

        self.modeTagButton = QPushButton(self.menu_frame)
        self.modeTagButton.setObjectName(u"modeTagButton")
        self.modeTagButton.setMinimumSize(QSize(120, 70))
        self.modeTagButton.setMaximumSize(QSize(120, 70))
        self.modeTagButton.setFont(font3)
        self.modeTagButton.setStyleSheet(u"font-size: 16px;")
        icon10 = QIcon()
        icon10.addFile(u":/icons/svg/cil-location-pin.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeTagButton.setIcon(icon10)
        self.modeTagButton.setIconSize(QSize(24, 24))
        self.modeTagButton.setCheckable(True)
        self.modeTagButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeTagButton, 3, 0, 1, 2)

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_14, 0, 0, 1, 1)

        self.modeSelectButton = QPushButton(self.menu_frame)
        self.modeSelectButton.setObjectName(u"modeSelectButton")
        self.modeSelectButton.setMinimumSize(QSize(120, 70))
        self.modeSelectButton.setMaximumSize(QSize(120, 70))
        self.modeSelectButton.setFont(font3)
        self.modeSelectButton.setStyleSheet(u"font-size: 16px;")
        icon11 = QIcon()
        icon11.addFile(u":/icons/svg/cil-list.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeSelectButton.setIcon(icon11)
        self.modeSelectButton.setIconSize(QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setChecked(True)
        self.modeSelectButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeSelectButton, 2, 0, 1, 2)

        self.toggleMenuButton = QPushButton(self.menu_frame)
        self.toggleMenuButton.setObjectName(u"toggleMenuButton")
        sizePolicy1.setHeightForWidth(self.toggleMenuButton.sizePolicy().hasHeightForWidth())
        self.toggleMenuButton.setSizePolicy(sizePolicy1)
        self.toggleMenuButton.setMinimumSize(QSize(0, 0))
        self.toggleMenuButton.setMaximumSize(QSize(16777215, 16777215))
        self.toggleMenuButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleMenuButton.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u":/icons/svg/cil-menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleMenuButton.setIcon(icon12)
        self.toggleMenuButton.setIconSize(QSize(24, 24))
        self.toggleMenuButton.setAutoDefault(False)
        self.toggleMenuButton.setFlat(False)

        self.gridLayout_2.addWidget(self.toggleMenuButton, 1, 0, 1, 2)

        self.modePrefitButton = QPushButton(self.menu_frame)
        self.modePrefitButton.setObjectName(u"modePrefitButton")
        self.modePrefitButton.setMinimumSize(QSize(120, 70))
        self.modePrefitButton.setMaximumSize(QSize(120, 70))
        self.modePrefitButton.setFont(font3)
        self.modePrefitButton.setStyleSheet(u"font-size: 16px;")
        icon13 = QIcon()
        icon13.addFile(u":/icons/svg/cil-chart-line.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modePrefitButton.setIcon(icon13)
        self.modePrefitButton.setIconSize(QSize(24, 24))
        self.modePrefitButton.setCheckable(True)
        self.modePrefitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modePrefitButton, 4, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 6, 1, 1, 1)


        self.gridLayout.addWidget(self.menu_frame, 0, 0, 4, 1)

        self.mplFigureCanvas = MplFigureCanvas(self.windowBodyFrame)
        self.mplFigureCanvas.setObjectName(u"mplFigureCanvas")
        sizePolicy.setHeightForWidth(self.mplFigureCanvas.sizePolicy().hasHeightForWidth())
        self.mplFigureCanvas.setSizePolicy(sizePolicy)
        self.mplFigureCanvas.setMinimumSize(QSize(550, 300))
        self.mplFigureCanvas.setMaximumSize(QSize(16777215, 16777215))
        self.mplFigureCanvas.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"\n"
"QToolTip {\n"
"	color: #1e1e1e;\n"
"	background-color: rgba(255, 255, 255, 160);\n"
"	border: 1px solid rgb(200, 200, 200);\n"
"	border-radius: 2px;\n"
"}\n"
"")
        self.mplFigureCanvas.setLineWidth(0)
        self.mplFigureButtons = MplNavButtons(self.mplFigureCanvas)
        self.mplFigureButtons.setObjectName(u"mplFigureButtons")
        self.mplFigureButtons.setGeometry(QRect(0, 0, 621, 60))
        self.mplFigureButtons.setAutoFillBackground(False)
        self.mplFigureButtons.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QToolTip {\n"
"	color: #1e1e1e;\n"
"	background-color: rgba(255, 255, 255, 160);\n"
"	border: 1px solid rgb(200, 200, 200);\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:checked {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"color: rgb(30, 30, 30);")
        self.resetViewButton = QPushButton(self.mplFigureButtons)
        self.resetViewButton.setObjectName(u"resetViewButton")
        self.resetViewButton.setGeometry(QRect(30, 10, 40, 40))
#if QT_CONFIG(tooltip)
        self.resetViewButton.setToolTip(u"Reset plot area")
#endif // QT_CONFIG(tooltip)
        icon14 = QIcon()
        icon14.addFile(u":/icons/svg/cil-reload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon14)
        self.resetViewButton.setIconSize(QSize(18, 18))
        self.panViewButton = QPushButton(self.mplFigureButtons)
        self.panViewButton.setObjectName(u"panViewButton")
        self.panViewButton.setGeometry(QRect(100, 10, 40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip(u"Pan mode: Drag to move the canvas")
#endif // QT_CONFIG(tooltip)
        icon15 = QIcon()
        icon15.addFile(u":/icons/svg/cil-move.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.panViewButton.setIcon(icon15)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.zoomViewButton = QPushButton(self.mplFigureButtons)
        self.zoomViewButton.setObjectName(u"zoomViewButton")
        self.zoomViewButton.setGeometry(QRect(155, 10, 40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip(u"Zoom mode: Drag to magnify a region")
#endif // QT_CONFIG(tooltip)
        icon16 = QIcon()
        icon16.addFile(u":/icons/svg/cil-zoom.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomViewButton.setIcon(icon16)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.horizontalSnapButton = QPushButton(self.mplFigureButtons)
        self.horizontalSnapButton.setObjectName(u"horizontalSnapButton")
        self.horizontalSnapButton.setGeometry(QRect(280, 10, 40, 40))
#if QT_CONFIG(tooltip)
        self.horizontalSnapButton.setToolTip(u"Dataset snapping: align the x-coordinates for datasets")
#endif // QT_CONFIG(tooltip)
        icon17 = QIcon()
        icon17.addFile(u":/icons/svg/cil-lock-unlocked.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon17.addFile(u":/icons/svg/cil-lock-locked.svg", QSize(), QIcon.Normal, QIcon.On)
        self.horizontalSnapButton.setIcon(icon17)
        self.horizontalSnapButton.setCheckable(True)
        self.horizontalSnapButton.setChecked(True)
        self.horizontalSnapButton.setAutoExclusive(False)
        self.selectViewButton = QPushButton(self.mplFigureButtons)
        self.selectViewButton.setObjectName(u"selectViewButton")
        self.selectViewButton.setGeometry(QRect(210, 10, 40, 40))
        self.selectViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.selectViewButton.setToolTip(u"Extract mode: Click to extract peaks")
#endif // QT_CONFIG(tooltip)
        self.selectViewButton.setIcon(icon10)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.verticalSnapButton = QPushButton(self.mplFigureButtons)
        self.verticalSnapButton.setObjectName(u"verticalSnapButton")
        self.verticalSnapButton.setGeometry(QRect(335, 10, 40, 40))
#if QT_CONFIG(tooltip)
        self.verticalSnapButton.setToolTip(u"Peak snapping: Locate the nearby peak along y axis")
#endif // QT_CONFIG(tooltip)
        icon18 = QIcon()
        icon18.addFile(u":/icons/svg/cil-vertical-align-center.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.verticalSnapButton.setIcon(icon18)
        self.verticalSnapButton.setCheckable(True)
        self.verticalSnapButton.setChecked(True)
        self.verticalSnapButton.setAutoExclusive(False)
        self.line_2 = QFrame(self.mplFigureCanvas)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(263, 10, 3, 41))
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(0)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_3 = QFrame(self.mplFigureCanvas)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(83, 10, 3, 41))
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setLineWidth(0)
        self.line_3.setFrameShape(QFrame.VLine)
        self.label_9 = QLabel(self.mplFigureCanvas)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(30, 50, 41, 20))
        font6 = QFont()
        font6.setFamilies([u"Roboto Medium"])
        font6.setBold(False)
        self.label_9.setFont(font6)
        self.label_9.setStyleSheet(u"color: #5d5d5d; background-color: transparent;")
        self.label_9.setAlignment(Qt.AlignCenter)
        self.label_27 = QLabel(self.mplFigureCanvas)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(105, 50, 31, 20))
        self.label_27.setStyleSheet(u"color: #5d5d5d; background-color: transparent;")
        self.label_27.setAlignment(Qt.AlignCenter)
        self.label_34 = QLabel(self.mplFigureCanvas)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(155, 50, 41, 20))
        self.label_34.setStyleSheet(u"color: #5d5d5d; background-color: transparent;")
        self.label_34.setAlignment(Qt.AlignCenter)
        self.label_35 = QLabel(self.mplFigureCanvas)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setGeometry(QRect(210, 50, 41, 20))
        self.label_35.setStyleSheet(u"color: #5d5d5d; background-color: transparent;")
        self.label_35.setAlignment(Qt.AlignCenter)
        self.label_36 = QLabel(self.mplFigureCanvas)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setGeometry(QRect(277, 50, 51, 20))
        self.label_36.setStyleSheet(u"color: #5d5d5d; background-color: transparent;")
        self.label_36.setAlignment(Qt.AlignCenter)
        self.label_37 = QLabel(self.mplFigureCanvas)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setGeometry(QRect(331, 50, 51, 20))
        self.label_37.setFont(font1)
        self.label_37.setStyleSheet(u"color: #5d5d5d; background-color: transparent;")
        self.label_37.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.mplFigureCanvas, 0, 2, 1, 2)

        self.pagesStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.pagesStackedWidget.setObjectName(u"pagesStackedWidget")
        sizePolicy4.setHeightForWidth(self.pagesStackedWidget.sizePolicy().hasHeightForWidth())
        self.pagesStackedWidget.setSizePolicy(sizePolicy4)
        self.pagesStackedWidget.setMinimumSize(QSize(410, 0))
        self.pagesStackedWidget.setMaximumSize(QSize(410, 10000))
        font7 = QFont()
        font7.setFamilies([u"Roboto Medium"])
        font7.setPointSize(9)
        font7.setKerning(True)
        self.pagesStackedWidget.setFont(font7)
        self.pagesStackedWidget.setStyleSheet(u"")
        self.pagesStackedWidget.setFrameShadow(QFrame.Raised)
        self.extractPointsWidget = DataExtractingWidget()
        self.extractPointsWidget.setObjectName(u"extractPointsWidget")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.extractPointsWidget.sizePolicy().hasHeightForWidth())
        self.extractPointsWidget.setSizePolicy(sizePolicy11)
        self.verticalLayout_9 = QVBoxLayout(self.extractPointsWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame = QFrame(self.extractPointsWidget)
        self.frame.setObjectName(u"frame")
        sizePolicy12 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy12)
        self.frame.setMinimumSize(QSize(0, 0))
        self.frame.setFont(font1)
        self.frame.setCursor(QCursor(Qt.ArrowCursor))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_17 = QVBoxLayout(self.frame)
        self.verticalLayout_17.setSpacing(5)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(5, 20, 0, 0)
        self.widget_3 = QWidget(self.frame)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")
        sizePolicy8.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy8)
        self.label_5.setMinimumSize(QSize(0, 23))
        self.label_5.setFont(font3)
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-family: \"Roboto Medium\";\n"
"    font-size: 16px;\n"
"    color: rgb(190, 130, 250);\n"
"}")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.calibrationHelpPushButton = QPushButton(self.widget_3)
        self.calibrationHelpPushButton.setObjectName(u"calibrationHelpPushButton")
        self.calibrationHelpPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.calibrationHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.calibrationHelpPushButton.setIcon(icon8)
        self.calibrationHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_7.addWidget(self.calibrationHelpPushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout_17.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.frame)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_4)
#ifndef Q_OS_MAC
        self.horizontalLayout_11.setSpacing(-1)
#endif
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(12, -1, -1, -1)
        self.label_13 = QLabel(self.widget_4)
        self.label_13.setObjectName(u"label_13")
        sizePolicy7.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy7)
        self.label_13.setMinimumSize(QSize(42, 0))
        self.label_13.setFont(font1)
        self.label_13.setStyleSheet(u"font-size: 13px;")
        self.label_13.setText(u"Z")
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_13)

        self.zComboBox = QComboBox(self.widget_4)
        self.zComboBox.setObjectName(u"zComboBox")
        sizePolicy4.setHeightForWidth(self.zComboBox.sizePolicy().hasHeightForWidth())
        self.zComboBox.setSizePolicy(sizePolicy4)
        self.zComboBox.setMinimumSize(QSize(300, 30))
        self.zComboBox.setMaximumSize(QSize(300, 30))
        self.zComboBox.setAutoFillBackground(False)
        self.zComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.zComboBox.setFrame(True)

        self.horizontalLayout_11.addWidget(self.zComboBox)


        self.verticalLayout_17.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.frame)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy1.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy1)
        self.horizontalLayout_12 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_12 = QLabel(self.widget_5)
        self.label_12.setObjectName(u"label_12")
        sizePolicy7.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy7)
        self.label_12.setStyleSheet(u"font-size: 13px;")
        self.label_12.setText(u"AXIS X")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_12)

        self.xComboBox = QComboBox(self.widget_5)
        self.xComboBox.setObjectName(u"xComboBox")
        sizePolicy4.setHeightForWidth(self.xComboBox.sizePolicy().hasHeightForWidth())
        self.xComboBox.setSizePolicy(sizePolicy4)
        self.xComboBox.setMinimumSize(QSize(300, 30))
        self.xComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")

        self.horizontalLayout_12.addWidget(self.xComboBox)


        self.verticalLayout_17.addWidget(self.widget_5)

        self.calibrateXGridFrame = QFrame(self.frame)
        self.calibrateXGridFrame.setObjectName(u"calibrateXGridFrame")
        sizePolicy4.setHeightForWidth(self.calibrateXGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateXGridFrame.setSizePolicy(sizePolicy4)
        self.calibrateXGridFrame.setMinimumSize(QSize(363, 100))
        self.calibrateXGridFrame.setMaximumSize(QSize(363, 16777215))
        self.calibrateXGridFrame.setStyleSheet(u"QPushButton {\n"
"	background-color: #4B4B4B;\n"
"	border-radius: 5px;	\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #363636;\n"
"    icon: url(:/icons/svg/target-pressed.svg)\n"
"}")
        self.gridLayout_10 = QGridLayout(self.calibrateXGridFrame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(0)
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 12)
        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX1LineEdit.setObjectName(u"mapX1LineEdit")
        sizePolicy4.setHeightForWidth(self.mapX1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX1LineEdit.setSizePolicy(sizePolicy4)
        self.mapX1LineEdit.setMinimumSize(QSize(120, 30))
        self.mapX1LineEdit.setMaximumSize(QSize(120, 30))
#if QT_CONFIG(tooltip)
        self.mapX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.mapX1LineEdit, 1, 7, 1, 1)

        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX2LineEdit.setObjectName(u"rawX2LineEdit")
        sizePolicy4.setHeightForWidth(self.rawX2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX2LineEdit.setSizePolicy(sizePolicy4)
        self.rawX2LineEdit.setMinimumSize(QSize(120, 30))
        self.rawX2LineEdit.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.rawX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.rawX2LineEdit, 2, 4, 1, 1)

        self.calibrateX2Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX2Button.setObjectName(u"calibrateX2Button")
        sizePolicy4.setHeightForWidth(self.calibrateX2Button.sizePolicy().hasHeightForWidth())
        self.calibrateX2Button.setSizePolicy(sizePolicy4)
        self.calibrateX2Button.setMinimumSize(QSize(28, 28))
        self.calibrateX2Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateX2Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX2Button.setStyleSheet(u"")
        icon19 = QIcon()
        icon19.addFile(u":/icons/svg/target.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrateX2Button.setIcon(icon19)
        self.calibrateX2Button.setCheckable(True)
        self.calibrateX2Button.setChecked(False)

        self.gridLayout_10.addWidget(self.calibrateX2Button, 2, 1, 1, 1)

        self.label_15 = QLabel(self.calibrateXGridFrame)
        self.label_15.setObjectName(u"label_15")
        sizePolicy6.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy6)
        self.label_15.setFont(font1)
        self.label_15.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_15, 1, 2, 1, 1)

        self.horizontalSpacer_29 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_29, 1, 0, 1, 1)

        self.calibrateX1Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX1Button.setObjectName(u"calibrateX1Button")
        sizePolicy4.setHeightForWidth(self.calibrateX1Button.sizePolicy().hasHeightForWidth())
        self.calibrateX1Button.setSizePolicy(sizePolicy4)
        self.calibrateX1Button.setMinimumSize(QSize(28, 28))
        self.calibrateX1Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateX1Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX1Button.setStyleSheet(u"")
        self.calibrateX1Button.setIcon(icon19)
        self.calibrateX1Button.setCheckable(True)
        self.calibrateX1Button.setChecked(False)

        self.gridLayout_10.addWidget(self.calibrateX1Button, 1, 1, 1, 1)

        self.horizontalSpacer_20 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_20, 1, 3, 1, 1)

        self.horizontalSpacer_19 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_19, 1, 6, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_17, 1, 8, 1, 1)

        self.label_16 = QLabel(self.calibrateXGridFrame)
        self.label_16.setObjectName(u"label_16")
        sizePolicy6.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy6)
        self.label_16.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_16, 2, 2, 1, 1)

        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX2LineEdit.setObjectName(u"mapX2LineEdit")
        sizePolicy4.setHeightForWidth(self.mapX2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX2LineEdit.setSizePolicy(sizePolicy4)
        self.mapX2LineEdit.setMinimumSize(QSize(120, 30))
        self.mapX2LineEdit.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.mapX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.mapX2LineEdit, 2, 7, 1, 1)

        self.label_11 = QLabel(self.calibrateXGridFrame)
        self.label_11.setObjectName(u"label_11")
        sizePolicy4.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy4)
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_11, 0, 7, 1, 1)

        self.label_17 = QLabel(self.calibrateXGridFrame)
        self.label_17.setObjectName(u"label_17")
        sizePolicy6.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy6)
        self.label_17.setMaximumSize(QSize(16777215, 16777215))
        self.label_17.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_17, 1, 5, 1, 1)

        self.label_10 = QLabel(self.calibrateXGridFrame)
        self.label_10.setObjectName(u"label_10")
        sizePolicy4.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy4)
        self.label_10.setFont(font1)
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_10.addWidget(self.label_10, 0, 4, 1, 1)

        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX1LineEdit.setObjectName(u"rawX1LineEdit")
        sizePolicy4.setHeightForWidth(self.rawX1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX1LineEdit.setSizePolicy(sizePolicy4)
        self.rawX1LineEdit.setMinimumSize(QSize(120, 30))
        self.rawX1LineEdit.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.rawX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.rawX1LineEdit, 1, 4, 1, 1)

        self.label_18 = QLabel(self.calibrateXGridFrame)
        self.label_18.setObjectName(u"label_18")
        sizePolicy6.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy6)
        self.label_18.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_18, 2, 5, 1, 1)


        self.verticalLayout_17.addWidget(self.calibrateXGridFrame)

        self.widget_6 = QWidget(self.frame)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_14 = QLabel(self.widget_6)
        self.label_14.setObjectName(u"label_14")
        sizePolicy7.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy7)
        self.label_14.setStyleSheet(u"font-size: 13px;")
        self.label_14.setText(u"AXIS Y")
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_14)

        self.yComboBox = QComboBox(self.widget_6)
        self.yComboBox.setObjectName(u"yComboBox")
        sizePolicy4.setHeightForWidth(self.yComboBox.sizePolicy().hasHeightForWidth())
        self.yComboBox.setSizePolicy(sizePolicy4)
        self.yComboBox.setMinimumSize(QSize(300, 30))
        self.yComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")

        self.horizontalLayout_13.addWidget(self.yComboBox)


        self.verticalLayout_17.addWidget(self.widget_6)

        self.calibrateYGridFrame = QFrame(self.frame)
        self.calibrateYGridFrame.setObjectName(u"calibrateYGridFrame")
        sizePolicy4.setHeightForWidth(self.calibrateYGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateYGridFrame.setSizePolicy(sizePolicy4)
        self.calibrateYGridFrame.setMinimumSize(QSize(363, 100))
        self.calibrateYGridFrame.setMaximumSize(QSize(363, 16777215))
#if QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setStyleSheet(u"QPushButton {\n"
"	background-color: #4B4B4B;\n"
"	border-radius: 5px;	\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #363636;\n"
"    icon: url(:/icons/svg/target-pressed.svg)\n"
"}")
        self.gridLayout_11 = QGridLayout(self.calibrateYGridFrame)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(0)
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 12)
        self.calibrateY2Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY2Button.setObjectName(u"calibrateY2Button")
        sizePolicy4.setHeightForWidth(self.calibrateY2Button.sizePolicy().hasHeightForWidth())
        self.calibrateY2Button.setSizePolicy(sizePolicy4)
        self.calibrateY2Button.setMinimumSize(QSize(28, 28))
        self.calibrateY2Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateY2Button.setToolTip(u"Calibrate y2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY2Button.setStyleSheet(u"")
        self.calibrateY2Button.setIcon(icon19)
        self.calibrateY2Button.setCheckable(True)
        self.calibrateY2Button.setChecked(False)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 2, 1, 1, 1)

        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY2LineEdit.setObjectName(u"rawY2LineEdit")
        sizePolicy4.setHeightForWidth(self.rawY2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY2LineEdit.setSizePolicy(sizePolicy4)
        self.rawY2LineEdit.setMinimumSize(QSize(120, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(120, 16777215))
        self.rawY2LineEdit.setFont(font1)
#if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 2, 5, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_24, 1, 4, 1, 1)

        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY2LineEdit.setObjectName(u"mapY2LineEdit")
        sizePolicy4.setHeightForWidth(self.mapY2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY2LineEdit.setSizePolicy(sizePolicy4)
        self.mapY2LineEdit.setMinimumSize(QSize(120, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 2, 8, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridFrame)
        self.label_22.setObjectName(u"label_22")
        sizePolicy6.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy6)
        self.label_22.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_22, 2, 6, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_22, 1, 9, 1, 1)

        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY1LineEdit.setObjectName(u"rawY1LineEdit")
        sizePolicy4.setHeightForWidth(self.rawY1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY1LineEdit.setSizePolicy(sizePolicy4)
        self.rawY1LineEdit.setMinimumSize(QSize(120, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 1, 5, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY1LineEdit.setObjectName(u"mapY1LineEdit")
        sizePolicy4.setHeightForWidth(self.mapY1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY1LineEdit.setSizePolicy(sizePolicy4)
        self.mapY1LineEdit.setMinimumSize(QSize(120, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(120, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 1, 8, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridFrame)
        self.label_20.setObjectName(u"label_20")
        sizePolicy6.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy6)
        self.label_20.setFont(font1)
        self.label_20.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_20, 2, 3, 1, 1)

        self.calibrateY1Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY1Button.setObjectName(u"calibrateY1Button")
        sizePolicy4.setHeightForWidth(self.calibrateY1Button.sizePolicy().hasHeightForWidth())
        self.calibrateY1Button.setSizePolicy(sizePolicy4)
        self.calibrateY1Button.setMinimumSize(QSize(28, 28))
        self.calibrateY1Button.setMaximumSize(QSize(16777215, 16777215))
        self.calibrateY1Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateY1Button.setToolTip(u"Calibrate y1, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY1Button.setStyleSheet(u"")
        self.calibrateY1Button.setIcon(icon19)
        self.calibrateY1Button.setCheckable(True)
        self.calibrateY1Button.setChecked(False)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 1, 1, 1, 1)

        self.label_23 = QLabel(self.calibrateYGridFrame)
        self.label_23.setObjectName(u"label_23")
        sizePolicy4.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy4)

        self.gridLayout_11.addWidget(self.label_23, 0, 5, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridFrame)
        self.label_21.setObjectName(u"label_21")
        sizePolicy6.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy6)
        self.label_21.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_21, 1, 6, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_21, 1, 7, 1, 1)

        self.label_19 = QLabel(self.calibrateYGridFrame)
        self.label_19.setObjectName(u"label_19")
        sizePolicy6.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy6)
        self.label_19.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_19, 1, 3, 1, 1)

        self.label_24 = QLabel(self.calibrateYGridFrame)
        self.label_24.setObjectName(u"label_24")
        sizePolicy4.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy4)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_24, 0, 8, 1, 1)

        self.horizontalSpacer_23 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_23, 1, 0, 1, 1)


        self.verticalLayout_17.addWidget(self.calibrateYGridFrame)

        self.calibrationTitleWidget = QWidget(self.frame)
        self.calibrationTitleWidget.setObjectName(u"calibrationTitleWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.calibrationTitleWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 24, 0)

        self.verticalLayout_17.addWidget(self.calibrationTitleWidget)

        self.widget_7 = QWidget(self.frame)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_14 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.swapXYButton = QPushButton(self.widget_7)
        self.swapXYButton.setObjectName(u"swapXYButton")
        self.swapXYButton.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.swapXYButton.sizePolicy().hasHeightForWidth())
        self.swapXYButton.setSizePolicy(sizePolicy4)
        self.swapXYButton.setMinimumSize(QSize(208, 30))
        self.swapXYButton.setFont(font4)
        self.swapXYButton.setCursor(QCursor(Qt.ArrowCursor))
        self.swapXYButton.setStyleSheet(u"QPushButton {\n"
"color: #DBBCFB;\n"
"background-color: #4B4B4B;\n"
"border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/updown-pressed.svg);\n"
"}")
        icon20 = QIcon()
        icon20.addFile(u":/icons/svg/updown.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.swapXYButton.setIcon(icon20)
        self.swapXYButton.setIconSize(QSize(14, 16))

        self.horizontalLayout_14.addWidget(self.swapXYButton)


        self.verticalLayout_17.addWidget(self.widget_7)

        self.verticalSpacer_2 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_2)


        self.verticalLayout_9.addWidget(self.frame)

        self.pagesStackedWidget.addWidget(self.extractPointsWidget)
        self.taggingWidget = QWidget()
        self.taggingWidget.setObjectName(u"taggingWidget")
        sizePolicy11.setHeightForWidth(self.taggingWidget.sizePolicy().hasHeightForWidth())
        self.taggingWidget.setSizePolicy(sizePolicy11)
        self.verticalLayout_10 = QVBoxLayout(self.taggingWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_9 = QFrame(self.taggingWidget)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy12.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy12)
        self.frame_9.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_10)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(5, 20, 0, 0)
        self.widget_9 = QWidget(self.frame_10)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_16 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_16.setSpacing(19)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 12, 0, 0)
        self.newRowButton = QPushButton(self.widget_9)
        self.newRowButton.setObjectName(u"newRowButton")
        sizePolicy4.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy4)
        self.newRowButton.setMinimumSize(QSize(86, 30))
        self.newRowButton.setFont(font4)
#if QT_CONFIG(tooltip)
        self.newRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.newRowButton.setStyleSheet(u"QPushButton{\n"
"    background-color: #4B4B4B;\n"
"    border-radius: 6px;\n"
"    color: #DBBCFB;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/plus-pressed.svg);\n"
"}")
        self.newRowButton.setText(u"  New")
        icon21 = QIcon()
        icon21.addFile(u":/icons/svg/plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.newRowButton.setIcon(icon21)
        self.newRowButton.setIconSize(QSize(20, 20))

        self.horizontalLayout_16.addWidget(self.newRowButton)

        self.clearAllButton = QPushButton(self.widget_9)
        self.clearAllButton.setObjectName(u"clearAllButton")
        sizePolicy5.setHeightForWidth(self.clearAllButton.sizePolicy().hasHeightForWidth())
        self.clearAllButton.setSizePolicy(sizePolicy5)
        self.clearAllButton.setMinimumSize(QSize(109, 30))
        self.clearAllButton.setMaximumSize(QSize(109, 30))
        self.clearAllButton.setFont(font4)
#if QT_CONFIG(tooltip)
        self.clearAllButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.clearAllButton.setStyleSheet(u"QPushButton{\n"
"    background-color: #4B4B4B;\n"
"    border-radius: 6px;\n"
"    color: #DBBCFB;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/trash-pressed.svg);\n"
"}")
        self.clearAllButton.setText(u"  Clear All")
        icon22 = QIcon()
        icon22.addFile(u":/icons/svg/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.clearAllButton.setIcon(icon22)

        self.horizontalLayout_16.addWidget(self.clearAllButton)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_14)


        self.gridLayout_7.addWidget(self.widget_9, 1, 0, 1, 2)

        self.label_32 = QLabel(self.frame_10)
        self.label_32.setObjectName(u"label_32")
        sizePolicy5.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy5)
        self.label_32.setMinimumSize(QSize(0, 23))
        self.label_32.setFont(font3)
        self.label_32.setStyleSheet(u"color: rgb(190, 130, 250);\n"
" font-size:16px;")
        self.label_32.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_7.addWidget(self.label_32, 0, 0, 1, 2)

        self.widget_10 = QWidget(self.frame_10)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_17 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.datasetListView = ListView(self.widget_10)
        self.datasetListView.setObjectName(u"datasetListView")
        sizePolicy13 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.datasetListView.sizePolicy().hasHeightForWidth())
        self.datasetListView.setSizePolicy(sizePolicy13)
        self.datasetListView.setMinimumSize(QSize(120, 500))
        self.datasetListView.setMaximumSize(QSize(120, 500))
        font8 = QFont()
        font8.setFamilies([u"Roboto Medium"])
        font8.setPointSize(13)
        self.datasetListView.setFont(font8)
        self.datasetListView.setStyleSheet(u"QListView\n"
"{\n"
"    background-color: #2F2F2F;\n"
"	color: #FFFFFF;\n"
"}\n"
"/*\n"
"ListView::item:hover {\n"
"	 background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, \n"
"                                              stop: 0 #FAFBFE, stop: 1 #DCDEF1);\n"
"}\n"
"*/\n"
"QListView::item:selected {\n"
"	background: #171717;\n"
"    color: #FFFFFF;\n"
"}\n"
"QListView::item:hover {\n"
"	background: #171717;\n"
"    color: #FFFFFF;\n"
"}\n"
"QListView::item {\n"
"	height: 50px;\n"
"}")
        self.datasetListView.setFrameShape(QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_17.addWidget(self.datasetListView)

        self.widget_11 = QWidget(self.widget_10)
        self.widget_11.setObjectName(u"widget_11")
        sizePolicy4.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy4)
        self.widget_11.setMinimumSize(QSize(265, 500))
        self.widget_11.setMaximumSize(QSize(265, 500))
        self.widget_11.setStyleSheet(u"background-color: #171717;\n"
"\n"
"")
        self.gridLayout_8 = QGridLayout(self.widget_11)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(12)
        self.gridLayout_8.setContentsMargins(0, 12, 0, 0)
        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_8, 20, 1, 1, 1)

        self.noTagRadioButton = QRadioButton(self.widget_11)
        self.noTagRadioButton.setObjectName(u"noTagRadioButton")
        self.noTagRadioButton.setFont(font1)
        self.noTagRadioButton.setText(u"Unknown")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.gridLayout_8.addWidget(self.noTagRadioButton, 0, 1, 1, 11)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 2, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_11, 21, 11, 1, 1)

        self.tagDressedGroupBox = QGroupBox(self.widget_11)
        self.tagDressedGroupBox.setObjectName(u"tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.tagDressedGroupBox.sizePolicy().hasHeightForWidth())
        self.tagDressedGroupBox.setSizePolicy(sizePolicy5)
        font9 = QFont()
        font9.setFamilies([u"Roboto"])
        font9.setPointSize(13)
        font9.setBold(False)
        font9.setItalic(False)
        self.tagDressedGroupBox.setFont(font9)
#if QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 13pt \"Roboto\";\n"
"}\n"
"\n"
"QSpinBox {\n"
"    color: #FFFFFF;\n"
"    background-color: #171717;\n"
"	height: 28px;\n"
"    width: 28px; \n"
"    background-image: url(:/images/spin_box_bg.svg) 1;\n"
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
"	background-color: #2F2F2F;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: left; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px;\n"
"	background-color: #2F2F2F;\n"
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
"QSpinBox::up-arrow:pressed {\n"
"    width: 20px;\n"
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
        self.gridLayout_13 = QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setHorizontalSpacing(0)
        self.gridLayout_13.setVerticalSpacing(12)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(124, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 4, 2, 1, 1)

        self.line_4 = QFrame(self.tagDressedGroupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setStyleSheet(u"border: 0.5px solid #2F2F2F;\n"
"border-style: inset;")
        self.line_4.setLineWidth(0)
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_13.addWidget(self.line_4, 1, 0, 6, 1)

        self.finalStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.finalStateSpinBox.setObjectName(u"finalStateSpinBox")
        sizePolicy4.setHeightForWidth(self.finalStateSpinBox.sizePolicy().hasHeightForWidth())
        self.finalStateSpinBox.setSizePolicy(sizePolicy4)
        self.finalStateSpinBox.setMinimumSize(QSize(96, 35))
        self.finalStateSpinBox.setMaximumSize(QSize(16777215, 30))
        self.finalStateSpinBox.setFrame(True)
        self.finalStateSpinBox.setAlignment(Qt.AlignCenter)
        self.finalStateSpinBox.setValue(1)

        self.gridLayout_13.addWidget(self.finalStateSpinBox, 4, 1, 1, 1)

        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName(u"label_30")
        sizePolicy9.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy9)
#if QT_CONFIG(tooltip)
        self.label_30.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(u"Initial")
        self.label_30.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 1, 1, 1, 1)

        self.phNumberDressedSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setObjectName(u"phNumberDressedSpinBox")
        self.phNumberDressedSpinBox.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy4)
        self.phNumberDressedSpinBox.setMinimumSize(QSize(96, 35))
        self.phNumberDressedSpinBox.setMaximumSize(QSize(96, 16777215))
        self.phNumberDressedSpinBox.setBaseSize(QSize(0, 0))
        self.phNumberDressedSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberDressedSpinBox.setMinimum(1)

        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 6, 1, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName(u"label_29")
        sizePolicy9.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy9)
#if QT_CONFIG(tooltip)
        self.label_29.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(u"Photons")

        self.gridLayout_13.addWidget(self.label_29, 5, 1, 1, 1)

        self.initialStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setObjectName(u"initialStateSpinBox")
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.initialStateSpinBox.sizePolicy().hasHeightForWidth())
        self.initialStateSpinBox.setSizePolicy(sizePolicy4)
        self.initialStateSpinBox.setMinimumSize(QSize(96, 35))
        self.initialStateSpinBox.setAutoFillBackground(False)
        self.initialStateSpinBox.setStyleSheet(u"")
        self.initialStateSpinBox.setAlignment(Qt.AlignCenter)
        self.initialStateSpinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)

        self.gridLayout_13.addWidget(self.initialStateSpinBox, 2, 1, 1, 1)

        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName(u"label_31")
#if QT_CONFIG(tooltip)
        self.label_31.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(u"Final")
        self.label_31.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_31, 3, 1, 1, 1)


        self.gridLayout_8.addWidget(self.tagDressedGroupBox, 3, 0, 1, 12)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.widget_11)
        self.tagDispersiveDressedRadioButton.setObjectName(u"tagDispersiveDressedRadioButton")
        font10 = QFont()
        font10.setFamilies([u"Roboto Medium"])
        font10.setKerning(True)
        self.tagDispersiveDressedRadioButton.setFont(font10)
#if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setText(u"By dressed indices")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.gridLayout_8.addWidget(self.tagDispersiveDressedRadioButton, 1, 1, 1, 11)

        self.tagDispersiveBareRadioButton = QRadioButton(self.widget_11)
        self.tagDispersiveBareRadioButton.setObjectName(u"tagDispersiveBareRadioButton")
        self.tagDispersiveBareRadioButton.setFont(font1)
#if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setText(u"By bare states")
        self.tagDispersiveBareRadioButton.setIconSize(QSize(16, 16))

        self.gridLayout_8.addWidget(self.tagDispersiveBareRadioButton, 2, 1, 1, 11)

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_10, 1, 0, 1, 1)

        self.tagBareGroupBox = QGroupBox(self.widget_11)
        self.tagBareGroupBox.setObjectName(u"tagBareGroupBox")
        self.tagBareGroupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 13pt \"Roboto\";\n"
"}\n"
"\n"
"QSpinBox {\n"
"    color: #FFFFFF;\n"
"    background-color: #171717;\n"
"	height: 28px;\n"
"    width: 28px; \n"
"    background-image: url(:/images/spin_box_bg.svg) 1;\n"
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
"	background-color: #2F2F2F;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: left; /* position at the top right corner */\n"
"	height: 28px;\n"
"    width: 28px;\n"
"	background-color: #2F2F2F;\n"
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
"QSpinBox::up-arrow:pressed {\n"
"    width: 20px;\n"
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
        self.gridLayout_14 = QGridLayout(self.tagBareGroupBox)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(0)
        self.gridLayout_14.setVerticalSpacing(12)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.finalStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setObjectName(u"finalStateLineEdit")
        sizePolicy2.setHeightForWidth(self.finalStateLineEdit.sizePolicy().hasHeightForWidth())
        self.finalStateLineEdit.setSizePolicy(sizePolicy2)
        self.finalStateLineEdit.setMinimumSize(QSize(230, 30))
        self.finalStateLineEdit.setMaximumSize(QSize(230, 30))
        self.finalStateLineEdit.setStyleSheet(u"")
        self.finalStateLineEdit.setPlaceholderText(u"<level subsys1>, <level subsys2>, ...")

        self.gridLayout_14.addWidget(self.finalStateLineEdit, 4, 1, 1, 1)

        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setObjectName(u"initialStateLineEdit")
        self.initialStateLineEdit.setMinimumSize(QSize(230, 30))
        self.initialStateLineEdit.setMaximumSize(QSize(230, 30))
        self.initialStateLineEdit.setPlaceholderText(u"<level subsys1>, <level subsys2>, ...")

        self.gridLayout_14.addWidget(self.initialStateLineEdit, 2, 1, 1, 1)

        self.label_28 = QLabel(self.tagBareGroupBox)
        self.label_28.setObjectName(u"label_28")
        sizePolicy5.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy5)
        self.label_28.setText(u"Initial")
        self.label_28.setIndent(-1)

        self.gridLayout_14.addWidget(self.label_28, 1, 1, 1, 1)

        self.label_26 = QLabel(self.tagBareGroupBox)
        self.label_26.setObjectName(u"label_26")
        sizePolicy5.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy5)
        self.label_26.setText(u"Final")

        self.gridLayout_14.addWidget(self.label_26, 3, 1, 1, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName(u"phNumberBareSpinBox")
        sizePolicy14 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy14)
        self.phNumberBareSpinBox.setMinimumSize(QSize(96, 35))
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_14.addWidget(self.phNumberBareSpinBox, 6, 1, 1, 1)

        self.line_5 = QFrame(self.tagBareGroupBox)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setStyleSheet(u"border: 0.5px solid #2F2F2F;\n"
"border-style: inset;")
        self.line_5.setLineWidth(0)
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.gridLayout_14.addWidget(self.line_5, 0, 0, 7, 1)

        self.label_25 = QLabel(self.tagBareGroupBox)
        self.label_25.setObjectName(u"label_25")
        sizePolicy9.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy9)
        self.label_25.setText(u"Photons")

        self.gridLayout_14.addWidget(self.label_25, 5, 1, 1, 1)

        self.bareLabelOrder = QLabel(self.tagBareGroupBox)
        self.bareLabelOrder.setObjectName(u"bareLabelOrder")
        sizePolicy15 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.bareLabelOrder.sizePolicy().hasHeightForWidth())
        self.bareLabelOrder.setSizePolicy(sizePolicy15)
        self.bareLabelOrder.setWordWrap(True)

        self.gridLayout_14.addWidget(self.bareLabelOrder, 0, 1, 1, 1)


        self.gridLayout_8.addWidget(self.tagBareGroupBox, 19, 0, 1, 12)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.deleteRowButton = QPushButton(self.widget_11)
        self.deleteRowButton.setObjectName(u"deleteRowButton")
        sizePolicy4.setHeightForWidth(self.deleteRowButton.sizePolicy().hasHeightForWidth())
        self.deleteRowButton.setSizePolicy(sizePolicy4)
        self.deleteRowButton.setMinimumSize(QSize(40, 40))
        self.deleteRowButton.setMaximumSize(QSize(40, 40))
#if QT_CONFIG(tooltip)
        self.deleteRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.deleteRowButton.setStyleSheet(u"QPushButton{\n"
"    height: 40px;\n"
"    width: 40px;\n"
"    background-color: #2F2F2F;\n"
"    border-radius: 14px;\n"
"}\n"
"\n"
"QPushButton: pressed{\n"
"    background-color: #1F1F1F;\n"
"    icon: url(:/icons/svg/trash-pressed.svg)\n"
"}")
        self.deleteRowButton.setText(u"")
        self.deleteRowButton.setIcon(icon22)
        self.deleteRowButton.setIconSize(QSize(20, 20))

        self.gridLayout_8.addWidget(self.deleteRowButton, 21, 10, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 22, 10, 1, 1)


        self.horizontalLayout_17.addWidget(self.widget_11)


        self.gridLayout_7.addWidget(self.widget_10, 2, 0, 2, 1)


        self.verticalLayout_13.addWidget(self.frame_10)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_6)


        self.verticalLayout_10.addWidget(self.frame_9)

        self.pagesStackedWidget.addWidget(self.taggingWidget)
        self.prefitWidget = QWidget()
        self.prefitWidget.setObjectName(u"prefitWidget")
        sizePolicy11.setHeightForWidth(self.prefitWidget.sizePolicy().hasHeightForWidth())
        self.prefitWidget.setSizePolicy(sizePolicy11)
        self.verticalLayout_3 = QVBoxLayout(self.prefitWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(12, -1, -1, 12)
        self.frame_prefit = QFrame(self.prefitWidget)
        self.frame_prefit.setObjectName(u"frame_prefit")
        sizePolicy11.setHeightForWidth(self.frame_prefit.sizePolicy().hasHeightForWidth())
        self.frame_prefit.setSizePolicy(sizePolicy11)
        self.frame_prefit.setFrameShape(QFrame.NoFrame)
        self.frame_prefit.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_prefit)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_6.setContentsMargins(5, 20, 0, 0)
        self.widget_8 = QWidget(self.frame_prefit)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy5.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy5)
        self.horizontalLayout_15 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.widget_8)
        self.label_6.setObjectName(u"label_6")
        sizePolicy5.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy5)
        self.label_6.setMinimumSize(QSize(0, 23))
        self.label_6.setFont(font3)
        self.label_6.setStyleSheet(u"color: rgb(190, 130, 250); \n"
" font-size: 16px;")
        self.label_6.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_15.addWidget(self.label_6)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addWidget(self.widget_8)

        self.verticalSpacer_16 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_16)

        self.prefitScrollArea = QScrollArea(self.frame_prefit)
        self.prefitScrollArea.setObjectName(u"prefitScrollArea")
        sizePolicy3.setHeightForWidth(self.prefitScrollArea.sizePolicy().hasHeightForWidth())
        self.prefitScrollArea.setSizePolicy(sizePolicy3)
        self.prefitScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.prefitScrollArea.setFrameShape(QFrame.NoFrame)
        self.prefitScrollArea.setFrameShadow(QFrame.Plain)
        self.prefitScrollArea.setWidgetResizable(True)
        self.prefitScrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.prefitScrollAreaWidget = QWidget()
        self.prefitScrollAreaWidget.setObjectName(u"prefitScrollAreaWidget")
        self.prefitScrollAreaWidget.setGeometry(QRect(0, 0, 381, 427))
        self.verticalLayout_11 = QVBoxLayout(self.prefitScrollAreaWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.prefitScrollArea.setWidget(self.prefitScrollAreaWidget)

        self.verticalLayout_6.addWidget(self.prefitScrollArea)


        self.verticalLayout_3.addWidget(self.frame_prefit)

        self.frame_3 = QFrame(self.prefitWidget)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy15.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy15)
        self.frame_3.setMinimumSize(QSize(0, 100))
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_30 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_30, 0, 2, 1, 1)

        self.horizontalSpacer_31 = QSpacerItem(21, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_31, 0, 4, 1, 1)

        self.exportToFitButton = QPushButton(self.frame_3)
        self.exportToFitButton.setObjectName(u"exportToFitButton")
        sizePolicy4.setHeightForWidth(self.exportToFitButton.sizePolicy().hasHeightForWidth())
        self.exportToFitButton.setSizePolicy(sizePolicy4)
        self.exportToFitButton.setMinimumSize(QSize(170, 34))
        self.exportToFitButton.setFont(font4)
        self.exportToFitButton.setStyleSheet(u"QPushButton {\n"
"color: #DBBCFB;\n"
"background-color: #4B4B4B;\n"
"border-radius: 6px;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/copy-pressed.svg);\n"
"}")
        icon23 = QIcon()
        icon23.addFile(u":/icons/svg/copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exportToFitButton.setIcon(icon23)
        self.exportToFitButton.setIconSize(QSize(20, 20))

        self.gridLayout_15.addWidget(self.exportToFitButton, 2, 1, 1, 1)

        self.autoRunCheckBox = QCheckBox(self.frame_3)
        self.autoRunCheckBox.setObjectName(u"autoRunCheckBox")
        sizePolicy4.setHeightForWidth(self.autoRunCheckBox.sizePolicy().hasHeightForWidth())
        self.autoRunCheckBox.setSizePolicy(sizePolicy4)
        self.autoRunCheckBox.setMinimumSize(QSize(134, 0))

        self.gridLayout_15.addWidget(self.autoRunCheckBox, 0, 3, 1, 1)

        self.plotButton = QPushButton(self.frame_3)
        self.plotButton.setObjectName(u"plotButton")
        sizePolicy4.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy4)
        self.plotButton.setMinimumSize(QSize(170, 34))
        font11 = QFont()
        font11.setFamilies([u"Roboto Medium"])
        font11.setBold(True)
        font11.setKerning(True)
        self.plotButton.setFont(font11)
#if QT_CONFIG(tooltip)
        self.plotButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.plotButton.setStyleSheet(u"QPushButton{\n"
"color: #212121;\n"
"background-color: #BE82FA;\n"
"border-radius: 6px;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #9163BF;\n"
"}")
        icon24 = QIcon()
        icon24.addFile(u":/icons/svg/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.plotButton.setIcon(icon24)
        self.plotButton.setIconSize(QSize(20, 20))

        self.gridLayout_15.addWidget(self.plotButton, 0, 1, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(27, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_18, 0, 0, 1, 1)

        self.verticalSpacer_15 = QSpacerItem(20, 27, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_15.addItem(self.verticalSpacer_15, 1, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_prefit_minmax = QFrame(self.prefitWidget)
        self.frame_prefit_minmax.setObjectName(u"frame_prefit_minmax")
        sizePolicy5.setHeightForWidth(self.frame_prefit_minmax.sizePolicy().hasHeightForWidth())
        self.frame_prefit_minmax.setSizePolicy(sizePolicy5)
        self.frame_prefit_minmax.setMinimumSize(QSize(0, 0))
        self.verticalLayout_14 = QVBoxLayout(self.frame_prefit_minmax)
#ifndef Q_OS_MAC
        self.verticalLayout_14.setSpacing(-1)
#endif
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.frame_prefit_minmax)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy16 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy16)
        self.scrollArea.setMinimumSize(QSize(0, 250))
        self.scrollArea.setMaximumSize(QSize(16777215, 250))
        self.scrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.prefitMinmaxScrollAreaWidget = QWidget()
        self.prefitMinmaxScrollAreaWidget.setObjectName(u"prefitMinmaxScrollAreaWidget")
        self.prefitMinmaxScrollAreaWidget.setGeometry(QRect(0, 0, 386, 250))
        self.verticalLayout_16 = QVBoxLayout(self.prefitMinmaxScrollAreaWidget)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.scrollArea.setWidget(self.prefitMinmaxScrollAreaWidget)

        self.verticalLayout_14.addWidget(self.scrollArea)


        self.verticalLayout_3.addWidget(self.frame_prefit_minmax)

        self.pagesStackedWidget.addWidget(self.prefitWidget)
        self.fitWidget = QWidget()
        self.fitWidget.setObjectName(u"fitWidget")
        sizePolicy11.setHeightForWidth(self.fitWidget.sizePolicy().hasHeightForWidth())
        self.fitWidget.setSizePolicy(sizePolicy11)
        self.fitWidget.setAutoFillBackground(False)
        self.verticalLayout_15 = QVBoxLayout(self.fitWidget)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_fit = QFrame(self.fitWidget)
        self.frame_fit.setObjectName(u"frame_fit")
        sizePolicy1.setHeightForWidth(self.frame_fit.sizePolicy().hasHeightForWidth())
        self.frame_fit.setSizePolicy(sizePolicy1)
        self.frame_fit.setFrameShape(QFrame.NoFrame)
        self.frame_fit.setFrameShadow(QFrame.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.frame_fit)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(5, 20, 0, 0)
        self.fitTitleWidget = QWidget(self.frame_fit)
        self.fitTitleWidget.setObjectName(u"fitTitleWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.fitTitleWidget)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.fitLabel = QLabel(self.fitTitleWidget)
        self.fitLabel.setObjectName(u"fitLabel")
        sizePolicy5.setHeightForWidth(self.fitLabel.sizePolicy().hasHeightForWidth())
        self.fitLabel.setSizePolicy(sizePolicy5)
        self.fitLabel.setMinimumSize(QSize(0, 23))
        self.fitLabel.setMaximumSize(QSize(16777215, 16777215))
        self.fitLabel.setFont(font3)
        self.fitLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font-size: 16px;\n"
"")
        self.fitLabel.setFrameShape(QFrame.NoFrame)
        self.fitLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.fitLabel)

        self.fitHelpPushButton = QPushButton(self.fitTitleWidget)
        self.fitHelpPushButton.setObjectName(u"fitHelpPushButton")
        self.fitHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.fitHelpPushButton.setIcon(icon8)
        self.fitHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_5.addWidget(self.fitHelpPushButton)

        self.horizontalSpacer_5 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_8.addWidget(self.fitTitleWidget)

        self.widget_13 = QWidget(self.frame_fit)
        self.widget_13.setObjectName(u"widget_13")
        self.horizontalLayout_18 = QHBoxLayout(self.widget_13)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_27 = QSpacerItem(160, 47, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_27)

        self.pushButton_2 = QPushButton(self.widget_13)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy4.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy4)
        self.pushButton_2.setMinimumSize(QSize(160, 30))
        self.pushButton_2.setFont(font4)
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"color: #DBBCFB;\n"
"background-color: #4B4B4B;\n"
"border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/copy-pressed.svg);\n"
"}")
        self.pushButton_2.setIcon(icon23)

        self.horizontalLayout_18.addWidget(self.pushButton_2)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_28)


        self.verticalLayout_8.addWidget(self.widget_13)

        self.widget_12 = QWidget(self.frame_fit)
        self.widget_12.setObjectName(u"widget_12")
        self.horizontalLayout_8 = QHBoxLayout(self.widget_12)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_25 = QSpacerItem(130, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_25)

        self.label_7 = QLabel(self.widget_12)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setPixmap(QPixmap(u":/images/result-to-initial-arrow.svg"))
        self.label_7.setScaledContents(False)

        self.horizontalLayout_8.addWidget(self.label_7)

        self.horizontalSpacer_26 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_26)


        self.verticalLayout_8.addWidget(self.widget_12)

        self.fitScrollArea = QScrollArea(self.frame_fit)
        self.fitScrollArea.setObjectName(u"fitScrollArea")
        self.fitScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.fitScrollArea.setFrameShape(QFrame.NoFrame)
        self.fitScrollArea.setFrameShadow(QFrame.Plain)
        self.fitScrollArea.setWidgetResizable(True)
        self.fitScrollAreaWidget = QWidget()
        self.fitScrollAreaWidget.setObjectName(u"fitScrollAreaWidget")
        self.fitScrollAreaWidget.setGeometry(QRect(0, 0, 381, 555))
        self.verticalLayout_4 = QVBoxLayout(self.fitScrollAreaWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fitScrollArea.setWidget(self.fitScrollAreaWidget)

        self.verticalLayout_8.addWidget(self.fitScrollArea)


        self.verticalLayout_15.addWidget(self.frame_fit)

        self.frame_6 = QFrame(self.fitWidget)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy5.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy5)
        self.frame_6.setMinimumSize(QSize(0, 200))
        self.frame_6.setMaximumSize(QSize(16777215, 200))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_6)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.exportToPrefitButton = QPushButton(self.frame_6)
        self.exportToPrefitButton.setObjectName(u"exportToPrefitButton")
        sizePolicy4.setHeightForWidth(self.exportToPrefitButton.sizePolicy().hasHeightForWidth())
        self.exportToPrefitButton.setSizePolicy(sizePolicy4)
        self.exportToPrefitButton.setMinimumSize(QSize(191, 34))
        self.exportToPrefitButton.setMaximumSize(QSize(191, 34))
        self.exportToPrefitButton.setFont(font4)
        self.exportToPrefitButton.setStyleSheet(u"QPushButton {\n"
"color: #DBBCFB;\n"
"background-color: #4B4B4B;\n"
"border-radius: 6px;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/copy-pressed.svg);\n"
"}")
        self.exportToPrefitButton.setIcon(icon23)

        self.gridLayout_12.addWidget(self.exportToPrefitButton, 3, 1, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_12, 0, 1, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 49, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_12.addItem(self.verticalSpacer_11, 4, 1, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(27, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_16, 3, 0, 1, 1)

        self.fitButton = QPushButton(self.frame_6)
        self.fitButton.setObjectName(u"fitButton")
        sizePolicy4.setHeightForWidth(self.fitButton.sizePolicy().hasHeightForWidth())
        self.fitButton.setSizePolicy(sizePolicy4)
        self.fitButton.setMinimumSize(QSize(191, 34))
        self.fitButton.setMaximumSize(QSize(191, 34))
        self.fitButton.setFont(font4)
        self.fitButton.setStyleSheet(u"QPushButton{\n"
"color: #212121;\n"
"background-color: #BE82FA;\n"
"border-radius: 6px;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #9163BF;\n"
"}")
        self.fitButton.setIcon(icon24)
        self.fitButton.setIconSize(QSize(20, 20))

        self.gridLayout_12.addWidget(self.fitButton, 1, 1, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_15, 1, 2, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 27, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_12.addItem(self.verticalSpacer_13, 2, 1, 1, 1)


        self.verticalLayout_15.addWidget(self.frame_6)

        self.pagesStackedWidget.addWidget(self.fitWidget)

        self.gridLayout.addWidget(self.pagesStackedWidget, 0, 1, 3, 1)


        self.verticalLayout.addWidget(self.windowBodyFrame)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy5)
        self.statusBar.setMinimumSize(QSize(0, 27))
        self.statusBar.setStyleSheet(u"")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.bottomStackedWidget.setCurrentIndex(1)
        self.pagesStackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.calibratedCheckBox.setText(QCoreApplication.translate("MainWindow", u"View Calibrated Axes", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MAX", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MIN", None))

        self.colorComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"PuOr", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"SETTINGS: VISUAL", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"FILTERS", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"BACKGROUND SUBTRACT", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"COLORING", None))
#if QT_CONFIG(accessibility)
        self.frame_4.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.mseLabel.setText(QCoreApplication.translate("MainWindow", u"MSE:  - GHz\u00b2   (+0.00%)", None))
        self.pointsAddLineEdit.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.pointsAddLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"# of x value for spectrum sweep", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"TRANSITIONS", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"POINTS ADDED", None))
        self.prefitResultHelpPushButton.setText("")
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"PHOTONS", None))
        self.numericalSpectrumSettingsLabel.setText(QCoreApplication.translate("MainWindow", u"SETTINGS: NUMERICAL SPECTRUM", None))
        self.numericalSpectrumSettingsHelpPushButton.setText("")
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"EVALS COUNT", None))
        self.initStateLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"dressed or bare label", None))
        self.evalsCountLineEdit.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"INITIAL STATE", None))
        self.statusTextLabel.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.mseLabel_2.setText(QCoreApplication.translate("MainWindow", u"MSE:  - GHz\u00b2   (+0.00%)", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TOLERANCE", None))
        self.tolLineEdit.setText(QCoreApplication.translate("MainWindow", u"1e-6", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"OPTIMIZER", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"SETTINGS: FIT", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.optimizerComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"L-BFGS-B", None))
        self.optimizerComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Nelder-Mead", None))
        self.optimizerComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Powell", None))
        self.optimizerComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"shgo", None))
        self.optimizerComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"differential evolution", None))

        self.fitResultHelpPushButton.setText("")
        self.statusTextLabel_2.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.modeFitButton.setText(QCoreApplication.translate("MainWindow", u"   FIT", None))
        self.modeTagButton.setText(QCoreApplication.translate("MainWindow", u"  EXTRACT", None))
        self.modeSelectButton.setText(QCoreApplication.translate("MainWindow", u"  CALIBRATE", None))
        self.toggleMenuButton.setText("")
        self.modePrefitButton.setText(QCoreApplication.translate("MainWindow", u"  PRE-FIT", None))
        self.resetViewButton.setText("")
        self.panViewButton.setText("")
        self.zoomViewButton.setText("")
        self.horizontalSnapButton.setText("")
        self.selectViewButton.setText("")
        self.verticalSnapButton.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Pan", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Extract", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"X-snap", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Y-snap", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.calibrationHelpPushButton.setText("")
        self.zComboBox.setCurrentText("")
        self.mapX1LineEdit.setInputMask("")
        self.calibrateX2Button.setText("")
        self.calibrateX1Button.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Calibrated X</p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Raw X</p></body></html>", None))
        self.calibrateY2Button.setText("")
        self.calibrateY1Button.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Raw Y</p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Calibrated Y [GHz]</p></body></html>", None))
        self.swapXYButton.setText(QCoreApplication.translate("MainWindow", u"   Switch X And Y Axis", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"TRANSITIONS", None))
#if QT_CONFIG(statustip)
        self.tagDispersiveDressedRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.tagDispersiveBareRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
        self.bareLabelOrder.setText(QCoreApplication.translate("MainWindow", u"Labels order by:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PRE-FIT", None))
#if QT_CONFIG(tooltip)
        self.exportToFitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the pre-fitted parameters to the initial value of the fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToFitButton.setText(QCoreApplication.translate("MainWindow", u"   Results To Fit", None))
        self.autoRunCheckBox.setText(QCoreApplication.translate("MainWindow", u"Auto Update", None))
#if QT_CONFIG(accessibility)
        self.plotButton.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"   Plot Spectrum", None))
        self.fitLabel.setText(QCoreApplication.translate("MainWindow", u"FIT", None))
        self.fitHelpPushButton.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_2.setToolTip(QCoreApplication.translate("MainWindow", u"Load the current value to the initial value", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"   Results To Initial", None))
        self.label_7.setText("")
#if QT_CONFIG(tooltip)
        self.exportToPrefitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the fitted parameters to the pre-fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToPrefitButton.setText(QCoreApplication.translate("MainWindow", u"   Results To Pre-Fit", None))
        self.fitButton.setText(QCoreApplication.translate("MainWindow", u"   Run Fit", None))
        pass
    # retranslateUi

