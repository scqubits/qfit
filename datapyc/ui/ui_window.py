# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from datapyc.views.calibration_view import CalibrationLineEdit
from datapyc.views.canvas_view import FigureCanvas
from datapyc.views.extractdata_view import ListView, TableView
from datapyc.views.tagdata_view import IntTupleLineEdit, StrTupleLineEdit

import datapyc.ui.resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1300, 1104)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        MainWindow.setPalette(palette)
        font = QFont()
        font.setFamily(u"Roboto")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(u"datapyc")
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frameMain = QFrame(self.centralwidget)
        self.frameMain.setObjectName(u"frameMain")
        palette1 = QPalette()
        self.frameMain.setPalette(palette1)
        self.frameMain.setStyleSheet(u"/* LINE EDIT */\n"
"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
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
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
""
                        "	border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63"
                        ", 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px"
                        ";\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/16x16/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255"
                        ");	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"  "
                        "  background-color: rgb(85, 170, 255);\n"
"	border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")
        self.frameMain.setFrameShape(QFrame.NoFrame)
        self.frameMain.setFrameShadow(QFrame.Raised)
        self.frameMain.setLineWidth(1)
        self.verticalLayout = QVBoxLayout(self.frameMain)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frameTop = QFrame(self.frameMain)
        self.frameTop.setObjectName(u"frameTop")
        self.frameTop.setMaximumSize(QSize(16777215, 40))
        self.frameTop.setStyleSheet(u"background-color: rgb(18, 18, 18);")
        self.frameTop.setFrameShape(QFrame.NoFrame)
        self.frameTop.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frameTop)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frameTop)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(70, 35))
        self.frame_2.setMaximumSize(QSize(70, 35))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.frame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy2)
        self.pushButton_2.setMinimumSize(QSize(0, 0))
        self.pushButton_2.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_2.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/20x20/cil-menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon)

        self.verticalLayout_7.addWidget(self.pushButton_2)


        self.horizontalLayout_3.addWidget(self.frame_2)

        self.frame_5 = QFrame(self.frameTop)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy3)
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        palette2 = QPalette()
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        brush2 = QBrush(QColor(18, 18, 18, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        brush3 = QBrush(QColor(120, 120, 120, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.label.setPalette(palette2)
        font1 = QFont()
        font1.setFamily(u"Roboto")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.label.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.frameTop)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.frame_4.setLineWidth(0)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.buttonMinimize = QPushButton(self.frame_4)
        self.buttonMinimize.setObjectName(u"buttonMinimize")
        self.buttonMinimize.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.buttonMinimize.sizePolicy().hasHeightForWidth())
        self.buttonMinimize.setSizePolicy(sizePolicy4)
        self.buttonMinimize.setMinimumSize(QSize(40, 40))
        self.buttonMinimize.setMaximumSize(QSize(40, 16777215))
        self.buttonMinimize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonMinimize.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.buttonMinimize)

        self.buttonMaximize = QPushButton(self.frame_4)
        self.buttonMaximize.setObjectName(u"buttonMaximize")
        self.buttonMaximize.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.buttonMaximize.sizePolicy().hasHeightForWidth())
        self.buttonMaximize.setSizePolicy(sizePolicy4)
        self.buttonMaximize.setMinimumSize(QSize(40, 40))
        self.buttonMaximize.setMaximumSize(QSize(40, 16777215))
        self.buttonMaximize.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonMaximize.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.buttonMaximize)

        self.buttonClose = QPushButton(self.frame_4)
        self.buttonClose.setObjectName(u"buttonClose")
        self.buttonClose.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.buttonClose.sizePolicy().hasHeightForWidth())
        self.buttonClose.setSizePolicy(sizePolicy4)
        self.buttonClose.setMinimumSize(QSize(40, 40))
        self.buttonClose.setMaximumSize(QSize(40, 16777215))
        self.buttonClose.setStyleSheet(u"QPushButton {	\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonClose.setIcon(icon3)

        self.horizontalLayout_4.addWidget(self.buttonClose)


        self.horizontalLayout_3.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frameTop)

        self.frameTop_2 = QFrame(self.frameMain)
        self.frameTop_2.setObjectName(u"frameTop_2")
        self.frameTop_2.setMaximumSize(QSize(16777215, 40))
        self.frameTop_2.setStyleSheet(u"background-color: rgb(18, 18, 18);")
        self.frameTop_2.setFrameShape(QFrame.NoFrame)
        self.frameTop_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frameTop_2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.frameTop_2)
        self.frame_13.setObjectName(u"frame_13")
        sizePolicy1.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy1)
        self.frame_13.setMinimumSize(QSize(70, 10))
        self.frame_13.setMaximumSize(QSize(70, 35))
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_13)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_12.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.frameTop_2)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy3.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy3)
        self.frame_14.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")

        self.horizontalLayout_12.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.frameTop_2)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.frame_15.setLineWidth(0)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_12.addWidget(self.frame_15)


        self.verticalLayout.addWidget(self.frameTop_2)

        self.frameCenter = QFrame(self.frameMain)
        self.frameCenter.setObjectName(u"frameCenter")
        sizePolicy.setHeightForWidth(self.frameCenter.sizePolicy().hasHeightForWidth())
        self.frameCenter.setSizePolicy(sizePolicy)
        palette3 = QPalette()
        brush4 = QBrush(QColor(33, 33, 33, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush4)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush4)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush4)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        self.frameCenter.setPalette(palette3)
        self.frameCenter.setStyleSheet(u"background-color: rgb(33, 33, 33);")
        self.frameCenter.setFrameShape(QFrame.NoFrame)
        self.frameCenter.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frameCenter)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 12, 0)
        self.frame_6 = QFrame(self.frameCenter)
        self.frame_6.setObjectName(u"frame_6")
        palette4 = QPalette()
        brush5 = QBrush(QColor(200, 200, 200, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Button, brush4)
        palette4.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette4.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush4)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush4)
        brush6 = QBrush(QColor(200, 200, 200, 128))
        brush6.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Active, QPalette.PlaceholderText, brush6)
#endif
        palette4.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Button, brush4)
        palette4.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush4)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush4)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush6)
#endif
        palette4.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Button, brush4)
        palette4.setBrush(QPalette.Disabled, QPalette.Text, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        brush7 = QBrush(QColor(0, 0, 0, 128))
        brush7.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette4.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush7)
#endif
        self.frame_6.setPalette(palette4)
        font2 = QFont()
        font2.setFamily(u"Roboto")
        font2.setPointSize(9)
        self.frame_6.setFont(font2)
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.dataTableView = TableView(self.frame_6)
        self.dataTableView.setObjectName(u"dataTableView")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.dataTableView.sizePolicy().hasHeightForWidth())
        self.dataTableView.setSizePolicy(sizePolicy5)
        self.dataTableView.setMinimumSize(QSize(0, 105))
        self.dataTableView.setMaximumSize(QSize(16777215, 105))
        palette5 = QPalette()
        palette5.setBrush(QPalette.Active, QPalette.Button, brush4)
        palette5.setBrush(QPalette.Active, QPalette.Base, brush4)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush4)
        palette5.setBrush(QPalette.Inactive, QPalette.Button, brush4)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush4)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        palette5.setBrush(QPalette.Disabled, QPalette.Button, brush4)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        self.dataTableView.setPalette(palette5)
        self.dataTableView.setFont(font)
        self.dataTableView.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(63, 63, 63);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"	background-color: rgb(93, 93, 93);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
""
                        "QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"	background-color: rgb(93,93, 93);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"TableView\n"
