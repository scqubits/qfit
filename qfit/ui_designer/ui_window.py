# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_window.ui'
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
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)

from qfit.widgets.calibration import CalibrationLineEdit
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
        MainWindow.resize(1237, 784)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
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
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_frame = QFrame(self.windowBodyFrame)
        self.menu_frame.setObjectName(u"menu_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy2)
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
        self.modeFitButton = QPushButton(self.menu_frame)
        self.modeFitButton.setObjectName(u"modeFitButton")
        self.modeFitButton.setMinimumSize(QSize(120, 70))
        self.modeFitButton.setMaximumSize(QSize(120, 70))
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/cil-speedometer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeFitButton.setIcon(icon1)
        self.modeFitButton.setIconSize(QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeFitButton, 5, 0, 1, 1)

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

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_14, 0, 0, 1, 1)

        self.modeSelectButton = QPushButton(self.menu_frame)
        self.modeSelectButton.setObjectName(u"modeSelectButton")
        self.modeSelectButton.setMinimumSize(QSize(120, 70))
        self.modeSelectButton.setMaximumSize(QSize(120, 70))
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.modeSelectButton.setFont(font)
        icon3 = QIcon()
        icon3.addFile(u":/icons/svg/cil-list.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeSelectButton.setIcon(icon3)
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
        icon4 = QIcon()
        icon4.addFile(u":/icons/svg/cil-menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleMenuButton.setIcon(icon4)
        self.toggleMenuButton.setIconSize(QSize(24, 24))
        self.toggleMenuButton.setAutoDefault(False)
        self.toggleMenuButton.setFlat(False)

        self.gridLayout_2.addWidget(self.toggleMenuButton, 1, 0, 1, 2)

        self.modePrefitButton = QPushButton(self.menu_frame)
        self.modePrefitButton.setObjectName(u"modePrefitButton")
        self.modePrefitButton.setMinimumSize(QSize(120, 70))
        self.modePrefitButton.setMaximumSize(QSize(120, 70))
        icon5 = QIcon()
        icon5.addFile(u":/icons/svg/cil-chart-line.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modePrefitButton.setIcon(icon5)
        self.modePrefitButton.setIconSize(QSize(24, 24))
        self.modePrefitButton.setCheckable(True)
        self.modePrefitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modePrefitButton, 4, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 6, 1, 1, 1)


        self.gridLayout.addWidget(self.menu_frame, 0, 0, 3, 1)

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
        icon6 = QIcon()
        icon6.addFile(u":/icons/svg/cil-reload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon6)
        self.resetViewButton.setIconSize(QSize(18, 18))
        self.panViewButton = QPushButton(self.mplFigureButtons)
        self.panViewButton.setObjectName(u"panViewButton")
        self.panViewButton.setGeometry(QRect(90, 10, 40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip(u"Pan mode: Drag to move the canvas")
#endif // QT_CONFIG(tooltip)
        icon7 = QIcon()
        icon7.addFile(u":/icons/svg/cil-move.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.panViewButton.setIcon(icon7)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.zoomViewButton = QPushButton(self.mplFigureButtons)
        self.zoomViewButton.setObjectName(u"zoomViewButton")
        self.zoomViewButton.setGeometry(QRect(150, 10, 40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip(u"Zoom mode: Drag to magnify a region")
#endif // QT_CONFIG(tooltip)
        icon8 = QIcon()
        icon8.addFile(u":/icons/svg/cil-zoom.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomViewButton.setIcon(icon8)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.horizontalSnapButton = QPushButton(self.mplFigureButtons)
        self.horizontalSnapButton.setObjectName(u"horizontalSnapButton")
        self.horizontalSnapButton.setGeometry(QRect(270, 10, 40, 40))
#if QT_CONFIG(tooltip)
        self.horizontalSnapButton.setToolTip(u"Dataset snapping: align the x-coordinates for datasets")
#endif // QT_CONFIG(tooltip)
        icon9 = QIcon()
        icon9.addFile(u":/icons/svg/cil-lock-unlocked.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon9.addFile(u":/icons/svg/cil-lock-locked.svg", QSize(), QIcon.Normal, QIcon.On)
        self.horizontalSnapButton.setIcon(icon9)
        self.horizontalSnapButton.setCheckable(True)
        self.horizontalSnapButton.setChecked(True)
        self.horizontalSnapButton.setAutoExclusive(False)
        self.selectViewButton = QPushButton(self.mplFigureButtons)
        self.selectViewButton.setObjectName(u"selectViewButton")
        self.selectViewButton.setGeometry(QRect(210, 10, 41, 41))
        self.selectViewButton.setCursor(QCursor(Qt.ArrowCursor))
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
        icon10 = QIcon()
        icon10.addFile(u":/icons/svg/cil-vertical-align-center.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.verticalSnapButton.setIcon(icon10)
        self.verticalSnapButton.setCheckable(True)
        self.verticalSnapButton.setChecked(True)
        self.verticalSnapButton.setAutoExclusive(False)
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

        self.pagesStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.pagesStackedWidget.setObjectName(u"pagesStackedWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pagesStackedWidget.sizePolicy().hasHeightForWidth())
        self.pagesStackedWidget.setSizePolicy(sizePolicy3)
        self.pagesStackedWidget.setMinimumSize(QSize(120, 0))
        self.pagesStackedWidget.setMaximumSize(QSize(410, 10000))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setPointSize(9)
        font1.setKerning(True)
        self.pagesStackedWidget.setFont(font1)
        self.pagesStackedWidget.setStyleSheet(u"")
        self.pagesStackedWidget.setFrameShadow(QFrame.Raised)
        self.extractPointsWidget = DataExtractingWidget()
        self.extractPointsWidget.setObjectName(u"extractPointsWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.extractPointsWidget.sizePolicy().hasHeightForWidth())
        self.extractPointsWidget.setSizePolicy(sizePolicy4)
        self.verticalLayout_9 = QVBoxLayout(self.extractPointsWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame = QFrame(self.extractPointsWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 20))
        self.frame.setCursor(QCursor(Qt.ArrowCursor))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_14 = QGridLayout(self.frame)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(25, 20, 9, -1)
        self.verticalSpacer_2 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_14.addItem(self.verticalSpacer_2, 12, 3, 1, 1)

        self.swapXYButton = QPushButton(self.frame)
        self.swapXYButton.setObjectName(u"swapXYButton")
        self.swapXYButton.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.swapXYButton.sizePolicy().hasHeightForWidth())
        self.swapXYButton.setSizePolicy(sizePolicy5)
        self.swapXYButton.setMinimumSize(QSize(40, 20))
        self.swapXYButton.setCursor(QCursor(Qt.ArrowCursor))
        self.swapXYButton.setIconSize(QSize(16, 16))

        self.gridLayout_14.addWidget(self.swapXYButton, 2, 3, 1, 1)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setMinimumSize(QSize(0, 15))
        self.label_5.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_14.addWidget(self.label_5, 0, 0, 1, 1)

        self.DataXYFrame = QFrame(self.frame)
        self.DataXYFrame.setObjectName(u"DataXYFrame")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.DataXYFrame.sizePolicy().hasHeightForWidth())
        self.DataXYFrame.setSizePolicy(sizePolicy6)
        self.DataXYFrame.setMinimumSize(QSize(330, 0))
        self.DataXYFrame.setFrameShape(QFrame.NoFrame)
        self.DataXYFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.DataXYFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(12)
        self.gridLayout_4.setContentsMargins(-1, 0, 0, 0)
        self.label_12 = QLabel(self.DataXYFrame)
        self.label_12.setObjectName(u"label_12")
        sizePolicy6.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy6)
        self.label_12.setText(u"AXIS X")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)

        self.label_14 = QLabel(self.DataXYFrame)
        self.label_14.setObjectName(u"label_14")
        sizePolicy6.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy6)
        self.label_14.setText(u"AXIS Y")
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 3, 0, 1, 1)

        self.label_13 = QLabel(self.DataXYFrame)
        self.label_13.setObjectName(u"label_13")
        sizePolicy6.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy6)
        self.label_13.setText(u"Z")
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_13, 0, 0, 1, 1)

        self.yComboBox = QComboBox(self.DataXYFrame)
        self.yComboBox.setObjectName(u"yComboBox")
        sizePolicy3.setHeightForWidth(self.yComboBox.sizePolicy().hasHeightForWidth())
        self.yComboBox.setSizePolicy(sizePolicy3)
        self.yComboBox.setMinimumSize(QSize(250, 30))
        self.yComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")

        self.gridLayout_4.addWidget(self.yComboBox, 3, 1, 1, 1)

        self.xComboBox = QComboBox(self.DataXYFrame)
        self.xComboBox.setObjectName(u"xComboBox")
        sizePolicy3.setHeightForWidth(self.xComboBox.sizePolicy().hasHeightForWidth())
        self.xComboBox.setSizePolicy(sizePolicy3)
        self.xComboBox.setMinimumSize(QSize(250, 30))
        self.xComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")

        self.gridLayout_4.addWidget(self.xComboBox, 1, 1, 1, 1)

        self.zComboBox = QComboBox(self.DataXYFrame)
        self.zComboBox.setObjectName(u"zComboBox")
        sizePolicy3.setHeightForWidth(self.zComboBox.sizePolicy().hasHeightForWidth())
        self.zComboBox.setSizePolicy(sizePolicy3)
        self.zComboBox.setMinimumSize(QSize(250, 30))
        self.zComboBox.setAutoFillBackground(False)
        self.zComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.zComboBox.setFrame(True)

        self.gridLayout_4.addWidget(self.zComboBox, 0, 1, 1, 1)


        self.gridLayout_14.addWidget(self.DataXYFrame, 1, 0, 1, 2)

        self.horizontalSpacer_14 = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_14, 2, 2, 1, 1)

        self.calibrateYGridFrame = QFrame(self.frame)
        self.calibrateYGridFrame.setObjectName(u"calibrateYGridFrame")
        sizePolicy5.setHeightForWidth(self.calibrateYGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateYGridFrame.setSizePolicy(sizePolicy5)
        self.calibrateYGridFrame.setMinimumSize(QSize(330, 100))
        self.calibrateYGridFrame.setMaximumSize(QSize(320, 16777215))
#if QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	text-align: center;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(71, 30, 79);\n"
"}")
        self.gridLayout_11 = QGridLayout(self.calibrateYGridFrame)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.calibrateY1Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY1Button.setObjectName(u"calibrateY1Button")
        self.calibrateY1Button.setMinimumSize(QSize(30, 30))
        self.calibrateY1Button.setMaximumSize(QSize(16777215, 16777192))
        self.calibrateY1Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateY1Button.setToolTip(u"Calibrate y1, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY1Button.setStyleSheet(u"")
        self.calibrateY1Button.setIcon(icon2)
        self.calibrateY1Button.setCheckable(True)
        self.calibrateY1Button.setChecked(False)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 1, 0, 1, 1)

        self.label_23 = QLabel(self.calibrateYGridFrame)
        self.label_23.setObjectName(u"label_23")
        sizePolicy5.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy5)

        self.gridLayout_11.addWidget(self.label_23, 0, 2, 1, 1)

        self.label_19 = QLabel(self.calibrateYGridFrame)
        self.label_19.setObjectName(u"label_19")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy7)
        self.label_19.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_19, 1, 1, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridFrame)
        self.label_22.setObjectName(u"label_22")
        sizePolicy7.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy7)
        self.label_22.setText(u"<html><head/><body><p align=\"right\">\u2192 Y<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_22, 2, 3, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridFrame)
        self.label_20.setObjectName(u"label_20")
        sizePolicy7.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy7)
        self.label_20.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_20, 2, 1, 1, 1)

        self.calibrateY2Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY2Button.setObjectName(u"calibrateY2Button")
        self.calibrateY2Button.setMinimumSize(QSize(30, 30))
        self.calibrateY2Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateY2Button.setToolTip(u"Calibrate y2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateY2Button.setStyleSheet(u"")
        self.calibrateY2Button.setIcon(icon2)
        self.calibrateY2Button.setCheckable(True)
        self.calibrateY2Button.setChecked(False)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 2, 0, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridFrame)
        self.label_21.setObjectName(u"label_21")
        sizePolicy7.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy7)
        self.label_21.setText(u"<html><head/><body><p align=\"right\">\u2192 Y<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_21, 1, 3, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY1LineEdit.setObjectName(u"mapY1LineEdit")
        sizePolicy3.setHeightForWidth(self.mapY1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY1LineEdit.setSizePolicy(sizePolicy3)
        self.mapY1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 1, 4, 1, 1)

        self.label_24 = QLabel(self.calibrateYGridFrame)
        self.label_24.setObjectName(u"label_24")
        sizePolicy5.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy5)

        self.gridLayout_11.addWidget(self.label_24, 0, 4, 1, 1)

        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY2LineEdit.setObjectName(u"rawY2LineEdit")
        sizePolicy3.setHeightForWidth(self.rawY2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY2LineEdit.setSizePolicy(sizePolicy3)
        self.rawY2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 2, 2, 1, 1)

        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY1LineEdit.setObjectName(u"rawY1LineEdit")
        sizePolicy3.setHeightForWidth(self.rawY1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY1LineEdit.setSizePolicy(sizePolicy3)
        self.rawY1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 1, 2, 1, 1)

        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY2LineEdit.setObjectName(u"mapY2LineEdit")
        sizePolicy3.setHeightForWidth(self.mapY2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY2LineEdit.setSizePolicy(sizePolicy3)
        self.mapY2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 2, 4, 1, 1)


        self.gridLayout_14.addWidget(self.calibrateYGridFrame, 10, 0, 1, 1)

        self.calibrateXGridFrame = QFrame(self.frame)
        self.calibrateXGridFrame.setObjectName(u"calibrateXGridFrame")
        sizePolicy5.setHeightForWidth(self.calibrateXGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateXGridFrame.setSizePolicy(sizePolicy5)
        self.calibrateXGridFrame.setMinimumSize(QSize(330, 100))
        self.calibrateXGridFrame.setMaximumSize(QSize(320, 16777215))
        self.calibrateXGridFrame.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(93, 93, 93);\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	text-align: center;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: rgb(71, 30, 79);\n"
"}")
        self.gridLayout_10 = QGridLayout(self.calibrateXGridFrame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX1LineEdit.setObjectName(u"rawX1LineEdit")
        sizePolicy3.setHeightForWidth(self.rawX1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX1LineEdit.setSizePolicy(sizePolicy3)
        self.rawX1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.rawX1LineEdit, 1, 2, 1, 1)

        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX2LineEdit.setObjectName(u"rawX2LineEdit")
        sizePolicy3.setHeightForWidth(self.rawX2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawX2LineEdit.setSizePolicy(sizePolicy3)
        self.rawX2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.rawX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.rawX2LineEdit, 2, 2, 1, 1)

        self.calibrateX2Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX2Button.setObjectName(u"calibrateX2Button")
        self.calibrateX2Button.setMinimumSize(QSize(30, 30))
        self.calibrateX2Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateX2Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX2Button.setStyleSheet(u"")
        self.calibrateX2Button.setIcon(icon2)
        self.calibrateX2Button.setCheckable(True)
        self.calibrateX2Button.setChecked(False)

        self.gridLayout_10.addWidget(self.calibrateX2Button, 2, 0, 1, 1)

        self.label_18 = QLabel(self.calibrateXGridFrame)
        self.label_18.setObjectName(u"label_18")
        sizePolicy7.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy7)
        self.label_18.setText(u"<html><head/><body><p align=\"right\">\u2192 X<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_18, 2, 3, 1, 1)

        self.label_11 = QLabel(self.calibrateXGridFrame)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_10.addWidget(self.label_11, 0, 4, 1, 1)

        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX1LineEdit.setObjectName(u"mapX1LineEdit")
        sizePolicy3.setHeightForWidth(self.mapX1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX1LineEdit.setSizePolicy(sizePolicy3)
        self.mapX1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX1LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapX1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.mapX1LineEdit, 1, 4, 1, 1)

        self.label_15 = QLabel(self.calibrateXGridFrame)
        self.label_15.setObjectName(u"label_15")
        sizePolicy7.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy7)
        self.label_15.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_15, 1, 1, 1, 1)

        self.label_17 = QLabel(self.calibrateXGridFrame)
        self.label_17.setObjectName(u"label_17")
        sizePolicy7.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy7)
        self.label_17.setText(u"<html><head/><body><p align=\"right\">\u2192 X<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_10.addWidget(self.label_17, 1, 3, 1, 1)

        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX2LineEdit.setObjectName(u"mapX2LineEdit")
        sizePolicy3.setHeightForWidth(self.mapX2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapX2LineEdit.setSizePolicy(sizePolicy3)
        self.mapX2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX2LineEdit.setMaximumSize(QSize(200, 16777215))
#if QT_CONFIG(tooltip)
        self.mapX2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.mapX2LineEdit, 2, 4, 1, 1)

        self.label_16 = QLabel(self.calibrateXGridFrame)
        self.label_16.setObjectName(u"label_16")
        sizePolicy7.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy7)
        self.label_16.setText(u"<html><head/><body><p align=\"right\">X<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_10.addWidget(self.label_16, 2, 1, 1, 1)

        self.label_10 = QLabel(self.calibrateXGridFrame)
        self.label_10.setObjectName(u"label_10")
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)

        self.gridLayout_10.addWidget(self.label_10, 0, 2, 1, 1)

        self.calibrateX1Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX1Button.setObjectName(u"calibrateX1Button")
        self.calibrateX1Button.setMinimumSize(QSize(30, 30))
        self.calibrateX1Button.setCursor(QCursor(Qt.PointingHandCursor))
