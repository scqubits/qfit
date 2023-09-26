# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_window_test_merge.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QStackedWidget,
    QVBoxLayout, QWidget)

from qfit.widgets.calibration import CalibrationLineEdit
from qfit.widgets.data_extracting import (DataExtractingWidget, DatasetWidget, ListView, TableView)
from qfit.widgets.data_tagging import (DataTaggingWidget, IntTupleLineEdit, StrTupleLineEdit)
from qfit.widgets.mpl_canvas import (MplFigureCanvas, MplNavButtons)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1143, 812)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
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
"	font-size: 9pt;\n"
"}\n"
"\n"
"QLabel {\n"
"	color: rgb(170, 170, 170);\n"
"}\n"
"\n"
"/* LINE EDIT */\n"
"QLineEdit {\n"
"	color: rgb(170, 170, 170);\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
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
"  "
                        "  background: rgb(85, 170, 255);\n"
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
"	border-radius: 0"
                        "px;\n"
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
"	color: rgb(170, 170, 170);\n"
"}\n"
"\n"
"QCheckBox::indicator {"
                        "\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
" 	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"	border: 3px solid rgb(196, 150, 250);\n"
"   background: rgb(52, 59, 72);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"	border: 3px solid rgb(196, 150, 250);\n"
"   background: rgb(52, 59, 72);\n"
"	image: url(:/icons/svg/cil-check-alt.svg);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton {\n"
"	color: rgb(170, 170, 170);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(196, 150, 250);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"   border: 3px solid rgb(196, 150, 250);\n"
"   background: rgb(52, 59, 72);\n"
"   image: url(:/icons/svg/cil-check-alt.svg);\n"
"}\n"
"\n"
"\n"
"\n"
"/* SLIDERS */\n"
""
                        "QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
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
"    margin: "
                        "0px;\n"
"	border-radius: 9px;\n"
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
""
                        "}\n"
"\n"
"QSpinBox::up-arrow {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    image: url(:/icons/svg/cil-plus.svg) 1;\n"
"}\n"
"\n"
"QSpinBox::down-arrow {\n"
"    image: url(:/icons/svg/cil-minus.svg) 1;\n"
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
"	color: rgb(170, 170, 170);\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:hover{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"	background-color: rgb(27, 29, 35);\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-r"
                        "ight-radius: 3px;	\n"