"{\n"
"	background-color: rgb(63, 63, 63);\n"
"	color: rgb(200,200,200);\n"
"}")
        self.dataTableView.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_5.addWidget(self.dataTableView)


        self.gridLayout.addWidget(self.frame_6, 1, 2, 1, 1)

        self.tabWidget = QTabWidget(self.frameCenter)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy6)
        palette6 = QPalette()
        brush8 = QBrush(QColor(172, 172, 172, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette6.setBrush(QPalette.Active, QPalette.WindowText, brush8)
        palette6.setBrush(QPalette.Active, QPalette.Button, brush4)
        palette6.setBrush(QPalette.Active, QPalette.Text, brush8)
        palette6.setBrush(QPalette.Active, QPalette.ButtonText, brush8)
        palette6.setBrush(QPalette.Active, QPalette.Base, brush4)
        palette6.setBrush(QPalette.Active, QPalette.Window, brush4)
        brush9 = QBrush(QColor(172, 172, 172, 128))
        brush9.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Active, QPalette.PlaceholderText, brush9)
#endif
        palette6.setBrush(QPalette.Inactive, QPalette.WindowText, brush8)
        palette6.setBrush(QPalette.Inactive, QPalette.Button, brush4)
        palette6.setBrush(QPalette.Inactive, QPalette.Text, brush8)
        palette6.setBrush(QPalette.Inactive, QPalette.ButtonText, brush8)
        palette6.setBrush(QPalette.Inactive, QPalette.Base, brush4)
        palette6.setBrush(QPalette.Inactive, QPalette.Window, brush4)
        brush10 = QBrush(QColor(172, 172, 172, 128))
        brush10.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush10)
#endif
        palette6.setBrush(QPalette.Disabled, QPalette.WindowText, brush8)
        palette6.setBrush(QPalette.Disabled, QPalette.Button, brush4)
        palette6.setBrush(QPalette.Disabled, QPalette.Text, brush8)
        palette6.setBrush(QPalette.Disabled, QPalette.ButtonText, brush8)
        palette6.setBrush(QPalette.Disabled, QPalette.Base, brush4)
        palette6.setBrush(QPalette.Disabled, QPalette.Window, brush4)
        brush11 = QBrush(QColor(172, 172, 172, 128))
        brush11.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette6.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush11)
#endif
        self.tabWidget.setPalette(palette6)
        font3 = QFont()
        font3.setFamily(u"Roboto Medium")
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setWeight(50)
        self.tabWidget.setFont(font3)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"QTabWidget\n"
"{\n"
"	border: 0px;\n"
"}\n"
"\n"
"QTabBar\n"
"{\n"
"    color: rgb(170,170,170);\n"
" }\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"	color: rgb(30,30,30);\n"
"    background-color: rgb(190, 130, 250);\n"
" }\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"	color: rgb(170,170,170);\n"
"    background-color: rgb(47, 47, 47);\n"
" }\n"
"\n"
"")
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.selectTab = QWidget()
        self.selectTab.setObjectName(u"selectTab")
        self.selectTab.setStyleSheet(u"background-color: rgb(47, 47, 47);\n"
"color: rgb(200, 200, 200);")
        self.verticalLayout_2 = QVBoxLayout(self.selectTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.imageOptionsVerticalGroupBox = QGroupBox(self.selectTab)
        self.imageOptionsVerticalGroupBox.setObjectName(u"imageOptionsVerticalGroupBox")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.imageOptionsVerticalGroupBox.sizePolicy().hasHeightForWidth())
        self.imageOptionsVerticalGroupBox.setSizePolicy(sizePolicy7)
        self.imageOptionsVerticalGroupBox.setMinimumSize(QSize(330, 0))
        font4 = QFont()
        font4.setFamily(u"Roboto Medium")
        font4.setPointSize(10)
        self.imageOptionsVerticalGroupBox.setFont(font4)
        self.imageOptionsVerticalGroupBox.setStyleSheet(u"border:0")
        self.imageOptionsVerticalGroupBox.setTitle(u"FILTERING")
        self.gridLayout_8 = QGridLayout(self.imageOptionsVerticalGroupBox)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(7)
        self.gridLayout_8.setContentsMargins(-1, 27, -1, -1)
        self.bgndSubtractXCheckBox = QCheckBox(self.imageOptionsVerticalGroupBox)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        palette7 = QPalette()
        palette7.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        brush12 = QBrush(QColor(47, 47, 47, 255))
        brush12.setStyle(Qt.SolidPattern)
        palette7.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette7.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette7.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette7.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette7.setBrush(QPalette.Active, QPalette.Window, brush12)
        brush13 = QBrush(QColor(200, 200, 200, 128))
        brush13.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Active, QPalette.PlaceholderText, brush13)
#endif
        palette7.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette7.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette7.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette7.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette7.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette7.setBrush(QPalette.Inactive, QPalette.Window, brush12)
        brush14 = QBrush(QColor(200, 200, 200, 128))
        brush14.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush14)
#endif
        palette7.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette7.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette7.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette7.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette7.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette7.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        brush15 = QBrush(QColor(200, 200, 200, 128))
        brush15.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette7.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush15)
#endif
        self.bgndSubtractXCheckBox.setPalette(palette7)
        self.bgndSubtractXCheckBox.setFont(font2)
#if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip(u"Background subtraction along X")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"")
        self.bgndSubtractXCheckBox.setText(u"X BGND SUBTRACT")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 2, 0, 1, 1)

        self.bgndSubtractYCheckBox = QCheckBox(self.imageOptionsVerticalGroupBox)
        self.bgndSubtractYCheckBox.setObjectName(u"bgndSubtractYCheckBox")
        palette8 = QPalette()
        palette8.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette8.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette8.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette8.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette8.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette8.setBrush(QPalette.Active, QPalette.Window, brush12)
        brush16 = QBrush(QColor(200, 200, 200, 128))
        brush16.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Active, QPalette.PlaceholderText, brush16)
#endif
        palette8.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette8.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette8.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette8.setBrush(QPalette.Inactive, QPalette.Window, brush12)
        brush17 = QBrush(QColor(200, 200, 200, 128))
        brush17.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush17)
#endif
        palette8.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette8.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette8.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette8.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette8.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette8.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        brush18 = QBrush(QColor(200, 200, 200, 128))
        brush18.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette8.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush18)
#endif
        self.bgndSubtractYCheckBox.setPalette(palette8)
        self.bgndSubtractYCheckBox.setFont(font2)
#if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"")
        self.bgndSubtractYCheckBox.setText(u"Y BGND SUBTRACT")

        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 2, 1, 1, 1)

        self.waveletCheckBox = QCheckBox(self.imageOptionsVerticalGroupBox)
        self.waveletCheckBox.setObjectName(u"waveletCheckBox")
        palette9 = QPalette()
        palette9.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette9.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette9.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette9.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette9.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette9.setBrush(QPalette.Active, QPalette.Window, brush12)
        brush19 = QBrush(QColor(200, 200, 200, 128))
        brush19.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Active, QPalette.PlaceholderText, brush19)
#endif
        palette9.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette9.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette9.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette9.setBrush(QPalette.Inactive, QPalette.Window, brush12)
        brush20 = QBrush(QColor(200, 200, 200, 128))
        brush20.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush20)
#endif
        palette9.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette9.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette9.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette9.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        brush21 = QBrush(QColor(200, 200, 200, 128))
        brush21.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette9.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush21)
#endif
        self.waveletCheckBox.setPalette(palette9)
        self.waveletCheckBox.setFont(font2)
#if QT_CONFIG(tooltip)
        self.waveletCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.waveletCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"")
        self.waveletCheckBox.setText(u"WAVELET DENOISE")

        self.gridLayout_8.addWidget(self.waveletCheckBox, 0, 1, 1, 1)

        self.topHatCheckBox = QCheckBox(self.imageOptionsVerticalGroupBox)
        self.topHatCheckBox.setObjectName(u"topHatCheckBox")
        palette10 = QPalette()
        palette10.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette10.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette10.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette10.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette10.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette10.setBrush(QPalette.Active, QPalette.Window, brush12)
        brush22 = QBrush(QColor(85, 255, 255, 128))
        brush22.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Active, QPalette.PlaceholderText, brush22)