#if QT_CONFIG(tooltip)
        self.calibrateX1Button.setToolTip(u"Calibrate x2, allows selection of coordinate inside plot")
#endif // QT_CONFIG(tooltip)
        self.calibrateX1Button.setStyleSheet(u"")
        self.calibrateX1Button.setIcon(icon2)
        self.calibrateX1Button.setCheckable(True)
        self.calibrateX1Button.setChecked(False)

        self.gridLayout_10.addWidget(self.calibrateX1Button, 1, 0, 1, 1)


        self.gridLayout_14.addWidget(self.calibrateXGridFrame, 9, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_10, 9, 4, 1, 1)

        self.calibrationTitleWidget = QWidget(self.frame)
        self.calibrationTitleWidget.setObjectName(u"calibrationTitleWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.calibrationTitleWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 40, 0)
        self.calibrationLabel = QLabel(self.calibrationTitleWidget)
        self.calibrationLabel.setObjectName(u"calibrationLabel")
        sizePolicy3.setHeightForWidth(self.calibrationLabel.sizePolicy().hasHeightForWidth())
        self.calibrationLabel.setSizePolicy(sizePolicy3)
        self.calibrationLabel.setMinimumSize(QSize(100, 15))
        self.calibrationLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.calibrationLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.calibrationLabel)

        self.calibrationHelpPushButton = QPushButton(self.calibrationTitleWidget)
        self.calibrationHelpPushButton.setObjectName(u"calibrationHelpPushButton")
        self.calibrationHelpPushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.calibrationHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/icons/svg/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrationHelpPushButton.setIcon(icon11)
        self.calibrationHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_2.addWidget(self.calibrationHelpPushButton)


        self.gridLayout_14.addWidget(self.calibrationTitleWidget, 3, 0, 1, 1)

        self.calibratedCheckBox = QCheckBox(self.frame)
        self.calibratedCheckBox.setObjectName(u"calibratedCheckBox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.calibratedCheckBox.sizePolicy().hasHeightForWidth())
        self.calibratedCheckBox.setSizePolicy(sizePolicy8)
        self.calibratedCheckBox.setMinimumSize(QSize(140, 20))
        self.calibratedCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.calibratedCheckBox.setText(u"TOGGLE CALIBRATION")

        self.gridLayout_14.addWidget(self.calibratedCheckBox, 11, 1, 1, 1)


        self.verticalLayout_9.addWidget(self.frame)

        self.pagesStackedWidget.addWidget(self.extractPointsWidget)
        self.taggingWidget = QWidget()
        self.taggingWidget.setObjectName(u"taggingWidget")
        sizePolicy4.setHeightForWidth(self.taggingWidget.sizePolicy().hasHeightForWidth())
        self.taggingWidget.setSizePolicy(sizePolicy4)
        self.verticalLayout_10 = QVBoxLayout(self.taggingWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_9 = QFrame(self.taggingWidget)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy9)
        self.frame_9.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(25, 20, 9, -1)
        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.frame_10)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.allDatasetsButtonsFrame = QFrame(self.frame_10)
        self.allDatasetsButtonsFrame.setObjectName(u"allDatasetsButtonsFrame")
        sizePolicy5.setHeightForWidth(self.allDatasetsButtonsFrame.sizePolicy().hasHeightForWidth())
        self.allDatasetsButtonsFrame.setSizePolicy(sizePolicy5)
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
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy10)
        self.newRowButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.newRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.newRowButton.setText(u"NEW   ")
        icon12 = QIcon()
        icon12.addFile(u":/icons/svg/cil-plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.newRowButton.setIcon(icon12)

        self.verticalLayout_14.addWidget(self.newRowButton)

        self.deleteRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.deleteRowButton.setObjectName(u"deleteRowButton")
        sizePolicy3.setHeightForWidth(self.deleteRowButton.sizePolicy().hasHeightForWidth())
        self.deleteRowButton.setSizePolicy(sizePolicy3)
        self.deleteRowButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.deleteRowButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.deleteRowButton.setText(u"DELETE  ")
        icon13 = QIcon()
        icon13.addFile(u":/icons/svg/cil-minus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteRowButton.setIcon(icon13)

        self.verticalLayout_14.addWidget(self.deleteRowButton)

        self.clearAllButton = QPushButton(self.allDatasetsButtonsFrame)
        self.clearAllButton.setObjectName(u"clearAllButton")
        sizePolicy3.setHeightForWidth(self.clearAllButton.sizePolicy().hasHeightForWidth())
        self.clearAllButton.setSizePolicy(sizePolicy3)
        self.clearAllButton.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.clearAllButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.clearAllButton.setText(u"CLEAR ALL")

        self.verticalLayout_14.addWidget(self.clearAllButton)


        self.gridLayout_7.addWidget(self.allDatasetsButtonsFrame, 1, 0, 1, 1)

        self.datasetListView = ListView(self.frame_10)
        self.datasetListView.setObjectName(u"datasetListView")
        sizePolicy11 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.datasetListView.sizePolicy().hasHeightForWidth())
        self.datasetListView.setSizePolicy(sizePolicy11)
        self.datasetListView.setMinimumSize(QSize(0, 100))
        self.datasetListView.setMaximumSize(QSize(230, 130))
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(9)
        self.datasetListView.setFont(font2)
        self.datasetListView.setStyleSheet(u"background-color: rgb(47, 47, 47)")
        self.datasetListView.setFrameShape(QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QFrame.Plain)

        self.gridLayout_7.addWidget(self.datasetListView, 1, 1, 1, 1)

        self.label_32 = QLabel(self.frame_10)
        self.label_32.setObjectName(u"label_32")
        sizePolicy3.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy3)
        self.label_32.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.label_32.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout_7.addWidget(self.label_32, 0, 0, 1, 2)


        self.verticalLayout_13.addWidget(self.frame_10)

        self.transitionLabel = QLabel(self.frame_9)
        self.transitionLabel.setObjectName(u"transitionLabel")
        self.transitionLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.transitionLabel.setMargin(3)

        self.verticalLayout_13.addWidget(self.transitionLabel)

        self.scrollArea_2 = QScrollArea(self.frame_9)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.scrollArea_2.setFrameShape(QFrame.NoFrame)
        self.scrollArea_2.setFrameShadow(QFrame.Plain)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 342, 361))
        self.verticalLayout_16 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_16.setSpacing(12)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.noTagRadioButton = QRadioButton(self.scrollAreaWidgetContents)
        self.noTagRadioButton.setObjectName(u"noTagRadioButton")
        self.noTagRadioButton.setText(u"UNKNOWN")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.verticalLayout_16.addWidget(self.noTagRadioButton)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.scrollAreaWidgetContents)
        self.tagDispersiveDressedRadioButton.setObjectName(u"tagDispersiveDressedRadioButton")