" }\n"
" \n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item{\n"
"    min-height: 50px;\n"
"}\n"
"\n"
"\n"
"QTableWidget {	\n"
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
"QHeaderView::section{\n"
"	Background-color: rgb(39, 44, 54);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 60);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTa"
                        "bleWidget::horizontalHeader {	\n"
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
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy1)
        self.verticalLayout_7 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.fullWindowFrame = QFrame(self.centralWidget)
        self.fullWindowFrame.setObjectName(u"fullWindowFrame")
        self.fullWindowFrame.setMaximumSize(QSize(16777215, 16777215))
        self.fullWindowFrame.setFrameShape(QFrame.NoFrame)
        self.fullWindowFrame.setFrameShadow(QFrame.Raised)
        self.fullWindowFrame.setLineWidth(1)
        self.verticalLayout = QVBoxLayout(self.fullWindowFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.windowTitleFrame = QFrame(self.fullWindowFrame)
        self.windowTitleFrame.setObjectName(u"windowTitleFrame")
        self.windowTitleFrame.setMaximumSize(QSize(16777215, 40))
        self.windowTitleFrame.setFrameShape(QFrame.NoFrame)
        self.windowTitleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.windowTitleFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.windowTitleFrame)

        self.windowBodyFrame = QFrame(self.fullWindowFrame)
        self.windowBodyFrame.setObjectName(u"windowBodyFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.windowBodyFrame.sizePolicy().hasHeightForWidth())
        self.windowBodyFrame.setSizePolicy(sizePolicy2)
        self.windowBodyFrame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(33,33,33);\n"
"}")
        self.gridLayout = QGridLayout(self.windowBodyFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_frame = QFrame(self.windowBodyFrame)
        self.menu_frame.setObjectName(u"menu_frame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy3)
        self.menu_frame.setMinimumSize(QSize(190, 0))
        self.menu_frame.setMaximumSize(QSize(190, 16777215))
        self.menu_frame.setStyleSheet(u"QFrame {\n"
"	color: white;\n"
"	background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton {	\n"
"	font: 57 11pt \"Roboto Medium\";\n"
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
        self.modeSelectButton = QPushButton(self.menu_frame)
        self.modeSelectButton.setObjectName(u"modeSelectButton")
        self.modeSelectButton.setMinimumSize(QSize(120, 70))
        self.modeSelectButton.setMaximumSize(QSize(16777215, 70))
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.modeSelectButton.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/cil-list.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeSelectButton.setIcon(icon1)
        self.modeSelectButton.setIconSize(QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setChecked(True)
        self.modeSelectButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeSelectButton, 2, 0, 1, 2)

        self.modeTagButton = QPushButton(self.menu_frame)
        self.modeTagButton.setObjectName(u"modeTagButton")
        self.modeTagButton.setMinimumSize(QSize(120, 70))
        self.modeTagButton.setMaximumSize(QSize(120, 70))
        icon2 = QIcon()
        icon2.addFile(u":/icons/svg/cil-location-pin.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeTagButton.setIcon(icon2)
        self.modeTagButton.setIconSize(QSize(24, 24))
        self.modeTagButton.setCheckable(True)
        self.modeTagButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeTagButton, 3, 0, 1, 2)

        self.modeFitButton = QPushButton(self.menu_frame)
        self.modeFitButton.setObjectName(u"modeFitButton")
        self.modeFitButton.setMinimumSize(QSize(120, 70))
        self.modeFitButton.setMaximumSize(QSize(120, 70))
        icon3 = QIcon()
        icon3.addFile(u":/icons/svg/cil-speedometer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeFitButton.setIcon(icon3)
        self.modeFitButton.setIconSize(QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeFitButton, 5, 0, 1, 1)

        self.toggleMenuButton = QPushButton(self.menu_frame)
        self.toggleMenuButton.setObjectName(u"toggleMenuButton")
        sizePolicy2.setHeightForWidth(self.toggleMenuButton.sizePolicy().hasHeightForWidth())
        self.toggleMenuButton.setSizePolicy(sizePolicy2)
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
        icon4 = QIcon()
        icon4.addFile(u":/icons/svg/cil-menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleMenuButton.setIcon(icon4)
        self.toggleMenuButton.setIconSize(QSize(24, 24))
        self.toggleMenuButton.setAutoDefault(False)
        self.toggleMenuButton.setFlat(False)

        self.gridLayout_2.addWidget(self.toggleMenuButton, 1, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 6, 1, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_14, 0, 0, 1, 1)

        self.modePrefitButton = QPushButton(self.menu_frame)
        self.modePrefitButton.setObjectName(u"modePrefitButton")
        self.modePrefitButton.setMinimumSize(QSize(170, 70))
        self.modePrefitButton.setMaximumSize(QSize(120, 70))
        icon5 = QIcon()
        icon5.addFile(u":/icons/svg/cil-chart-line.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modePrefitButton.setIcon(icon5)
        self.modePrefitButton.setIconSize(QSize(24, 24))
        self.modePrefitButton.setCheckable(True)
        self.modePrefitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modePrefitButton, 4, 0, 1, 2)

        self.frame = QFrame(self.menu_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_10, 1, 3, 1, 1)

        self.calibrateYGridFrame = QFrame(self.frame)
        self.calibrateYGridFrame.setObjectName(u"calibrateYGridFrame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.calibrateYGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateYGridFrame.setSizePolicy(sizePolicy4)
        self.calibrateYGridFrame.setMinimumSize(QSize(330, 120))
        self.calibrateYGridFrame.setMaximumSize(QSize(320, 16777215))
#if QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	text-align: center;\n"
"}")
        self.gridLayout_11 = QGridLayout(self.calibrateYGridFrame)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(-1, 15, -1, -1)
        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY2LineEdit.setObjectName(u"mapY2LineEdit")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.mapY2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY2LineEdit.setSizePolicy(sizePolicy5)
        self.mapY2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 1, 4, 1, 1)

        self.label_19 = QLabel(self.calibrateYGridFrame)
        self.label_19.setObjectName(u"label_19")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy6)
        self.label_19.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)

        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY2LineEdit.setObjectName(u"rawY2LineEdit")
        sizePolicy5.setHeightForWidth(self.rawY2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY2LineEdit.setSizePolicy(sizePolicy5)
        self.rawY2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 1, 2, 1, 1)

        self.calibrateY2Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY2Button.setObjectName(u"calibrateY2Button")
        self.calibrateY2Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateY2Button.setToolTip(u"Calibrate y2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        icon6 = QIcon()
        icon6.addFile(u":/icons/svg/cil-at.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrateY2Button.setIcon(icon6)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 1, 0, 1, 1)

        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY1LineEdit.setObjectName(u"rawY1LineEdit")
        sizePolicy5.setHeightForWidth(self.rawY1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY1LineEdit.setSizePolicy(sizePolicy5)
        self.rawY1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 0, 2, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY1LineEdit.setObjectName(u"mapY1LineEdit")
        sizePolicy5.setHeightForWidth(self.mapY1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY1LineEdit.setSizePolicy(sizePolicy5)
        self.mapY1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 0, 4, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridFrame)
        self.label_22.setObjectName(u"label_22")
        sizePolicy6.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy6)
        self.label_22.setText(u"<html><head/><body><p align=\"right\">\u2192 Y<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_22, 1, 3, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridFrame)
        self.label_20.setObjectName(u"label_20")
        sizePolicy6.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy6)
        self.label_20.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_20, 1, 1, 1, 1)

        self.calibrateY1Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY1Button.setObjectName(u"calibrateY1Button")
        self.calibrateY1Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateY1Button.setToolTip(u"Calibrate y1, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY1Button.setIcon(icon6)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 0, 0, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridFrame)
        self.label_21.setObjectName(u"label_21")
        sizePolicy6.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy6)
        self.label_21.setText(u"<html><head/><body><p align=\"right\">\u2192 Y<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_21, 0, 3, 1, 1)


        self.gridLayout_14.addWidget(self.calibrateYGridFrame, 1, 2, 1, 1)

        self.calibratedCheckBox = QCheckBox(self.frame)
        self.calibratedCheckBox.setObjectName(u"calibratedCheckBox")
        sizePolicy5.setHeightForWidth(self.calibratedCheckBox.sizePolicy().hasHeightForWidth())
        self.calibratedCheckBox.setSizePolicy(sizePolicy5)
        self.calibratedCheckBox.setMinimumSize(QSize(0, 20))
        self.calibratedCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.calibratedCheckBox.setText(u"TOGGLE CALIBRATION")

        self.gridLayout_14.addWidget(self.calibratedCheckBox, 2, 2, 1, 1)

        self.calibrateXGridFrame = QFrame(self.frame)
        self.calibrateXGridFrame.setObjectName(u"calibrateXGridFrame")
        sizePolicy4.setHeightForWidth(self.calibrateXGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateXGridFrame.setSizePolicy(sizePolicy4)
        self.calibrateXGridFrame.setMinimumSize(QSize(330, 90))
        self.calibrateXGridFrame.setMaximumSize(QSize(320, 16777215))
        self.calibrateXGridFrame.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	text-align: center;\n"
"}")
        self.gridLayout_10 = QGridLayout(self.calibrateXGridFrame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setContentsMargins(-1, 9, -1, -1)
        self.label_17 = QLabel(self.calibrateXGridFrame)
        self.label_17.setObjectName(u"label_17")
        sizePolicy6.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy6)
        self.label_17.setText(u"<html><head/><body><p align=\"right\">\u2192 X<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_17, 1, 3, 1, 1)

        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX1LineEdit.setObjectName(u"mapX1LineEdit")
        sizePolicy5.setHeightForWidth(self.mapX1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX1LineEdit.setSizePolicy(sizePolicy5)
        self.mapX1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.mapX1LineEdit, 1, 4, 1, 1)

        self.label_18 = QLabel(self.calibrateXGridFrame)
        self.label_18.setObjectName(u"label_18")
        sizePolicy6.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy6)
        self.label_18.setText(u"<html><head/><body><p align=\"right\">\u2192 X<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_18, 2, 3, 1, 1)

        self.calibrateX1Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX1Button.setObjectName(u"calibrateX1Button")
        self.calibrateX1Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateX1Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX1Button.setIcon(icon6)

        self.gridLayout_10.addWidget(self.calibrateX1Button, 1, 0, 1, 1)

        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX1LineEdit.setObjectName(u"rawX1LineEdit")
        sizePolicy5.setHeightForWidth(self.rawX1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX1LineEdit.setSizePolicy(sizePolicy5)
        self.rawX1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.rawX1LineEdit, 1, 2, 1, 1)

        self.calibrateX2Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX2Button.setObjectName(u"calibrateX2Button")
        self.calibrateX2Button.setMinimumSize(QSize(30, 30))
#if QT_CONFIG(tooltip)
        self.calibrateX2Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX2Button.setIcon(icon6)

        self.gridLayout_10.addWidget(self.calibrateX2Button, 2, 0, 1, 1)

        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX2LineEdit.setObjectName(u"mapX2LineEdit")
        sizePolicy5.setHeightForWidth(self.mapX2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX2LineEdit.setSizePolicy(sizePolicy5)
        self.mapX2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.mapX2LineEdit, 2, 4, 1, 1)

        self.label_15 = QLabel(self.calibrateXGridFrame)
        self.label_15.setObjectName(u"label_15")
        sizePolicy6.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy6)
        self.label_15.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_15, 1, 1, 1, 1)

        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX2LineEdit.setObjectName(u"rawX2LineEdit")
        sizePolicy5.setHeightForWidth(self.rawX2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX2LineEdit.setSizePolicy(sizePolicy5)
        self.rawX2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.rawX2LineEdit, 2, 2, 1, 1)

        self.label_16 = QLabel(self.calibrateXGridFrame)
        self.label_16.setObjectName(u"label_16")
        sizePolicy6.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy6)
        self.label_16.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_16, 2, 1, 1, 1)


        self.gridLayout_14.addWidget(self.calibrateXGridFrame, 1, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_11, 1, 1, 1, 1)

        self.label_27 = QLabel(self.frame)
        self.label_27.setObjectName(u"label_27")
        sizePolicy5.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy5)
        self.label_27.setMinimumSize(QSize(0, 15))
        self.label_27.setStyleSheet(u"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_27.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_14.addWidget(self.label_27, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.frame, 5, 1, 1, 1)


        self.gridLayout.addWidget(self.menu_frame, 0, 0, 3, 1)

        self.bottomStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.bottomStackedWidget.setObjectName(u"bottomStackedWidget")
        sizePolicy7 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.bottomStackedWidget.sizePolicy().hasHeightForWidth())
        self.bottomStackedWidget.setSizePolicy(sizePolicy7)
        self.bottomStackedWidget.setMinimumSize(QSize(0, 200))
        self.bottomStackedWidget.setStyleSheet(u"")
        self.bottomStackedWidget.setFrameShape(QFrame.NoFrame)
        self.bottomStackedWidget.setFrameShadow(QFrame.Raised)
        self.calibrationPage = QWidget()
        self.calibrationPage.setObjectName(u"calibrationPage")
        sizePolicy5.setHeightForWidth(self.calibrationPage.sizePolicy().hasHeightForWidth())
        self.calibrationPage.setSizePolicy(sizePolicy5)
        self.horizontalLayout_4 = QHBoxLayout(self.calibrationPage)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.bottomStackedWidget.addWidget(self.calibrationPage)
        self.datapointsPage = QWidget()
        self.datapointsPage.setObjectName(u"datapointsPage")
        sizePolicy2.setHeightForWidth(self.datapointsPage.sizePolicy().hasHeightForWidth())
        self.datapointsPage.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.datapointsPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_10 = QFrame(self.datapointsPage)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_10)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.allDatasetsButtonsFrame = QFrame(self.frame_10)
        self.allDatasetsButtonsFrame.setObjectName(u"allDatasetsButtonsFrame")
        sizePolicy4.setHeightForWidth(self.allDatasetsButtonsFrame.sizePolicy().hasHeightForWidth())
        self.allDatasetsButtonsFrame.setSizePolicy(sizePolicy4)
        self.allDatasetsButtonsFrame.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 15px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"	color: rgb(200, 200, 200);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}")
        self.verticalLayout_14 = QVBoxLayout(self.allDatasetsButtonsFrame)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.newRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.newRowButton.setObjectName(u"newRowButton")
        sizePolicy5.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy5)
        self.newRowButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.newRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.newRowButton.setText(u"NEW   ")
        icon7 = QIcon()
        icon7.addFile(u":/icons/svg/cil-plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.newRowButton.setIcon(icon7)

        self.verticalLayout_14.addWidget(self.newRowButton)

        self.deleteRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.deleteRowButton.setObjectName(u"deleteRowButton")
        sizePolicy5.setHeightForWidth(self.deleteRowButton.sizePolicy().hasHeightForWidth())
        self.deleteRowButton.setSizePolicy(sizePolicy5)
        self.deleteRowButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.deleteRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.deleteRowButton.setText(u"DELETE  ")
        icon8 = QIcon()
        icon8.addFile(u":/icons/svg/cil-minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteRowButton.setIcon(icon8)

        self.verticalLayout_14.addWidget(self.deleteRowButton)

        self.clearAllButton = QPushButton(self.allDatasetsButtonsFrame)
        self.clearAllButton.setObjectName(u"clearAllButton")
        sizePolicy5.setHeightForWidth(self.clearAllButton.sizePolicy().hasHeightForWidth())
        self.clearAllButton.setSizePolicy(sizePolicy5)
        self.clearAllButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.clearAllButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.clearAllButton.setText(u"CLEAR ALL")

        self.verticalLayout_14.addWidget(self.clearAllButton)


        self.gridLayout_7.addWidget(self.allDatasetsButtonsFrame, 1, 0, 1, 1)

        self.dataTableFrame = DatasetWidget(self.frame_10)
        self.dataTableFrame.setObjectName(u"dataTableFrame")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.dataTableFrame.sizePolicy().hasHeightForWidth())
        self.dataTableFrame.setSizePolicy(sizePolicy8)
        self.dataTableFrame.setMaximumSize(QSize(16777215, 140))
        self.dataTableFrame.setStyleSheet(u"")
        self.horizontalLayout_5 = QHBoxLayout(self.dataTableFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.datasetListView = ListView(self.dataTableFrame)
        self.datasetListView.setObjectName(u"datasetListView")
        sizePolicy9 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.datasetListView.sizePolicy().hasHeightForWidth())
        self.datasetListView.setSizePolicy(sizePolicy9)
        self.datasetListView.setMinimumSize(QSize(0, 100))
        self.datasetListView.setMaximumSize(QSize(230, 100))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setPointSize(9)
        self.datasetListView.setFont(font1)
        self.datasetListView.setStyleSheet(u"background-color: rgb(47, 47, 47)")
        self.datasetListView.setFrameShape(QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_5.addWidget(self.datasetListView)

        self.dataTableView = TableView(self.dataTableFrame)
        self.dataTableView.setObjectName(u"dataTableView")
        sizePolicy5.setHeightForWidth(self.dataTableView.sizePolicy().hasHeightForWidth())
        self.dataTableView.setSizePolicy(sizePolicy5)
        self.dataTableView.setMinimumSize(QSize(0, 105))
        self.dataTableView.setMaximumSize(QSize(16777215, 105))
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


        self.gridLayout_7.addWidget(self.dataTableFrame, 1, 1, 1, 1)

        self.label_32 = QLabel(self.frame_10)
        self.label_32.setObjectName(u"label_32")
        sizePolicy5.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy5)
        self.label_32.setStyleSheet(u"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_32.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_7.addWidget(self.label_32, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.frame_10)

        self.bottomStackedWidget.addWidget(self.datapointsPage)
        self.prefitPage = QWidget()
        self.prefitPage.setObjectName(u"prefitPage")
        sizePolicy2.setHeightForWidth(self.prefitPage.sizePolicy().hasHeightForWidth())
        self.prefitPage.setSizePolicy(sizePolicy2)
        self.horizontalLayout_9 = QHBoxLayout(self.prefitPage)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.frame_4 = QFrame(self.prefitPage)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_43 = QLabel(self.frame_4)
        self.label_43.setObjectName(u"label_43")
        sizePolicy10 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy10)

        self.gridLayout_3.addWidget(self.label_43, 4, 1, 1, 1)

        self.label_42 = QLabel(self.frame_4)
        self.label_42.setObjectName(u"label_42")
        sizePolicy10.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy10)

        self.gridLayout_3.addWidget(self.label_42, 3, 1, 1, 1)

        self.exportToFitButton = QPushButton(self.frame_4)
        self.exportToFitButton.setObjectName(u"exportToFitButton")
        sizePolicy5.setHeightForWidth(self.exportToFitButton.sizePolicy().hasHeightForWidth())
        self.exportToFitButton.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.exportToFitButton, 1, 8, 1, 1)

        self.mseLabel = QLabel(self.frame_4)
        self.mseLabel.setObjectName(u"mseLabel")
        sizePolicy10.setHeightForWidth(self.mseLabel.sizePolicy().hasHeightForWidth())
        self.mseLabel.setSizePolicy(sizePolicy10)
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(9)
        font2.setBold(True)
        self.mseLabel.setFont(font2)

        self.gridLayout_3.addWidget(self.mseLabel, 1, 6, 1, 1)

        self.subsysComboBox = QComboBox(self.frame_4)
        self.subsysComboBox.setObjectName(u"subsysComboBox")
        sizePolicy5.setHeightForWidth(self.subsysComboBox.sizePolicy().hasHeightForWidth())
        self.subsysComboBox.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.subsysComboBox, 1, 2, 1, 1)

        self.statusTextLabel = QLabel(self.frame_4)
        self.statusTextLabel.setObjectName(u"statusTextLabel")
        self.statusTextLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel.setWordWrap(True)
        self.statusTextLabel.setMargin(5)

        self.gridLayout_3.addWidget(self.statusTextLabel, 3, 6, 2, 4)

        self.label_44 = QLabel(self.frame_4)
        self.label_44.setObjectName(u"label_44")
        sizePolicy10.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy10)

        self.gridLayout_3.addWidget(self.label_44, 1, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 1, 7, 1, 1)

        self.initStateLineEdit = QLineEdit(self.frame_4)
        self.initStateLineEdit.setObjectName(u"initStateLineEdit")
        sizePolicy5.setHeightForWidth(self.initStateLineEdit.sizePolicy().hasHeightForWidth())
        self.initStateLineEdit.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.initStateLineEdit, 2, 2, 1, 1)

        self.plotButton = QPushButton(self.frame_4)
        self.plotButton.setObjectName(u"plotButton")
        sizePolicy4.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy4)
        self.plotButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.plotButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.plotButton.setText(u"PLOT SPECTRUM")

        self.gridLayout_3.addWidget(self.plotButton, 1, 4, 1, 1)

        self.autoRunCheckBox = QCheckBox(self.frame_4)
        self.autoRunCheckBox.setObjectName(u"autoRunCheckBox")

        self.gridLayout_3.addWidget(self.autoRunCheckBox, 2, 4, 1, 1)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        sizePolicy10.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy10)

        self.gridLayout_3.addWidget(self.label, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 3, 1, 1)

        self.label_46 = QLabel(self.frame_4)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_3.addWidget(self.label_46, 2, 6, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 1, 5, 1, 1)

        self.evalsCountLineEdit = QLineEdit(self.frame_4)
        self.evalsCountLineEdit.setObjectName(u"evalsCountLineEdit")
        sizePolicy5.setHeightForWidth(self.evalsCountLineEdit.sizePolicy().hasHeightForWidth())
        self.evalsCountLineEdit.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.evalsCountLineEdit, 3, 2, 1, 1)

        self.pointsAddLineEdit = QLineEdit(self.frame_4)
        self.pointsAddLineEdit.setObjectName(u"pointsAddLineEdit")
        sizePolicy5.setHeightForWidth(self.pointsAddLineEdit.sizePolicy().hasHeightForWidth())
        self.pointsAddLineEdit.setSizePolicy(sizePolicy5)

        self.gridLayout_3.addWidget(self.pointsAddLineEdit, 4, 2, 1, 1)

        self.label_9 = QLabel(self.frame_4)
        self.label_9.setObjectName(u"label_9")
        sizePolicy5.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy5)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(u"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)


        self.horizontalLayout_9.addWidget(self.frame_4)

        self.bottomStackedWidget.addWidget(self.prefitPage)
        self.fitPage = QWidget()
        self.fitPage.setObjectName(u"fitPage")
        sizePolicy2.setHeightForWidth(self.fitPage.sizePolicy().hasHeightForWidth())
        self.fitPage.setSizePolicy(sizePolicy2)
        self.horizontalLayout_10 = QHBoxLayout(self.fitPage)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.frame_5 = QFrame(self.fitPage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalSpacer_7 = QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_7, 1, 5, 1, 1)

        self.mseLabel_2 = QLabel(self.frame_5)
        self.mseLabel_2.setObjectName(u"mseLabel_2")
        sizePolicy10.setHeightForWidth(self.mseLabel_2.sizePolicy().hasHeightForWidth())
        self.mseLabel_2.setSizePolicy(sizePolicy10)
        self.mseLabel_2.setFont(font2)

        self.gridLayout_6.addWidget(self.mseLabel_2, 1, 8, 1, 1)

        self.label_49 = QLabel(self.frame_5)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_6.addWidget(self.label_49, 2, 8, 1, 1)

        self.label_47 = QLabel(self.frame_5)
        self.label_47.setObjectName(u"label_47")
        sizePolicy10.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy10)

        self.gridLayout_6.addWidget(self.label_47, 1, 1, 1, 1)

        self.tolLineEdit = QLineEdit(self.frame_5)
        self.tolLineEdit.setObjectName(u"tolLineEdit")
        sizePolicy5.setHeightForWidth(self.tolLineEdit.sizePolicy().hasHeightForWidth())
        self.tolLineEdit.setSizePolicy(sizePolicy5)

        self.gridLayout_6.addWidget(self.tolLineEdit, 2, 4, 1, 1)

        self.statusTextLabel_2 = QLabel(self.frame_5)
        self.statusTextLabel_2.setObjectName(u"statusTextLabel_2")
        sizePolicy2.setHeightForWidth(self.statusTextLabel_2.sizePolicy().hasHeightForWidth())
        self.statusTextLabel_2.setSizePolicy(sizePolicy2)
        self.statusTextLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel_2.setWordWrap(True)
        self.statusTextLabel_2.setMargin(5)

        self.gridLayout_6.addWidget(self.statusTextLabel_2, 3, 8, 2, 4)

        self.optimizerComboBox = QComboBox(self.frame_5)
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.setObjectName(u"optimizerComboBox")
        sizePolicy5.setHeightForWidth(self.optimizerComboBox.sizePolicy().hasHeightForWidth())
        self.optimizerComboBox.setSizePolicy(sizePolicy5)

        self.gridLayout_6.addWidget(self.optimizerComboBox, 1, 4, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_6, 1, 7, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        sizePolicy10.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy10)

        self.gridLayout_6.addWidget(self.label_8, 2, 1, 1, 1)

        self.fitButton = QPushButton(self.frame_5)
        self.fitButton.setObjectName(u"fitButton")
        sizePolicy4.setHeightForWidth(self.fitButton.sizePolicy().hasHeightForWidth())
        self.fitButton.setSizePolicy(sizePolicy4)

        self.gridLayout_6.addWidget(self.fitButton, 1, 6, 1, 1)

        self.exportToPrefitButton = QPushButton(self.frame_5)
        self.exportToPrefitButton.setObjectName(u"exportToPrefitButton")
        sizePolicy4.setHeightForWidth(self.exportToPrefitButton.sizePolicy().hasHeightForWidth())
        self.exportToPrefitButton.setSizePolicy(sizePolicy4)

        self.gridLayout_6.addWidget(self.exportToPrefitButton, 1, 10, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_9, 1, 9, 1, 1)

        self.label_45 = QLabel(self.frame_5)
        self.label_45.setObjectName(u"label_45")
        sizePolicy5.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy5)
        self.label_45.setStyleSheet(u"font: 57 11pt \"Roboto Medium\";\n"
"")

        self.gridLayout_6.addWidget(self.label_45, 0, 0, 1, 1)


        self.horizontalLayout_10.addWidget(self.frame_5)

        self.bottomStackedWidget.addWidget(self.fitPage)

        self.gridLayout.addWidget(self.bottomStackedWidget, 1, 1, 1, 3)

        self.pagesStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.pagesStackedWidget.setObjectName(u"pagesStackedWidget")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.pagesStackedWidget.sizePolicy().hasHeightForWidth())
        self.pagesStackedWidget.setSizePolicy(sizePolicy11)
        self.pagesStackedWidget.setMaximumSize(QSize(420, 10000))
        self.extractPointsWidget = DataExtractingWidget()
        self.extractPointsWidget.setObjectName(u"extractPointsWidget")
        sizePolicy11.setHeightForWidth(self.extractPointsWidget.sizePolicy().hasHeightForWidth())
        self.extractPointsWidget.setSizePolicy(sizePolicy11)
        self.verticalLayout_9 = QVBoxLayout(self.extractPointsWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_8 = QFrame(self.extractPointsWidget)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy11.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy11)
        self.frame_8.setStyleSheet(u"QPushButton {\n"
"	font: 57 10pt \"Roboto Medium\";\n"
"	color: rgb(170, 170, 170);\n"
"	text-align: left;\n"
"	border: none;\n"
"}")
        self.verticalLayout_12 = QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(20, 25, -1, -1)
        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_4.setMargin(3)

        self.verticalLayout_12.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_12.addItem(self.verticalSpacer)

        self.scrollArea = QScrollArea(self.frame_8)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 1000000))
        self.scrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 364, 619))
        sizePolicy8.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy8)
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.coloringPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.coloringPushButton.setObjectName(u"coloringPushButton")
        icon9 = QIcon()
        icon9.addFile(u":/icons/svg/cil-caret-right.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon9.addFile(u":/icons/svg/cil-caret-bottom.svg", QSize(), QIcon.Normal, QIcon.On)
        self.coloringPushButton.setIcon(icon9)
        self.coloringPushButton.setCheckable(True)
        self.coloringPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.coloringPushButton)

        self.colorGridGroupBox = QGroupBox(self.scrollAreaWidgetContents_4)
        self.colorGridGroupBox.setObjectName(u"colorGridGroupBox")
        sizePolicy12 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.colorGridGroupBox.sizePolicy().hasHeightForWidth())
        self.colorGridGroupBox.setSizePolicy(sizePolicy12)
        self.colorGridGroupBox.setMinimumSize(QSize(330, 0))
        self.colorGridGroupBox.setTitle(u"")
        self.gridLayout_9 = QGridLayout(self.colorGridGroupBox)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.rangeSliderMin = QSlider(self.colorGridGroupBox)
        self.rangeSliderMin.setObjectName(u"rangeSliderMin")
        self.rangeSliderMin.setMinimumSize(QSize(0, 18))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMin, 2, 0, 1, 1)

        self.label_3 = QLabel(self.colorGridGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_9.addWidget(self.label_3, 4, 1, 1, 1)

        self.colorComboBox = QComboBox(self.colorGridGroupBox)
        icon10 = QIcon()
        icon10.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon10, u"PuOr")
        icon11 = QIcon()
        icon11.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon11, u"RdYlBu")
        icon12 = QIcon()
        icon12.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon12, u"bwr")
        icon13 = QIcon()
        icon13.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon13, u"viridis")
        icon14 = QIcon()
        icon14.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon14, u"cividis")
        icon15 = QIcon()
        icon15.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon15, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy5.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy5)
        self.colorComboBox.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(150, 20))
        self.colorComboBox.setFrame(False)

        self.gridLayout_9.addWidget(self.colorComboBox, 1, 0, 1, 1)

        self.logScaleCheckBox = QCheckBox(self.colorGridGroupBox)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText(u"LOG")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout_9.addWidget(self.logScaleCheckBox, 1, 1, 1, 1)

        self.rangeSliderMax = QSlider(self.colorGridGroupBox)
        self.rangeSliderMax.setObjectName(u"rangeSliderMax")
        self.rangeSliderMax.setMinimumSize(QSize(0, 18))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMax, 4, 0, 1, 1)

        self.label_2 = QLabel(self.colorGridGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_9.addWidget(self.label_2, 2, 1, 1, 1)


        self.verticalLayout_5.addWidget(self.colorGridGroupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.bgndSubtractPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.bgndSubtractPushButton.setObjectName(u"bgndSubtractPushButton")
        self.bgndSubtractPushButton.setIcon(icon9)
        self.bgndSubtractPushButton.setCheckable(True)
        self.bgndSubtractPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.bgndSubtractPushButton)

        self.bgndSubtractQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.bgndSubtractQFrame.setObjectName(u"bgndSubtractQFrame")
        sizePolicy4.setHeightForWidth(self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth())
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy4)
        self.bgndSubtractQFrame.setMinimumSize(QSize(330, 0))
        self.bgndSubtractQFrame.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout_8 = QGridLayout(self.bgndSubtractQFrame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(7)
        self.gridLayout_8.setContentsMargins(-1, 4, -1, -1)
        self.bgndSubtractYCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractYCheckBox.setObjectName(u"bgndSubtractYCheckBox")
        sizePolicy4.setHeightForWidth(self.bgndSubtractYCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractYCheckBox.setSizePolicy(sizePolicy4)
#if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText(u"ALONG Y AXIS")
        self.bgndSubtractYCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 3, 1, 1, 1)

        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        sizePolicy4.setHeightForWidth(self.bgndSubtractXCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractXCheckBox.setSizePolicy(sizePolicy4)
        self.bgndSubtractXCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip(u"Background subtraction along X")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setText(u"ALONG X AXIS")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 3, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.bgndSubtractQFrame)

        self.verticalSpacer_13 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_13)

        self.filtersPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.filtersPushButton.setObjectName(u"filtersPushButton")
        self.filtersPushButton.setIcon(icon9)
        self.filtersPushButton.setCheckable(True)

        self.verticalLayout_5.addWidget(self.filtersPushButton)

        self.filterQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.filterQFrame.setObjectName(u"filterQFrame")
        self.horizontalLayout_7 = QHBoxLayout(self.filterQFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 4, -1, -1)
        self.topHatCheckBox = QCheckBox(self.filterQFrame)
        self.topHatCheckBox.setObjectName(u"topHatCheckBox")
        self.topHatCheckBox.setFont(font1)
