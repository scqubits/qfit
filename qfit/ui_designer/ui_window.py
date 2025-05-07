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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

from qfit.views.calibration_view import CalibrationLineEdit
from qfit.widgets.data_extracting import (DataExtractingWidget, ListView)
from qfit.widgets.mpl_canvas import MplFigureCanvas
from qfit.widgets.validated_line_edits import (MultiIntTuplesLineEdit, MultiIntsLineEdit)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1333, 776)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
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
                        "    background: #64568e;\n"
"    min-width: 20px;\n"
"	border-radius: 5px\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: #3b3940;\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: #3b3940;\n"
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
"	border-radius: 0px;\n"
" }\n"
"\n"
" QSc"
                        "rollBar::handle:vertical {	\n"
"	background: #64568e;\n"
"    min-height: 25px;\n"
"	border-radius: 5px\n"
" }\n"
"\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: #3b3940;\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
"\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: #3b3940;\n"
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
"    font-size: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    bord"
                        "er: 1px solid #DBBCFB;\n"
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
"QCheckBox:disabled {	\n"
"	color: rgb(60, 60, 60);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled {	\n"
"	border: 1px solid rgb(60, 60, 60);\n"
"   background: transparent;\n"
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
"	b"
                        "order: 1px solid #BE82FA;\n"
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
"	background-color: #3c3a40;\n"
"}\n"
"\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: #3c3a40;\n"
"}\n"
"\n"
"QSlider::handle:vertical {\n"
"    background-color: #64568e;\n"
"	borde"
                        "r: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: #64568e;\n"