#if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_16.addWidget(self.tagDispersiveDressedRadioButton)

        self.tagDressedGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.tagDressedGroupBox.setObjectName(u"tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
        sizePolicy10.setHeightForWidth(self.tagDressedGroupBox.sizePolicy().hasHeightForWidth())
        self.tagDressedGroupBox.setSizePolicy(sizePolicy10)
#if QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 10pt \"Roboto\";\n"
"}")
        self.tagDressedGroupBox.setTitle(u"")
        self.gridLayout_13 = QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 0, -1, 12)
        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName(u"label_31")
#if QT_CONFIG(tooltip)
        self.label_31.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(u"FINAL")
        self.label_31.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_31, 2, 1, 1, 1)

        self.phNumberDressedSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setObjectName(u"phNumberDressedSpinBox")
        self.phNumberDressedSpinBox.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy3)
        self.phNumberDressedSpinBox.setMinimumSize(QSize(65, 0))
        self.phNumberDressedSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberDressedSpinBox.setMinimum(1)

        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 4, 2, 1, 1)

        self.initialStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setObjectName(u"initialStateSpinBox")
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.initialStateSpinBox.sizePolicy().hasHeightForWidth())
        self.initialStateSpinBox.setSizePolicy(sizePolicy3)
        self.initialStateSpinBox.setMinimumSize(QSize(65, 20))
        self.initialStateSpinBox.setAlignment(Qt.AlignCenter)

        self.gridLayout_13.addWidget(self.initialStateSpinBox, 1, 2, 1, 1)

        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName(u"label_30")
        sizePolicy12 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy12)