#if QT_CONFIG(tooltip)
        self.topHatCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.topHatCheckBox.setText(u"TOP-HAT")

        self.horizontalLayout_7.addWidget(self.topHatCheckBox)

        self.edgeFilterCheckBox = QCheckBox(self.filterQFrame)
        self.edgeFilterCheckBox.setObjectName(u"edgeFilterCheckBox")
#if QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setText(u"EDGE")

        self.horizontalLayout_7.addWidget(self.edgeFilterCheckBox)

        self.waveletCheckBox = QCheckBox(self.filterQFrame)
        self.waveletCheckBox.setObjectName(u"waveletCheckBox")
#if QT_CONFIG(tooltip)
        self.waveletCheckBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.waveletCheckBox.setText(u"DENOISE")

        self.horizontalLayout_7.addWidget(self.waveletCheckBox)


        self.verticalLayout_5.addWidget(self.filterQFrame)

        self.verticalSpacer_4 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.dataGroupPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.dataGroupPushButton.setObjectName(u"dataGroupPushButton")
        self.dataGroupPushButton.setIcon(icon9)
        self.dataGroupPushButton.setCheckable(True)

        self.verticalLayout_5.addWidget(self.dataGroupPushButton)

        self.xyzDataGridFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.xyzDataGridFrame.setObjectName(u"xyzDataGridFrame")
        self.xyzDataGridFrame.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.xyzDataGridFrame.sizePolicy().hasHeightForWidth())
        self.xyzDataGridFrame.setSizePolicy(sizePolicy4)
        self.xyzDataGridFrame.setMinimumSize(QSize(330, 0))
        self.gridLayout_4 = QGridLayout(self.xyzDataGridFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.zComboBox = QComboBox(self.xyzDataGridFrame)
        self.zComboBox.setObjectName(u"zComboBox")
        self.zComboBox.setMinimumSize(QSize(250, 30))
        self.zComboBox.setAutoFillBackground(False)
        self.zComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.zComboBox.setFrame(True)

        self.gridLayout_4.addWidget(self.zComboBox, 2, 1, 1, 1)

        self.label_14 = QLabel(self.xyzDataGridFrame)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setText(u"AXIS 2")
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 5, 0, 1, 1)

        self.label_13 = QLabel(self.xyzDataGridFrame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setText(u"Z")
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.xComboBox = QComboBox(self.xyzDataGridFrame)
        self.xComboBox.setObjectName(u"xComboBox")
        self.xComboBox.setMinimumSize(QSize(250, 30))
        self.xComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")

        self.gridLayout_4.addWidget(self.xComboBox, 4, 1, 1, 1)

        self.yComboBox = QComboBox(self.xyzDataGridFrame)
        self.yComboBox.setObjectName(u"yComboBox")
        self.yComboBox.setMinimumSize(QSize(250, 30))
        self.yComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")

        self.gridLayout_4.addWidget(self.yComboBox, 5, 1, 1, 1)

        self.label_12 = QLabel(self.xyzDataGridFrame)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setText(u"AXIS 1")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 4, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.xyzDataGridFrame)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_15)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.verticalSpacer_12 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_12.addItem(self.verticalSpacer_12)


        self.verticalLayout_9.addWidget(self.frame_8)

        self.pagesStackedWidget.addWidget(self.extractPointsWidget)
        self.taggingWidget = DataTaggingWidget()
        self.taggingWidget.setObjectName(u"taggingWidget")
        sizePolicy11.setHeightForWidth(self.taggingWidget.sizePolicy().hasHeightForWidth())
        self.taggingWidget.setSizePolicy(sizePolicy11)
        self.verticalLayout_10 = QVBoxLayout(self.taggingWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_9 = QFrame(self.taggingWidget)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy8.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy8)
        self.frame_9.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(25, 25, -1, -1)
        self.label_5 = QLabel(self.frame_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.label_5.setMargin(3)

        self.verticalLayout_13.addWidget(self.label_5)

        self.scrollArea_2 = QScrollArea(self.frame_9)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 316, 679))
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_16.addItem(self.verticalSpacer_6)

        self.tagChoicesFrame = QFrame(self.scrollAreaWidgetContents)
        self.tagChoicesFrame.setObjectName(u"tagChoicesFrame")
        self.tagChoicesFrame.setFrameShape(QFrame.NoFrame)
        self.tagChoicesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.tagChoicesFrame)
        self.verticalLayout_4.setSpacing(12)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.noTagRadioButton = QRadioButton(self.tagChoicesFrame)
        self.noTagRadioButton.setObjectName(u"noTagRadioButton")
        self.noTagRadioButton.setText(u"NO TAG")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.verticalLayout_4.addWidget(self.noTagRadioButton)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.label_23 = QLabel(self.tagChoicesFrame)
        self.label_23.setObjectName(u"label_23")