#endif
        palette10.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette10.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette10.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette10.setBrush(QPalette.Inactive, QPalette.Window, brush12)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush22)
#endif
        palette10.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette10.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette10.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette10.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette10.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette10.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        brush23 = QBrush(QColor(172, 172, 172, 128))
        brush23.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette10.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush23)
#endif
        self.topHatCheckBox.setPalette(palette10)
        self.topHatCheckBox.setFont(font2)
#if QT_CONFIG(tooltip)
        self.topHatCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.topHatCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"")
        self.topHatCheckBox.setText(u"TOP-HAT FILTER")

        self.gridLayout_8.addWidget(self.topHatCheckBox, 0, 0, 1, 1)

        self.edgeFilterCheckBox = QCheckBox(self.imageOptionsVerticalGroupBox)
        self.edgeFilterCheckBox.setObjectName(u"edgeFilterCheckBox")
        palette11 = QPalette()
        palette11.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette11.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette11.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette11.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette11.setBrush(QPalette.Active, QPalette.Window, brush12)
        brush24 = QBrush(QColor(200, 200, 200, 128))
        brush24.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Active, QPalette.PlaceholderText, brush24)
#endif
        palette11.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette11.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette11.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette11.setBrush(QPalette.Inactive, QPalette.Window, brush12)
        brush25 = QBrush(QColor(200, 200, 200, 128))
        brush25.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush25)
#endif
        palette11.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette11.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette11.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette11.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        brush26 = QBrush(QColor(200, 200, 200, 128))
        brush26.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette11.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush26)
#endif
        self.edgeFilterCheckBox.setPalette(palette11)
        self.edgeFilterCheckBox.setFont(font2)
#if QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"")
        self.edgeFilterCheckBox.setText(u"EDGE FILTER")

        self.gridLayout_8.addWidget(self.edgeFilterCheckBox, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.imageOptionsVerticalGroupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.colorGridGroupBox = QGroupBox(self.selectTab)
        self.colorGridGroupBox.setObjectName(u"colorGridGroupBox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.colorGridGroupBox.sizePolicy().hasHeightForWidth())
        self.colorGridGroupBox.setSizePolicy(sizePolicy8)
        self.colorGridGroupBox.setMinimumSize(QSize(330, 0))
        self.colorGridGroupBox.setFont(font4)
        self.colorGridGroupBox.setStyleSheet(u"border:0")
        self.colorGridGroupBox.setTitle(u"COLORS")
        self.gridLayout_9 = QGridLayout(self.colorGridGroupBox)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(-1, 27, -1, -1)
        self.colorComboBox = QComboBox(self.colorGridGroupBox)
        icon4 = QIcon()
        icon4.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon4, u"PuOr")
        icon5 = QIcon()
        icon5.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon5, u"RdYlBu")
        icon6 = QIcon()
        icon6.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon6, u"bwr")
        icon7 = QIcon()
        icon7.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon7, u"viridis")
        icon8 = QIcon()
        icon8.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon8, u"cividis")
        icon9 = QIcon()
        icon9.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon9, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy9)
        palette12 = QPalette()
        palette12.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        brush27 = QBrush(QColor(27, 29, 35, 255))
        brush27.setStyle(Qt.SolidPattern)
        palette12.setBrush(QPalette.Active, QPalette.Button, brush27)
        palette12.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette12.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette12.setBrush(QPalette.Active, QPalette.Base, brush27)
        palette12.setBrush(QPalette.Active, QPalette.Window, brush27)
        brush28 = QBrush(QColor(200, 200, 200, 128))
        brush28.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette12.setBrush(QPalette.Active, QPalette.PlaceholderText, brush28)
#endif
        palette12.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette12.setBrush(QPalette.Inactive, QPalette.Button, brush27)
        palette12.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette12.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette12.setBrush(QPalette.Inactive, QPalette.Base, brush27)
        palette12.setBrush(QPalette.Inactive, QPalette.Window, brush27)
        brush29 = QBrush(QColor(200, 200, 200, 128))
        brush29.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette12.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush29)
#endif
        palette12.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette12.setBrush(QPalette.Disabled, QPalette.Button, brush27)
        palette12.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette12.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette12.setBrush(QPalette.Disabled, QPalette.Base, brush27)
        palette12.setBrush(QPalette.Disabled, QPalette.Window, brush27)
        brush30 = QBrush(QColor(200, 200, 200, 128))
        brush30.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette12.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush30)
#endif
        self.colorComboBox.setPalette(palette12)
#if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.colorComboBox.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}")
        self.colorComboBox.setIconSize(QSize(100, 10))
        self.colorComboBox.setFrame(True)

        self.gridLayout_9.addWidget(self.colorComboBox, 0, 0, 1, 1)

        self.logScaleCheckBox = QCheckBox(self.colorGridGroupBox)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        self.logScaleCheckBox.setFont(font2)
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"")
        self.logScaleCheckBox.setText(u"LOG")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout_9.addWidget(self.logScaleCheckBox, 0, 1, 1, 1)

        self.rangeSliderMax = QSlider(self.colorGridGroupBox)
        self.rangeSliderMax.setObjectName(u"rangeSliderMax")
        self.rangeSliderMax.setMinimumSize(QSize(0, 18))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMax, 3, 0, 1, 1)

        self.rangeSliderMin = QSlider(self.colorGridGroupBox)
        self.rangeSliderMin.setObjectName(u"rangeSliderMin")
        self.rangeSliderMin.setMinimumSize(QSize(0, 18))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMin, 1, 0, 1, 1)

        self.label_2 = QLabel(self.colorGridGroupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.gridLayout_9.addWidget(self.label_2, 1, 1, 1, 1)

        self.label_3 = QLabel(self.colorGridGroupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.gridLayout_9.addWidget(self.label_3, 3, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.colorGridGroupBox)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.xyzDataGridGroupBox = QGroupBox(self.selectTab)
        self.xyzDataGridGroupBox.setObjectName(u"xyzDataGridGroupBox")
        sizePolicy7.setHeightForWidth(self.xyzDataGridGroupBox.sizePolicy().hasHeightForWidth())
        self.xyzDataGridGroupBox.setSizePolicy(sizePolicy7)
        self.xyzDataGridGroupBox.setMinimumSize(QSize(330, 0))
        self.xyzDataGridGroupBox.setFont(font4)
        self.xyzDataGridGroupBox.setStyleSheet(u"border:0")
        self.gridLayout_4 = QGridLayout(self.xyzDataGridGroupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, 27, -1, -1)
        self.xComboBox = QComboBox(self.xyzDataGridGroupBox)
        self.xComboBox.setObjectName(u"xComboBox")
        self.xComboBox.setMinimumSize(QSize(250, 0))
        self.xComboBox.setFont(font2)
        self.xComboBox.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}")

        self.gridLayout_4.addWidget(self.xComboBox, 3, 1, 1, 1)

        self.zComboBox = QComboBox(self.xyzDataGridGroupBox)
        self.zComboBox.setObjectName(u"zComboBox")
        self.zComboBox.setMinimumSize(QSize(250, 0))
        palette13 = QPalette()
        palette13.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        palette13.setBrush(QPalette.Active, QPalette.Button, brush27)
        palette13.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette13.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette13.setBrush(QPalette.Active, QPalette.Base, brush27)
        palette13.setBrush(QPalette.Active, QPalette.Window, brush27)
        brush31 = QBrush(QColor(200, 200, 200, 128))
        brush31.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette13.setBrush(QPalette.Active, QPalette.PlaceholderText, brush31)
#endif
        palette13.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette13.setBrush(QPalette.Inactive, QPalette.Button, brush27)
        palette13.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette13.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette13.setBrush(QPalette.Inactive, QPalette.Base, brush27)
        palette13.setBrush(QPalette.Inactive, QPalette.Window, brush27)
        brush32 = QBrush(QColor(200, 200, 200, 128))
        brush32.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette13.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush32)