#if QT_CONFIG(tooltip)
        self.label_30.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(u"INITIAL")
        self.label_30.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 1, 5, 1, 1)

        self.finalStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.finalStateSpinBox.setObjectName(u"finalStateSpinBox")
        sizePolicy3.setHeightForWidth(self.finalStateSpinBox.sizePolicy().hasHeightForWidth())
        self.finalStateSpinBox.setSizePolicy(sizePolicy3)
        self.finalStateSpinBox.setMinimumSize(QSize(65, 20))
        self.finalStateSpinBox.setFrame(True)
        self.finalStateSpinBox.setAlignment(Qt.AlignCenter)
        self.finalStateSpinBox.setValue(1)

        self.gridLayout_13.addWidget(self.finalStateSpinBox, 2, 2, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName(u"label_29")
        sizePolicy12.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy12)
#if QT_CONFIG(tooltip)
        self.label_29.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(u"PHOTONS")

        self.gridLayout_13.addWidget(self.label_29, 4, 1, 1, 1)


        self.verticalLayout_16.addWidget(self.tagDressedGroupBox)

        self.tagDispersiveBareRadioButton = QRadioButton(self.scrollAreaWidgetContents)
        self.tagDispersiveBareRadioButton.setObjectName(u"tagDispersiveBareRadioButton")
#if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setText(u"BY BARE STATES")
        self.tagDispersiveBareRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_16.addWidget(self.tagDispersiveBareRadioButton)

        self.tagBareGroupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.tagBareGroupBox.setObjectName(u"tagBareGroupBox")
        self.tagBareGroupBox.setEnabled(True)
        sizePolicy10.setHeightForWidth(self.tagBareGroupBox.sizePolicy().hasHeightForWidth())
        self.tagBareGroupBox.setSizePolicy(sizePolicy10)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setStyleSheet(u"QGroupBox {\n"
"	font: 10pt \"Roboto\";\n"
"}")
        self.tagBareGroupBox.setTitle(u"")
        self.tagBareGroupBox.setFlat(False)
        self.gridLayout_12 = QGridLayout(self.tagBareGroupBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(12, 0, 12, 12)
        self.label_26 = QLabel(self.tagBareGroupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setText(u"FINAL")

        self.gridLayout_12.addWidget(self.label_26, 3, 0, 1, 1)

        self.label_25 = QLabel(self.tagBareGroupBox)
        self.label_25.setObjectName(u"label_25")
        sizePolicy12.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy12)
        self.label_25.setText(u"PHOTONS")

        self.gridLayout_12.addWidget(self.label_25, 4, 0, 1, 1)

        self.label_28 = QLabel(self.tagBareGroupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setText(u"INITIAL")

        self.gridLayout_12.addWidget(self.label_28, 2, 0, 1, 1)

        self.finalStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setObjectName(u"finalStateLineEdit")
        self.finalStateLineEdit.setMinimumSize(QSize(0, 30))
        self.finalStateLineEdit.setPlaceholderText(u"<level subsys1>, <level subsys2>, ...")

        self.gridLayout_12.addWidget(self.finalStateLineEdit, 3, 1, 1, 1)

        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setObjectName(u"initialStateLineEdit")
        self.initialStateLineEdit.setMinimumSize(QSize(0, 30))
        self.initialStateLineEdit.setPlaceholderText(u"<level subsys1>, <level subsys2>, ...")

        self.gridLayout_12.addWidget(self.initialStateLineEdit, 2, 1, 1, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName(u"phNumberBareSpinBox")
        sizePolicy13 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy13)
        self.phNumberBareSpinBox.setMinimumSize(QSize(65, 20))
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 4, 1, 1, 1)

        self.bareLabelOrder = QLabel(self.tagBareGroupBox)
        self.bareLabelOrder.setObjectName(u"bareLabelOrder")
        sizePolicy10.setHeightForWidth(self.bareLabelOrder.sizePolicy().hasHeightForWidth())
        self.bareLabelOrder.setSizePolicy(sizePolicy10)
        self.bareLabelOrder.setWordWrap(True)

        self.gridLayout_12.addWidget(self.bareLabelOrder, 1, 0, 1, 2)


        self.verticalLayout_16.addWidget(self.tagBareGroupBox)

        self.verticalSpacer_4 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_4)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_13.addWidget(self.scrollArea_2)


        self.verticalLayout_10.addWidget(self.frame_9)

        self.pagesStackedWidget.addWidget(self.taggingWidget)
        self.prefitWidget = QWidget()
        self.prefitWidget.setObjectName(u"prefitWidget")
        sizePolicy4.setHeightForWidth(self.prefitWidget.sizePolicy().hasHeightForWidth())
        self.prefitWidget.setSizePolicy(sizePolicy4)
        self.verticalLayout_3 = QVBoxLayout(self.prefitWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(12, -1, -1, -1)
        self.frame_prefit = QFrame(self.prefitWidget)
        self.frame_prefit.setObjectName(u"frame_prefit")
        sizePolicy4.setHeightForWidth(self.frame_prefit.sizePolicy().hasHeightForWidth())
        self.frame_prefit.setSizePolicy(sizePolicy4)
        self.frame_prefit.setFrameShape(QFrame.NoFrame)
        self.frame_prefit.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_prefit)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_6.setContentsMargins(25, 20, 9, -1)
        self.label_6 = QLabel(self.frame_prefit)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
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
        self.prefitScrollAreaWidget.setGeometry(QRect(0, 0, 352, 366))
        self.verticalLayout_11 = QVBoxLayout(self.prefitScrollAreaWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.prefitScrollArea.setWidget(self.prefitScrollAreaWidget)

        self.verticalLayout_6.addWidget(self.prefitScrollArea)


        self.verticalLayout_3.addWidget(self.frame_prefit)

        self.frame_3 = QFrame(self.prefitWidget)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy10.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy10)
        self.frame_3.setMinimumSize(QSize(0, 35))
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
#ifndef Q_OS_MAC
        self.horizontalLayout_3.setSpacing(-1)