"}\n"
"\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: #64568e;\n"
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
"	"
                        "background-color: rgb(93,93,93);\n"
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
""
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
        self.gridLayout_5 = QGridLayout(self.centralWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.windowBodyFrame = QFrame(self.centralWidget)
        self.windowBodyFrame.setObjectName(u"windowBodyFrame")
        sizePolicy.setHeightForWidth(self.windowBodyFrame.sizePolicy().hasHeightForWidth())
        self.windowBodyFrame.setSizePolicy(sizePolicy)
        self.windowBodyFrame.setMinimumSize(QSize(120, 0))
        self.windowBodyFrame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(33,33,33);\n"
"}")
        self.gridLayout = QGridLayout(self.windowBodyFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_frame = QFrame(self.windowBodyFrame)
        self.menu_frame.setObjectName(u"menu_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy1)
        self.menu_frame.setMinimumSize(QSize(200, 0))
        self.menu_frame.setMaximumSize(QSize(200, 16777215))
        self.menu_frame.setStyleSheet(u"QFrame {\n"
"	color: white;\n"
"	background-color: rgb(18, 18, 18);\n"
"}")
        self.menu_frame.setFrameShape(QFrame.NoFrame)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.menu_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(37, 0, 20, 0)
        self.modeSetupFigButton = QPushButton(self.menu_frame)
        self.modeSetupFigButton.setObjectName(u"modeSetupFigButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modeSetupFigButton.sizePolicy().hasHeightForWidth())
        self.modeSetupFigButton.setSizePolicy(sizePolicy2)
        self.modeSetupFigButton.setMinimumSize(QSize(145, 70))
        self.modeSetupFigButton.setMaximumSize(QSize(145, 70))
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setWeight(QFont.Light)
        self.modeSetupFigButton.setFont(font1)
        self.modeSetupFigButton.setStyleSheet(u"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-size: 16px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:checked {	\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:disabled {	\n"
"	color: rgb(128, 128, 128);\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/svg/file-import-solid.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeSetupFigButton.setIcon(icon1)
        self.modeSetupFigButton.setIconSize(QSize(24, 24))
        self.modeSetupFigButton.setCheckable(True)
        self.modeSetupFigButton.setChecked(True)
        self.modeSetupFigButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeSetupFigButton, 2, 0, 1, 1)

        self.toggleMenuButton = QPushButton(self.menu_frame)
        self.toggleMenuButton.setObjectName(u"toggleMenuButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.toggleMenuButton.sizePolicy().hasHeightForWidth())
        self.toggleMenuButton.setSizePolicy(sizePolicy3)
        self.toggleMenuButton.setMinimumSize(QSize(0, 0))
        self.toggleMenuButton.setMaximumSize(QSize(16777215, 16777215))
        self.toggleMenuButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleMenuButton.setStyleSheet(u"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-size: 16px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(52, 59, 72);\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"\n"
"QPushButton:checked {	\n"
"	background-color: rgb(85, 170, 255);\n"
"	color: rgb(190, 130, 250);\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/svg/cil-menu.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleMenuButton.setIcon(icon2)
        self.toggleMenuButton.setIconSize(QSize(24, 24))
        self.toggleMenuButton.setAutoDefault(False)
        self.toggleMenuButton.setFlat(False)

        self.gridLayout_2.addWidget(self.toggleMenuButton, 1, 0, 1, 2)

        self.modeTagButton = QPushButton(self.menu_frame)
        self.modeTagButton.setObjectName(u"modeTagButton")
        self.modeTagButton.setEnabled(False)
        self.modeTagButton.setMinimumSize(QSize(145, 70))
        self.modeTagButton.setMaximumSize(QSize(145, 70))
        self.modeTagButton.setFont(font1)
        self.modeTagButton.setStyleSheet(u"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-size: 16px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:checked {	\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:disabled {	\n"
"	color: rgb(128, 128, 128);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/svg/cil-location-pin.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeTagButton.setIcon(icon3)
        self.modeTagButton.setIconSize(QSize(24, 24))
        self.modeTagButton.setCheckable(True)
        self.modeTagButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeTagButton, 4, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 7, 0, 1, 1)

        self.modePrefitButton = QPushButton(self.menu_frame)
        self.modePrefitButton.setObjectName(u"modePrefitButton")
        self.modePrefitButton.setEnabled(False)
        self.modePrefitButton.setMinimumSize(QSize(145, 70))
        self.modePrefitButton.setMaximumSize(QSize(145, 70))
        self.modePrefitButton.setFont(font1)
        self.modePrefitButton.setStyleSheet(u"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-size: 16px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:checked {	\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:disabled {	\n"
"	color: rgb(128, 128, 128);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/svg/slider-horizontal.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modePrefitButton.setIcon(icon4)
        self.modePrefitButton.setIconSize(QSize(24, 24))
        self.modePrefitButton.setCheckable(True)
        self.modePrefitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modePrefitButton, 5, 0, 1, 2)

        self.modeSelectButton = QPushButton(self.menu_frame)
        self.modeSelectButton.setObjectName(u"modeSelectButton")
        self.modeSelectButton.setEnabled(False)
        self.modeSelectButton.setMinimumSize(QSize(145, 70))
        self.modeSelectButton.setMaximumSize(QSize(145, 70))
        self.modeSelectButton.setFont(font1)
        self.modeSelectButton.setStyleSheet(u"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-size: 16px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:checked {	\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:disabled {	\n"
"	color: rgb(128, 128, 128);\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/icons/svg/ruler-square.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeSelectButton.setIcon(icon5)
        self.modeSelectButton.setIconSize(QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeSelectButton, 3, 0, 1, 2)

        self.verticalSpacer_14 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer_14, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.modeFitButton = QPushButton(self.menu_frame)
        self.modeFitButton.setObjectName(u"modeFitButton")
        self.modeFitButton.setEnabled(False)
        self.modeFitButton.setMinimumSize(QSize(145, 70))
        self.modeFitButton.setMaximumSize(QSize(145, 70))
        self.modeFitButton.setFont(font1)
        self.modeFitButton.setStyleSheet(u"QPushButton {	\n"
"	text-align: left;\n"
"	color: white;\n"
"	border: none;\n"
"	background-color: transparent;\n"
"	font-size: 16px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:checked {	\n"
"	color: rgb(190, 130, 250);\n"
"}\n"
"QPushButton:disabled {	\n"
"	color: rgb(128, 128, 128);\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/icons/svg/cil-speedometer.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.modeFitButton.setIcon(icon6)
        self.modeFitButton.setIconSize(QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeFitButton, 6, 0, 1, 1)

        self.settingsPushButton = QPushButton(self.menu_frame)
        self.settingsPushButton.setObjectName(u"settingsPushButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.settingsPushButton.sizePolicy().hasHeightForWidth())
        self.settingsPushButton.setSizePolicy(sizePolicy4)
        self.settingsPushButton.setMinimumSize(QSize(40, 40))
        self.settingsPushButton.setMaximumSize(QSize(40, 40))
        self.settingsPushButton.setStyleSheet(u"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: #4B4B4B;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #5C3F83;\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #5C3F83;\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:checked {	\n"
"	background-color: #5C3F83;\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/icons/svg/settings.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon7.addFile(u":/icons/svg/settings-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.settingsPushButton.setIcon(icon7)
        self.settingsPushButton.setIconSize(QSize(20, 20))

        self.gridLayout_2.addWidget(self.settingsPushButton, 9, 0, 1, 1)


        self.gridLayout.addWidget(self.menu_frame, 0, 0, 4, 1)

        self.pagesStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.pagesStackedWidget.setObjectName(u"pagesStackedWidget")
        sizePolicy4.setHeightForWidth(self.pagesStackedWidget.sizePolicy().hasHeightForWidth())
        self.pagesStackedWidget.setSizePolicy(sizePolicy4)
        self.pagesStackedWidget.setMinimumSize(QSize(470, 0))
        self.pagesStackedWidget.setMaximumSize(QSize(470, 10000))
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(9)
        font2.setKerning(True)
        self.pagesStackedWidget.setFont(font2)
        self.pagesStackedWidget.setStyleSheet(u"")
        self.pagesStackedWidget.setFrameShadow(QFrame.Raised)
        self.setupFigsWidget = QWidget()
        self.setupFigsWidget.setObjectName(u"setupFigsWidget")
        self.verticalLayout_7 = QVBoxLayout(self.setupFigsWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frame = QFrame(self.setupFigsWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame)
        self.verticalLayout_12.setSpacing(15)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.metadataTitleWidget = QWidget(self.frame)
        self.metadataTitleWidget.setObjectName(u"metadataTitleWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.metadataTitleWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.metadataTitleWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy5)
        self.label_8.setMinimumSize(QSize(0, 0))
        self.label_8.setFont(font1)
        self.label_8.setStyleSheet(u"QLabel {\n"
"    font-family: \"Roboto Medium\";\n"
"    font-size: 16px;\n"
"    color: rgb(190, 130, 250);\n"
"}")
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_8)

        self.fileNameInfo = QLabel(self.metadataTitleWidget)
        self.fileNameInfo.setObjectName(u"fileNameInfo")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.fileNameInfo.sizePolicy().hasHeightForWidth())
        self.fileNameInfo.setSizePolicy(sizePolicy6)

        self.horizontalLayout_3.addWidget(self.fileNameInfo)

        self.horizontalSpacer_7 = QSpacerItem(302, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)


        self.verticalLayout_12.addWidget(self.metadataTitleWidget)

        self.scrollArea_2 = QScrollArea(self.frame)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.scrollArea_2.sizePolicy().hasHeightForWidth())
        self.scrollArea_2.setSizePolicy(sizePolicy7)
        self.scrollArea_2.setMinimumSize(QSize(0, 210))
        self.scrollArea_2.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea_2.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.scrollArea_2.setFrameShape(QFrame.NoFrame)
        self.scrollArea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 422, 210))
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy8)
        self.scrollAreaWidgetContents.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(15)
        self.gridLayout_3.setContentsMargins(-1, 5, 18, 5)
        self.widget_15 = QWidget(self.scrollAreaWidgetContents)
        self.widget_15.setObjectName(u"widget_15")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_15)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 5, 0)
        self.label_4 = QLabel(self.widget_15)
        self.label_4.setObjectName(u"label_4")
        sizePolicy5.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy5)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_10.addWidget(self.label_4)

        self.yCandInfo = QLabel(self.widget_15)
        self.yCandInfo.setObjectName(u"yCandInfo")
        sizePolicy9 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.yCandInfo.sizePolicy().hasHeightForWidth())
        self.yCandInfo.setSizePolicy(sizePolicy9)
        self.yCandInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.yCandInfo.setWordWrap(True)

        self.horizontalLayout_10.addWidget(self.yCandInfo)


        self.gridLayout_3.addWidget(self.widget_15, 3, 0, 1, 1)

        self.widget_20 = QWidget(self.scrollAreaWidgetContents)
        self.widget_20.setObjectName(u"widget_20")
        sizePolicy8.setHeightForWidth(self.widget_20.sizePolicy().hasHeightForWidth())
        self.widget_20.setSizePolicy(sizePolicy8)
        self.horizontalLayout_21 = QHBoxLayout(self.widget_20)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(5, 0, 5, 0)
        self.label_43 = QLabel(self.widget_20)
        self.label_43.setObjectName(u"label_43")
        sizePolicy5.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy5)
        self.label_43.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_21.addWidget(self.label_43)

        self.zCandInfo = QLabel(self.widget_20)
        self.zCandInfo.setObjectName(u"zCandInfo")
        sizePolicy9.setHeightForWidth(self.zCandInfo.sizePolicy().hasHeightForWidth())
        self.zCandInfo.setSizePolicy(sizePolicy9)
        self.zCandInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.zCandInfo.setWordWrap(True)

        self.horizontalLayout_21.addWidget(self.zCandInfo)


        self.gridLayout_3.addWidget(self.widget_20, 4, 0, 1, 1)

        self.widget_16 = QWidget(self.scrollAreaWidgetContents)
        self.widget_16.setObjectName(u"widget_16")
        sizePolicy3.setHeightForWidth(self.widget_16.sizePolicy().hasHeightForWidth())
        self.widget_16.setSizePolicy(sizePolicy3)
        self.horizontalLayout_19 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(5, 0, 5, 0)
        self.label_10 = QLabel(self.widget_16)
        self.label_10.setObjectName(u"label_10")
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_19.addWidget(self.label_10)

        self.discAxesInfo = QLabel(self.widget_16)
        self.discAxesInfo.setObjectName(u"discAxesInfo")
        sizePolicy9.setHeightForWidth(self.discAxesInfo.sizePolicy().hasHeightForWidth())
        self.discAxesInfo.setSizePolicy(sizePolicy9)
        self.discAxesInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.discAxesInfo.setWordWrap(True)

        self.horizontalLayout_19.addWidget(self.discAxesInfo)


        self.gridLayout_3.addWidget(self.widget_16, 5, 0, 1, 1)

        self.widget_2 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(5, 0, 5, 0)
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy5.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy5)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.label_2)

        self.dimInfo = QLabel(self.widget_2)
        self.dimInfo.setObjectName(u"dimInfo")
        sizePolicy9.setHeightForWidth(self.dimInfo.sizePolicy().hasHeightForWidth())
        self.dimInfo.setSizePolicy(sizePolicy9)
        self.dimInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.dimInfo.setWordWrap(True)

        self.horizontalLayout_6.addWidget(self.dimInfo)


        self.gridLayout_3.addWidget(self.widget_2, 1, 0, 1, 1)

        self.widget_14 = QWidget(self.scrollAreaWidgetContents)
        self.widget_14.setObjectName(u"widget_14")
        sizePolicy3.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy3)
        self.widget_14.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_9 = QHBoxLayout(self.widget_14)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(5, 0, 5, 0)
        self.label_3 = QLabel(self.widget_14)
        self.label_3.setObjectName(u"label_3")
        sizePolicy5.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy5)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_9.addWidget(self.label_3)

        self.xCandInfo = QLabel(self.widget_14)
        self.xCandInfo.setObjectName(u"xCandInfo")
        sizePolicy9.setHeightForWidth(self.xCandInfo.sizePolicy().hasHeightForWidth())
        self.xCandInfo.setSizePolicy(sizePolicy9)
        self.xCandInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.xCandInfo.setWordWrap(True)

        self.horizontalLayout_9.addWidget(self.xCandInfo)


        self.gridLayout_3.addWidget(self.widget_14, 2, 0, 1, 1)

        self.widget_19 = QWidget(self.scrollAreaWidgetContents)
        self.widget_19.setObjectName(u"widget_19")
        self.horizontalLayout_22 = QHBoxLayout(self.widget_19)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(5, 0, 5, 0)
        self.label_42 = QLabel(self.widget_19)
        self.label_42.setObjectName(u"label_42")
        sizePolicy5.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy5)
        self.label_42.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_22.addWidget(self.label_42)

        self.fileLocInfo = QLabel(self.widget_19)
        self.fileLocInfo.setObjectName(u"fileLocInfo")
        sizePolicy9.setHeightForWidth(self.fileLocInfo.sizePolicy().hasHeightForWidth())
        self.fileLocInfo.setSizePolicy(sizePolicy9)
        self.fileLocInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.fileLocInfo.setWordWrap(True)

        self.horizontalLayout_22.addWidget(self.fileLocInfo)


        self.gridLayout_3.addWidget(self.widget_19, 0, 0, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 2, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_9, 6, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_12.addWidget(self.scrollArea_2)

        self.label_39 = QLabel(self.frame)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font1)
        self.label_39.setStyleSheet(u"QLabel {\n"
"    font-family: \"Roboto Medium\";\n"
"    font-size: 16px;\n"
"    color: rgb(190, 130, 250);\n"
"}")

        self.verticalLayout_12.addWidget(self.label_39)

        self.widget_17 = QWidget(self.frame)
        self.widget_17.setObjectName(u"widget_17")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.widget_17.sizePolicy().hasHeightForWidth())
        self.widget_17.setSizePolicy(sizePolicy10)
        self.widget_17.setMinimumSize(QSize(0, 230))
        self.widget_17.setMaximumSize(QSize(16777215, 250))
        self.gridLayout_4 = QGridLayout(self.widget_17)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(20)
        self.yAxesScrollArea = QScrollArea(self.widget_17)
        self.yAxesScrollArea.setObjectName(u"yAxesScrollArea")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.yAxesScrollArea.sizePolicy().hasHeightForWidth())
        self.yAxesScrollArea.setSizePolicy(sizePolicy11)
        self.yAxesScrollArea.setMinimumSize(QSize(0, 0))
        self.yAxesScrollArea.setMaximumSize(QSize(200, 16777215))
        self.yAxesScrollArea.setStyleSheet(u"background-color: #2A2A2A;")
        self.yAxesScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 187, 180))
        self.verticalLayout_19 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.yAxesScrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout_4.addWidget(self.yAxesScrollArea, 1, 1, 1, 1)

        self.label_38 = QLabel(self.widget_17)
        self.label_38.setObjectName(u"label_38")
        sizePolicy6.setHeightForWidth(self.label_38.sizePolicy().hasHeightForWidth())
        self.label_38.setSizePolicy(sizePolicy6)
        self.label_38.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_38, 0, 1, 1, 1)

        self.label_11 = QLabel(self.widget_17)
        self.label_11.setObjectName(u"label_11")
        sizePolicy6.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy6)
        self.label_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)

        self.xAxesScrollArea = QScrollArea(self.widget_17)
        self.xAxesScrollArea.setObjectName(u"xAxesScrollArea")
        sizePolicy3.setHeightForWidth(self.xAxesScrollArea.sizePolicy().hasHeightForWidth())
        self.xAxesScrollArea.setSizePolicy(sizePolicy3)
        self.xAxesScrollArea.setMinimumSize(QSize(0, 0))
        self.xAxesScrollArea.setMaximumSize(QSize(200, 16777215))
        self.xAxesScrollArea.setStyleSheet(u"background-color: #2A2A2A;")
        self.xAxesScrollArea.setFrameShape(QFrame.NoFrame)
        self.xAxesScrollArea.setFrameShadow(QFrame.Sunken)
        self.xAxesScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 189, 182))
        self.verticalLayout_18 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.xAxesScrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_4.addWidget(self.xAxesScrollArea, 1, 0, 1, 1)


        self.verticalLayout_12.addWidget(self.widget_17)

        self.widget_18 = QWidget(self.frame)
        self.widget_18.setObjectName(u"widget_18")
        self.horizontalLayout_20 = QHBoxLayout(self.widget_18)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.transposeButton = QPushButton(self.widget_18)
        self.transposeButton.setObjectName(u"transposeButton")
        self.transposeButton.setEnabled(True)
        self.transposeButton.setMinimumSize(QSize(208, 30))
        self.transposeButton.setMaximumSize(QSize(208, 30))
        font3 = QFont()
        font3.setFamilies([u"Roboto Medium"])
        font3.setBold(True)
        self.transposeButton.setFont(font3)
        self.transposeButton.setStyleSheet(u"QPushButton {\n"
"color: #DBBCFB;\n"
"background-color: #4B4B4B;\n"
"border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"color: #A08CB5;\n"
"background-color: #353535;\n"
"icon: url(:/icons/svg/updown-pressed.svg);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	color: rgb(128, 128, 128);\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/icons/svg/updown.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.transposeButton.setIcon(icon8)

        self.horizontalLayout_20.addWidget(self.transposeButton)


        self.verticalLayout_12.addWidget(self.widget_18)

        self.verticalSpacer_5 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_5)

        self.widget_21 = QWidget(self.frame)
        self.widget_21.setObjectName(u"widget_21")
        sizePolicy3.setHeightForWidth(self.widget_21.sizePolicy().hasHeightForWidth())
        self.widget_21.setSizePolicy(sizePolicy3)
        self.horizontalLayout_23 = QHBoxLayout(self.widget_21)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.finalizeStep0Button = QPushButton(self.widget_21)
        self.finalizeStep0Button.setObjectName(u"finalizeStep0Button")
        self.finalizeStep0Button.setEnabled(True)
        sizePolicy5.setHeightForWidth(self.finalizeStep0Button.sizePolicy().hasHeightForWidth())
        self.finalizeStep0Button.setSizePolicy(sizePolicy5)
        self.finalizeStep0Button.setMinimumSize(QSize(189, 34))
        self.finalizeStep0Button.setMaximumSize(QSize(189, 34))
        self.finalizeStep0Button.setFont(font3)
        self.finalizeStep0Button.setStyleSheet(u"QPushButton{\n"
"color: #212121;\n"
"background-color: #BE82FA;\n"
"border-radius: 6px;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #9163BF;\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"background-color: #4B4B4B;\n"
"	color: rgb(128, 128, 128);\n"
"}")

        self.horizontalLayout_23.addWidget(self.finalizeStep0Button)


        self.verticalLayout_12.addWidget(self.widget_21)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_12.addItem(self.verticalSpacer_7)


        self.verticalLayout_7.addWidget(self.frame)

        self.pagesStackedWidget.addWidget(self.setupFigsWidget)
        self.extractPointsWidget = DataExtractingWidget()
        self.extractPointsWidget.setObjectName(u"extractPointsWidget")
        sizePolicy12 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.extractPointsWidget.sizePolicy().hasHeightForWidth())
        self.extractPointsWidget.setSizePolicy(sizePolicy12)
        self.extractPointsWidget.setMinimumSize(QSize(470, 0))
        self.extractPointsWidget.setMaximumSize(QSize(470, 16777215))
        self.verticalLayout_9 = QVBoxLayout(self.extractPointsWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.calibrationFrame = QFrame(self.extractPointsWidget)
        self.calibrationFrame.setObjectName(u"calibrationFrame")
        sizePolicy13 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.calibrationFrame.sizePolicy().hasHeightForWidth())
        self.calibrationFrame.setSizePolicy(sizePolicy13)
        self.calibrationFrame.setMinimumSize(QSize(0, 0))
        font4 = QFont()
        font4.setFamilies([u"Roboto Medium"])
        self.calibrationFrame.setFont(font4)
        self.calibrationFrame.setCursor(QCursor(Qt.ArrowCursor))
        self.calibrationFrame.setStyleSheet(u"")
        self.calibrationFrame.setFrameShape(QFrame.NoFrame)
        self.calibrationFrame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_17 = QVBoxLayout(self.calibrationFrame)
        self.verticalLayout_17.setSpacing(5)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(5, 20, 0, 0)
        self.widget_3 = QWidget(self.calibrationFrame)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_7 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.widget_3)
        self.label_5.setObjectName(u"label_5")
        sizePolicy2.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy2)
        self.label_5.setMinimumSize(QSize(0, 23))
        self.label_5.setFont(font1)
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
        icon9 = QIcon()
        icon9.addFile(u":/icons/svg/question-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrationHelpPushButton.setIcon(icon9)
        self.calibrationHelpPushButton.setIconSize(QSize(23, 23))

        self.horizontalLayout_7.addWidget(self.calibrationHelpPushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout_17.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.calibrationFrame)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_11 = QHBoxLayout(self.widget_4)
#ifndef Q_OS_MAC
        self.horizontalLayout_11.setSpacing(-1)
#endif
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer_38 = QSpacerItem(23, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_38)

        self.label_13 = QLabel(self.widget_4)
        self.label_13.setObjectName(u"label_13")
        sizePolicy14 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy14)
        self.label_13.setMinimumSize(QSize(42, 0))
        self.label_13.setMaximumSize(QSize(42, 16777215))
        self.label_13.setFont(font4)
        self.label_13.setStyleSheet(u"font-size: 13px;")
        self.label_13.setText(u"Z")
        self.label_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_13)

        self.zComboBox = QComboBox(self.widget_4)
        self.zComboBox.setObjectName(u"zComboBox")
        sizePolicy4.setHeightForWidth(self.zComboBox.sizePolicy().hasHeightForWidth())
        self.zComboBox.setSizePolicy(sizePolicy4)
        self.zComboBox.setMinimumSize(QSize(330, 30))
        self.zComboBox.setMaximumSize(QSize(330, 30))
        self.zComboBox.setAutoFillBackground(False)
        self.zComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.zComboBox.setFrame(True)

        self.horizontalLayout_11.addWidget(self.zComboBox)

        self.horizontalSpacer_39 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_39)


        self.verticalLayout_17.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.calibrationFrame)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy3.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy3)
        self.horizontalLayout_12 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer_37 = QSpacerItem(23, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_37)

        self.label_12 = QLabel(self.widget_5)
        self.label_12.setObjectName(u"label_12")
        sizePolicy15 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy15.setHorizontalStretch(42)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy15)
        self.label_12.setMinimumSize(QSize(42, 0))
        self.label_12.setStyleSheet(u"font-size: 13px;")
        self.label_12.setText(u"AXIS X")
        self.label_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_12)

        self.horizontalSpacer_36 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_36)


        self.verticalLayout_17.addWidget(self.widget_5)

        self.calibrateXScrollArea = QScrollArea(self.calibrationFrame)
        self.calibrateXScrollArea.setObjectName(u"calibrateXScrollArea")
        self.calibrateXScrollArea.setMinimumSize(QSize(0, 250))
        self.calibrateXScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);\n"