#endif
        palette13.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette13.setBrush(QPalette.Disabled, QPalette.Button, brush27)
        palette13.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette13.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette13.setBrush(QPalette.Disabled, QPalette.Base, brush27)
        palette13.setBrush(QPalette.Disabled, QPalette.Window, brush27)
        brush33 = QBrush(QColor(200, 200, 200, 128))
        brush33.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette13.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush33)
#endif
        self.zComboBox.setPalette(palette13)
        self.zComboBox.setFont(font2)
        self.zComboBox.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/16x16/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}")
        self.zComboBox.setFrame(True)

        self.gridLayout_4.addWidget(self.zComboBox, 1, 1, 1, 1)

        self.label_13 = QLabel(self.xyzDataGridGroupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font2)
        self.label_13.setText(u"Z")
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_13, 1, 0, 1, 1)

        self.label_12 = QLabel(self.xyzDataGridGroupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font2)
        self.label_12.setText(u"AXIS 1")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 3, 0, 1, 1)

        self.label_14 = QLabel(self.xyzDataGridGroupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font2)
        self.label_14.setText(u"AXIS 2")
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 4, 0, 1, 1)

        self.yComboBox = QComboBox(self.xyzDataGridGroupBox)
        self.yComboBox.setObjectName(u"yComboBox")
        self.yComboBox.setMinimumSize(QSize(250, 0))
        self.yComboBox.setFont(font2)
        self.yComboBox.setStyleSheet(u"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}")

        self.gridLayout_4.addWidget(self.yComboBox, 4, 1, 1, 1)


        self.verticalLayout_2.addWidget(self.xyzDataGridGroupBox)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.calibrateXGridGroupBox = QGroupBox(self.selectTab)
        self.calibrateXGridGroupBox.setObjectName(u"calibrateXGridGroupBox")
        sizePolicy7.setHeightForWidth(self.calibrateXGridGroupBox.sizePolicy().hasHeightForWidth())
        self.calibrateXGridGroupBox.setSizePolicy(sizePolicy7)
        self.calibrateXGridGroupBox.setMinimumSize(QSize(330, 0))
        self.calibrateXGridGroupBox.setMaximumSize(QSize(320, 16777215))
        self.calibrateXGridGroupBox.setFont(font4)
        self.calibrateXGridGroupBox.setStyleSheet(u"border:0")
        self.calibrateXGridGroupBox.setTitle(u"CALIBRATE X")
        self.gridLayout_10 = QGridLayout(self.calibrateXGridGroupBox)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setContentsMargins(-1, 27, -1, -1)
        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        self.rawX1LineEdit.setObjectName(u"rawX1LineEdit")
        sizePolicy5.setHeightForWidth(self.rawX1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX1LineEdit.setSizePolicy(sizePolicy5)
        self.rawX1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX1LineEdit.setMaximumSize(QSize(200, 16777215))
        self.rawX1LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.rawX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX1LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.rawX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.rawX1LineEdit, 0, 2, 1, 1)

        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        self.mapX2LineEdit.setObjectName(u"mapX2LineEdit")
        sizePolicy5.setHeightForWidth(self.mapX2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX2LineEdit.setSizePolicy(sizePolicy5)
        self.mapX2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX2LineEdit.setMaximumSize(QSize(200, 16777215))
        self.mapX2LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.mapX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX2LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.mapX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.mapX2LineEdit, 1, 4, 1, 1)

        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        self.rawX2LineEdit.setObjectName(u"rawX2LineEdit")
        sizePolicy5.setHeightForWidth(self.rawX2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX2LineEdit.setSizePolicy(sizePolicy5)
        self.rawX2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX2LineEdit.setMaximumSize(QSize(200, 16777215))
        self.rawX2LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.rawX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX2LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.rawX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.rawX2LineEdit, 1, 2, 1, 1)

        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        self.mapX1LineEdit.setObjectName(u"mapX1LineEdit")
        sizePolicy5.setHeightForWidth(self.mapX1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX1LineEdit.setSizePolicy(sizePolicy5)
        self.mapX1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX1LineEdit.setMaximumSize(QSize(200, 16777215))
        self.mapX1LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.mapX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX1LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.mapX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.mapX1LineEdit, 0, 4, 1, 1)

        self.label_15 = QLabel(self.calibrateXGridGroupBox)
        self.label_15.setObjectName(u"label_15")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy10)
        self.label_15.setFont(font2)
        self.label_15.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_15, 0, 1, 1, 1)

        self.label_16 = QLabel(self.calibrateXGridGroupBox)
        self.label_16.setObjectName(u"label_16")
        sizePolicy10.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy10)
        self.label_16.setFont(font2)
        self.label_16.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_16, 1, 1, 1, 1)

        self.label_17 = QLabel(self.calibrateXGridGroupBox)
        self.label_17.setObjectName(u"label_17")
        sizePolicy10.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy10)
        self.label_17.setFont(font2)
        self.label_17.setText(u"<html><head/><body><p align=\"right\">\u2192 X<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_17, 0, 3, 1, 1)

        self.label_18 = QLabel(self.calibrateXGridGroupBox)
        self.label_18.setObjectName(u"label_18")
        sizePolicy10.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy10)
        self.label_18.setFont(font2)
        self.label_18.setText(u"<html><head/><body><p align=\"right\">\u2192 X<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_18, 1, 3, 1, 1)

        self.calibrateX1Button = QPushButton(self.calibrateXGridGroupBox)
        self.calibrateX1Button.setObjectName(u"calibrateX1Button")
        self.calibrateX1Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateX1Button.setToolTip(u"Calibrate x1, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX1Button.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/icons/16x16/cil-at.png", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrateX1Button.setIcon(icon10)

        self.gridLayout_10.addWidget(self.calibrateX1Button, 0, 0, 1, 1)

        self.calibrateX2Button = QPushButton(self.calibrateXGridGroupBox)
        self.calibrateX2Button.setObjectName(u"calibrateX2Button")
        self.calibrateX2Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateX2Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX2Button.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"}")
        self.calibrateX2Button.setIcon(icon10)

        self.gridLayout_10.addWidget(self.calibrateX2Button, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.calibrateXGridGroupBox)

        self.calibrateYGridGroupBox = QGroupBox(self.selectTab)
        self.calibrateYGridGroupBox.setObjectName(u"calibrateYGridGroupBox")
        sizePolicy7.setHeightForWidth(self.calibrateYGridGroupBox.sizePolicy().hasHeightForWidth())
        self.calibrateYGridGroupBox.setSizePolicy(sizePolicy7)
        self.calibrateYGridGroupBox.setMinimumSize(QSize(330, 0))
        self.calibrateYGridGroupBox.setMaximumSize(QSize(320, 16777215))
        self.calibrateYGridGroupBox.setFont(font4)
#if QT_CONFIG(tooltip)
        self.calibrateYGridGroupBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.calibrateYGridGroupBox.setStyleSheet(u"border:0")
        self.calibrateYGridGroupBox.setTitle(u"CALIBRATE Y")
        self.gridLayout_11 = QGridLayout(self.calibrateYGridGroupBox)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(-1, 27, -1, -1)
        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        self.rawY2LineEdit.setObjectName(u"rawY2LineEdit")
        sizePolicy5.setHeightForWidth(self.rawY2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY2LineEdit.setSizePolicy(sizePolicy5)
        self.rawY2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(200, 16777215))
        self.rawY2LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.rawY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 1, 2, 1, 1)

        self.label_19 = QLabel(self.calibrateYGridGroupBox)
        self.label_19.setObjectName(u"label_19")
        sizePolicy10.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy10)
        self.label_19.setFont(font2)
        self.label_19.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        self.mapY1LineEdit.setObjectName(u"mapY1LineEdit")
        sizePolicy5.setHeightForWidth(self.mapY1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY1LineEdit.setSizePolicy(sizePolicy5)
        self.mapY1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(200, 16777215))
        self.mapY1LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.mapY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 0, 4, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridGroupBox)
        self.label_20.setObjectName(u"label_20")
        sizePolicy10.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy10)
        self.label_20.setFont(font2)
        self.label_20.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_20, 1, 1, 1, 1)

        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        self.mapY2LineEdit.setObjectName(u"mapY2LineEdit")
        sizePolicy5.setHeightForWidth(self.mapY2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY2LineEdit.setSizePolicy(sizePolicy5)
        self.mapY2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(200, 16777215))
        self.mapY2LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.mapY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 1, 4, 1, 1)

        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        self.rawY1LineEdit.setObjectName(u"rawY1LineEdit")
        sizePolicy5.setHeightForWidth(self.rawY1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY1LineEdit.setSizePolicy(sizePolicy5)
        self.rawY1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(200, 16777215))
        self.rawY1LineEdit.setFont(font2)