#endif
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(12, 0, -1, 0)
        self.plotButton = QPushButton(self.frame_3)
        self.plotButton.setObjectName(u"plotButton")
        sizePolicy5.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy5)
        self.plotButton.setMinimumSize(QSize(120, 20))
        self.plotButton.setFont(font1)
#if QT_CONFIG(tooltip)
        self.plotButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.plotButton.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.plotButton)

        self.autoRunCheckBox = QCheckBox(self.frame_3)
        self.autoRunCheckBox.setObjectName(u"autoRunCheckBox")
        sizePolicy5.setHeightForWidth(self.autoRunCheckBox.sizePolicy().hasHeightForWidth())
        self.autoRunCheckBox.setSizePolicy(sizePolicy5)
        self.autoRunCheckBox.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_3.addWidget(self.autoRunCheckBox)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.pagesStackedWidget.addWidget(self.prefitWidget)
        self.fitWidget = QWidget()
        self.fitWidget.setObjectName(u"fitWidget")
        sizePolicy4.setHeightForWidth(self.fitWidget.sizePolicy().hasHeightForWidth())
        self.fitWidget.setSizePolicy(sizePolicy4)
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
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(25, 20, 9, -1)
        self.fitTitleWidget = QWidget(self.frame_fit)
        self.fitTitleWidget.setObjectName(u"fitTitleWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.fitTitleWidget)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.fitLabel = QLabel(self.fitTitleWidget)
        self.fitLabel.setObjectName(u"fitLabel")
        sizePolicy1.setHeightForWidth(self.fitLabel.sizePolicy().hasHeightForWidth())
        self.fitLabel.setSizePolicy(sizePolicy1)
        self.fitLabel.setMinimumSize(QSize(0, 0))
        self.fitLabel.setMaximumSize(QSize(16777215, 16777215))
        self.fitLabel.setFont(font)
        self.fitLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";\n"
"")
        self.fitLabel.setFrameShape(QFrame.NoFrame)
        self.fitLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.fitLabel.setMargin(0)
        self.fitLabel.setIndent(0)

        self.horizontalLayout_5.addWidget(self.fitLabel)

        self.fitHelpPushButton = QPushButton(self.fitTitleWidget)
        self.fitHelpPushButton.setObjectName(u"fitHelpPushButton")
        self.fitHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.fitHelpPushButton.setIcon(icon11)
        self.fitHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_5.addWidget(self.fitHelpPushButton)

        self.horizontalSpacer_5 = QSpacerItem(200, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_8.addWidget(self.fitTitleWidget)

        self.verticalSpacer_18 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_18)

        self.fitScrollArea = QScrollArea(self.frame_fit)
        self.fitScrollArea.setObjectName(u"fitScrollArea")
        self.fitScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.fitScrollArea.setFrameShape(QFrame.NoFrame)
        self.fitScrollArea.setFrameShadow(QFrame.Plain)
        self.fitScrollArea.setWidgetResizable(True)
        self.fitScrollAreaWidget = QWidget()
        self.fitScrollAreaWidget.setObjectName(u"fitScrollAreaWidget")
        self.fitScrollAreaWidget.setGeometry(QRect(0, 0, 352, 363))
        self.verticalLayout_4 = QVBoxLayout(self.fitScrollAreaWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fitScrollArea.setWidget(self.fitScrollAreaWidget)

        self.verticalLayout_8.addWidget(self.fitScrollArea)


        self.verticalLayout_15.addWidget(self.frame_fit)

        self.frame_6 = QFrame(self.fitWidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.fitButton = QPushButton(self.frame_6)
        self.fitButton.setObjectName(u"fitButton")
        sizePolicy5.setHeightForWidth(self.fitButton.sizePolicy().hasHeightForWidth())
        self.fitButton.setSizePolicy(sizePolicy5)
        self.fitButton.setMinimumSize(QSize(120, 20))

        self.horizontalLayout_8.addWidget(self.fitButton)

        self.pushButton_2 = QPushButton(self.frame_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy5.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy5)
        self.pushButton_2.setMinimumSize(QSize(120, 20))

        self.horizontalLayout_8.addWidget(self.pushButton_2)


        self.verticalLayout_15.addWidget(self.frame_6)

        self.pagesStackedWidget.addWidget(self.fitWidget)

        self.gridLayout.addWidget(self.pagesStackedWidget, 0, 1, 1, 1)

        self.bottomStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.bottomStackedWidget.setObjectName(u"bottomStackedWidget")
        sizePolicy15 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.bottomStackedWidget.sizePolicy().hasHeightForWidth())
        self.bottomStackedWidget.setSizePolicy(sizePolicy15)
        self.bottomStackedWidget.setMinimumSize(QSize(0, 220))
        self.bottomStackedWidget.setStyleSheet(u"")
        self.bottomStackedWidget.setFrameShape(QFrame.NoFrame)
        self.bottomStackedWidget.setFrameShadow(QFrame.Raised)
        self.calibrationPage = QWidget()
        self.calibrationPage.setObjectName(u"calibrationPage")
        sizePolicy14.setHeightForWidth(self.calibrationPage.sizePolicy().hasHeightForWidth())
        self.calibrationPage.setSizePolicy(sizePolicy14)
        self.horizontalLayout_4 = QHBoxLayout(self.calibrationPage)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_2 = QFrame(self.calibrationPage)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_4.addWidget(self.frame_2)

        self.bottomStackedWidget.addWidget(self.calibrationPage)
        self.datapointsPage = QWidget()
        self.datapointsPage.setObjectName(u"datapointsPage")
        sizePolicy14.setHeightForWidth(self.datapointsPage.sizePolicy().hasHeightForWidth())
        self.datapointsPage.setSizePolicy(sizePolicy14)
        self.datapointsPage.setLayoutDirection(Qt.LeftToRight)
        self.datapointsPage.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(self.datapointsPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 12)
        self.frame_8 = QFrame(self.datapointsPage)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy1.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy1)
        self.frame_8.setStyleSheet(u"QPushButton {\n"
"	font: 57 10pt \"Roboto Medium\";\n"
"	color: rgb(170, 170, 170);\n"
"	text-align: left;\n"
"	border: none;\n"
"}")
        self.gridLayout_5 = QGridLayout(self.frame_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(12, 12, -1, 0)
        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_4.setMargin(3)

        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 4)

        self.widget = QWidget(self.frame_8)
        self.widget.setObjectName(u"widget")
        sizePolicy7.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy7)
        self.widget.setMinimumSize(QSize(300, 0))
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.coloringPushButton = QPushButton(self.widget)
        self.coloringPushButton.setObjectName(u"coloringPushButton")
        icon14 = QIcon()
        icon14.addFile(u":/icons/svg/cil-caret-right.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon14.addFile(u":/icons/svg/cil-caret-bottom.svg", QSize(), QIcon.Normal, QIcon.On)
        self.coloringPushButton.setIcon(icon14)
        self.coloringPushButton.setCheckable(True)
        self.coloringPushButton.setChecked(True)

        self.verticalLayout_2.addWidget(self.coloringPushButton)

        self.colorGridGroupBox = QGroupBox(self.widget)
        self.colorGridGroupBox.setObjectName(u"colorGridGroupBox")
        sizePolicy15.setHeightForWidth(self.colorGridGroupBox.sizePolicy().hasHeightForWidth())
        self.colorGridGroupBox.setSizePolicy(sizePolicy15)
        self.colorGridGroupBox.setMinimumSize(QSize(0, 0))
        self.colorGridGroupBox.setMaximumSize(QSize(1000000, 16777215))
        self.colorGridGroupBox.setTitle(u"")
        self.gridLayout_9 = QGridLayout(self.colorGridGroupBox)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.rangeSliderMin = QSlider(self.colorGridGroupBox)
        self.rangeSliderMin.setObjectName(u"rangeSliderMin")
        self.rangeSliderMin.setMinimumSize(QSize(0, 18))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMin, 2, 0, 1, 1)

        self.label_2 = QLabel(self.colorGridGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_9.addWidget(self.label_2, 2, 1, 1, 1)

        self.label_3 = QLabel(self.colorGridGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_9.addWidget(self.label_3, 4, 1, 1, 1)

        self.rangeSliderMax = QSlider(self.colorGridGroupBox)
        self.rangeSliderMax.setObjectName(u"rangeSliderMax")
        self.rangeSliderMax.setMinimumSize(QSize(0, 18))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMax, 4, 0, 1, 1)

        self.logScaleCheckBox = QCheckBox(self.colorGridGroupBox)
        self.logScaleCheckBox.setObjectName(u"logScaleCheckBox")
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText(u"LOG")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout_9.addWidget(self.logScaleCheckBox, 1, 1, 1, 1)

        self.colorComboBox = QComboBox(self.colorGridGroupBox)
        icon15 = QIcon()
        icon15.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon15, u"PuOr")
        icon16 = QIcon()
        icon16.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon16, u"RdYlBu")
        icon17 = QIcon()
        icon17.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon17, u"bwr")
        icon18 = QIcon()
        icon18.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon18, u"viridis")
        icon19 = QIcon()
        icon19.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon19, u"cividis")
        icon20 = QIcon()
        icon20.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon20, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy3.setHeightForWidth(self.colorComboBox.sizePolicy().hasHeightForWidth())
        self.colorComboBox.setSizePolicy(sizePolicy3)
        self.colorComboBox.setMinimumSize(QSize(100, 30))
