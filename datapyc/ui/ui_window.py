# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\window.ui',
# licensing of '.\window.ui' applies.
#
# Created: Wed Aug 11 13:30:57 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

import datapyc.ui.resources_rc

from datapyc.calibration.calibration_view import CalibrationLineEdit
from datapyc.canvas.canvas_view import FigureCanvas
from datapyc.data.extracted_view import ListView, TableView
from datapyc.data.tagdata_view import IntTupleLineEdit, StrTupleLineEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1300, 1104)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("datapyc")
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QFrame {\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QToolTip {\n"
"    color: #ffffff;\n"
"    background-color: rgba(27, 29, 35, 160);\n"
"    border: 1px solid rgb(40, 40, 40);\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QWidget {\n"
"    font-family: Roboto;\n"
"    font-size: 9pt;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: rgb(170, 170, 170);\n"
"}\n"
"\n"
"/* LINE EDIT */\n"
"QLineEdit {\n"
"    color: rgb(170, 170, 170);\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"    border-radius: 7px\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"    border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"    border-top-left-radius: 7px;\n"
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
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"\n"
" QScrollBar::handle:vertical {    \n"
"    background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"    border-radius: 7px\n"
" }\n"
"\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"    border-top-left-radius: 7px;\n"
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
"    color: rgb(170, 170, 170);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"    border: 3px solid rgb(52, 59, 72);    \n"
"    background-image: url(:/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton {\n"
"    color: rgb(170, 170, 170);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"    border: 3px solid rgb(52, 59, 72);    \n"
"}\n"
"\n"
"\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"    margin: 0px;\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"QSlider::groove:horizontal:hover {\n"
"    background-color: rgb(55, 62, 76);\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"QSlider::groove:vertical:hover {\n"
"    background-color: rgb(55, 62, 76);\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    border-radius: 9px;\n"
"}\n"
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
"    border: 0;\n"
"    color: rgb(170, 170, 170);\n"
"    font: 57 10pt \"Roboto Medium\";\n"
"}\n"
"\n"
"QSpinBox {\n"
"    background-color: transparent;\n"
"    color: rgb(170, 170, 170);\n"
"    padding-right: 5px; /* make room for the arrows */\n"
"    border-width: 3;\n"
"}\n"
"\n"
"QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right; /* position at the top right corner */\n"
"    height: 16px;\n"
"    width: 16px; \n"
"    border-width: 1px;\n"
"    background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top left; /* position at the top right corner */\n"
"    height: 16px;\n"
"    width: 16px;\n"
"    border-width: 1px;\n"
"    background-color: rgb(93,93,93);\n"
"}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    image: url(:/icons/16x16/cil-plus.png) 1;\n"
"}\n"
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
"\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox {\n"
"    color: rgb(170, 170, 170);\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"QComboBox:hover{\n"
"    background-color: rgb(27, 29, 35);\n"
"    border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    background-color: rgb(27, 29, 35);\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 25px; \n"
"    border-left-width: 3px;\n"
"    border-left-color: rgba(39, 44, 54, 150);\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;    \n"
"    background-image: url(:/icons/16x16/cil-arrow-bottom.png);\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
" }\n"
" \n"
"QComboBox QAbstractItemView {\n"
"    color: rgb(85, 170, 255);    \n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 10px;\n"
"    selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"\n"
"QTableWidget {    \n"
"    background-color: rgb(37, 37, 42);\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"    color: rgb(200,200,200);\n"
"    border-color: rgb(44, 49, 60);\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QHeaderView::section{\n"
"    Background-color: rgb(39, 44, 54);\n"
"    max-width: 30px;\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {    \n"
"    background-color: rgb(81, 255, 0);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 3px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"ListView\n"
"{\n"
"    background-color: rgb(63,63,63);\n"
"    color: rgb(200,200,200);\n"
"}\n"
"")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frameMain = QtWidgets.QFrame(self.centralwidget)
        self.frameMain.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frameMain.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameMain.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameMain.setLineWidth(1)
        self.frameMain.setObjectName("frameMain")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameMain)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frameTop = QtWidgets.QFrame(self.frameMain)
        self.frameTop.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frameTop.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameTop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTop.setObjectName("frameTop")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frameTop)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_2 = QtWidgets.QFrame(self.frameTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(70, 35))
        self.frame_2.setMaximumSize(QtCore.QSize(70, 35))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.toggleMenuButton = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleMenuButton.sizePolicy().hasHeightForWidth())
        self.toggleMenuButton.setSizePolicy(sizePolicy)
        self.toggleMenuButton.setMinimumSize(QtCore.QSize(0, 0))
        self.toggleMenuButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.toggleMenuButton.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.toggleMenuButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/20x20/cil-menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleMenuButton.setIcon(icon)
        self.toggleMenuButton.setObjectName("toggleMenuButton")
        self.verticalLayout_7.addWidget(self.toggleMenuButton)
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.frame_5 = QtWidgets.QFrame(self.frameTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setStyleSheet("color: rgb(255, 255, 255); font: 10pt \"Roboto\";")
        self.label.setLineWidth(0)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.horizontalLayout_3.addWidget(self.frame_5)
        self.frame_4 = QtWidgets.QFrame(self.frameTop)
        self.frame_4.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setLineWidth(0)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.buttonMinimize = QtWidgets.QPushButton(self.frame_4)
        self.buttonMinimize.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonMinimize.sizePolicy().hasHeightForWidth())
        self.buttonMinimize.setSizePolicy(sizePolicy)
        self.buttonMinimize.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonMinimize.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonMinimize.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-window-minimize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonMinimize.setIcon(icon1)
        self.buttonMinimize.setObjectName("buttonMinimize")
        self.horizontalLayout_4.addWidget(self.buttonMinimize)
        self.buttonMaximize = QtWidgets.QPushButton(self.frame_4)
        self.buttonMaximize.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonMaximize.sizePolicy().hasHeightForWidth())
        self.buttonMaximize.setSizePolicy(sizePolicy)
        self.buttonMaximize.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonMaximize.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonMaximize.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-window-maximize.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonMaximize.setIcon(icon2)
        self.buttonMaximize.setObjectName("buttonMaximize")
        self.horizontalLayout_4.addWidget(self.buttonMaximize)
        self.buttonClose = QtWidgets.QPushButton(self.frame_4)
        self.buttonClose.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonClose.sizePolicy().hasHeightForWidth())
        self.buttonClose.setSizePolicy(sizePolicy)
        self.buttonClose.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonClose.setMaximumSize(QtCore.QSize(40, 16777215))
        self.buttonClose.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonClose.setIcon(icon3)
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout_4.addWidget(self.buttonClose)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.frameTop)
        self.frameTop_2 = QtWidgets.QFrame(self.frameMain)
        self.frameTop_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frameTop_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameTop_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTop_2.setObjectName("frameTop_2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frameTop_2)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frame_13 = QtWidgets.QFrame(self.frameTop_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setMinimumSize(QtCore.QSize(70, 10))
        self.frame_13.setMaximumSize(QtCore.QSize(70, 35))
        self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_12.addWidget(self.frame_13)
        self.frame_14 = QtWidgets.QFrame(self.frameTop_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy)
        self.frame_14.setStyleSheet("background-color: rgb(33,33,33);")
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalLayout_12.addWidget(self.frame_14)
        self.frame_15 = QtWidgets.QFrame(self.frameTop_2)
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setLineWidth(0)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_12.addWidget(self.frame_15)
        self.verticalLayout.addWidget(self.frameTop_2)
        self.frameCenter = QtWidgets.QFrame(self.frameMain)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameCenter.sizePolicy().hasHeightForWidth())
        self.frameCenter.setSizePolicy(sizePolicy)
        self.frameCenter.setStyleSheet("QFrame {\n"
"    background-color: rgb(33, 33, 33);\n"
"}")
        self.frameCenter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameCenter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameCenter.setObjectName("frameCenter")
        self.gridLayout = QtWidgets.QGridLayout(self.frameCenter)
        self.gridLayout.setContentsMargins(0, 0, 12, 0)
        self.gridLayout.setHorizontalSpacing(14)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName("gridLayout")
        self.mplFigureCanvas = FigureCanvas(self.frameCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mplFigureCanvas.sizePolicy().hasHeightForWidth())
        self.mplFigureCanvas.setSizePolicy(sizePolicy)
        self.mplFigureCanvas.setMinimumSize(QtCore.QSize(0, 60))
        self.mplFigureCanvas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mplFigureCanvas.setStyleSheet("background-color: rgb(37, 37, 42);\n"
"color: rgb(200, 200, 200);")
        self.mplFigureCanvas.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mplFigureCanvas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mplFigureCanvas.setLineWidth(0)
        self.mplFigureCanvas.setObjectName("mplFigureCanvas")
        self.frame_7 = QtWidgets.QFrame(self.mplFigureCanvas)
        self.frame_7.setGeometry(QtCore.QRect(20, 20, 361, 80))
        self.frame_7.setStyleSheet("QFrame {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 0px solid rgb(52, 59, 72);\n"
"    border-radius: 18px;    \n"
"    background-color: rgb(93, 93, 93);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:checked {    \n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.resetViewButton = QtWidgets.QPushButton(self.frame_7)
        self.resetViewButton.setGeometry(QtCore.QRect(30, 20, 40, 40))
        self.resetViewButton.setToolTip("Reset plot area")
        self.resetViewButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-reload.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resetViewButton.setIcon(icon4)
        self.resetViewButton.setObjectName("resetViewButton")
        self.panViewButton = QtWidgets.QPushButton(self.frame_7)
        self.panViewButton.setGeometry(QtCore.QRect(90, 20, 40, 40))
        self.panViewButton.setCursor(QtCore.Qt.ArrowCursor)
        self.panViewButton.setToolTip("Pan mode: move plot region by dragging")
        self.panViewButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-move.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.panViewButton.setIcon(icon5)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.panViewButton.setObjectName("panViewButton")
        self.zoomViewButton = QtWidgets.QPushButton(self.frame_7)
        self.zoomViewButton.setGeometry(QtCore.QRect(150, 20, 40, 40))
        self.zoomViewButton.setCursor(QtCore.Qt.ArrowCursor)
        self.zoomViewButton.setToolTip("Zoom mode: select a plot region to enlarge")
        self.zoomViewButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zoomViewButton.setIcon(icon6)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.zoomViewButton.setObjectName("zoomViewButton")
        self.selectViewButton = QtWidgets.QPushButton(self.frame_7)
        self.selectViewButton.setGeometry(QtCore.QRect(210, 20, 41, 41))
        self.selectViewButton.setCursor(QtCore.Qt.CrossCursor)
        self.selectViewButton.setToolTip("")
        self.selectViewButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-location-pin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectViewButton.setIcon(icon7)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.selectViewButton.setObjectName("selectViewButton")
        self.swapXYButton = QtWidgets.QPushButton(self.frame_7)
        self.swapXYButton.setGeometry(QtCore.QRect(270, 20, 71, 41))
        self.swapXYButton.setCursor(QtCore.Qt.CrossCursor)
        self.swapXYButton.setToolTip("")
        self.swapXYButton.setStyleSheet("QPushButton {\n"
"    border: 0px solid rgb(52, 59, 72);\n"
"    border-radius: 15px;    \n"
"    background-color: rgb(93, 93, 93);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.swapXYButton.setCheckable(True)
        self.swapXYButton.setChecked(True)
        self.swapXYButton.setAutoExclusive(True)
        self.swapXYButton.setObjectName("swapXYButton")
        self.gridLayout.addWidget(self.mplFigureCanvas, 0, 3, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.frameCenter)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.dataTableView = TableView(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataTableView.sizePolicy().hasHeightForWidth())
        self.dataTableView.setSizePolicy(sizePolicy)
        self.dataTableView.setMinimumSize(QtCore.QSize(0, 105))
        self.dataTableView.setMaximumSize(QtCore.QSize(16777215, 105))
        self.dataTableView.setStyleSheet("QTableWidget {    \n"
"    background-color: rgb(63, 63, 63);\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"    border-color: rgb(44, 49, 60);\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"QHeaderView::section{\n"
"    background-color: rgb(93, 93, 93);\n"
"    max-width: 30px;\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"    border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {    \n"
"    background-color: rgb(93, 93, 93);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(32, 34, 42);\n"
"    background-color: rgb(93,93, 93);\n"
"    padding: 3px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"TableView\n"
"{\n"
"    background-color: rgb(63, 63, 63);\n"
"    color: rgb(200,200,200);\n"
"}")
        self.dataTableView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dataTableView.setObjectName("dataTableView")
        self.horizontalLayout_5.addWidget(self.dataTableView)
        self.gridLayout.addWidget(self.frame_6, 1, 3, 1, 1)
        self.frame = QtWidgets.QFrame(self.frameCenter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(70, 0))
        self.frame.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame.setStyleSheet("QFrame {\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.modeSelectButton = QtWidgets.QPushButton(self.frame)
        self.modeSelectButton.setMinimumSize(QtCore.QSize(0, 70))
        self.modeSelectButton.setMaximumSize(QtCore.QSize(16777215, 70))
        self.modeSelectButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-location-pin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modeSelectButton.setIcon(icon8)
        self.modeSelectButton.setIconSize(QtCore.QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setChecked(True)
        self.modeSelectButton.setAutoExclusive(True)
        self.modeSelectButton.setObjectName("modeSelectButton")
        self.verticalLayout_5.addWidget(self.modeSelectButton)
        self.modeTagButton = QtWidgets.QPushButton(self.frame)
        self.modeTagButton.setMinimumSize(QtCore.QSize(0, 70))
        self.modeTagButton.setMaximumSize(QtCore.QSize(16777215, 70))
        self.modeTagButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modeTagButton.setIcon(icon9)
        self.modeTagButton.setIconSize(QtCore.QSize(24, 24))
        self.modeTagButton.setCheckable(True)
        self.modeTagButton.setAutoExclusive(True)
        self.modeTagButton.setObjectName("modeTagButton")
        self.verticalLayout_5.addWidget(self.modeTagButton)
        self.modePlotButton = QtWidgets.QPushButton(self.frame)
        self.modePlotButton.setMinimumSize(QtCore.QSize(0, 70))
        self.modePlotButton.setMaximumSize(QtCore.QSize(16777215, 70))
        self.modePlotButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-chart-line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modePlotButton.setIcon(icon10)
        self.modePlotButton.setIconSize(QtCore.QSize(24, 24))
        self.modePlotButton.setCheckable(True)
        self.modePlotButton.setAutoExclusive(True)
        self.modePlotButton.setObjectName("modePlotButton")
        self.verticalLayout_5.addWidget(self.modePlotButton)
        self.modeFitButton = QtWidgets.QPushButton(self.frame)
        self.modeFitButton.setMinimumSize(QtCore.QSize(0, 70))
        self.modeFitButton.setMaximumSize(QtCore.QSize(16777215, 70))
        self.modeFitButton.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-speedometer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modeFitButton.setIcon(icon11)
        self.modeFitButton.setIconSize(QtCore.QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)
        self.modeFitButton.setObjectName("modeFitButton")
        self.verticalLayout_5.addWidget(self.modeFitButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.gridLayout.addWidget(self.frame, 0, 0, 3, 1)
        self.frame_3 = QtWidgets.QFrame(self.frameCenter)
        self.frame_3.setStyleSheet("QFrame {\n"
"    background-color: rgb(47, 47, 47);\n"
"    color: rgb(170, 170, 170);\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(15, -1, 15, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame1 = QtWidgets.QFrame(self.frame_3)
        self.frame1.setStyleSheet("QPushButton {\n"
"    border: 0px solid rgb(52, 59, 72);\n"
"    border-radius: 15px;    \n"
"    background-color: rgb(93, 93, 93);\n"
"    color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(196, 150, 250);\n"
"    border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.frame1.setObjectName("frame1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame1)
        self.verticalLayout_6.setContentsMargins(-1, -1, 4, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.newRowButton = QtWidgets.QPushButton(self.frame1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy)
        self.newRowButton.setMinimumSize(QtCore.QSize(100, 30))
        self.newRowButton.setToolTip("")
        self.newRowButton.setText("+ NEW   ")
        self.newRowButton.setObjectName("newRowButton")
        self.verticalLayout_6.addWidget(self.newRowButton)
        self.deleteRowButton = QtWidgets.QPushButton(self.frame1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteRowButton.sizePolicy().hasHeightForWidth())
        self.deleteRowButton.setSizePolicy(sizePolicy)
        self.deleteRowButton.setMinimumSize(QtCore.QSize(100, 30))
        self.deleteRowButton.setToolTip("")
        self.deleteRowButton.setText("- DELETE  ")
        self.deleteRowButton.setObjectName("deleteRowButton")
        self.verticalLayout_6.addWidget(self.deleteRowButton)
        self.clearAllButton = QtWidgets.QPushButton(self.frame1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearAllButton.sizePolicy().hasHeightForWidth())
        self.clearAllButton.setSizePolicy(sizePolicy)
        self.clearAllButton.setMinimumSize(QtCore.QSize(100, 30))
        self.clearAllButton.setToolTip("")
        self.clearAllButton.setText("CLEAR ALL")
        self.clearAllButton.setObjectName("clearAllButton")
        self.verticalLayout_6.addWidget(self.clearAllButton)
        self.horizontalLayout_2.addWidget(self.frame1)
        self.datasetListView = ListView(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datasetListView.sizePolicy().hasHeightForWidth())
        self.datasetListView.setSizePolicy(sizePolicy)
        self.datasetListView.setMinimumSize(QtCore.QSize(0, 100))
        self.datasetListView.setMaximumSize(QtCore.QSize(230, 100))
        self.datasetListView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.datasetListView.setObjectName("datasetListView")
        self.horizontalLayout_2.addWidget(self.datasetListView)
        self.gridLayout.addWidget(self.frame_3, 1, 1, 1, 1)
        self.pagesStackedWidget = QtWidgets.QStackedWidget(self.frameCenter)
        self.pagesStackedWidget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.pagesStackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.pagesStackedWidget.setObjectName("pagesStackedWidget")
        self.modeSelectPage = QtWidgets.QWidget()
        self.modeSelectPage.setObjectName("modeSelectPage")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.modeSelectPage)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_8 = QtWidgets.QFrame(self.modeSelectPage)
        self.frame_8.setStyleSheet("QFrame {\n"
"    background-color: rgb(47, 47, 47);\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: rgb(93, 93, 93);\n"
"    border: 0px solid rgb(52, 59, 72);\n"
"    border-radius: 5px;    \n"
"}")
        self.frame_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_4 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(7)
        font.setItalic(False)
        font.setBold(False)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_12.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_12.addItem(spacerItem1)
        self.imageOptionsVerticalGroupBox = QtWidgets.QGroupBox(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageOptionsVerticalGroupBox.sizePolicy().hasHeightForWidth())
        self.imageOptionsVerticalGroupBox.setSizePolicy(sizePolicy)
        self.imageOptionsVerticalGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.imageOptionsVerticalGroupBox.setTitle("FILTERING")
        self.imageOptionsVerticalGroupBox.setObjectName("imageOptionsVerticalGroupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.imageOptionsVerticalGroupBox)
        self.gridLayout_8.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(7)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.bgndSubtractYCheckBox = QtWidgets.QCheckBox(self.imageOptionsVerticalGroupBox)
        self.bgndSubtractYCheckBox.setToolTip("Background subtraction along Y")
        self.bgndSubtractYCheckBox.setText("Y BGND SUBTRACT")
        self.bgndSubtractYCheckBox.setObjectName("bgndSubtractYCheckBox")
        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 2, 1, 1, 1)
        self.edgeFilterCheckBox = QtWidgets.QCheckBox(self.imageOptionsVerticalGroupBox)
        self.edgeFilterCheckBox.setToolTip("")
        self.edgeFilterCheckBox.setText("EDGE FILTER")
        self.edgeFilterCheckBox.setObjectName("edgeFilterCheckBox")
        self.gridLayout_8.addWidget(self.edgeFilterCheckBox, 1, 0, 1, 1)
        self.bgndSubtractXCheckBox = QtWidgets.QCheckBox(self.imageOptionsVerticalGroupBox)
        self.bgndSubtractXCheckBox.setToolTip("Background subtraction along X")
        self.bgndSubtractXCheckBox.setText("X BGND SUBTRACT")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)
        self.bgndSubtractXCheckBox.setObjectName("bgndSubtractXCheckBox")
        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 2, 0, 1, 1)
        self.topHatCheckBox = QtWidgets.QCheckBox(self.imageOptionsVerticalGroupBox)
        self.topHatCheckBox.setToolTip("")
        self.topHatCheckBox.setText("TOP-HAT FILTER")
        self.topHatCheckBox.setObjectName("topHatCheckBox")
        self.gridLayout_8.addWidget(self.topHatCheckBox, 0, 0, 1, 1)
        self.waveletCheckBox = QtWidgets.QCheckBox(self.imageOptionsVerticalGroupBox)
        self.waveletCheckBox.setToolTip("")
        self.waveletCheckBox.setText("WAVELET DENOISE")
        self.waveletCheckBox.setObjectName("waveletCheckBox")
        self.gridLayout_8.addWidget(self.waveletCheckBox, 0, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.imageOptionsVerticalGroupBox)
        self.colorGridGroupBox = QtWidgets.QGroupBox(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorGridGroupBox.sizePolicy().hasHeightForWidth())
        self.colorGridGroupBox.setSizePolicy(sizePolicy)
        self.colorGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.colorGridGroupBox.setTitle("COLORS")
        self.colorGridGroupBox.setObjectName("colorGridGroupBox")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.colorGridGroupBox)
        self.gridLayout_9.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.colorComboBox = QtWidgets.QComboBox(self.colorGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy)
        self.colorComboBox.setMinimumSize(QtCore.QSize(0, 30))
        self.colorComboBox.setToolTip("")
        self.colorComboBox.setIconSize(QtCore.QSize(100, 10))
        self.colorComboBox.setFrame(True)
        self.colorComboBox.setObjectName("colorComboBox")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/PuOr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorComboBox.addItem(icon12, "")
        self.colorComboBox.setItemText(0, "PuOr")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/RdYlBu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorComboBox.addItem(icon13, "")
        self.colorComboBox.setItemText(1, "RdYlBu")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/bwr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorComboBox.addItem(icon14, "")
        self.colorComboBox.setItemText(2, "bwr")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/viridis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorComboBox.addItem(icon15, "")
        self.colorComboBox.setItemText(3, "viridis")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/cividis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorComboBox.addItem(icon16, "")
        self.colorComboBox.setItemText(4, "cividis")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icons/gray.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.colorComboBox.addItem(icon17, "")
        self.colorComboBox.setItemText(5, "gray")
        self.gridLayout_9.addWidget(self.colorComboBox, 0, 0, 1, 1)
        self.logScaleCheckBox = QtWidgets.QCheckBox(self.colorGridGroupBox)
        self.logScaleCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText("LOG")
        self.logScaleCheckBox.setChecked(False)
        self.logScaleCheckBox.setObjectName("logScaleCheckBox")
        self.gridLayout_9.addWidget(self.logScaleCheckBox, 0, 1, 1, 1)
        self.rangeSliderMax = QtWidgets.QSlider(self.colorGridGroupBox)
        self.rangeSliderMax.setMinimumSize(QtCore.QSize(0, 18))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setProperty("value", 99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(QtCore.Qt.Horizontal)
        self.rangeSliderMax.setObjectName("rangeSliderMax")
        self.gridLayout_9.addWidget(self.rangeSliderMax, 3, 0, 1, 1)
        self.rangeSliderMin = QtWidgets.QSlider(self.colorGridGroupBox)
        self.rangeSliderMin.setMinimumSize(QtCore.QSize(0, 18))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(QtCore.Qt.Horizontal)
        self.rangeSliderMin.setObjectName("rangeSliderMin")
        self.gridLayout_9.addWidget(self.rangeSliderMin, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.colorGridGroupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_9.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.colorGridGroupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_9.addWidget(self.label_3, 3, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.colorGridGroupBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 96, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem3)
        self.xyzDataGridGroupBox = QtWidgets.QGroupBox(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xyzDataGridGroupBox.sizePolicy().hasHeightForWidth())
        self.xyzDataGridGroupBox.setSizePolicy(sizePolicy)
        self.xyzDataGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.xyzDataGridGroupBox.setObjectName("xyzDataGridGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.xyzDataGridGroupBox)
        self.gridLayout_4.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.xComboBox = QtWidgets.QComboBox(self.xyzDataGridGroupBox)
        self.xComboBox.setMinimumSize(QtCore.QSize(250, 30))
        self.xComboBox.setObjectName("xComboBox")
        self.gridLayout_4.addWidget(self.xComboBox, 3, 1, 1, 1)
        self.zComboBox = QtWidgets.QComboBox(self.xyzDataGridGroupBox)
        self.zComboBox.setMinimumSize(QtCore.QSize(250, 30))
        self.zComboBox.setStyleSheet("")
        self.zComboBox.setCurrentText("")
        self.zComboBox.setFrame(True)
        self.zComboBox.setObjectName("zComboBox")
        self.gridLayout_4.addWidget(self.zComboBox, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.xyzDataGridGroupBox)
        self.label_13.setText("Z")
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 1, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.xyzDataGridGroupBox)
        self.label_12.setText("AXIS 1")
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 3, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.xyzDataGridGroupBox)
        self.label_14.setText("AXIS 2")
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 4, 0, 1, 1)
        self.yComboBox = QtWidgets.QComboBox(self.xyzDataGridGroupBox)
        self.yComboBox.setMinimumSize(QtCore.QSize(250, 30))
        self.yComboBox.setObjectName("yComboBox")
        self.gridLayout_4.addWidget(self.yComboBox, 4, 1, 1, 1)
        self.verticalLayout_12.addWidget(self.xyzDataGridGroupBox)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem4)
        self.calibrateXGridGroupBox = QtWidgets.QGroupBox(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibrateXGridGroupBox.sizePolicy().hasHeightForWidth())
        self.calibrateXGridGroupBox.setSizePolicy(sizePolicy)
        self.calibrateXGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.calibrateXGridGroupBox.setMaximumSize(QtCore.QSize(320, 16777215))
        self.calibrateXGridGroupBox.setTitle("CALIBRATE X")
        self.calibrateXGridGroupBox.setObjectName("calibrateXGridGroupBox")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.calibrateXGridGroupBox)
        self.gridLayout_10.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawX1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX1LineEdit.setSizePolicy(sizePolicy)
        self.rawX1LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.rawX1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawX1LineEdit.setToolTip("")
        self.rawX1LineEdit.setText("0.0")
        self.rawX1LineEdit.setObjectName("rawX1LineEdit")
        self.gridLayout_10.addWidget(self.rawX1LineEdit, 0, 2, 1, 1)
        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapX2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX2LineEdit.setSizePolicy(sizePolicy)
        self.mapX2LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.mapX2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapX2LineEdit.setToolTip("")
        self.mapX2LineEdit.setText("1.0")
        self.mapX2LineEdit.setObjectName("mapX2LineEdit")
        self.gridLayout_10.addWidget(self.mapX2LineEdit, 1, 4, 1, 1)
        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawX2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX2LineEdit.setSizePolicy(sizePolicy)
        self.rawX2LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.rawX2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawX2LineEdit.setToolTip("")
        self.rawX2LineEdit.setText("1.0")
        self.rawX2LineEdit.setObjectName("rawX2LineEdit")
        self.gridLayout_10.addWidget(self.rawX2LineEdit, 1, 2, 1, 1)
        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapX1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX1LineEdit.setSizePolicy(sizePolicy)
        self.mapX1LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.mapX1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapX1LineEdit.setToolTip("")
        self.mapX1LineEdit.setInputMask("")
        self.mapX1LineEdit.setText("0.0")
        self.mapX1LineEdit.setObjectName("mapX1LineEdit")
        self.gridLayout_10.addWidget(self.mapX1LineEdit, 0, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setText("<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">1</span></p></body></html>")
        self.label_15.setObjectName("label_15")
        self.gridLayout_10.addWidget(self.label_15, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setText("<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">2</span></p></body></html>")
        self.label_16.setObjectName("label_16")
        self.gridLayout_10.addWidget(self.label_16, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setText("<html><head/><body><p align=\"right\">→ X<span style=\" vertical-align:sub;\">1</span>\'</p></body></html>")
        self.label_17.setObjectName("label_17")
        self.gridLayout_10.addWidget(self.label_17, 0, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setText("<html><head/><body><p align=\"right\">→ X<span style=\" vertical-align:sub;\">2</span>\'</p></body></html>")
        self.label_18.setObjectName("label_18")
        self.gridLayout_10.addWidget(self.label_18, 1, 3, 1, 1)
        self.calibrateX1Button = QtWidgets.QPushButton(self.calibrateXGridGroupBox)
        self.calibrateX1Button.setMinimumSize(QtCore.QSize(30, 30))
        self.calibrateX1Button.setToolTip("Calibrate x1, allows selection of coordinate inside plot")
        self.calibrateX1Button.setText("")
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icons/16x16/cil-at.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.calibrateX1Button.setIcon(icon18)
        self.calibrateX1Button.setObjectName("calibrateX1Button")
        self.gridLayout_10.addWidget(self.calibrateX1Button, 0, 0, 1, 1)
        self.calibrateX2Button = QtWidgets.QPushButton(self.calibrateXGridGroupBox)
        self.calibrateX2Button.setMinimumSize(QtCore.QSize(30, 30))
        self.calibrateX2Button.setToolTip("Calibrate x2, allows selection of coordinate inside plot")
        self.calibrateX2Button.setText("")
        self.calibrateX2Button.setIcon(icon18)
        self.calibrateX2Button.setObjectName("calibrateX2Button")
        self.gridLayout_10.addWidget(self.calibrateX2Button, 1, 0, 1, 1)
        self.verticalLayout_12.addWidget(self.calibrateXGridGroupBox)
        self.calibrateYGridGroupBox = QtWidgets.QGroupBox(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibrateYGridGroupBox.sizePolicy().hasHeightForWidth())
        self.calibrateYGridGroupBox.setSizePolicy(sizePolicy)
        self.calibrateYGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.calibrateYGridGroupBox.setMaximumSize(QtCore.QSize(320, 16777215))
        self.calibrateYGridGroupBox.setToolTip("")
        self.calibrateYGridGroupBox.setTitle("CALIBRATE Y")
        self.calibrateYGridGroupBox.setObjectName("calibrateYGridGroupBox")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.calibrateYGridGroupBox)
        self.gridLayout_11.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawY2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY2LineEdit.setSizePolicy(sizePolicy)
        self.rawY2LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.rawY2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawY2LineEdit.setToolTip("")
        self.rawY2LineEdit.setText("1.0")
        self.rawY2LineEdit.setObjectName("rawY2LineEdit")
        self.gridLayout_11.addWidget(self.rawY2LineEdit, 1, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setText("<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span></p></body></html>")
        self.label_19.setObjectName("label_19")
        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)
        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapY1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY1LineEdit.setSizePolicy(sizePolicy)
        self.mapY1LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.mapY1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapY1LineEdit.setToolTip("")
        self.mapY1LineEdit.setText("0.0")
        self.mapY1LineEdit.setObjectName("mapY1LineEdit")
        self.gridLayout_11.addWidget(self.mapY1LineEdit, 0, 4, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setText("<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span></p></body></html>")
        self.label_20.setObjectName("label_20")
        self.gridLayout_11.addWidget(self.label_20, 1, 1, 1, 1)
        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapY2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY2LineEdit.setSizePolicy(sizePolicy)
        self.mapY2LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.mapY2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapY2LineEdit.setToolTip("")
        self.mapY2LineEdit.setText("1.0")
        self.mapY2LineEdit.setObjectName("mapY2LineEdit")
        self.gridLayout_11.addWidget(self.mapY2LineEdit, 1, 4, 1, 1)
        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawY1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY1LineEdit.setSizePolicy(sizePolicy)
        self.rawY1LineEdit.setMinimumSize(QtCore.QSize(80, 30))
        self.rawY1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawY1LineEdit.setToolTip("")
        self.rawY1LineEdit.setText("0.0")
        self.rawY1LineEdit.setObjectName("rawY1LineEdit")
        self.gridLayout_11.addWidget(self.rawY1LineEdit, 0, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setText("<html><head/><body><p align=\"right\">→ Y<span style=\" vertical-align:sub;\">1</span>\'</p></body></html>")
        self.label_21.setObjectName("label_21")
        self.gridLayout_11.addWidget(self.label_21, 0, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setText("<html><head/><body><p align=\"right\">→ Y<span style=\" vertical-align:sub;\">2</span>\'</p></body></html>")
        self.label_22.setObjectName("label_22")
        self.gridLayout_11.addWidget(self.label_22, 1, 3, 1, 1)
        self.calibrateY2Button = QtWidgets.QPushButton(self.calibrateYGridGroupBox)
        self.calibrateY2Button.setMinimumSize(QtCore.QSize(30, 30))
        self.calibrateY2Button.setToolTip("Calibrate y2, allows selection of coordinate inside plot")
        self.calibrateY2Button.setText("")
        self.calibrateY2Button.setIcon(icon18)
        self.calibrateY2Button.setObjectName("calibrateY2Button")
        self.gridLayout_11.addWidget(self.calibrateY2Button, 1, 0, 1, 1)
        self.calibrateY1Button = QtWidgets.QPushButton(self.calibrateYGridGroupBox)
        self.calibrateY1Button.setMinimumSize(QtCore.QSize(30, 30))
        self.calibrateY1Button.setToolTip("Calibrate y1, allows selection of coordinate inside plot")
        self.calibrateY1Button.setText("")
        self.calibrateY1Button.setIcon(icon18)
        self.calibrateY1Button.setObjectName("calibrateY1Button")
        self.gridLayout_11.addWidget(self.calibrateY1Button, 0, 0, 1, 1)
        self.verticalLayout_12.addWidget(self.calibrateYGridGroupBox)
        self.calibratedCheckBox = QtWidgets.QCheckBox(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibratedCheckBox.sizePolicy().hasHeightForWidth())
        self.calibratedCheckBox.setSizePolicy(sizePolicy)
        self.calibratedCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.calibratedCheckBox.setText("TOGGLE CALIBRATION")
        self.calibratedCheckBox.setObjectName("calibratedCheckBox")
        self.verticalLayout_12.addWidget(self.calibratedCheckBox)
        self.verticalLayout_9.addWidget(self.frame_8)
        self.pagesStackedWidget.addWidget(self.modeSelectPage)
        self.modeTagPage = QtWidgets.QWidget()
        self.modeTagPage.setObjectName("modeTagPage")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.modeTagPage)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_9 = QtWidgets.QFrame(self.modeTagPage)
        self.frame_9.setStyleSheet("QFrame {\n"
"    background-color: rgb(47, 47, 47);\n"
"}")
        self.frame_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_5 = QtWidgets.QLabel(self.frame_9)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_13.addWidget(self.label_5)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_13.addItem(spacerItem5)
        self.noTagRadioButton = QtWidgets.QRadioButton(self.frame_9)
        self.noTagRadioButton.setToolTip("")
        self.noTagRadioButton.setText("NO TAG")
        self.noTagRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.noTagRadioButton.setChecked(True)
        self.noTagRadioButton.setObjectName("noTagRadioButton")
        self.verticalLayout_13.addWidget(self.noTagRadioButton)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_13.addItem(spacerItem6)
        self.tagChoicesFrame = QtWidgets.QFrame(self.frame_9)
        self.tagChoicesFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tagChoicesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tagChoicesFrame.setObjectName("tagChoicesFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tagChoicesFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_23 = QtWidgets.QLabel(self.tagChoicesFrame)
        self.label_23.setToolTip("")
        self.label_23.setStyleSheet("font: 10pt \"Roboto\";")
        self.label_23.setText("DISPERSIVE TRANSITION")
        self.label_23.setObjectName("label_23")
        self.verticalLayout_4.addWidget(self.label_23)
        self.tagDispersiveBareRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveBareRadioButton.setToolTip("")
        self.tagDispersiveBareRadioButton.setText("BY BARE STATES")
        self.tagDispersiveBareRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagDispersiveBareRadioButton.setObjectName("tagDispersiveBareRadioButton")
        self.verticalLayout_4.addWidget(self.tagDispersiveBareRadioButton)
        self.tagDispersiveDressedRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveDressedRadioButton.setToolTip("")
        self.tagDispersiveDressedRadioButton.setText("BY DRESSED INDICES")
        self.tagDispersiveDressedRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagDispersiveDressedRadioButton.setObjectName("tagDispersiveDressedRadioButton")
        self.verticalLayout_4.addWidget(self.tagDispersiveDressedRadioButton)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem7)
        self.label_24 = QtWidgets.QLabel(self.tagChoicesFrame)
        self.label_24.setToolTip("")
        self.label_24.setStyleSheet("font: 10pt \"Roboto\";")
        self.label_24.setText("AVOIDED CROSSING")
        self.label_24.setObjectName("label_24")
        self.verticalLayout_4.addWidget(self.label_24)
        self.tagCrossingRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.tagCrossingRadioButton.setToolTip("")
        self.tagCrossingRadioButton.setText("INFER WHEN FITTING")
        self.tagCrossingRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagCrossingRadioButton.setObjectName("tagCrossingRadioButton")
        self.verticalLayout_4.addWidget(self.tagCrossingRadioButton)
        self.tagCrossingDressedRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.tagCrossingDressedRadioButton.setToolTip("")
        self.tagCrossingDressedRadioButton.setText("BY DRESSED INDICES")
        self.tagCrossingDressedRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagCrossingDressedRadioButton.setObjectName("tagCrossingDressedRadioButton")
        self.verticalLayout_4.addWidget(self.tagCrossingDressedRadioButton)
        self.verticalLayout_13.addWidget(self.tagChoicesFrame)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_13.addItem(spacerItem8)
        self.tagDressedGroupBox = QtWidgets.QGroupBox(self.frame_9)
        self.tagDressedGroupBox.setEnabled(True)
        self.tagDressedGroupBox.setToolTip("")
        self.tagDressedGroupBox.setStyleSheet("QGroupBox {\n"
"    font: 10pt \"Roboto\";\n"
"}")
        self.tagDressedGroupBox.setTitle("TAG BY DRESSED INDICES")
        self.tagDressedGroupBox.setObjectName("tagDressedGroupBox")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_30 = QtWidgets.QLabel(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setToolTip("")
        self.label_30.setText("INITIAL")
        self.label_30.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_30.setObjectName("label_30")
        self.gridLayout_13.addWidget(self.label_30, 0, 3, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setToolTip("")
        self.label_29.setText("PHOTONS")
        self.label_29.setObjectName("label_29")
        self.gridLayout_13.addWidget(self.label_29, 0, 0, 1, 1)
        self.phNumberDressedSpinBox = QtWidgets.QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy)
        self.phNumberDressedSpinBox.setMinimumSize(QtCore.QSize(60, 0))
        self.phNumberDressedSpinBox.setMinimum(1)
        self.phNumberDressedSpinBox.setObjectName("phNumberDressedSpinBox")
        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 0, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem9, 0, 2, 1, 1)
        self.finalStateSpinBox = QtWidgets.QSpinBox(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finalStateSpinBox.sizePolicy().hasHeightForWidth())
        self.finalStateSpinBox.setSizePolicy(sizePolicy)
        self.finalStateSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.finalStateSpinBox.setProperty("value", 1)
        self.finalStateSpinBox.setObjectName("finalStateSpinBox")
        self.gridLayout_13.addWidget(self.finalStateSpinBox, 1, 4, 1, 1)
        self.initialStateSpinBox = QtWidgets.QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.initialStateSpinBox.sizePolicy().hasHeightForWidth())
        self.initialStateSpinBox.setSizePolicy(sizePolicy)
        self.initialStateSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.initialStateSpinBox.setObjectName("initialStateSpinBox")
        self.gridLayout_13.addWidget(self.initialStateSpinBox, 0, 4, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.tagDressedGroupBox)
        self.label_31.setToolTip("")
        self.label_31.setText("FINAL")
        self.label_31.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout_13.addWidget(self.label_31, 1, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_13.addItem(spacerItem10, 0, 5, 1, 1)
        self.verticalLayout_13.addWidget(self.tagDressedGroupBox)
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_13.addItem(spacerItem11)
        self.tagBareGroupBox = QtWidgets.QGroupBox(self.frame_9)
        self.tagBareGroupBox.setEnabled(True)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setStyleSheet("QGroupBox {\n"
"    font: 10pt \"Roboto\";\n"
"}")
        self.tagBareGroupBox.setTitle("TAG BY BARE STATES")
        self.tagBareGroupBox.setFlat(False)
        self.tagBareGroupBox.setObjectName("tagBareGroupBox")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tagBareGroupBox)
        self.gridLayout_12.setContentsMargins(-1, 27, -1, -1)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.subsysNamesLineEdit = StrTupleLineEdit(self.tagBareGroupBox)
        self.subsysNamesLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.subsysNamesLineEdit.setText("")
        self.subsysNamesLineEdit.setPlaceholderText(" <subsystem name 1>, ...")
        self.subsysNamesLineEdit.setClearButtonEnabled(True)
        self.subsysNamesLineEdit.setObjectName("subsysNamesLineEdit")
        self.gridLayout_12.addWidget(self.subsysNamesLineEdit, 0, 0, 1, 5)
        self.label_25 = QtWidgets.QLabel(self.tagBareGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setText("PHOTONS")
        self.label_25.setObjectName("label_25")
        self.gridLayout_12.addWidget(self.label_25, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem12, 1, 2, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.tagBareGroupBox)
        self.label_28.setText("INITIAL")
        self.label_28.setObjectName("label_28")
        self.gridLayout_12.addWidget(self.label_28, 1, 3, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.tagBareGroupBox)
        self.label_26.setText("FINAL")
        self.label_26.setObjectName("label_26")
        self.gridLayout_12.addWidget(self.label_26, 2, 3, 1, 1)
        self.finalStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.finalStateLineEdit.setPlaceholderText("<level subsys 1>, <level subsys2>, ...")
        self.finalStateLineEdit.setObjectName("finalStateLineEdit")
        self.gridLayout_12.addWidget(self.finalStateLineEdit, 2, 4, 1, 1)
        self.phNumberBareSpinBox = QtWidgets.QSpinBox(self.tagBareGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy)
        self.phNumberBareSpinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.phNumberBareSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)
        self.phNumberBareSpinBox.setObjectName("phNumberBareSpinBox")
        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 1, 1, 1, 1)
        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.initialStateLineEdit.setPlaceholderText("<level subsys 1>, <level subsys2>, ...")
        self.initialStateLineEdit.setObjectName("initialStateLineEdit")
        self.gridLayout_12.addWidget(self.initialStateLineEdit, 1, 4, 1, 1)
        self.verticalLayout_13.addWidget(self.tagBareGroupBox)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem13)
        self.verticalLayout_10.addWidget(self.frame_9)
        self.pagesStackedWidget.addWidget(self.modeTagPage)
        self.gridLayout.addWidget(self.pagesStackedWidget, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frameCenter)
        self.horizontalLayout.addWidget(self.frameMain)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pagesStackedWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonMinimize, QtCore.SIGNAL("clicked()"), MainWindow.showMinimized)
        QtCore.QObject.connect(self.buttonClose, QtCore.SIGNAL("clicked()"), MainWindow.close)
        QtCore.QObject.connect(self.buttonMaximize, QtCore.SIGNAL("clicked()"), MainWindow.showMaximized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.bgndSubtractXCheckBox, self.bgndSubtractYCheckBox)
        MainWindow.setTabOrder(self.bgndSubtractYCheckBox, self.waveletCheckBox)
        MainWindow.setTabOrder(self.waveletCheckBox, self.topHatCheckBox)
        MainWindow.setTabOrder(self.topHatCheckBox, self.edgeFilterCheckBox)
        MainWindow.setTabOrder(self.edgeFilterCheckBox, self.colorComboBox)
        MainWindow.setTabOrder(self.colorComboBox, self.logScaleCheckBox)
        MainWindow.setTabOrder(self.logScaleCheckBox, self.yComboBox)
        MainWindow.setTabOrder(self.yComboBox, self.zComboBox)
        MainWindow.setTabOrder(self.zComboBox, self.xComboBox)
        MainWindow.setTabOrder(self.xComboBox, self.rawX1LineEdit)
        MainWindow.setTabOrder(self.rawX1LineEdit, self.calibrateX2Button)
        MainWindow.setTabOrder(self.calibrateX2Button, self.mapX2LineEdit)
        MainWindow.setTabOrder(self.mapX2LineEdit, self.rawX2LineEdit)
        MainWindow.setTabOrder(self.rawX2LineEdit, self.mapX1LineEdit)
        MainWindow.setTabOrder(self.mapX1LineEdit, self.calibrateX1Button)
        MainWindow.setTabOrder(self.calibrateX1Button, self.rawY2LineEdit)
        MainWindow.setTabOrder(self.rawY2LineEdit, self.calibrateY2Button)
        MainWindow.setTabOrder(self.calibrateY2Button, self.mapY1LineEdit)
        MainWindow.setTabOrder(self.mapY1LineEdit, self.calibrateY1Button)
        MainWindow.setTabOrder(self.calibrateY1Button, self.mapY2LineEdit)
        MainWindow.setTabOrder(self.mapY2LineEdit, self.rawY1LineEdit)
        MainWindow.setTabOrder(self.rawY1LineEdit, self.tagDispersiveBareRadioButton)
        MainWindow.setTabOrder(self.tagDispersiveBareRadioButton, self.tagDispersiveDressedRadioButton)
        MainWindow.setTabOrder(self.tagDispersiveDressedRadioButton, self.tagCrossingRadioButton)
        MainWindow.setTabOrder(self.tagCrossingRadioButton, self.tagCrossingDressedRadioButton)
        MainWindow.setTabOrder(self.tagCrossingDressedRadioButton, self.initialStateSpinBox)
        MainWindow.setTabOrder(self.initialStateSpinBox, self.finalStateSpinBox)
        MainWindow.setTabOrder(self.finalStateSpinBox, self.phNumberDressedSpinBox)
        MainWindow.setTabOrder(self.phNumberDressedSpinBox, self.subsysNamesLineEdit)
        MainWindow.setTabOrder(self.subsysNamesLineEdit, self.phNumberBareSpinBox)
        MainWindow.setTabOrder(self.phNumberBareSpinBox, self.initialStateLineEdit)
        MainWindow.setTabOrder(self.initialStateLineEdit, self.finalStateLineEdit)
        MainWindow.setTabOrder(self.finalStateLineEdit, self.resetViewButton)
        MainWindow.setTabOrder(self.resetViewButton, self.panViewButton)
        MainWindow.setTabOrder(self.panViewButton, self.zoomViewButton)
        MainWindow.setTabOrder(self.zoomViewButton, self.selectViewButton)
        MainWindow.setTabOrder(self.selectViewButton, self.swapXYButton)

    def retranslateUi(self, MainWindow):
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "datapyc", None, -1))
        self.swapXYButton.setText(QtWidgets.QApplication.translate("MainWindow", "X↔Y", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "SELECT", None, -1))
        self.colorComboBox.setCurrentText(QtWidgets.QApplication.translate("MainWindow", "PuOr", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "MIN", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "MAX", None, -1))
        self.xyzDataGridGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "DATA", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "TAG", None, -1))
        self.noTagRadioButton.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "RR", None, -1))
        self.tagDispersiveBareRadioButton.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "RR", None, -1))
        self.tagDispersiveDressedRadioButton.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "RR", None, -1))
        self.tagCrossingRadioButton.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "RR", None, -1))
        self.tagCrossingDressedRadioButton.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "RR", None, -1))