#if QT_CONFIG(tooltip)
        self.label_23.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_23.setStyleSheet(u"font: 10pt \"Roboto\";")
        self.label_23.setText(u"DISPERSIVE TRANSITION")

        self.verticalLayout_4.addWidget(self.label_23)

        self.tagDispersiveBareRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveBareRadioButton.setObjectName(u"tagDispersiveBareRadioButton")
#if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setText(u"BY BARE STATES")
        self.tagDispersiveBareRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveBareRadioButton)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveDressedRadioButton.setObjectName(u"tagDispersiveDressedRadioButton")
#if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveDressedRadioButton)

        self.verticalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.label_24 = QLabel(self.tagChoicesFrame)
        self.label_24.setObjectName(u"label_24")
#if QT_CONFIG(tooltip)
        self.label_24.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_24.setStyleSheet(u"font: 10pt \"Roboto\";")
        self.label_24.setText(u"AVOIDED CROSSING")

        self.verticalLayout_4.addWidget(self.label_24)

        self.tagCrossingRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingRadioButton.setObjectName(u"tagCrossingRadioButton")
#if QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setText(u"INFER WHEN FITTING")
        self.tagCrossingRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingRadioButton)

        self.tagCrossingDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingDressedRadioButton.setObjectName(u"tagCrossingDressedRadioButton")