"border: None;")
        self.calibrateXScrollArea.setWidgetResizable(True)
        self.calibrateXScrollAreaWidget = QWidget()
        self.calibrateXScrollAreaWidget.setObjectName(u"calibrateXScrollAreaWidget")
        self.calibrateXScrollAreaWidget.setGeometry(QRect(0, 0, 100, 250))
        sizePolicy13.setHeightForWidth(self.calibrateXScrollAreaWidget.sizePolicy().hasHeightForWidth())
        self.calibrateXScrollAreaWidget.setSizePolicy(sizePolicy13)
        self.verticalLayout_5 = QVBoxLayout(self.calibrateXScrollAreaWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.calibrateXScrollArea.setWidget(self.calibrateXScrollAreaWidget)

        self.verticalLayout_17.addWidget(self.calibrateXScrollArea)

        self.widget_6 = QWidget(self.calibrationFrame)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, -1, 0, -1)
        self.horizontalSpacer_40 = QSpacerItem(23, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_40)

        self.label_14 = QLabel(self.widget_6)
        self.label_14.setObjectName(u"label_14")
        sizePolicy14.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy14)
        self.label_14.setStyleSheet(u"font-size: 13px;")
        self.label_14.setText(u"AXIS Y")
        self.label_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_14)

        self.horizontalSpacer_41 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_41)


        self.verticalLayout_17.addWidget(self.widget_6)

        self.calibrateYGridFrame = QFrame(self.calibrationFrame)
        self.calibrateYGridFrame.setObjectName(u"calibrateYGridFrame")
        sizePolicy4.setHeightForWidth(self.calibrateYGridFrame.sizePolicy().hasHeightForWidth())
        self.calibrateYGridFrame.setSizePolicy(sizePolicy4)
        self.calibrateYGridFrame.setMinimumSize(QSize(450, 100))
        self.calibrateYGridFrame.setMaximumSize(QSize(450, 16777215))
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
"}\n"
"QPushButton:checked {\n"
"	background-color: #5C3F83;\n"
"}")
        self.gridLayout_11 = QGridLayout(self.calibrateYGridFrame)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(0)
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(0, 0, 0, 12)
        self.label_19 = QLabel(self.calibrateYGridFrame)
        self.label_19.setObjectName(u"label_19")
        sizePolicy6.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy6)
        self.label_19.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_19, 1, 4, 1, 1)

        self.horizontalSpacer_46 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_46, 1, 3, 1, 1)

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
        icon10 = QIcon()
        icon10.addFile(u":/icons/svg/target.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrateY2Button.setIcon(icon10)
        self.calibrateY2Button.setCheckable(True)
        self.calibrateY2Button.setChecked(False)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 2, 1, 1, 1)

        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY1LineEdit.setObjectName(u"rawY1LineEdit")
        sizePolicy4.setHeightForWidth(self.rawY1LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY1LineEdit.setSizePolicy(sizePolicy4)
        self.rawY1LineEdit.setMinimumSize(QSize(145, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(145, 16777215))
#if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 1, 6, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY1LineEdit.setObjectName(u"mapY1LineEdit")
        sizePolicy4.setHeightForWidth(self.mapY1LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY1LineEdit.setSizePolicy(sizePolicy4)
        self.mapY1LineEdit.setMinimumSize(QSize(145, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(145, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 1, 11, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridFrame)
        self.label_20.setObjectName(u"label_20")
        sizePolicy6.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy6)
        self.label_20.setFont(font4)
        self.label_20.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span></p></body></html>")

        self.gridLayout_11.addWidget(self.label_20, 2, 4, 1, 1)

        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY2LineEdit.setObjectName(u"rawY2LineEdit")
        sizePolicy4.setHeightForWidth(self.rawY2LineEdit.sizePolicy().hasHeightForWidth())
        self.rawY2LineEdit.setSizePolicy(sizePolicy4)
        self.rawY2LineEdit.setMinimumSize(QSize(145, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(145, 16777215))
        self.rawY2LineEdit.setFont(font4)
#if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 2, 6, 1, 1)

        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY2LineEdit.setObjectName(u"mapY2LineEdit")
        sizePolicy4.setHeightForWidth(self.mapY2LineEdit.sizePolicy().hasHeightForWidth())
        self.mapY2LineEdit.setSizePolicy(sizePolicy4)
        self.mapY2LineEdit.setMinimumSize(QSize(145, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(145, 16777215))
#if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 2, 11, 1, 1)

        self.horizontalSpacer_21 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_21, 1, 10, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridFrame)
        self.label_21.setObjectName(u"label_21")
        sizePolicy6.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy6)
        self.label_21.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">1</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_21, 1, 9, 1, 1)

        self.horizontalSpacer_23 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_23, 1, 0, 1, 1)

        self.horizontalSpacer_22 = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_22, 1, 12, 1, 1)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_24, 1, 5, 1, 1)

        self.label_23 = QLabel(self.calibrateYGridFrame)
        self.label_23.setObjectName(u"label_23")
        sizePolicy4.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy4)

        self.gridLayout_11.addWidget(self.label_23, 0, 6, 1, 1)

        self.label_24 = QLabel(self.calibrateYGridFrame)
        self.label_24.setObjectName(u"label_24")
        sizePolicy4.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy4)
        self.label_24.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.label_24, 0, 11, 1, 1)

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
        self.calibrateY1Button.setIcon(icon10)
        self.calibrateY1Button.setCheckable(True)
        self.calibrateY1Button.setChecked(False)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 1, 1, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridFrame)
        self.label_22.setObjectName(u"label_22")
        sizePolicy6.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy6)
        self.label_22.setText(u"<html><head/><body><p align=\"right\">Y<span style=\" vertical-align:sub;\">2</span>'</p></body></html>")

        self.gridLayout_11.addWidget(self.label_22, 2, 9, 1, 1)

        self.horizontalSpacer_45 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_45, 1, 8, 1, 1)

        self.horizontalSpacer_47 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_47, 2, 12, 1, 1)


        self.verticalLayout_17.addWidget(self.calibrateYGridFrame)

        self.calibrationTitleWidget = QWidget(self.calibrationFrame)
        self.calibrationTitleWidget.setObjectName(u"calibrationTitleWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.calibrationTitleWidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 24, 0)

        self.verticalLayout_17.addWidget(self.calibrationTitleWidget)

        self.widget_7 = QWidget(self.calibrationFrame)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_14 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")

        self.verticalLayout_17.addWidget(self.widget_7)

        self.verticalSpacer_2 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_2)


        self.verticalLayout_9.addWidget(self.calibrationFrame)

        self.pagesStackedWidget.addWidget(self.extractPointsWidget)
        self.taggingWidget = QWidget()
        self.taggingWidget.setObjectName(u"taggingWidget")
        sizePolicy12.setHeightForWidth(self.taggingWidget.sizePolicy().hasHeightForWidth())
        self.taggingWidget.setSizePolicy(sizePolicy12)
        self.taggingWidget.setMinimumSize(QSize(470, 0))
        self.taggingWidget.setMaximumSize(QSize(470, 16777215))
        self.verticalLayout_10 = QVBoxLayout(self.taggingWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_9 = QFrame(self.taggingWidget)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy13.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy13)
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
        self.newRowButton.setMaximumSize(QSize(86, 16777215))
        self.newRowButton.setFont(font3)
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
        icon11 = QIcon()
        icon11.addFile(u":/icons/svg/plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.newRowButton.setIcon(icon11)
        self.newRowButton.setIconSize(QSize(20, 20))

        self.horizontalLayout_16.addWidget(self.newRowButton)

        self.clearAllButton = QPushButton(self.widget_9)
        self.clearAllButton.setObjectName(u"clearAllButton")
        sizePolicy4.setHeightForWidth(self.clearAllButton.sizePolicy().hasHeightForWidth())
        self.clearAllButton.setSizePolicy(sizePolicy4)
        self.clearAllButton.setMinimumSize(QSize(109, 30))
        self.clearAllButton.setMaximumSize(QSize(109, 30))
        self.clearAllButton.setFont(font3)
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
        icon12 = QIcon()
        icon12.addFile(u":/icons/svg/trash.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.clearAllButton.setIcon(icon12)

        self.horizontalLayout_16.addWidget(self.clearAllButton)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_14)


        self.gridLayout_7.addWidget(self.widget_9, 1, 0, 1, 2)

        self.label_32 = QLabel(self.frame_10)
        self.label_32.setObjectName(u"label_32")
        sizePolicy10.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy10)
        self.label_32.setMinimumSize(QSize(0, 23))
        self.label_32.setFont(font1)
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
        sizePolicy16 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.datasetListView.sizePolicy().hasHeightForWidth())
        self.datasetListView.setSizePolicy(sizePolicy16)
        self.datasetListView.setMinimumSize(QSize(159, 500))
        self.datasetListView.setMaximumSize(QSize(120, 500))
        font5 = QFont()
        font5.setFamilies([u"Roboto Medium"])
        font5.setPointSize(13)
        self.datasetListView.setFont(font5)
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
        self.noTagRadioButton.setFont(font4)
        self.noTagRadioButton.setText(u"Unknown")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.gridLayout_8.addWidget(self.noTagRadioButton, 0, 1, 1, 11)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_6, 2, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_11, 21, 11, 1, 1)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.widget_11)
        self.tagDispersiveDressedRadioButton.setObjectName(u"tagDispersiveDressedRadioButton")
        font6 = QFont()
        font6.setFamilies([u"Roboto Medium"])
        font6.setKerning(True)
        self.tagDispersiveDressedRadioButton.setFont(font6)