#if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(150, 20))
        self.colorComboBox.setFrame(False)

        self.gridLayout_9.addWidget(self.colorComboBox, 1, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.colorGridGroupBox)


        self.gridLayout_5.addWidget(self.widget, 3, 1, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_12, 3, 3, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_7, 4, 3, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_11, 3, 0, 1, 1)

        self.widget_2 = QWidget(self.frame_8)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy7.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy7)
        self.widget_2.setMinimumSize(QSize(300, 0))
        self.widget_2.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bgndSubtractPushButton = QPushButton(self.widget_2)
        self.bgndSubtractPushButton.setObjectName(u"bgndSubtractPushButton")
        self.bgndSubtractPushButton.setIcon(icon14)
        self.bgndSubtractPushButton.setCheckable(True)
        self.bgndSubtractPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.bgndSubtractPushButton)

        self.bgndSubtractQFrame = QFrame(self.widget_2)
        self.bgndSubtractQFrame.setObjectName(u"bgndSubtractQFrame")
        sizePolicy15.setHeightForWidth(self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth())
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy15)
        self.bgndSubtractQFrame.setMinimumSize(QSize(330, 0))
        self.bgndSubtractQFrame.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout_8 = QGridLayout(self.bgndSubtractQFrame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(7)
        self.gridLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.bgndSubtractYCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractYCheckBox.setObjectName(u"bgndSubtractYCheckBox")
        sizePolicy5.setHeightForWidth(self.bgndSubtractYCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractYCheckBox.setSizePolicy(sizePolicy5)
#if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText(u"ALONG Y AXIS")
        self.bgndSubtractYCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 3, 1, 1, 1)

        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        sizePolicy5.setHeightForWidth(self.bgndSubtractXCheckBox.sizePolicy().hasHeightForWidth())
        self.bgndSubtractXCheckBox.setSizePolicy(sizePolicy5)
        self.bgndSubtractXCheckBox.setFont(font2)
#if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip(u"Background subtraction along X")
#endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setText(u"ALONG X AXIS")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 3, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.bgndSubtractQFrame)

        self.filtersPushButton = QPushButton(self.widget_2)
        self.filtersPushButton.setObjectName(u"filtersPushButton")
        self.filtersPushButton.setIcon(icon14)
        self.filtersPushButton.setCheckable(True)
        self.filtersPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.filtersPushButton)

        self.filterQFrame = QFrame(self.widget_2)
        self.filterQFrame.setObjectName(u"filterQFrame")
        sizePolicy14.setHeightForWidth(self.filterQFrame.sizePolicy().hasHeightForWidth())
        self.filterQFrame.setSizePolicy(sizePolicy14)
        self.horizontalLayout_7 = QHBoxLayout(self.filterQFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.topHatCheckBox = QCheckBox(self.filterQFrame)
        self.topHatCheckBox.setObjectName(u"topHatCheckBox")
        self.topHatCheckBox.setFont(font2)
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


        self.gridLayout_5.addWidget(self.widget_2, 3, 4, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_13, 3, 5, 1, 1)


        self.horizontalLayout.addWidget(self.frame_8)

        self.bottomStackedWidget.addWidget(self.datapointsPage)
        self.prefitPage = QWidget()
        self.prefitPage.setObjectName(u"prefitPage")
        sizePolicy14.setHeightForWidth(self.prefitPage.sizePolicy().hasHeightForWidth())
        self.prefitPage.setSizePolicy(sizePolicy14)
        self.horizontalLayout_9 = QHBoxLayout(self.prefitPage)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.frame_4 = QFrame(self.prefitPage)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_4)
#ifndef Q_OS_MAC
        self.gridLayout_3.setSpacing(-1)