#if QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagCrossingDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingDressedRadioButton)


        self.verticalLayout_16.addWidget(self.tagChoicesFrame)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_16.addItem(self.verticalSpacer_9)

        self.tagDressedGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.tagDressedGroupBox.setObjectName(u"tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
#if QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 10pt \"Roboto\";\n"
"}")
        self.tagDressedGroupBox.setTitle(u"TAG BY DRESSED INDICES")
        self.gridLayout_13 = QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 27, -1, -1)
        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName(u"label_30")
        sizePolicy13 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy13)
#if QT_CONFIG(tooltip)
        self.label_30.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(u"INITIAL")
        self.label_30.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 0, 3, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName(u"label_29")
        sizePolicy13.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy13)
#if QT_CONFIG(tooltip)
        self.label_29.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(u"PHOTONS")

        self.gridLayout_13.addWidget(self.label_29, 0, 0, 1, 1)

        self.phNumberDressedSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setObjectName(u"phNumberDressedSpinBox")
        self.phNumberDressedSpinBox.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy5)
        self.phNumberDressedSpinBox.setMinimumSize(QSize(60, 0))
        self.phNumberDressedSpinBox.setMinimum(1)

        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.finalStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.finalStateSpinBox.setObjectName(u"finalStateSpinBox")
        sizePolicy5.setHeightForWidth(self.finalStateSpinBox.sizePolicy().hasHeightForWidth())
        self.finalStateSpinBox.setSizePolicy(sizePolicy5)
        self.finalStateSpinBox.setMinimumSize(QSize(60, 20))
        self.finalStateSpinBox.setValue(1)

        self.gridLayout_13.addWidget(self.finalStateSpinBox, 1, 4, 1, 1)

        self.initialStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setObjectName(u"initialStateSpinBox")
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.initialStateSpinBox.sizePolicy().hasHeightForWidth())
        self.initialStateSpinBox.setSizePolicy(sizePolicy5)
        self.initialStateSpinBox.setMinimumSize(QSize(60, 20))

        self.gridLayout_13.addWidget(self.initialStateSpinBox, 0, 4, 1, 1)

        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName(u"label_31")