#if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setText(u"By dressed indices")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.gridLayout_8.addWidget(self.tagDispersiveDressedRadioButton, 1, 1, 1, 11)

        self.tagDispersiveBareRadioButton = QRadioButton(self.widget_11)
        self.tagDispersiveBareRadioButton.setObjectName(u"tagDispersiveBareRadioButton")
        self.tagDispersiveBareRadioButton.setFont(font4)
#if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setText(u"By bare indices")
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
        self.label_15 = QLabel(self.tagBareGroupBox)
        self.label_15.setObjectName(u"label_15")
        sizePolicy17 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy17)
        self.label_15.setMinimumSize(QSize(0, 0))
        self.label_15.setMaximumSize(QSize(230, 100))
        self.label_15.setStyleSheet(u"QLabel {\n"
"    font-size: 10pt;\n"
"}")
        self.label_15.setWordWrap(True)

        self.gridLayout_14.addWidget(self.label_15, 8, 1, 1, 1)

        self.label_25 = QLabel(self.tagBareGroupBox)
        self.label_25.setObjectName(u"label_25")
        sizePolicy18 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy18.setHorizontalStretch(0)
        sizePolicy18.setVerticalStretch(0)
        sizePolicy18.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy18)
        self.label_25.setText(u"Photons")

        self.gridLayout_14.addWidget(self.label_25, 5, 1, 1, 1)

        self.label_28 = QLabel(self.tagBareGroupBox)
        self.label_28.setObjectName(u"label_28")
        sizePolicy10.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy10)
        self.label_28.setText(u"Initial")
        self.label_28.setIndent(-1)

        self.gridLayout_14.addWidget(self.label_28, 1, 1, 1, 1)

        self.finalBareStateLineEdit = MultiIntTuplesLineEdit(self.tagBareGroupBox)
        self.finalBareStateLineEdit.setObjectName(u"finalBareStateLineEdit")
        sizePolicy7.setHeightForWidth(self.finalBareStateLineEdit.sizePolicy().hasHeightForWidth())
        self.finalBareStateLineEdit.setSizePolicy(sizePolicy7)
        self.finalBareStateLineEdit.setMinimumSize(QSize(230, 30))
        self.finalBareStateLineEdit.setMaximumSize(QSize(230, 30))
        self.finalBareStateLineEdit.setStyleSheet(u"")
        self.finalBareStateLineEdit.setPlaceholderText(u"<level subsys1>, <level subsys2>, ...")

        self.gridLayout_14.addWidget(self.finalBareStateLineEdit, 4, 1, 1, 1)

        self.initialBareStateLineEdit = MultiIntTuplesLineEdit(self.tagBareGroupBox)
        self.initialBareStateLineEdit.setObjectName(u"initialBareStateLineEdit")
        self.initialBareStateLineEdit.setMinimumSize(QSize(230, 30))
        self.initialBareStateLineEdit.setMaximumSize(QSize(230, 30))
        self.initialBareStateLineEdit.setPlaceholderText(u"<level subsys1>, <level subsys2>, ...")

        self.gridLayout_14.addWidget(self.initialBareStateLineEdit, 2, 1, 1, 1)

        self.label_48 = QLabel(self.tagBareGroupBox)
        self.label_48.setObjectName(u"label_48")
        sizePolicy14.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy14)
        self.label_48.setMinimumSize(QSize(2, 223))
        self.label_48.setMaximumSize(QSize(2, 16777215))
        self.label_48.setStyleSheet(u"background-color: #2F2F2F")
        self.label_48.setLineWidth(0)

        self.gridLayout_14.addWidget(self.label_48, 0, 0, 10, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName(u"phNumberBareSpinBox")
        sizePolicy19 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy19.setHorizontalStretch(0)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth())
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy19)
        self.phNumberBareSpinBox.setMinimumSize(QSize(96, 35))
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_14.addWidget(self.phNumberBareSpinBox, 6, 1, 1, 1)

        self.label_26 = QLabel(self.tagBareGroupBox)
        self.label_26.setObjectName(u"label_26")
        sizePolicy10.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy10)
        self.label_26.setText(u"Final")

        self.gridLayout_14.addWidget(self.label_26, 3, 1, 1, 1)

        self.bareLabelOrder = QLabel(self.tagBareGroupBox)
        self.bareLabelOrder.setObjectName(u"bareLabelOrder")
        sizePolicy9.setHeightForWidth(self.bareLabelOrder.sizePolicy().hasHeightForWidth())
        self.bareLabelOrder.setSizePolicy(sizePolicy9)
        self.bareLabelOrder.setMaximumSize(QSize(230, 230))
        self.bareLabelOrder.setStyleSheet(u"QLabel {\n"
"    font-size: 10pt;\n"
"}")
        self.bareLabelOrder.setWordWrap(True)

        self.gridLayout_14.addWidget(self.bareLabelOrder, 7, 1, 1, 1)


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
        self.deleteRowButton.setIcon(icon12)
        self.deleteRowButton.setIconSize(QSize(20, 20))

        self.gridLayout_8.addWidget(self.deleteRowButton, 21, 10, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 18, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_8.addItem(self.verticalSpacer_4, 22, 10, 1, 1)

        self.tagDressedGroupBox = QGroupBox(self.widget_11)
        self.tagDressedGroupBox.setObjectName(u"tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
        sizePolicy10.setHeightForWidth(self.tagDressedGroupBox.sizePolicy().hasHeightForWidth())
        self.tagDressedGroupBox.setSizePolicy(sizePolicy10)
        font7 = QFont()
        font7.setFamilies([u"Roboto"])
        font7.setPointSize(13)
        font7.setBold(False)
        font7.setItalic(False)
        self.tagDressedGroupBox.setFont(font7)
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
        self.initialDressedStateLineEdit = MultiIntsLineEdit(self.tagDressedGroupBox)
        self.initialDressedStateLineEdit.setObjectName(u"initialDressedStateLineEdit")
        self.initialDressedStateLineEdit.setMinimumSize(QSize(230, 30))
        self.initialDressedStateLineEdit.setMaximumSize(QSize(230, 30))

        self.gridLayout_13.addWidget(self.initialDressedStateLineEdit, 2, 2, 1, 1)

        self.label_41 = QLabel(self.tagDressedGroupBox)
        self.label_41.setObjectName(u"label_41")
        sizePolicy14.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy14)
        self.label_41.setMinimumSize(QSize(1, 208))
        self.label_41.setMaximumSize(QSize(2, 16777215))
        self.label_41.setStyleSheet(u"QLabel{\n"
"	width: 1px;\n"
"	background-color: #2F2F2F;\n"
"}")
        self.label_41.setLineWidth(0)
        self.label_41.setIndent(0)

        self.gridLayout_13.addWidget(self.label_41, 1, 0, 8, 1)

        self.label = QLabel(self.tagDressedGroupBox)
        self.label.setObjectName(u"label")
        sizePolicy9.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy9)
        self.label.setMinimumSize(QSize(230, 0))
        self.label.setMaximumSize(QSize(230, 230))
        font8 = QFont()
        font8.setFamilies([u"Roboto Medium"])
        font8.setPointSize(10)
        self.label.setFont(font8)
        self.label.setStyleSheet(u"QLabel {\n"
"    font-size: 10pt;\n"
"}")
        self.label.setWordWrap(True)

        self.gridLayout_13.addWidget(self.label, 7, 2, 1, 1)

        self.finalDressedStateLineEdit = MultiIntsLineEdit(self.tagDressedGroupBox)
        self.finalDressedStateLineEdit.setObjectName(u"finalDressedStateLineEdit")
        self.finalDressedStateLineEdit.setMinimumSize(QSize(230, 30))
        self.finalDressedStateLineEdit.setMaximumSize(QSize(230, 30))

        self.gridLayout_13.addWidget(self.finalDressedStateLineEdit, 4, 2, 1, 1)

        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName(u"label_30")
        sizePolicy18.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy18)