#endif
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.subsysComboBox = QComboBox(self.frame_4)
        self.subsysComboBox.setObjectName(u"subsysComboBox")
        sizePolicy3.setHeightForWidth(self.subsysComboBox.sizePolicy().hasHeightForWidth())
        self.subsysComboBox.setSizePolicy(sizePolicy3)
        self.subsysComboBox.setMinimumSize(QSize(0, 30))

        self.gridLayout_3.addWidget(self.subsysComboBox, 3, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 3, 10, 1, 1)

        self.horizontalSpacer = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 8, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 3, 6, 1, 1)

        self.initStateLineEdit = StateLineEdit(self.frame_4)
        self.initStateLineEdit.setObjectName(u"initStateLineEdit")
        sizePolicy3.setHeightForWidth(self.initStateLineEdit.sizePolicy().hasHeightForWidth())
        self.initStateLineEdit.setSizePolicy(sizePolicy3)
        self.initStateLineEdit.setMinimumSize(QSize(150, 30))

        self.gridLayout_3.addWidget(self.initStateLineEdit, 5, 2, 1, 1)

        self.evalsCountLineEdit = IntLineEdit(self.frame_4)
        self.evalsCountLineEdit.setObjectName(u"evalsCountLineEdit")
        sizePolicy3.setHeightForWidth(self.evalsCountLineEdit.sizePolicy().hasHeightForWidth())
        self.evalsCountLineEdit.setSizePolicy(sizePolicy3)
        self.evalsCountLineEdit.setMinimumSize(QSize(0, 30))

        self.gridLayout_3.addWidget(self.evalsCountLineEdit, 3, 5, 1, 1)

        self.prefitPhotonSpinBox = QSpinBox(self.frame_4)
        self.prefitPhotonSpinBox.setObjectName(u"prefitPhotonSpinBox")
        sizePolicy5.setHeightForWidth(self.prefitPhotonSpinBox.sizePolicy().hasHeightForWidth())
        self.prefitPhotonSpinBox.setSizePolicy(sizePolicy5)
        self.prefitPhotonSpinBox.setMinimumSize(QSize(65, 20))
        self.prefitPhotonSpinBox.setMinimum(1)

        self.gridLayout_3.addWidget(self.prefitPhotonSpinBox, 6, 2, 1, 1)

        self.label_44 = QLabel(self.frame_4)
        self.label_44.setObjectName(u"label_44")
        sizePolicy6.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.label_44, 3, 1, 1, 1)

        self.pointsAddLineEdit = IntLineEdit(self.frame_4)
        self.pointsAddLineEdit.setObjectName(u"pointsAddLineEdit")
        sizePolicy3.setHeightForWidth(self.pointsAddLineEdit.sizePolicy().hasHeightForWidth())
        self.pointsAddLineEdit.setSizePolicy(sizePolicy3)
        self.pointsAddLineEdit.setMinimumSize(QSize(150, 30))

        self.gridLayout_3.addWidget(self.pointsAddLineEdit, 5, 5, 1, 1)

        self.prefitResultHelpPushButton = QPushButton(self.frame_4)
        self.prefitResultHelpPushButton.setObjectName(u"prefitResultHelpPushButton")
        sizePolicy1.setHeightForWidth(self.prefitResultHelpPushButton.sizePolicy().hasHeightForWidth())
        self.prefitResultHelpPushButton.setSizePolicy(sizePolicy1)
        self.prefitResultHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.prefitResultHelpPushButton.setIcon(icon11)
        self.prefitResultHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout_3.addWidget(self.prefitResultHelpPushButton, 3, 9, 1, 1)

        self.exportToFitButton = QPushButton(self.frame_4)
        self.exportToFitButton.setObjectName(u"exportToFitButton")
        sizePolicy5.setHeightForWidth(self.exportToFitButton.sizePolicy().hasHeightForWidth())
        self.exportToFitButton.setSizePolicy(sizePolicy5)
        self.exportToFitButton.setMinimumSize(QSize(120, 20))

        self.gridLayout_3.addWidget(self.exportToFitButton, 3, 11, 1, 1)

        self.label_42 = QLabel(self.frame_4)
        self.label_42.setObjectName(u"label_42")
        sizePolicy6.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.label_42, 3, 3, 1, 1)

        self.label_43 = QLabel(self.frame_4)
        self.label_43.setObjectName(u"label_43")
        sizePolicy6.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.label_43, 5, 3, 1, 1)

        self.statusTextLabel = QLabel(self.frame_4)
        self.statusTextLabel.setObjectName(u"statusTextLabel")
        self.statusTextLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel.setWordWrap(True)
        self.statusTextLabel.setMargin(5)

        self.gridLayout_3.addWidget(self.statusTextLabel, 6, 8, 2, 6)

        self.label_33 = QLabel(self.frame_4)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_3.addWidget(self.label_33, 6, 1, 1, 1)

        self.label_46 = QLabel(self.frame_4)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_3.addWidget(self.label_46, 5, 8, 1, 1)

        self.mseLabel = QLabel(self.frame_4)
        self.mseLabel.setObjectName(u"mseLabel")
        sizePolicy6.setHeightForWidth(self.mseLabel.sizePolicy().hasHeightForWidth())
        self.mseLabel.setSizePolicy(sizePolicy6)
        font3 = QFont()
        font3.setFamilies([u"Roboto Medium"])
        font3.setPointSize(9)
        font3.setBold(True)
        self.mseLabel.setFont(font3)

        self.gridLayout_3.addWidget(self.mseLabel, 3, 8, 1, 1)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        sizePolicy6.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy6)

        self.gridLayout_3.addWidget(self.label, 5, 1, 1, 1)

        self.numericalSpectrumSettingsTitleWidget = QWidget(self.frame_4)
        self.numericalSpectrumSettingsTitleWidget.setObjectName(u"numericalSpectrumSettingsTitleWidget")
        self.horizontalLayout_6 = QHBoxLayout(self.numericalSpectrumSettingsTitleWidget)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.numericalSpectrumSettingsLabel = QLabel(self.numericalSpectrumSettingsTitleWidget)
        self.numericalSpectrumSettingsLabel.setObjectName(u"numericalSpectrumSettingsLabel")
        sizePolicy3.setHeightForWidth(self.numericalSpectrumSettingsLabel.sizePolicy().hasHeightForWidth())
        self.numericalSpectrumSettingsLabel.setSizePolicy(sizePolicy3)
        self.numericalSpectrumSettingsLabel.setFont(font)
        self.numericalSpectrumSettingsLabel.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")
        self.numericalSpectrumSettingsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.numericalSpectrumSettingsLabel)

        self.numericalSpectrumSettingsHelpPushButton = QPushButton(self.numericalSpectrumSettingsTitleWidget)
        self.numericalSpectrumSettingsHelpPushButton.setObjectName(u"numericalSpectrumSettingsHelpPushButton")
        self.numericalSpectrumSettingsHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.numericalSpectrumSettingsHelpPushButton.setIcon(icon11)
        self.numericalSpectrumSettingsHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_6.addWidget(self.numericalSpectrumSettingsHelpPushButton)


        self.gridLayout_3.addWidget(self.numericalSpectrumSettingsTitleWidget, 0, 1, 1, 2)


        self.horizontalLayout_9.addWidget(self.frame_4)

        self.bottomStackedWidget.addWidget(self.prefitPage)
        self.fitPage = QWidget()
        self.fitPage.setObjectName(u"fitPage")
        sizePolicy14.setHeightForWidth(self.fitPage.sizePolicy().hasHeightForWidth())
        self.fitPage.setSizePolicy(sizePolicy14)
        self.horizontalLayout_10 = QHBoxLayout(self.fitPage)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.frame_5 = QFrame(self.fitPage)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy1.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy1)
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_45 = QLabel(self.frame_5)
        self.label_45.setObjectName(u"label_45")
        sizePolicy3.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy3)
        self.label_45.setStyleSheet(u"color: rgb(190, 130, 250);\n"
"font: 57 11pt \"Roboto Medium\";")

        self.gridLayout_6.addWidget(self.label_45, 0, 0, 1, 2)

        self.horizontalSpacer_7 = QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_7, 1, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        sizePolicy6.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy6)

        self.gridLayout_6.addWidget(self.label_8, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer, 4, 7, 1, 1)

        self.label_49 = QLabel(self.frame_5)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_6.addWidget(self.label_49, 2, 7, 1, 1)

        self.mseLabel_2 = QLabel(self.frame_5)
        self.mseLabel_2.setObjectName(u"mseLabel_2")
        sizePolicy6.setHeightForWidth(self.mseLabel_2.sizePolicy().hasHeightForWidth())
        self.mseLabel_2.setSizePolicy(sizePolicy6)
        self.mseLabel_2.setFont(font3)

        self.gridLayout_6.addWidget(self.mseLabel_2, 1, 7, 1, 1)

        self.statusTextLabel_2 = QLabel(self.frame_5)
        self.statusTextLabel_2.setObjectName(u"statusTextLabel_2")
        sizePolicy14.setHeightForWidth(self.statusTextLabel_2.sizePolicy().hasHeightForWidth())
        self.statusTextLabel_2.setSizePolicy(sizePolicy14)
        self.statusTextLabel_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.statusTextLabel_2.setWordWrap(True)
        self.statusTextLabel_2.setMargin(5)

        self.gridLayout_6.addWidget(self.statusTextLabel_2, 3, 7, 1, 4)

        self.horizontalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_9, 1, 9, 1, 1)

        self.label_47 = QLabel(self.frame_5)
        self.label_47.setObjectName(u"label_47")
        sizePolicy6.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy6)

        self.gridLayout_6.addWidget(self.label_47, 1, 1, 1, 1)

        self.tolLineEdit = PositiveFloatLineEdit(self.frame_5)
        self.tolLineEdit.setObjectName(u"tolLineEdit")
        sizePolicy3.setHeightForWidth(self.tolLineEdit.sizePolicy().hasHeightForWidth())
        self.tolLineEdit.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.tolLineEdit, 2, 4, 1, 1)

        self.exportToPrefitButton = QPushButton(self.frame_5)
        self.exportToPrefitButton.setObjectName(u"exportToPrefitButton")
        sizePolicy5.setHeightForWidth(self.exportToPrefitButton.sizePolicy().hasHeightForWidth())
        self.exportToPrefitButton.setSizePolicy(sizePolicy5)
        self.exportToPrefitButton.setMinimumSize(QSize(120, 20))

        self.gridLayout_6.addWidget(self.exportToPrefitButton, 1, 10, 1, 1)

        self.optimizerComboBox = QComboBox(self.frame_5)
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.setObjectName(u"optimizerComboBox")
        sizePolicy3.setHeightForWidth(self.optimizerComboBox.sizePolicy().hasHeightForWidth())
        self.optimizerComboBox.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.optimizerComboBox, 1, 4, 1, 1)

        self.fitResultHelpPushButton = QPushButton(self.frame_5)
        self.fitResultHelpPushButton.setObjectName(u"fitResultHelpPushButton")
        self.fitResultHelpPushButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.fitResultHelpPushButton.setIcon(icon11)
        self.fitResultHelpPushButton.setIconSize(QSize(23, 23))

        self.gridLayout_6.addWidget(self.fitResultHelpPushButton, 1, 8, 1, 1)


        self.horizontalLayout_10.addWidget(self.frame_5)

        self.bottomStackedWidget.addWidget(self.fitPage)

        self.gridLayout.addWidget(self.bottomStackedWidget, 1, 1, 1, 3)


        self.verticalLayout.addWidget(self.windowBodyFrame)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy3)
        self.statusBar.setMinimumSize(QSize(0, 27))
        self.statusBar.setStyleSheet(u"")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.pagesStackedWidget.setCurrentIndex(0)
        self.bottomStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
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
        self.swapXYButton.setText(QCoreApplication.translate("MainWindow", u"X\u2194Y", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"DATA", None))
        self.zComboBox.setCurrentText("")
        self.calibrateY1Button.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"RAW Y", None))
        self.calibrateY2Button.setText("")
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"CALIBRATED Y [GHz]", None))
        self.calibrateX2Button.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"CALIBRATED X", None))
        self.mapX1LineEdit.setInputMask("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"RAW X", None))
        self.calibrateX1Button.setText("")
        self.calibrationLabel.setText(QCoreApplication.translate("MainWindow", u"CALIBRATION", None))
        self.calibrationHelpPushButton.setText("")
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"TRANSITIONS", None))
        self.transitionLabel.setText(QCoreApplication.translate("MainWindow", u"LABEL FOR Transition 1", None))