#if QT_CONFIG(tooltip)
        self.label_31.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(u"FINAL")
        self.label_31.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_31, 1, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)


        self.verticalLayout_16.addWidget(self.tagDressedGroupBox)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_16.addItem(self.verticalSpacer_10)

        self.tagBareGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.tagBareGroupBox.setObjectName(u"tagBareGroupBox")
        self.tagBareGroupBox.setEnabled(True)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 10pt \"Roboto\";\n"
"}")
        self.tagBareGroupBox.setTitle(u"TAG BY BARE STATES")
        self.tagBareGroupBox.setFlat(False)
        self.gridLayout_12 = QGridLayout(self.tagBareGroupBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(-1, 27, -1, -1)
        self.subsysNamesLineEdit = StrTupleLineEdit(self.tagBareGroupBox)
        self.subsysNamesLineEdit.setObjectName(u"subsysNamesLineEdit")
        self.subsysNamesLineEdit.setMinimumSize(QSize(0, 30))
        self.subsysNamesLineEdit.setText(u"")
        self.subsysNamesLineEdit.setPlaceholderText(u" <subsystem name 1>, ...")
        self.subsysNamesLineEdit.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.subsysNamesLineEdit, 0, 0, 1, 5)

        self.label_25 = QLabel(self.tagBareGroupBox)
        self.label_25.setObjectName(u"label_25")
        sizePolicy13.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy13)
        self.label_25.setText(u"PHOTONS")

        self.gridLayout_12.addWidget(self.label_25, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.label_28 = QLabel(self.tagBareGroupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setText(u"INITIAL")

        self.gridLayout_12.addWidget(self.label_28, 1, 3, 1, 1)

        self.label_26 = QLabel(self.tagBareGroupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setText(u"FINAL")

        self.gridLayout_12.addWidget(self.label_26, 2, 3, 1, 1)

        self.finalStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setObjectName(u"finalStateLineEdit")
        self.finalStateLineEdit.setMinimumSize(QSize(0, 30))
        self.finalStateLineEdit.setPlaceholderText(u"<level subsys 1>, <level subsys2>, ...")

        self.gridLayout_12.addWidget(self.finalStateLineEdit, 2, 4, 1, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName(u"phNumberBareSpinBox")
        sizePolicy12.setHeightForWidth(self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy12)
        self.phNumberBareSpinBox.setMinimumSize(QSize(60, 20))
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 1, 1, 1, 1)

        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setObjectName(u"initialStateLineEdit")
        self.initialStateLineEdit.setMinimumSize(QSize(0, 30))
        self.initialStateLineEdit.setPlaceholderText(u"<level subsys 1>, <level subsys2>, ...")

        self.gridLayout_12.addWidget(self.initialStateLineEdit, 1, 4, 1, 1)


        self.verticalLayout_16.addWidget(self.tagBareGroupBox)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_11)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_13.addWidget(self.scrollArea_2)


        self.verticalLayout_10.addWidget(self.frame_9)

        self.pagesStackedWidget.addWidget(self.taggingWidget)
        self.prefitWidget = QWidget()
        self.prefitWidget.setObjectName(u"prefitWidget")
        sizePolicy11.setHeightForWidth(self.prefitWidget.sizePolicy().hasHeightForWidth())
        self.prefitWidget.setSizePolicy(sizePolicy11)
        self.verticalLayout_3 = QVBoxLayout(self.prefitWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_prefit = QFrame(self.prefitWidget)
        self.frame_prefit.setObjectName(u"frame_prefit")
        sizePolicy11.setHeightForWidth(self.frame_prefit.sizePolicy().hasHeightForWidth())
        self.frame_prefit.setSizePolicy(sizePolicy11)
        self.frame_prefit.setFrameShape(QFrame.NoFrame)
        self.frame_prefit.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_prefit)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_6.setContentsMargins(25, 20, 9, -1)
        self.label_6 = QLabel(self.frame_prefit)
        self.label_6.setObjectName(u"label_6")
        sizePolicy5.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy5)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_6.setFrameShape(QFrame.NoFrame)
        self.label_6.setMargin(3)

        self.verticalLayout_6.addWidget(self.label_6)

        self.verticalSpacer_16 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_16)

        self.prefitScrollArea = QScrollArea(self.frame_prefit)
        self.prefitScrollArea.setObjectName(u"prefitScrollArea")
        sizePolicy14 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.prefitScrollArea.sizePolicy().hasHeightForWidth())
        self.prefitScrollArea.setSizePolicy(sizePolicy14)
        self.prefitScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.prefitScrollArea.setFrameShape(QFrame.NoFrame)
        self.prefitScrollArea.setFrameShadow(QFrame.Plain)
        self.prefitScrollArea.setWidgetResizable(True)
        self.prefitScrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.prefitScrollAreaWidget = QWidget()
        self.prefitScrollAreaWidget.setObjectName(u"prefitScrollAreaWidget")
        self.prefitScrollAreaWidget.setGeometry(QRect(0, 0, 42, 24))
        self.verticalLayout_11 = QVBoxLayout(self.prefitScrollAreaWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.prefitScrollArea.setWidget(self.prefitScrollAreaWidget)

        self.verticalLayout_6.addWidget(self.prefitScrollArea)

        self.verticalSpacer_17 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_17)


        self.verticalLayout_3.addWidget(self.frame_prefit)

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
        sizePolicy2.setHeightForWidth(self.frame_fit.sizePolicy().hasHeightForWidth())
        self.frame_fit.setSizePolicy(sizePolicy2)
        self.frame_fit.setFrameShape(QFrame.NoFrame)
        self.frame_fit.setFrameShadow(QFrame.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.frame_fit)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(25, 25, -1, -1)
        self.label_7 = QLabel(self.frame_fit)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.label_7.setFrameShape(QFrame.NoFrame)
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_7.setMargin(3)

        self.verticalLayout_8.addWidget(self.label_7)

        self.verticalSpacer_18 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_18)

        self.fitScrollArea = QScrollArea(self.frame_fit)
        self.fitScrollArea.setObjectName(u"fitScrollArea")
        self.fitScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.fitScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 37, 16))
        self.fitScrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_8.addWidget(self.fitScrollArea)

        self.verticalSpacer_19 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_19)


        self.verticalLayout_15.addWidget(self.frame_fit)

        self.frame_6 = QFrame(self.fitWidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_2 = QPushButton(self.frame_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy4.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy4)

        self.horizontalLayout_8.addWidget(self.pushButton_2)


        self.verticalLayout_15.addWidget(self.frame_6)

        self.pagesStackedWidget.addWidget(self.fitWidget)

        self.gridLayout.addWidget(self.pagesStackedWidget, 0, 1, 1, 1)

        self.mplFigureCanvas = MplFigureCanvas(self.windowBodyFrame)
        self.mplFigureCanvas.setObjectName(u"mplFigureCanvas")
        sizePolicy1.setHeightForWidth(self.mplFigureCanvas.sizePolicy().hasHeightForWidth())
        self.mplFigureCanvas.setSizePolicy(sizePolicy1)
        self.mplFigureCanvas.setMinimumSize(QSize(500, 300))
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
        icon16 = QIcon()
        icon16.addFile(u":/icons/svg/cil-reload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon16)
        self.resetViewButton.setIconSize(QSize(18, 18))
        self.panViewButton = QPushButton(self.mplFigureButtons)
        self.panViewButton.setObjectName(u"panViewButton")
        self.panViewButton.setGeometry(QRect(90, 10, 40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip(u"Pan mode: Drag to move the canvas")
#endif // QT_CONFIG(tooltip)
        icon17 = QIcon()
        icon17.addFile(u":/icons/svg/cil-move.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.panViewButton.setIcon(icon17)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.zoomViewButton = QPushButton(self.mplFigureButtons)
        self.zoomViewButton.setObjectName(u"zoomViewButton")
        self.zoomViewButton.setGeometry(QRect(150, 10, 40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip(u"Zoom mode: Drag to magnify a region")
#endif // QT_CONFIG(tooltip)
        icon18 = QIcon()
        icon18.addFile(u":/icons/svg/cil-zoom.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomViewButton.setIcon(icon18)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.horizontalSnapButton = QPushButton(self.mplFigureButtons)
        self.horizontalSnapButton.setObjectName(u"horizontalSnapButton")
        self.horizontalSnapButton.setGeometry(QRect(270, 10, 40, 40))
#if QT_CONFIG(tooltip)
        self.horizontalSnapButton.setToolTip(u"Dataset snapping: align the x-coordinates for datasets")
#endif // QT_CONFIG(tooltip)
        icon19 = QIcon()
        icon19.addFile(u":/icons/svg/cil-lock-unlocked.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon19.addFile(u":/icons/svg/cil-lock-locked.svg", QSize(), QIcon.Normal, QIcon.On)
        self.horizontalSnapButton.setIcon(icon19)
        self.horizontalSnapButton.setCheckable(True)
        self.horizontalSnapButton.setChecked(True)
        self.horizontalSnapButton.setAutoExclusive(False)
        self.selectViewButton = QPushButton(self.mplFigureButtons)
        self.selectViewButton.setObjectName(u"selectViewButton")
        self.selectViewButton.setGeometry(QRect(210, 10, 41, 41))
        self.selectViewButton.setCursor(QCursor(Qt.CrossCursor))
#if QT_CONFIG(tooltip)
        self.selectViewButton.setToolTip(u"Extract mode: Click to extract peaks")
#endif // QT_CONFIG(tooltip)
        self.selectViewButton.setIcon(icon2)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.verticalSnapButton = QPushButton(self.mplFigureButtons)
        self.verticalSnapButton.setObjectName(u"verticalSnapButton")
        self.verticalSnapButton.setGeometry(QRect(330, 10, 41, 41))
#if QT_CONFIG(tooltip)
        self.verticalSnapButton.setToolTip(u"Peak snapping: Locate the nearby peak along y axis")
#endif // QT_CONFIG(tooltip)
        icon20 = QIcon()
        icon20.addFile(u":/icons/svg/cil-vertical-align-center.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.verticalSnapButton.setIcon(icon20)
        self.verticalSnapButton.setCheckable(True)
        self.verticalSnapButton.setChecked(True)
        self.verticalSnapButton.setAutoExclusive(False)
        self.swapXYButton = QPushButton(self.mplFigureButtons)
        self.swapXYButton.setObjectName(u"swapXYButton")
        self.swapXYButton.setGeometry(QRect(390, 10, 71, 41))
        self.swapXYButton.setCursor(QCursor(Qt.CrossCursor))
#if QT_CONFIG(tooltip)
        self.swapXYButton.setToolTip(u"Transpose data")
#endif // QT_CONFIG(tooltip)
        self.swapXYButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 15px;	\n"
"	background-color: rgb(93, 93, 93);\n"
"color: rgb(225, 225, 225);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(196, 150, 250);\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.swapXYButton.setCheckable(True)
        self.swapXYButton.setChecked(True)
        self.swapXYButton.setAutoExclusive(True)
        self.line = QFrame(self.mplFigureCanvas)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(379, 10, 3, 41))
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.VLine)
        self.line_2 = QFrame(self.mplFigureCanvas)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(259, 10, 3, 41))
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(0)
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_3 = QFrame(self.mplFigureCanvas)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(79, 10, 3, 41))
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setLineWidth(0)
        self.line_3.setFrameShape(QFrame.VLine)

        self.gridLayout.addWidget(self.mplFigureCanvas, 0, 2, 1, 2)

        self.menu_frame.raise_()
        self.pagesStackedWidget.raise_()
        self.mplFigureCanvas.raise_()
        self.bottomStackedWidget.raise_()

        self.verticalLayout.addWidget(self.windowBodyFrame)


        self.verticalLayout_7.addWidget(self.fullWindowFrame)

        MainWindow.setCentralWidget(self.centralWidget)
        QWidget.setTabOrder(self.bgndSubtractXCheckBox, self.bgndSubtractYCheckBox)
        QWidget.setTabOrder(self.bgndSubtractYCheckBox, self.colorComboBox)
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
        QWidget.setTabOrder(self.rawY1LineEdit, self.tagDispersiveBareRadioButton)
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

        self.retranslateUi(MainWindow)
        self.dataGroupPushButton.toggled.connect(self.xyzDataGridFrame.setVisible)
        self.bgndSubtractPushButton.toggled.connect(self.bgndSubtractQFrame.setVisible)
        self.coloringPushButton.toggled.connect(self.colorGridGroupBox.setVisible)
        self.filtersPushButton.toggled.connect(self.filterQFrame.setVisible)

        self.bottomStackedWidget.setCurrentIndex(0)
        self.pagesStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.modeSelectButton.setText(QCoreApplication.translate("MainWindow", u"   VISUALIZE", None))
        self.modeTagButton.setText(QCoreApplication.translate("MainWindow", u"   EXTRACT", None))
        self.modeFitButton.setText(QCoreApplication.translate("MainWindow", u"   FIT", None))
        self.toggleMenuButton.setText("")
        self.modePrefitButton.setText(QCoreApplication.translate("MainWindow", u"   PRE-FIT", None))
        self.calibrateY2Button.setText("")
        self.calibrateY1Button.setText("")
        self.mapX1LineEdit.setInputMask("")
        self.calibrateX1Button.setText("")
        self.calibrateX2Button.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"CALIBRATION", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"EXTRACTED DATASET", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"POINTS ADDED", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"EVALS COUNT", None))
#if QT_CONFIG(tooltip)
        self.exportToFitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the pre-fitted parameters to the initial value of the fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToFitButton.setText(QCoreApplication.translate("MainWindow", u"RESULTS \u2192 FIT", None))
        self.mseLabel.setText(QCoreApplication.translate("MainWindow", u"MSE:  0.647 GHz^2   (+0.86%)", None))
        self.statusTextLabel.setText(QCoreApplication.translate("MainWindow", u"Status Text", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"TRANSITIONS", None))
        self.autoRunCheckBox.setText(QCoreApplication.translate("MainWindow", u"AUTO-UPDATE", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"INITIAL STATE", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"SETTINGS", None))
        self.mseLabel_2.setText(QCoreApplication.translate("MainWindow", u"MSE:  0.647 GHz^2   (+0.86%)", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"OPTIMIZER", None))
        self.tolLineEdit.setText(QCoreApplication.translate("MainWindow", u"1e-6", None))
        self.statusTextLabel_2.setText(QCoreApplication.translate("MainWindow", u"Status Text", None))
        self.optimizerComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"L-BFGS-B", None))
        self.optimizerComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Nelder-Mead", None))
        self.optimizerComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Powell", None))
        self.optimizerComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"shgo", None))
        self.optimizerComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"differential evolution", None))

        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TOLERANCE", None))
        self.fitButton.setText(QCoreApplication.translate("MainWindow", u"RUN FIT", None))