#if QT_CONFIG(tooltip)
        self.label_30.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_30.setText(u"Initial")
        self.label_30.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 1, 2, 1, 1)

        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName(u"label_31")
#if QT_CONFIG(tooltip)
        self.label_31.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_31.setText(u"Final")
        self.label_31.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_31, 3, 2, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName(u"label_29")
        sizePolicy18.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy18)
#if QT_CONFIG(tooltip)
        self.label_29.setToolTip(u"")
#endif // QT_CONFIG(tooltip)
        self.label_29.setText(u"Photons")

        self.gridLayout_13.addWidget(self.label_29, 5, 2, 1, 1)

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

        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 6, 2, 1, 1)


        self.gridLayout_8.addWidget(self.tagDressedGroupBox, 3, 0, 1, 12)


        self.horizontalLayout_17.addWidget(self.widget_11)


        self.gridLayout_7.addWidget(self.widget_10, 2, 0, 2, 1)


        self.verticalLayout_13.addWidget(self.frame_10)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_6)


        self.verticalLayout_10.addWidget(self.frame_9)

        self.pagesStackedWidget.addWidget(self.taggingWidget)
        self.prefitWidget = QWidget()
        self.prefitWidget.setObjectName(u"prefitWidget")
        sizePolicy12.setHeightForWidth(self.prefitWidget.sizePolicy().hasHeightForWidth())
        self.prefitWidget.setSizePolicy(sizePolicy12)
        self.prefitWidget.setMinimumSize(QSize(470, 0))
        self.prefitWidget.setMaximumSize(QSize(470, 16777215))
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
        sizePolicy10.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy10)
        self.horizontalLayout_15 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.widget_8)
        self.label_6.setObjectName(u"label_6")
        sizePolicy10.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy10)
        self.label_6.setMinimumSize(QSize(0, 23))
        self.label_6.setFont(font1)
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
        sizePolicy17.setHeightForWidth(self.prefitScrollArea.sizePolicy().hasHeightForWidth())
        self.prefitScrollArea.setSizePolicy(sizePolicy17)
        self.prefitScrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.prefitScrollArea.setFrameShape(QFrame.NoFrame)
        self.prefitScrollArea.setFrameShadow(QFrame.Plain)
        self.prefitScrollArea.setWidgetResizable(True)
        self.prefitScrollArea.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.prefitScrollAreaWidget = QWidget()
        self.prefitScrollAreaWidget.setObjectName(u"prefitScrollAreaWidget")
        self.prefitScrollAreaWidget.setGeometry(QRect(0, 0, 100, 30))
        self.verticalLayout_11 = QVBoxLayout(self.prefitScrollAreaWidget)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.prefitScrollArea.setWidget(self.prefitScrollAreaWidget)

        self.verticalLayout_6.addWidget(self.prefitScrollArea)


        self.verticalLayout_3.addWidget(self.frame_prefit)

        self.frame_prefit_minmax = QFrame(self.prefitWidget)
        self.frame_prefit_minmax.setObjectName(u"frame_prefit_minmax")
        sizePolicy13.setHeightForWidth(self.frame_prefit_minmax.sizePolicy().hasHeightForWidth())
        self.frame_prefit_minmax.setSizePolicy(sizePolicy13)
        self.frame_prefit_minmax.setMinimumSize(QSize(0, 100))
        self.frame_prefit_minmax.setMaximumSize(QSize(16777215, 0))
        self.verticalLayout_14 = QVBoxLayout(self.frame_prefit_minmax)
#ifndef Q_OS_MAC
        self.verticalLayout_14.setSpacing(-1)