#if QT_CONFIG(statustip)
        self.tagDispersiveDressedRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.tagDispersiveBareRadioButton.setStatusTip(QCoreApplication.translate("MainWindow", u"RR", None))
#endif // QT_CONFIG(statustip)
        self.bareLabelOrder.setText(QCoreApplication.translate("MainWindow", u"    Ordered by: ", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PRE-FIT", None))
#if QT_CONFIG(accessibility)
        self.plotButton.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"PLOT SPECTRUM", None))
        self.autoRunCheckBox.setText(QCoreApplication.translate("MainWindow", u"AUTO-UPDATE", None))
        self.fitLabel.setText(QCoreApplication.translate("MainWindow", u"FIT", None))
        self.fitHelpPushButton.setText("")
        self.fitButton.setText(QCoreApplication.translate("MainWindow", u"RUN FIT", None))
#if QT_CONFIG(tooltip)
        self.pushButton_2.setToolTip(QCoreApplication.translate("MainWindow", u"Load the current value to the initial value", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"RESULTS \u2192 INITIAL", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"SETTINGS: VISUAL", None))
        self.coloringPushButton.setText(QCoreApplication.translate("MainWindow", u"COLORING", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MIN", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MAX", None))

        self.colorComboBox.setCurrentText(QCoreApplication.translate("MainWindow", u"PuOr", None))
        self.bgndSubtractPushButton.setText(QCoreApplication.translate("MainWindow", u"BACKGROUND SUBTRACT", None))
        self.filtersPushButton.setText(QCoreApplication.translate("MainWindow", u"FILTERS", None))
#if QT_CONFIG(accessibility)
        self.frame_4.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.initStateLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"dressed or bare label", None))
        self.evalsCountLineEdit.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"TRANSITIONS", None))
        self.pointsAddLineEdit.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.pointsAddLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"# of x value for spectrum sweep", None))
        self.prefitResultHelpPushButton.setText("")
#if QT_CONFIG(tooltip)
        self.exportToFitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the pre-fitted parameters to the initial value of the fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToFitButton.setText(QCoreApplication.translate("MainWindow", u"RESULTS \u2192 FIT", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"EVALS COUNT", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"POINTS ADDED", None))
        self.statusTextLabel.setText(QCoreApplication.translate("MainWindow", u"Status Text", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"PHOTONS", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.mseLabel.setText(QCoreApplication.translate("MainWindow", u"MSE:  0.647 GHz^2   (+0.86%)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"INITIAL STATE", None))
        self.numericalSpectrumSettingsLabel.setText(QCoreApplication.translate("MainWindow", u"SETTINGS: NUMERICAL SPECTRUM", None))
        self.numericalSpectrumSettingsHelpPushButton.setText("")
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"SETTINGS: FIT", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"TOLERANCE", None))
        self.label_49.setText(QCoreApplication.translate("MainWindow", u"STATUS:", None))
        self.mseLabel_2.setText(QCoreApplication.translate("MainWindow", u"MSE:  0.647 GHz^2   (+0.86%)", None))
        self.statusTextLabel_2.setText(QCoreApplication.translate("MainWindow", u"Status Text", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"OPTIMIZER", None))
        self.tolLineEdit.setText(QCoreApplication.translate("MainWindow", u"1e-6", None))
#if QT_CONFIG(tooltip)
        self.exportToPrefitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the fitted parameters to the pre-fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToPrefitButton.setText(QCoreApplication.translate("MainWindow", u"RESULTS \u2192 PRE-FIT", None))
        self.optimizerComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"L-BFGS-B", None))
        self.optimizerComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Nelder-Mead", None))
        self.optimizerComboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Powell", None))
        self.optimizerComboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"shgo", None))
        self.optimizerComboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"differential evolution", None))

        self.fitResultHelpPushButton.setText("")
        pass
    # retranslateUi