#if QT_CONFIG(tooltip)
        self.exportToPrefitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the fitted parameters to the pre-fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToPrefitButton.setText(QCoreApplication.translate("MainWindow", u"RESULTS \u2192 PRE-FIT", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"SETTINGS", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"EXTRACT", None))
        self.coloringPushButton.setText(QCoreApplication.translate("MainWindow", u"COLORING", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MAX", None))

        self.colorComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"PuOr", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MIN", None))
        self.bgndSubtractPushButton.setText(QCoreApplication.translate("MainWindow", u"BACKGROUND SUBTRACT", None))
        self.filtersPushButton.setText(QCoreApplication.translate("MainWindow", u"FILTERS", None))
        self.dataGroupPushButton.setText(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.zComboBox.setCurrentText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TAG", None))
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
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PRE-FIT", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"FIT", None))
#if QT_CONFIG(tooltip)
        self.pushButton_2.setToolTip(QCoreApplication.translate("MainWindow", u"Load the current value to the initial value", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"RESULTS \u2192 INITIAL", None))
        self.resetViewButton.setText("")
        self.panViewButton.setText("")
        self.zoomViewButton.setText("")
        self.horizontalSnapButton.setText("")
        self.selectViewButton.setText("")
        self.verticalSnapButton.setText("")
        self.swapXYButton.setText(QCoreApplication.translate("MainWindow", u"X\u2194Y", None))
        pass
    # retranslateUi