#endif
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.frame_prefit_minmax)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 60))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setStyleSheet(u"background-color: #292929;\n"
"border-top-right-radius: 6px;\n"
"border-bottom-right-radius: 6px;	")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.prefitMinmaxScrollAreaWidget = QWidget()
        self.prefitMinmaxScrollAreaWidget.setObjectName(u"prefitMinmaxScrollAreaWidget")
        self.prefitMinmaxScrollAreaWidget.setGeometry(QRect(0, 0, 100, 60))
        self.verticalLayout_16 = QVBoxLayout(self.prefitMinmaxScrollAreaWidget)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.scrollArea.setWidget(self.prefitMinmaxScrollAreaWidget)

        self.verticalLayout_14.addWidget(self.scrollArea)


        self.verticalLayout_3.addWidget(self.frame_prefit_minmax)

        self.frame_3 = QFrame(self.prefitWidget)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy10.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy10)
        self.frame_3.setMinimumSize(QSize(0, 130))
        self.frame_3.setMaximumSize(QSize(16777215, 130))
        self.frame_3.setStyleSheet(u"")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_15 = QSpacerItem(20, 19, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_15.addItem(self.verticalSpacer_15, 4, 1, 1, 1)

        self.autoRunCheckBox = QCheckBox(self.frame_3)
        self.autoRunCheckBox.setObjectName(u"autoRunCheckBox")
        sizePolicy4.setHeightForWidth(self.autoRunCheckBox.sizePolicy().hasHeightForWidth())
        self.autoRunCheckBox.setSizePolicy(sizePolicy4)
        self.autoRunCheckBox.setMinimumSize(QSize(189, 0))
        self.autoRunCheckBox.setStyleSheet(u"padding-left: 45px")

        self.gridLayout_15.addWidget(self.autoRunCheckBox, 3, 1, 1, 2)

        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_15.addItem(self.verticalSpacer_17, 0, 1, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_18, 1, 0, 1, 1)

        self.horizontalSpacer_30 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_30, 1, 2, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_15.addItem(self.verticalSpacer_13, 2, 3, 3, 1)

        self.horizontalSpacer_31 = QSpacerItem(21, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_31, 1, 4, 1, 1)

        self.plotButton = QPushButton(self.frame_3)
        self.plotButton.setObjectName(u"plotButton")
        sizePolicy4.setHeightForWidth(self.plotButton.sizePolicy().hasHeightForWidth())
        self.plotButton.setSizePolicy(sizePolicy4)
        self.plotButton.setMinimumSize(QSize(189, 34))
        self.plotButton.setMaximumSize(QSize(189, 16777215))
        font9 = QFont()
        font9.setFamilies([u"Roboto Medium"])
        font9.setBold(True)
        font9.setKerning(True)
        self.plotButton.setFont(font9)
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
        icon13 = QIcon()
        icon13.addFile(u":/icons/svg/play.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.plotButton.setIcon(icon13)
        self.plotButton.setIconSize(QSize(15, 15))

        self.gridLayout_15.addWidget(self.plotButton, 1, 1, 1, 1)

        self.verticalSpacer_18 = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_15.addItem(self.verticalSpacer_18, 2, 1, 1, 1)

        self.exportToFitButton = QPushButton(self.frame_3)
        self.exportToFitButton.setObjectName(u"exportToFitButton")
        sizePolicy4.setHeightForWidth(self.exportToFitButton.sizePolicy().hasHeightForWidth())
        self.exportToFitButton.setSizePolicy(sizePolicy4)
        self.exportToFitButton.setMinimumSize(QSize(189, 34))
        self.exportToFitButton.setMaximumSize(QSize(189, 16777215))
        self.exportToFitButton.setFont(font3)
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
        icon14 = QIcon()
        icon14.addFile(u":/icons/svg/copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exportToFitButton.setIcon(icon14)
        self.exportToFitButton.setIconSize(QSize(20, 20))

        self.gridLayout_15.addWidget(self.exportToFitButton, 1, 3, 1, 1)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.pagesStackedWidget.addWidget(self.prefitWidget)
        self.fitWidget = QWidget()
        self.fitWidget.setObjectName(u"fitWidget")
        sizePolicy12.setHeightForWidth(self.fitWidget.sizePolicy().hasHeightForWidth())
        self.fitWidget.setSizePolicy(sizePolicy12)
        self.fitWidget.setMinimumSize(QSize(470, 0))
        self.fitWidget.setMaximumSize(QSize(470, 16777215))
        self.fitWidget.setAutoFillBackground(False)
        self.verticalLayout_15 = QVBoxLayout(self.fitWidget)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.frame_fit = QFrame(self.fitWidget)
        self.frame_fit.setObjectName(u"frame_fit")
        sizePolicy3.setHeightForWidth(self.frame_fit.sizePolicy().hasHeightForWidth())
        self.frame_fit.setSizePolicy(sizePolicy3)
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
        sizePolicy10.setHeightForWidth(self.fitLabel.sizePolicy().hasHeightForWidth())
        self.fitLabel.setSizePolicy(sizePolicy10)
        self.fitLabel.setMinimumSize(QSize(0, 23))
        self.fitLabel.setMaximumSize(QSize(16777215, 16777215))
        self.fitLabel.setFont(font1)
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
        self.fitHelpPushButton.setIcon(icon9)
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
        self.horizontalSpacer_27 = QSpacerItem(215, 47, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_27)

        self.pushButton_2 = QPushButton(self.widget_13)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy4.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy4)
        self.pushButton_2.setMinimumSize(QSize(160, 30))
        self.pushButton_2.setFont(font3)
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
        self.pushButton_2.setIcon(icon14)

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
        self.horizontalSpacer_25 = QSpacerItem(185, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_25)

        self.label_7 = QLabel(self.widget_12)
        self.label_7.setObjectName(u"label_7")
        font10 = QFont()
        font10.setFamilies([u"Roboto Medium"])
        font10.setStyleStrategy(QFont.NoAntialias)
        self.label_7.setFont(font10)
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
        self.fitScrollAreaWidget.setGeometry(QRect(0, 0, 100, 30))
        self.verticalLayout_4 = QVBoxLayout(self.fitScrollAreaWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.fitScrollArea.setWidget(self.fitScrollAreaWidget)

        self.verticalLayout_8.addWidget(self.fitScrollArea)


        self.verticalLayout_15.addWidget(self.frame_fit)

        self.frame_6 = QFrame(self.fitWidget)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy10.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy10)
        self.frame_6.setMinimumSize(QSize(0, 130))
        self.frame_6.setMaximumSize(QSize(16777215, 130))
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.gridLayout_12 = QGridLayout(self.frame_6)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.fitButton = QPushButton(self.frame_6)
        self.fitButton.setObjectName(u"fitButton")
        sizePolicy4.setHeightForWidth(self.fitButton.sizePolicy().hasHeightForWidth())
        self.fitButton.setSizePolicy(sizePolicy4)
        self.fitButton.setMinimumSize(QSize(189, 34))
        self.fitButton.setMaximumSize(QSize(189, 34))
        self.fitButton.setFont(font3)
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
        self.fitButton.setIcon(icon13)
        self.fitButton.setIconSize(QSize(15, 15))

        self.gridLayout_12.addWidget(self.fitButton, 2, 1, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_12.addItem(self.verticalSpacer_11, 4, 1, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_12, 0, 1, 1, 1)

        self.exportToPrefitButton = QPushButton(self.frame_6)
        self.exportToPrefitButton.setObjectName(u"exportToPrefitButton")
        sizePolicy4.setHeightForWidth(self.exportToPrefitButton.sizePolicy().hasHeightForWidth())
        self.exportToPrefitButton.setSizePolicy(sizePolicy4)
        self.exportToPrefitButton.setMinimumSize(QSize(189, 34))
        self.exportToPrefitButton.setMaximumSize(QSize(189, 34))
        self.exportToPrefitButton.setFont(font3)
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
        self.exportToPrefitButton.setIcon(icon14)

        self.gridLayout_12.addWidget(self.exportToPrefitButton, 2, 3, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_15, 2, 2, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_16, 2, 0, 1, 1)

        self.horizontalSpacer_35 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_12.addItem(self.horizontalSpacer_35, 2, 4, 1, 1)


        self.verticalLayout_15.addWidget(self.frame_6)

        self.pagesStackedWidget.addWidget(self.fitWidget)

        self.gridLayout.addWidget(self.pagesStackedWidget, 0, 1, 3, 1)

        self.mplFigureCanvasContainerWidget = QWidget(self.windowBodyFrame)
        self.mplFigureCanvasContainerWidget.setObjectName(u"mplFigureCanvasContainerWidget")
        sizePolicy.setHeightForWidth(self.mplFigureCanvasContainerWidget.sizePolicy().hasHeightForWidth())
        self.mplFigureCanvasContainerWidget.setSizePolicy(sizePolicy)
        self.mplFigureCanvasContainerWidget.setMinimumSize(QSize(0, 0))
        self.mplFigureCanvasContainerWidget.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.mplFigureCanvasContainerWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.widget = QWidget(self.mplFigureCanvasContainerWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"\n"
"	background-color: #2A2A2A; \n"
"	border: 0px solid black; \n"
"	border-radius: 10px;\n"
"")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 12, 12, 0)
        self.mplFigureButtons = QWidget(self.widget)
        self.mplFigureButtons.setObjectName(u"mplFigureButtons")
        sizePolicy7.setHeightForWidth(self.mplFigureButtons.sizePolicy().hasHeightForWidth())
        self.mplFigureButtons.setSizePolicy(sizePolicy7)
        self.mplFigureButtons.setMinimumSize(QSize(0, 90))
        self.mplFigureButtons.setMaximumSize(QSize(16777215, 90))
        self.mplFigureButtons.setAutoFillBackground(False)
        self.mplFigureButtons.setStyleSheet(u"QToolTip {\n"
"	color: #1e1e1e;\n"
"	background-color: rgba(255, 255, 255, 160);\n"
"	border: 1px solid rgb(200, 200, 200);\n"
"	border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"	border-radius: 18px;	\n"
"	background-color: #4B4B4B;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #5C3F83;\n"
"	border: 0px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: #5C3F83;\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"QPushButton:checked {	\n"
"	background-color: #5C3F83;\n"
"	border: 0px solid rgb(43, 50, 61);\n"
"}\n"
"")
        self.gridLayout_6 = QGridLayout(self.mplFigureButtons)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(20)
        self.gridLayout_6.setContentsMargins(12, -1, -1, -1)
        self.zoomViewButton = QPushButton(self.mplFigureButtons)
        self.zoomViewButton.setObjectName(u"zoomViewButton")
        sizePolicy4.setHeightForWidth(self.zoomViewButton.sizePolicy().hasHeightForWidth())
        self.zoomViewButton.setSizePolicy(sizePolicy4)
        self.zoomViewButton.setMinimumSize(QSize(40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip(u"Zoom mode: Drag to magnify a region")
#endif // QT_CONFIG(tooltip)
        icon15 = QIcon()
        icon15.addFile(u":/icons/svg/zoom.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon15.addFile(u":/icons/svg/zoom-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.zoomViewButton.setIcon(icon15)
        self.zoomViewButton.setIconSize(QSize(20, 20))
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)

        self.gridLayout_6.addWidget(self.zoomViewButton, 0, 3, 1, 1)

        self.verticalSnapButton = QPushButton(self.mplFigureButtons)
        self.verticalSnapButton.setObjectName(u"verticalSnapButton")
        sizePolicy4.setHeightForWidth(self.verticalSnapButton.sizePolicy().hasHeightForWidth())
        self.verticalSnapButton.setSizePolicy(sizePolicy4)
        self.verticalSnapButton.setMinimumSize(QSize(40, 40))
#if QT_CONFIG(tooltip)
        self.verticalSnapButton.setToolTip(u"Peak snapping: Locate the nearby peak along y axis")
#endif // QT_CONFIG(tooltip)
        icon16 = QIcon()
        icon16.addFile(u":/icons/svg/y-snap.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon16.addFile(u":/icons/svg/y-snap-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.verticalSnapButton.setIcon(icon16)
        self.verticalSnapButton.setIconSize(QSize(23, 28))
        self.verticalSnapButton.setCheckable(True)
        self.verticalSnapButton.setChecked(True)
        self.verticalSnapButton.setAutoExclusive(False)

        self.gridLayout_6.addWidget(self.verticalSnapButton, 0, 8, 1, 1)

        self.resetViewButton = QPushButton(self.mplFigureButtons)
        self.resetViewButton.setObjectName(u"resetViewButton")
        sizePolicy4.setHeightForWidth(self.resetViewButton.sizePolicy().hasHeightForWidth())
        self.resetViewButton.setSizePolicy(sizePolicy4)
        self.resetViewButton.setMinimumSize(QSize(40, 40))
#if QT_CONFIG(tooltip)
        self.resetViewButton.setToolTip(u"Reset plot area")
#endif // QT_CONFIG(tooltip)
        icon17 = QIcon()
        icon17.addFile(u":/icons/svg/reset.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon17)
        self.resetViewButton.setIconSize(QSize(20, 20))

        self.gridLayout_6.addWidget(self.resetViewButton, 0, 0, 1, 1)

        self.label_35 = QLabel(self.mplFigureButtons)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setStyleSheet(u"color: #DDDDDD; background-color: transparent;")
        self.label_35.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_35, 1, 8, 1, 1)

        self.label_51 = QLabel(self.mplFigureButtons)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setMinimumSize(QSize(2, 0))
        self.label_51.setMaximumSize(QSize(2, 16777215))
        self.label_51.setStyleSheet(u"background-color: #4B4B4B")

        self.gridLayout_6.addWidget(self.label_51, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(10, 10, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_8, 0, 9, 1, 1)

        self.label_36 = QLabel(self.mplFigureButtons)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setStyleSheet(u"color: #DDDDDD; background-color: transparent;")
        self.label_36.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_36, 1, 4, 1, 1)

        self.label_34 = QLabel(self.mplFigureButtons)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setStyleSheet(u"color: #DDDDDD; background-color: transparent;")
        self.label_34.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_34, 1, 3, 1, 1)

        self.label_50 = QLabel(self.mplFigureButtons)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setMinimumSize(QSize(2, 0))
        self.label_50.setMaximumSize(QSize(2, 16777215))
        self.label_50.setStyleSheet(u"background-color: #4B4B4B")

        self.gridLayout_6.addWidget(self.label_50, 0, 5, 1, 1)

        self.label_27 = QLabel(self.mplFigureButtons)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setStyleSheet(u"color: #DDDDDD; background-color: transparent;")
        self.label_27.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_27, 1, 2, 1, 1)

        self.selectViewButton = QPushButton(self.mplFigureButtons)
        self.selectViewButton.setObjectName(u"selectViewButton")
        sizePolicy4.setHeightForWidth(self.selectViewButton.sizePolicy().hasHeightForWidth())
        self.selectViewButton.setSizePolicy(sizePolicy4)
        self.selectViewButton.setMinimumSize(QSize(40, 40))
        self.selectViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.selectViewButton.setToolTip(u"Extract mode: Click to extract peaks")
#endif // QT_CONFIG(tooltip)
        icon18 = QIcon()
        icon18.addFile(u":/icons/svg/extract.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon18.addFile(u":/icons/svg/extract-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.selectViewButton.setIcon(icon18)
        self.selectViewButton.setIconSize(QSize(20, 20))
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)

        self.gridLayout_6.addWidget(self.selectViewButton, 0, 4, 1, 1)

        self.panViewButton = QPushButton(self.mplFigureButtons)
        self.panViewButton.setObjectName(u"panViewButton")
        sizePolicy4.setHeightForWidth(self.panViewButton.sizePolicy().hasHeightForWidth())
        self.panViewButton.setSizePolicy(sizePolicy4)
        self.panViewButton.setMinimumSize(QSize(40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
#if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip(u"Pan mode: Drag to move the canvas")
#endif // QT_CONFIG(tooltip)
        icon19 = QIcon()
        icon19.addFile(u":/icons/svg/move.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon19.addFile(u":/icons/svg/move-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.panViewButton.setIcon(icon19)
        self.panViewButton.setIconSize(QSize(20, 20))
        self.panViewButton.setCheckable(True)
        self.panViewButton.setChecked(False)
        self.panViewButton.setAutoExclusive(True)

        self.gridLayout_6.addWidget(self.panViewButton, 0, 2, 1, 1)

        self.horizontalSnapButton = QPushButton(self.mplFigureButtons)
        self.horizontalSnapButton.setObjectName(u"horizontalSnapButton")
        sizePolicy4.setHeightForWidth(self.horizontalSnapButton.sizePolicy().hasHeightForWidth())
        self.horizontalSnapButton.setSizePolicy(sizePolicy4)
        self.horizontalSnapButton.setMinimumSize(QSize(40, 40))
#if QT_CONFIG(tooltip)
        self.horizontalSnapButton.setToolTip(u"Dataset snapping: align the x-coordinates for datasets")
#endif // QT_CONFIG(tooltip)
        icon20 = QIcon()
        icon20.addFile(u":/icons/svg/x-snap.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon20.addFile(u":/icons/svg/x-snap-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.horizontalSnapButton.setIcon(icon20)
        self.horizontalSnapButton.setIconSize(QSize(21, 24))
        self.horizontalSnapButton.setCheckable(True)
        self.horizontalSnapButton.setChecked(True)
        self.horizontalSnapButton.setAutoExclusive(False)

        self.gridLayout_6.addWidget(self.horizontalSnapButton, 0, 6, 1, 1)

        self.label_9 = QLabel(self.mplFigureButtons)
        self.label_9.setObjectName(u"label_9")
        font11 = QFont()
        font11.setFamilies([u"Roboto Medium"])
        font11.setBold(False)
        self.label_9.setFont(font11)
        self.label_9.setStyleSheet(u"color: #DDDDDD; background-color: transparent;")
        self.label_9.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_9, 1, 0, 1, 1)

        self.calibratedCheckBox = QPushButton(self.mplFigureButtons)
        self.calibratedCheckBox.setObjectName(u"calibratedCheckBox")
        sizePolicy4.setHeightForWidth(self.calibratedCheckBox.sizePolicy().hasHeightForWidth())
        self.calibratedCheckBox.setSizePolicy(sizePolicy4)
        self.calibratedCheckBox.setMinimumSize(QSize(150, 65))
        self.calibratedCheckBox.setMaximumSize(QSize(200, 65))
        font12 = QFont()
        font12.setFamilies([u"Roboto Medium"])
        font12.setKerning(False)
        self.calibratedCheckBox.setFont(font12)
        self.calibratedCheckBox.setStyleSheet(u"QPushButton {\n"
"color: #DDDDDD;\n"
"background-color: #2A2A2A;\n"
"font-size: 14px;\n"
"}\n"
"\n"
"QPushButton::checked {\n"
"background-color: #2A2A2A;\n"
"}\n"
"\n"
"")
        icon21 = QIcon()
        icon21.addFile(u":/icons/svg/toggle-off.svg", QSize(), QIcon.Normal, QIcon.Off)
        icon21.addFile(u":/icons/svg/toggle-on.svg", QSize(), QIcon.Normal, QIcon.On)
        self.calibratedCheckBox.setIcon(icon21)
        self.calibratedCheckBox.setIconSize(QSize(60, 50))
        self.calibratedCheckBox.setCheckable(True)

        self.gridLayout_6.addWidget(self.calibratedCheckBox, 0, 10, 2, 1)

        self.label_37 = QLabel(self.mplFigureButtons)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font4)
        self.label_37.setStyleSheet(u"color: #DDDDDD; background-color: transparent;")
        self.label_37.setAlignment(Qt.AlignCenter)

        self.gridLayout_6.addWidget(self.label_37, 1, 6, 1, 1)


        self.verticalLayout.addWidget(self.mplFigureButtons)

        self.mplFigureCanvas = MplFigureCanvas(self.widget)
        self.mplFigureCanvas.setObjectName(u"mplFigureCanvas")
        sizePolicy20 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy20.setHorizontalStretch(100)
        sizePolicy20.setVerticalStretch(100)
        sizePolicy20.setHeightForWidth(self.mplFigureCanvas.sizePolicy().hasHeightForWidth())
        self.mplFigureCanvas.setSizePolicy(sizePolicy20)
        self.mplFigureCanvas.setMinimumSize(QSize(500, 500))
        self.mplFigureCanvas.setMaximumSize(QSize(16777215, 16777215))
        self.mplFigureCanvas.setStyleSheet(u"QFrame {\n"
"	background-color: #2A2A2A;\n"
"	border: 0px solid rgb(52, 59, 72);\n"
"}\n"
"\n"
"QToolTip {\n"
"	color: #1e1e1e;\n"
"	background-color: rgba(255, 255, 255, 160);\n"
"	border: 1px solid rgb(200, 200, 200);\n"
"	border-radius: 2px;\n"
"}\n"
"")
        self.mplFigureCanvas.setLineWidth(0)

        self.verticalLayout.addWidget(self.mplFigureCanvas)

        self.figureTabContainerWidget = QWidget(self.widget)
        self.figureTabContainerWidget.setObjectName(u"figureTabContainerWidget")
        sizePolicy21 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy21.setHorizontalStretch(0)
        sizePolicy21.setVerticalStretch(0)
        sizePolicy21.setHeightForWidth(self.figureTabContainerWidget.sizePolicy().hasHeightForWidth())
        self.figureTabContainerWidget.setSizePolicy(sizePolicy21)
        self.figureTabContainerWidget.setMinimumSize(QSize(0, 50))
        self.figureTabContainerWidget.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.figureTabContainerWidget)
#ifndef Q_OS_MAC
        self.horizontalLayout.setSpacing(-1)
#endif
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.figureTabWidget = QTabWidget(self.figureTabContainerWidget)
        self.figureTabWidget.setObjectName(u"figureTabWidget")
        sizePolicy21.setHeightForWidth(self.figureTabWidget.sizePolicy().hasHeightForWidth())
        self.figureTabWidget.setSizePolicy(sizePolicy21)
        self.figureTabWidget.setMinimumSize(QSize(0, 50))
        self.figureTabWidget.setMaximumSize(QSize(16777215, 50))
        self.figureTabWidget.setFont(font11)
        self.figureTabWidget.setAutoFillBackground(False)
        self.figureTabWidget.setStyleSheet(u"QTabWidget::tab-bar {\n"
"	left: 0px;\n"
"}\n"
"QTabBar::tab {\n"
"    background: #171717;\n"
"	border-left: 2px solid #4B4B4B;\n"
"	border-right: 2px solid #4B4B4B;\n"
"	border-bottom: 2px solid #4B4B4B;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    min-width: 2ex;\n"
"	padding: 10px;\n"
"	padding-left: 10px;\n"
"	padding-right: 10px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"	background: #2A2A2A;\n"
"	font: 13px \"Roboto Medium\";\n"
"    color: #DBBCFB;\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"	font: 13px \"Roboto Medium\";\n"
"    color: #797979;\n"
"	margin-bottom: 4px; \n"
"	border-left: 1px solid #2A2A2A;\n"
"	border-right: 1px solid #2A2A2A;\n"
"	border-bottom: 1px solid #2A2A2A;\n"
"}")
        self.figureTabWidget.setTabPosition(QTabWidget.North)
        self.figureTabWidget.setTabShape(QTabWidget.Rounded)
        self.figureTabWidget.setUsesScrollButtons(True)

        self.horizontalLayout.addWidget(self.figureTabWidget)

        self.addFigPushButton = QPushButton(self.figureTabContainerWidget)
        self.addFigPushButton.setObjectName(u"addFigPushButton")
        sizePolicy4.setHeightForWidth(self.addFigPushButton.sizePolicy().hasHeightForWidth())
        self.addFigPushButton.setSizePolicy(sizePolicy4)
        self.addFigPushButton.setMinimumSize(QSize(40, 30))
        self.addFigPushButton.setMaximumSize(QSize(40, 30))
        self.addFigPushButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}")
        icon22 = QIcon()
        icon22.addFile(u":/icons/svg/plus-fig.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addFigPushButton.setIcon(icon22)
        self.addFigPushButton.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.addFigPushButton)

        self.deleteFigPushButton = QPushButton(self.figureTabContainerWidget)
        self.deleteFigPushButton.setObjectName(u"deleteFigPushButton")
        sizePolicy4.setHeightForWidth(self.deleteFigPushButton.sizePolicy().hasHeightForWidth())
        self.deleteFigPushButton.setSizePolicy(sizePolicy4)
        self.deleteFigPushButton.setMinimumSize(QSize(40, 30))
        self.deleteFigPushButton.setMaximumSize(QSize(40, 30))
        self.deleteFigPushButton.setStyleSheet(u"QPushButton{\n"
"	border: none;\n"
"	background-color: transparent;\n"
"}")
        icon23 = QIcon()
        icon23.addFile(u":/icons/svg/trash-fig.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteFigPushButton.setIcon(icon23)
        self.deleteFigPushButton.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.deleteFigPushButton)


        self.verticalLayout.addWidget(self.figureTabContainerWidget)


        self.verticalLayout_2.addWidget(self.widget)


        self.gridLayout.addWidget(self.mplFigureCanvasContainerWidget, 0, 2, 1, 1)


        self.gridLayout_5.addWidget(self.windowBodyFrame, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.setEnabled(True)
        sizePolicy10.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy10)
        self.statusBar.setMinimumSize(QSize(0, 60))
        self.statusBar.setMaximumSize(QSize(16777215, 60))
        self.statusBar.setFont(font12)
        self.statusBar.setStyleSheet(u"background-color: #2F2F2F;\n"
"color: #AAAAAA;\n"
"")
        self.statusBar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.pagesStackedWidget.setCurrentIndex(0)
        self.figureTabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.modeSetupFigButton.setText(QCoreApplication.translate("MainWindow", u"  IMPORT", None))
        self.toggleMenuButton.setText("")
        self.modeTagButton.setText(QCoreApplication.translate("MainWindow", u"  EXTRACT", None))
        self.modePrefitButton.setText(QCoreApplication.translate("MainWindow", u"  PRE-FIT", None))
        self.modeSelectButton.setText(QCoreApplication.translate("MainWindow", u"  CALIBRATE", None))
        self.modeFitButton.setText(QCoreApplication.translate("MainWindow", u"  FIT", None))
        self.settingsPushButton.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"METADATA:", None))
        self.fileNameInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Y Candidates:   ", None))
        self.yCandInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"Z Candidates:   ", None))
        self.zCandInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Discarded Items:   ", None))
        self.discAxesInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Dimension:   ", None))
        self.dimInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"X Candidates:   ", None))
        self.xCandInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"File Location:   ", None))
        self.fileLocInfo.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"SELECT AXES", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Y-Axis: Frequency  ", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"X-Axis: Tuning Parameters", None))
        self.transposeButton.setText(QCoreApplication.translate("MainWindow", u"   Transpose Figure", None))
        self.finalizeStep0Button.setText(QCoreApplication.translate("MainWindow", u"Proceed To Calibrate", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"CALIBRATE", None))
        self.calibrationHelpPushButton.setText("")
        self.zComboBox.setCurrentText("")
        self.calibrateY2Button.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Raw Y</p></body></html>", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Calibrated Y [GHz]</p></body></html>", None))
        self.calibrateY1Button.setText("")
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"EXTRACT", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"** For uncertain initial/final indices: Leave it blank or use multiple indices separated by \";\"", None))
        self.label_48.setText("")
        self.bareLabelOrder.setText(QCoreApplication.translate("MainWindow", u"* Indices order by:", None))
        self.initialDressedStateLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"<eigenstate index>", None))
        self.label_41.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"* For uncertain initial/final indices: Leave it blank or use multiple indices separated by \";\"", None))
        self.finalDressedStateLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"<eigenstate index>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"PRE-FIT", None))
        self.autoRunCheckBox.setText(QCoreApplication.translate("MainWindow", u"Auto Update", None))