#if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(196, 150, 248);\n"
"}")
        self.rawY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 0, 2, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridGroupBox)
        self.label_21.setObjectName(u"label_21")
        sizePolicy10.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy10)
        self.label_21.setFont(font2)
        self.label_21.setText(u"<html><head/><body><p align=\"right\">\u2192 Y<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_21, 0, 3, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridGroupBox)
        self.label_22.setObjectName(u"label_22")
        sizePolicy10.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy10)
        self.label_22.setFont(font2)
        self.label_22.setText(u"<html><head/><body><p align=\"right\">\u2192 Y<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_22, 1, 3, 1, 1)

        self.calibrateY2Button = QPushButton(self.calibrateYGridGroupBox)
        self.calibrateY2Button.setObjectName(u"calibrateY2Button")
        self.calibrateY2Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateY2Button.setToolTip(u"Calibrate y2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY2Button.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"}")
        self.calibrateY2Button.setIcon(icon10)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 1, 0, 1, 1)

        self.calibrateY1Button = QPushButton(self.calibrateYGridGroupBox)
        self.calibrateY1Button.setObjectName(u"calibrateY1Button")
        self.calibrateY1Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateY1Button.setToolTip(u"Calibrate y1, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY1Button.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"}")
        self.calibrateY1Button.setIcon(icon10)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.calibrateYGridGroupBox)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.calibratedCheckBox = QCheckBox(self.selectTab)
        self.calibratedCheckBox.setObjectName(u"calibratedCheckBox")
        sizePolicy5.setHeightForWidth(self.calibratedCheckBox.sizePolicy().hasHeightForWidth())
        self.calibratedCheckBox.setSizePolicy(sizePolicy5)
        self.calibratedCheckBox.setFont(font2)
        self.calibratedCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.calibratedCheckBox.setStyleSheet(u"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}")
        self.calibratedCheckBox.setText(u"TOGGLE CALIBRATION")

        self.verticalLayout_2.addWidget(self.calibratedCheckBox)

        self.tabWidget.addTab(self.selectTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.selectTab), u"SELECT")
        self.tagTab = QWidget()
        self.tagTab.setObjectName(u"tagTab")
        self.tagTab.setStyleSheet(u"background-color: rgb(47, 47, 47);\n"
"color: rgb(200, 200, 200);")
        self.verticalLayout_3 = QVBoxLayout(self.tagTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tagChoicesFrame = QFrame(self.tagTab)
        self.tagChoicesFrame.setObjectName(u"tagChoicesFrame")
        self.tagChoicesFrame.setFrameShape(QFrame.NoFrame)
        self.tagChoicesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.tagChoicesFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.noTagRadioButton = QRadioButton(self.tagChoicesFrame)
        self.noTagRadioButton.setObjectName(u"noTagRadioButton")
        self.noTagRadioButton.setFont(font)
#if QT_CONFIG(tooltip)
        self.noTagRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.noTagRadioButton.setStyleSheet(u"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"}\n"
"")
        self.noTagRadioButton.setText(u"NO TAG")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.verticalLayout_4.addWidget(self.noTagRadioButton)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.label_23 = QLabel(self.tagChoicesFrame)
        self.label_23.setObjectName(u"label_23")
        font5 = QFont()
        font5.setFamily(u"Roboto")
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setWeight(50)
        self.label_23.setFont(font5)
#if QT_CONFIG(tooltip)
        self.label_23.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_23.setText(u"DISPERSIVE TRANSITION")

        self.verticalLayout_4.addWidget(self.label_23)

        self.tagDispersiveBareRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveBareRadioButton.setObjectName(u"tagDispersiveBareRadioButton")
        self.tagDispersiveBareRadioButton.setFont(font2)
#if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setStyleSheet(u"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"}\n"
"")
        self.tagDispersiveBareRadioButton.setText(u"BY BARE STATES")
        self.tagDispersiveBareRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveBareRadioButton)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveDressedRadioButton.setObjectName(u"tagDispersiveDressedRadioButton")
        self.tagDispersiveDressedRadioButton.setFont(font2)
#if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setStyleSheet(u"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"}\n"
"")
        self.tagDispersiveDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveDressedRadioButton)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.label_24 = QLabel(self.tagChoicesFrame)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font5)
#if QT_CONFIG(tooltip)
        self.label_24.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_24.setText(u"AVOIDED CROSSING")

        self.verticalLayout_4.addWidget(self.label_24)

        self.tagCrossingRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingRadioButton.setObjectName(u"tagCrossingRadioButton")
        self.tagCrossingRadioButton.setFont(font2)
#if QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setStyleSheet(u"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"}\n"
"")
        self.tagCrossingRadioButton.setText(u"INFER WHEN FITTING")
        self.tagCrossingRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingRadioButton)

        self.tagCrossingDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingDressedRadioButton.setObjectName(u"tagCrossingDressedRadioButton")
        self.tagCrossingDressedRadioButton.setFont(font2)
#if QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setStyleSheet(u"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(196, 150, 248);	\n"
"}\n"
"")
        self.tagCrossingDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagCrossingDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingDressedRadioButton)


        self.verticalLayout_3.addWidget(self.tagChoicesFrame)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_9)

        self.tagDressedGroupBox = QGroupBox(self.tagTab)
        self.tagDressedGroupBox.setObjectName(u"tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
        self.tagDressedGroupBox.setFont(font)
#if QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setStyleSheet(u"QGroupBox {\n"
"	border:0;\n"
"}\n"
"")
        self.tagDressedGroupBox.setTitle(u"TAG BY DRESSED INDICES")
        self.gridLayout_13 = QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 27, -1, -1)
        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.initialStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setObjectName(u"initialStateSpinBox")
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.initialStateSpinBox.sizePolicy().hasHeightForWidth())
        self.initialStateSpinBox.setSizePolicy(sizePolicy5)
        self.initialStateSpinBox.setMinimumSize(QSize(60, 20))
        self.initialStateSpinBox.setFont(font)
        self.initialStateSpinBox.setStyleSheet(u"QSpinBox {\n"
"    padding-right: 5px; /* make room for the arrows */\n"
"    border-width: 3;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top left; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px;\n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    image: url(:/icons/16x16/cil-plus.png) 1;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/16x16/cil-minus.png) 1;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed {\n"
"    background-color: rgb(200,200,200);\n"
"}\n"
"")
        self.initialStateSpinBox.setAlignment(Qt.AlignCenter)

        self.gridLayout_13.addWidget(self.initialStateSpinBox, 0, 4, 1, 1)

        self.finalStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.finalStateSpinBox.setObjectName(u"finalStateSpinBox")
        sizePolicy5.setHeightForWidth(self.finalStateSpinBox.sizePolicy().hasHeightForWidth())
        self.finalStateSpinBox.setSizePolicy(sizePolicy5)
        self.finalStateSpinBox.setMinimumSize(QSize(60, 20))
        self.finalStateSpinBox.setFont(font)
        self.finalStateSpinBox.setStyleSheet(u"QSpinBox {\n"
"    padding-right: 5px; /* make room for the arrows */\n"
"    border-width: 3;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top left; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px;\n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    image: url(:/icons/16x16/cil-plus.png) 1;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/16x16/cil-minus.png) 1;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed {\n"
"    background-color: rgb(200,200,200);\n"
"}\n"
"")
        self.finalStateSpinBox.setAlignment(Qt.AlignCenter)
        self.finalStateSpinBox.setValue(1)

        self.gridLayout_13.addWidget(self.finalStateSpinBox, 1, 4, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName(u"label_29")
        sizePolicy11 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy11)
        font6 = QFont()
        font6.setFamily(u"Roboto")
        self.label_29.setFont(font6)