#if QT_CONFIG(accessibility)
        self.plotButton.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"   Plot Spectrum", None))
#if QT_CONFIG(tooltip)
        self.exportToFitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the pre-fitted parameters to the initial value of the fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToFitButton.setText(QCoreApplication.translate("MainWindow", u"   Results To Fit", None))
        self.fitLabel.setText(QCoreApplication.translate("MainWindow", u"FIT", None))
        self.fitHelpPushButton.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_2.setToolTip(QCoreApplication.translate("MainWindow", u"Load the current value to the initial value", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"   Results To Initial", None))
        self.label_7.setText("")
        self.fitButton.setText(QCoreApplication.translate("MainWindow", u"   Run Fit", None))
#if QT_CONFIG(tooltip)
        self.exportToPrefitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Load the fitted parameters to the pre-fit section", None))
#endif // QT_CONFIG(tooltip)
        self.exportToPrefitButton.setText(QCoreApplication.translate("MainWindow", u"   Results To Pre-Fit", None))
        self.zoomViewButton.setText("")
        self.verticalSnapButton.setText("")
        self.resetViewButton.setText("")
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Y-Snap", None))
        self.label_51.setText("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Extract", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.label_50.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Pan", None))
        self.selectViewButton.setText("")
        self.panViewButton.setText("")
        self.horizontalSnapButton.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
        self.calibratedCheckBox.setText(QCoreApplication.translate("MainWindow", u"View\n"
"Calibrated\n"
"Axes", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"X-Snap", None))
        self.addFigPushButton.setText("")
        self.deleteFigPushButton.setText("")
        pass
    # retranslateUi