#if QT_CONFIG(tooltip)
        self.label_29.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(u"PHOTONS")

        self.gridLayout_13.addWidget(self.label_29, 0, 0, 1, 1)

        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName(u"label_30")
        sizePolicy11.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy11)
        self.label_30.setFont(font6)
#if QT_CONFIG(tooltip)
        self.label_30.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(u"INITIAL")
        self.label_30.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 0, 3, 1, 1)

        self.phNumberDressedSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setObjectName(u"phNumberDressedSpinBox")
        self.phNumberDressedSpinBox.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy5)
        self.phNumberDressedSpinBox.setMinimumSize(QSize(60, 0))
        self.phNumberDressedSpinBox.setFont(font)
        self.phNumberDressedSpinBox.setStyleSheet(u"QSpinBox {\n"
"    padding-right: 5px; /* make room for the arrows */\n"
"    border-width: 3;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top left; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px;\n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    image: url(:/icons/16x16/cil-plus.png) 1;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/16x16/cil-minus.png) 1;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed {\n"
"    background-color: rgb(200,200,200);\n"
"}\n"
"")
        self.phNumberDressedSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberDressedSpinBox.setMinimum(1)

        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 0, 1, 1, 1)

        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font6)
#if QT_CONFIG(tooltip)
        self.label_31.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(u"FINAL")
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_31, 1, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)


        self.verticalLayout_3.addWidget(self.tagDressedGroupBox)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_10)

        self.tagBareGroupBox = QGroupBox(self.tagTab)
        self.tagBareGroupBox.setObjectName(u"tagBareGroupBox")
        self.tagBareGroupBox.setEnabled(True)
        self.tagBareGroupBox.setFont(font)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setStyleSheet(u"border:0")
        self.tagBareGroupBox.setTitle(u"TAG BY BARE STATES")
        self.tagBareGroupBox.setFlat(False)
        self.gridLayout_12 = QGridLayout(self.tagBareGroupBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(-1, 27, -1, -1)
        self.subsysNamesLineEdit = StrTupleLineEdit(self.tagBareGroupBox)
        self.subsysNamesLineEdit.setObjectName(u"subsysNamesLineEdit")
        self.subsysNamesLineEdit.setMinimumSize(QSize(0, 30))
        self.subsysNamesLineEdit.setFont(font6)
        self.subsysNamesLineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.subsysNamesLineEdit.setText(u"")
        self.subsysNamesLineEdit.setPlaceholderText(u" <subsystem name 1>, ...")
        self.subsysNamesLineEdit.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.subsysNamesLineEdit, 0, 0, 1, 5)

        self.label_25 = QLabel(self.tagBareGroupBox)
        self.label_25.setObjectName(u"label_25")
        sizePolicy11.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy11)
        self.label_25.setFont(font6)
        self.label_25.setText(u"PHOTONS")

        self.gridLayout_12.addWidget(self.label_25, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.label_28 = QLabel(self.tagBareGroupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font6)
        self.label_28.setText(u"INITIAL")

        self.gridLayout_12.addWidget(self.label_28, 1, 3, 1, 1)

        self.label_26 = QLabel(self.tagBareGroupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font6)
        self.label_26.setText(u"FINAL")

        self.gridLayout_12.addWidget(self.label_26, 2, 3, 1, 1)

        self.finalStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setObjectName(u"finalStateLineEdit")
        self.finalStateLineEdit.setMinimumSize(QSize(0, 30))
        self.finalStateLineEdit.setFont(font6)
        self.finalStateLineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.finalStateLineEdit.setPlaceholderText(u"<level subsys 1>, <level subsys2>, ...")

        self.gridLayout_12.addWidget(self.finalStateLineEdit, 2, 4, 1, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName(u"phNumberBareSpinBox")
        sizePolicy8.setHeightForWidth(self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy8)
        self.phNumberBareSpinBox.setMinimumSize(QSize(60, 20))
        self.phNumberBareSpinBox.setFont(font2)
        self.phNumberBareSpinBox.setStyleSheet(u"QSpinBox {\n"
"    padding-right: 5px; /* make room for the arrows */\n"
"    border-width: 3;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top left; /* position at the top right corner */\n"
"	height: 16px;\n"
"    width: 16px;\n"
"    border-width: 1px;\n"
"	background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    image: url(:/icons/16x16/cil-plus.png) 1;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/16x16/cil-minus.png) 1;\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed {\n"
"    background-color: rgb(200,200,200);\n"
"}\n"
"")
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 1, 1, 1, 1)

        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setObjectName(u"initialStateLineEdit")
        self.initialStateLineEdit.setMinimumSize(QSize(0, 30))
        self.initialStateLineEdit.setFont(font6)
        self.initialStateLineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")
        self.initialStateLineEdit.setPlaceholderText(u"<level subsys 1>, <level subsys2>, ...")

        self.gridLayout_12.addWidget(self.initialStateLineEdit, 1, 4, 1, 1)


        self.verticalLayout_3.addWidget(self.tagBareGroupBox)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_11)

        self.tabWidget.addTab(self.tagTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tagTab), u"TAG")

        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)

        self.frame = QFrame(self.frameCenter)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QSize(70, 0))
        self.frame.setMaximumSize(QSize(70, 16777215))
        self.frame.setStyleSheet(u"background-color: rgb(18, 18, 18);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.frame, 0, 0, 3, 1)

        self.frame_3 = QFrame(self.frameCenter)
        self.frame_3.setObjectName(u"frame_3")
        palette14 = QPalette()
        palette14.setBrush(QPalette.Active, QPalette.Button, brush12)
        palette14.setBrush(QPalette.Active, QPalette.Base, brush12)
        palette14.setBrush(QPalette.Active, QPalette.Window, brush12)
        palette14.setBrush(QPalette.Inactive, QPalette.Button, brush12)
        palette14.setBrush(QPalette.Inactive, QPalette.Base, brush12)
        palette14.setBrush(QPalette.Inactive, QPalette.Window, brush12)
        palette14.setBrush(QPalette.Disabled, QPalette.Button, brush12)
        palette14.setBrush(QPalette.Disabled, QPalette.Base, brush12)
        palette14.setBrush(QPalette.Disabled, QPalette.Window, brush12)
        self.frame_3.setPalette(palette14)
        self.frame_3.setFont(font2)
        self.frame_3.setStyleSheet(u"background-color: rgb(47, 47, 47);")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, -1, 4, -1)
        self.newRowButton = QPushButton(self.frame_3)
        self.newRowButton.setObjectName(u"newRowButton")
        sizePolicy5.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy5)
        self.newRowButton.setMinimumSize(QSize(100, 30))
        palette15 = QPalette()
        brush34 = QBrush(QColor(93, 93, 93, 255))
        brush34.setStyle(Qt.SolidPattern)
        palette15.setBrush(QPalette.Active, QPalette.Button, brush34)
        brush35 = QBrush(QColor(234, 234, 234, 255))
        brush35.setStyle(Qt.SolidPattern)
        palette15.setBrush(QPalette.Active, QPalette.ButtonText, brush35)
        palette15.setBrush(QPalette.Active, QPalette.Base, brush34)
        palette15.setBrush(QPalette.Active, QPalette.Window, brush34)
        palette15.setBrush(QPalette.Inactive, QPalette.Button, brush34)
        palette15.setBrush(QPalette.Inactive, QPalette.ButtonText, brush35)
        palette15.setBrush(QPalette.Inactive, QPalette.Base, brush34)
        palette15.setBrush(QPalette.Inactive, QPalette.Window, brush34)
        palette15.setBrush(QPalette.Disabled, QPalette.Button, brush34)
        palette15.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette15.setBrush(QPalette.Disabled, QPalette.Base, brush34)
        palette15.setBrush(QPalette.Disabled, QPalette.Window, brush34)
        self.newRowButton.setPalette(palette15)
        font7 = QFont()
        font7.setFamily(u"Roboto Medium")
        font7.setPointSize(9)
        self.newRowButton.setFont(font7)
#if QT_CONFIG(tooltip)
        self.newRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.newRowButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 15px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.newRowButton.setText(u"+ NEW   ")

        self.verticalLayout_6.addWidget(self.newRowButton)

        self.deleteRowButton = QPushButton(self.frame_3)
        self.deleteRowButton.setObjectName(u"deleteRowButton")
        sizePolicy5.setHeightForWidth(self.deleteRowButton.sizePolicy().hasHeightForWidth())
        self.deleteRowButton.setSizePolicy(sizePolicy5)
        self.deleteRowButton.setMinimumSize(QSize(100, 30))
        palette16 = QPalette()
        brush36 = QBrush(QColor(188, 188, 188, 255))
        brush36.setStyle(Qt.SolidPattern)
        palette16.setBrush(QPalette.Active, QPalette.WindowText, brush36)
        palette16.setBrush(QPalette.Active, QPalette.Button, brush34)
        palette16.setBrush(QPalette.Active, QPalette.ButtonText, brush35)
        palette16.setBrush(QPalette.Active, QPalette.Base, brush34)
        palette16.setBrush(QPalette.Active, QPalette.Window, brush34)
        palette16.setBrush(QPalette.Inactive, QPalette.WindowText, brush36)
        palette16.setBrush(QPalette.Inactive, QPalette.Button, brush34)
        palette16.setBrush(QPalette.Inactive, QPalette.ButtonText, brush35)
        palette16.setBrush(QPalette.Inactive, QPalette.Base, brush34)
        palette16.setBrush(QPalette.Inactive, QPalette.Window, brush34)
        palette16.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette16.setBrush(QPalette.Disabled, QPalette.Button, brush34)
        palette16.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette16.setBrush(QPalette.Disabled, QPalette.Base, brush34)
        palette16.setBrush(QPalette.Disabled, QPalette.Window, brush34)
        self.deleteRowButton.setPalette(palette16)
        self.deleteRowButton.setFont(font7)
#if QT_CONFIG(tooltip)
        self.deleteRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.deleteRowButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 15px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.deleteRowButton.setText(u"- DELETE  ")

        self.verticalLayout_6.addWidget(self.deleteRowButton)

        self.clearAllButton = QPushButton(self.frame_3)
        self.clearAllButton.setObjectName(u"clearAllButton")
        sizePolicy5.setHeightForWidth(self.clearAllButton.sizePolicy().hasHeightForWidth())
        self.clearAllButton.setSizePolicy(sizePolicy5)
        self.clearAllButton.setMinimumSize(QSize(100, 30))
        palette17 = QPalette()
        palette17.setBrush(QPalette.Active, QPalette.WindowText, brush36)
        palette17.setBrush(QPalette.Active, QPalette.Button, brush34)
        palette17.setBrush(QPalette.Active, QPalette.ButtonText, brush35)
        palette17.setBrush(QPalette.Active, QPalette.Base, brush34)
        palette17.setBrush(QPalette.Active, QPalette.Window, brush34)
        palette17.setBrush(QPalette.Inactive, QPalette.WindowText, brush36)
        palette17.setBrush(QPalette.Inactive, QPalette.Button, brush34)
        palette17.setBrush(QPalette.Inactive, QPalette.ButtonText, brush35)
        palette17.setBrush(QPalette.Inactive, QPalette.Base, brush34)
        palette17.setBrush(QPalette.Inactive, QPalette.Window, brush34)
        palette17.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette17.setBrush(QPalette.Disabled, QPalette.Button, brush34)
        palette17.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette17.setBrush(QPalette.Disabled, QPalette.Base, brush34)
        palette17.setBrush(QPalette.Disabled, QPalette.Window, brush34)
        self.clearAllButton.setPalette(palette17)
        self.clearAllButton.setFont(font7)
#if QT_CONFIG(tooltip)
        self.clearAllButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.clearAllButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 15px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.clearAllButton.setText(u"CLEAR ALL")

        self.verticalLayout_6.addWidget(self.clearAllButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.datasetListView = ListView(self.frame_3)
        self.datasetListView.setObjectName(u"datasetListView")
        sizePolicy7.setHeightForWidth(self.datasetListView.sizePolicy().hasHeightForWidth())
        self.datasetListView.setSizePolicy(sizePolicy7)
        self.datasetListView.setMinimumSize(QSize(0, 120))
        self.datasetListView.setMaximumSize(QSize(230, 100))
        self.datasetListView.setFont(font)
        self.datasetListView.setStyleSheet(u"QTableWidget {	\n"
"	background-color: rgb(37, 37, 42);\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	color: rgb(200,200,200);\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"	Background-color: rgb(39, 44, 54);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px "
                        "solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(81, 255, 0);\n"
"}\n"
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
"\n"
"ListView\n"
"{\n"
"	background-color: rgb(63,63,63);\n"
"	color: rgb(200,200,200);\n"
"}\n"
"")
        self.datasetListView.setFrameShape(QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.datasetListView)


        self.gridLayout.addWidget(self.frame_3, 1, 1, 1, 1)

        self.mplFigureCanvas = FigureCanvas(self.frameCenter)
        self.mplFigureCanvas.setObjectName(u"mplFigureCanvas")
        sizePolicy12 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.mplFigureCanvas.sizePolicy().hasHeightForWidth())
        self.mplFigureCanvas.setSizePolicy(sizePolicy12)
        self.mplFigureCanvas.setMinimumSize(QSize(0, 60))
        self.mplFigureCanvas.setMaximumSize(QSize(16777215, 16777215))
        palette18 = QPalette()
        palette18.setBrush(QPalette.Active, QPalette.WindowText, brush5)
        brush37 = QBrush(QColor(37, 37, 42, 255))
        brush37.setStyle(Qt.SolidPattern)
        palette18.setBrush(QPalette.Active, QPalette.Button, brush37)
        palette18.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette18.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette18.setBrush(QPalette.Active, QPalette.Base, brush37)
        palette18.setBrush(QPalette.Active, QPalette.Window, brush37)
        brush38 = QBrush(QColor(200, 200, 200, 128))
        brush38.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette18.setBrush(QPalette.Active, QPalette.PlaceholderText, brush38)
#endif
        palette18.setBrush(QPalette.Inactive, QPalette.WindowText, brush5)
        palette18.setBrush(QPalette.Inactive, QPalette.Button, brush37)
        palette18.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette18.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette18.setBrush(QPalette.Inactive, QPalette.Base, brush37)
        palette18.setBrush(QPalette.Inactive, QPalette.Window, brush37)
        brush39 = QBrush(QColor(200, 200, 200, 128))
        brush39.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette18.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush39)
#endif
        palette18.setBrush(QPalette.Disabled, QPalette.WindowText, brush5)
        palette18.setBrush(QPalette.Disabled, QPalette.Button, brush37)
        palette18.setBrush(QPalette.Disabled, QPalette.Text, brush5)
        palette18.setBrush(QPalette.Disabled, QPalette.ButtonText, brush5)
        palette18.setBrush(QPalette.Disabled, QPalette.Base, brush37)
        palette18.setBrush(QPalette.Disabled, QPalette.Window, brush37)
        brush40 = QBrush(QColor(200, 200, 200, 128))
        brush40.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette18.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush40)
#endif
        self.mplFigureCanvas.setPalette(palette18)
        self.mplFigureCanvas.setStyleSheet(u"background-color: rgb(37, 37, 42);\n"
"color: rgb(200, 200, 200);")
        self.mplFigureCanvas.setFrameShape(QFrame.NoFrame)
        self.mplFigureCanvas.setFrameShadow(QFrame.Raised)
        self.mplFigureCanvas.setLineWidth(0)
        self.frame_7 = QFrame(self.mplFigureCanvas)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setGeometry(QRect(20, 20, 361, 80))
        self.frame_7.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.resetViewButton = QPushButton(self.frame_7)
        self.resetViewButton.setObjectName(u"resetViewButton")
        self.resetViewButton.setGeometry(QRect(30, 20, 40, 40))
#if QT_CONFIG(tooltip)
        self.resetViewButton.setToolTip(u"Reset plot area")
#endif // QT_CONFIG(tooltip)
        self.resetViewButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
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
"}")
        icon11 = QIcon()
        icon11.addFile(u":/icons/16x16/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon11)
        self.panViewButton = QPushButton(self.frame_7)
        self.panViewButton.setObjectName(u"panViewButton")
        self.panViewButton.setGeometry(QRect(90, 20, 40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip(u"Pan mode: move plot region by dragging")
#endif // QT_CONFIG(tooltip)
        self.panViewButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
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
"}")
        icon12 = QIcon()
        icon12.addFile(u":/icons/16x16/cil-move.png", QSize(), QIcon.Normal, QIcon.Off)
        self.panViewButton.setIcon(icon12)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.zoomViewButton = QPushButton(self.frame_7)
        self.zoomViewButton.setObjectName(u"zoomViewButton")
        self.zoomViewButton.setGeometry(QRect(150, 20, 40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip(u"Zoom mode: select a plot region to enlarge")
#endif // QT_CONFIG(tooltip)
        self.zoomViewButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
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
"}")
        icon13 = QIcon()
        icon13.addFile(u":/icons/16x16/cil-zoom-in.png", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomViewButton.setIcon(icon13)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.selectViewButton = QPushButton(self.frame_7)
        self.selectViewButton.setObjectName(u"selectViewButton")
        self.selectViewButton.setGeometry(QRect(210, 20, 41, 41))
        self.selectViewButton.setCursor(QCursor(Qt.CrossCursor))
#if QT_CONFIG(tooltip)
        self.selectViewButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.selectViewButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
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
"}")
        icon14 = QIcon()
        icon14.addFile(u":/icons/16x16/cil-location-pin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.selectViewButton.setIcon(icon14)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.swapXYButton = QPushButton(self.frame_7)
        self.swapXYButton.setObjectName(u"swapXYButton")
        self.swapXYButton.setGeometry(QRect(270, 20, 71, 41))
        self.swapXYButton.setFont(font2)
        self.swapXYButton.setCursor(QCursor(Qt.CrossCursor))
#if QT_CONFIG(tooltip)
        self.swapXYButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.swapXYButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 15px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"")
        self.swapXYButton.setCheckable(True)
        self.swapXYButton.setChecked(True)
        self.swapXYButton.setAutoExclusive(True)

        self.gridLayout.addWidget(self.mplFigureCanvas, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.frameCenter)


        self.horizontalLayout.addWidget(self.frameMain)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.bgndSubtractXCheckBox, self.bgndSubtractYCheckBox)
        QWidget.setTabOrder(self.bgndSubtractYCheckBox, self.waveletCheckBox)
        QWidget.setTabOrder(self.waveletCheckBox, self.topHatCheckBox)
        QWidget.setTabOrder(self.topHatCheckBox, self.edgeFilterCheckBox)
        QWidget.setTabOrder(self.edgeFilterCheckBox, self.colorComboBox)
        QWidget.setTabOrder(self.colorComboBox, self.logScaleCheckBox)
        QWidget.setTabOrder(self.logScaleCheckBox, self.yComboBox)
        QWidget.setTabOrder(self.yComboBox, self.zComboBox)
        QWidget.setTabOrder(self.zComboBox, self.xComboBox)
        QWidget.setTabOrder(self.xComboBox, self.rawX1LineEdit)
        QWidget.setTabOrder(self.rawX1LineEdit, self.calibrateX2Button)
        QWidget.setTabOrder(self.calibrateX2Button, self.mapX2LineEdit)
        QWidget.setTabOrder(self.mapX2LineEdit, self.rawX2LineEdit)
        QWidget.setTabOrder(self.rawX2LineEdit, self.mapX1LineEdit)
        QWidget.setTabOrder(self.mapX1LineEdit, self.calibrateX1Button)
        QWidget.setTabOrder(self.calibrateX1Button, self.rawY2LineEdit)
        QWidget.setTabOrder(self.rawY2LineEdit, self.calibrateY2Button)
        QWidget.setTabOrder(self.calibrateY2Button, self.mapY1LineEdit)
        QWidget.setTabOrder(self.mapY1LineEdit, self.calibrateY1Button)
        QWidget.setTabOrder(self.calibrateY1Button, self.mapY2LineEdit)
        QWidget.setTabOrder(self.mapY2LineEdit, self.rawY1LineEdit)
        QWidget.setTabOrder(self.rawY1LineEdit, self.calibratedCheckBox)
        QWidget.setTabOrder(self.calibratedCheckBox, self.noTagRadioButton)
        QWidget.setTabOrder(self.noTagRadioButton, self.tagDispersiveBareRadioButton)
        QWidget.setTabOrder(self.tagDispersiveBareRadioButton, self.tagDispersiveDressedRadioButton)
        QWidget.setTabOrder(self.tagDispersiveDressedRadioButton, self.tagCrossingRadioButton)
        QWidget.setTabOrder(self.tagCrossingRadioButton, self.tagCrossingDressedRadioButton)
        QWidget.setTabOrder(self.tagCrossingDressedRadioButton, self.initialStateSpinBox)
        QWidget.setTabOrder(self.initialStateSpinBox, self.finalStateSpinBox)
        QWidget.setTabOrder(self.finalStateSpinBox, self.phNumberDressedSpinBox)
        QWidget.setTabOrder(self.phNumberDressedSpinBox, self.subsysNamesLineEdit)
        QWidget.setTabOrder(self.subsysNamesLineEdit, self.phNumberBareSpinBox)
        QWidget.setTabOrder(self.phNumberBareSpinBox, self.initialStateLineEdit)
        QWidget.setTabOrder(self.initialStateLineEdit, self.finalStateLineEdit)
        QWidget.setTabOrder(self.finalStateLineEdit, self.resetViewButton)
        QWidget.setTabOrder(self.resetViewButton, self.panViewButton)
        QWidget.setTabOrder(self.panViewButton, self.zoomViewButton)
        QWidget.setTabOrder(self.zoomViewButton, self.selectViewButton)
        QWidget.setTabOrder(self.selectViewButton, self.swapXYButton)

        self.retranslateUi(MainWindow)
        self.buttonMinimize.clicked.connect(MainWindow.showMinimized)
        self.buttonClose.clicked.connect(MainWindow.close)
        self.buttonMaximize.clicked.connect(MainWindow.showMaximized)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.pushButton_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"datapyc", None))
        self.buttonMinimize.setText("")
        self.buttonMaximize.setText("")
        self.buttonClose.setText("")

        self.colorComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"PuOr", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MIN", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MAX", None))
        self.xyzDataGridGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.zComboBox.setCurrentText("")
        self.mapX1LineEdit.setInputMask("")
        self.calibrateX1Button.setText("")
        self.calibrateX2Button.setText("")
        self.calibrateY2Button.setText("")
        self.calibrateY1Button.setText("")
#if QT_CONFIG(statustip)
        self.noTagRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.tagDispersiveBareRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.tagDispersiveDressedRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.tagCrossingRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.tagCrossingDressedRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
        self.resetViewButton.setText("")
        self.panViewButton.setText("")
        self.zoomViewButton.setText("")
        self.selectViewButton.setText("")
        self.swapXYButton.setText(QCoreApplication.translate("MainWindow", u"X\u2194Y", None))
        pass
    # retranslateUi

