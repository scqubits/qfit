# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from qfit.widgets.calibration import CalibrationLineEdit
from qfit.widgets.data_extracting import DataExtractingWidget, DatasetWidget, TableView
from qfit.widgets.data_tagging import (
    DataTaggingWidget,
    IntTupleLineEdit,
    StrTupleLineEdit,
)
from qfit.widgets.manage_datasets import ManageDatasetsWidget
from qfit.widgets.mpl_canvas import MplFigureCanvas
from qfit.widgets.mpl_navbuttons import MplNavButtons
from . import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1258, 990)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle(u"qfit")
        MainWindow.setWindowOpacity(1.000000000000000)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(
            u"QMainWindow {\n"
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
            "	font-family: Roboto;\n"
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
            "    backgroun"
            "d: rgb(85, 170, 255);\n"
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
            "	border-radius: 0px;\n"
            " }\n"
            ""
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
            "QCheckBox::indicator {\n"
            "    border"
            ": 3px solid rgb(52, 59, 72);\n"
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
            "	background-image: url(:/icons/16x16/cil-check-alt.png);\n"
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
            "	border: 3px solid rgb(196, 150, 250);\n"
            "   background: rgb(52, 59, 72);\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "/* SLIDERS */\n"
            "QSlider::groove:horizontal {\n"
            "    border-radius: 9"
            "px;\n"
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
            "    margin: 0px;\n"
            "	border-radius: 9px;\n"
            "}\n"
            "\n"
            "QSlider:"
            ":handle:vertical:hover {\n"
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
            '	font: 57 10pt "Roboto Medium";\n'
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
            "}\n"
            "\n"
            "QSpinBox::up-arrow {\n"
            "    width: 16p"
            "x;\n"
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
            "	color: rgb(170, 170, 170);\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	border-radius: 5px;\n"
            "	border: 2px solid rgb(27, 29, 35);\n"
            "	padding: 5px;\n"
            "	padding-left: 10px;\n"
            "}\n"
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
            "	border-bottom-right-radius: 3px;	\n"
            "	background-image: url(:/icons/16"
            "x16/cil-arrow-bottom.png);\n"
            "	background-position: center;\n"
            "	background-repeat: no-reperat;\n"
            " }\n"
            " \n"
            "QComboBox QAbstractItemView {\n"
            "	color: rgb(85, 170, 255);	\n"
            "	background-color: rgb(27, 29, 35);\n"
            "	padding: 10px;\n"
            "	selection-background-color: rgb(39, 44, 54);\n"
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
            "Q"
            "TableWidget::horizontalHeader {	\n"
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
            ""
        )
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        sizePolicy.setHeightForWidth(
            self.centralWidget.sizePolicy().hasHeightForWidth()
        )
        self.centralWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
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
        self.windowTitleLeftFrame = QFrame(self.windowTitleFrame)
        self.windowTitleLeftFrame.setObjectName(u"windowTitleLeftFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.windowTitleLeftFrame.sizePolicy().hasHeightForWidth()
        )
        self.windowTitleLeftFrame.setSizePolicy(sizePolicy1)
        self.windowTitleLeftFrame.setMinimumSize(QSize(70, 35))
        self.windowTitleLeftFrame.setMaximumSize(QSize(70, 35))
        self.windowTitleLeftFrame.setFrameShape(QFrame.NoFrame)
        self.windowTitleLeftFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.windowTitleLeftFrame)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.toggleMenuButton = QPushButton(self.windowTitleLeftFrame)
        self.toggleMenuButton.setObjectName(u"toggleMenuButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.toggleMenuButton.sizePolicy().hasHeightForWidth()
        )
        self.toggleMenuButton.setSizePolicy(sizePolicy2)
        self.toggleMenuButton.setMinimumSize(QSize(0, 0))
        self.toggleMenuButton.setMaximumSize(QSize(16777215, 16777215))
        self.toggleMenuButton.setStyleSheet(
            u"QPushButton {	\n"
            "	border: none;\n"
            "	background-color: transparent;\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(85, 170, 255);\n"
            "}"
        )
        icon = QIcon()
        icon.addFile(u":/icons/20x20/cil-menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleMenuButton.setIcon(icon)

        self.verticalLayout_7.addWidget(self.toggleMenuButton)

        self.horizontalLayout_3.addWidget(self.windowTitleLeftFrame)

        self.windowTitleMidFrame = QFrame(self.windowTitleFrame)
        self.windowTitleMidFrame.setObjectName(u"windowTitleMidFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.windowTitleMidFrame.sizePolicy().hasHeightForWidth()
        )
        self.windowTitleMidFrame.setSizePolicy(sizePolicy3)
        self.windowTitleMidFrame.setFrameShape(QFrame.NoFrame)
        self.windowTitleMidFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.windowTitleMidFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.windowTitleText = QLabel(self.windowTitleMidFrame)
        self.windowTitleText.setObjectName(u"windowTitleText")
        self.windowTitleText.setStyleSheet(
            u'color: rgb(255, 255, 255); font: 10pt "Roboto";'
        )
        self.windowTitleText.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.windowTitleText)

        self.horizontalLayout_3.addWidget(self.windowTitleMidFrame)

        self.windowTitleRightFrame = QFrame(self.windowTitleFrame)
        self.windowTitleRightFrame.setObjectName(u"windowTitleRightFrame")
        self.windowTitleRightFrame.setStyleSheet(
            u"QPushButton {	\n"
            "	border: none;\n"
            "	background-color: transparent;\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(85, 170, 255);\n"
            "}"
        )
        self.windowTitleRightFrame.setFrameShape(QFrame.NoFrame)
        self.windowTitleRightFrame.setFrameShadow(QFrame.Raised)
        self.windowTitleRightFrame.setLineWidth(0)
        self.horizontalLayout_4 = QHBoxLayout(self.windowTitleRightFrame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.buttonMinimize = QPushButton(self.windowTitleRightFrame)
        self.buttonMinimize.setObjectName(u"buttonMinimize")
        self.buttonMinimize.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.buttonMinimize.sizePolicy().hasHeightForWidth()
        )
        self.buttonMinimize.setSizePolicy(sizePolicy4)
        self.buttonMinimize.setMinimumSize(QSize(40, 40))
        self.buttonMinimize.setMaximumSize(QSize(40, 16777215))
        icon1 = QIcon()
        icon1.addFile(
            u":/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.buttonMinimize.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.buttonMinimize)

        self.buttonMaximize = QPushButton(self.windowTitleRightFrame)
        self.buttonMaximize.setObjectName(u"buttonMaximize")
        self.buttonMaximize.setEnabled(True)
        sizePolicy4.setHeightForWidth(
            self.buttonMaximize.sizePolicy().hasHeightForWidth()
        )
        self.buttonMaximize.setSizePolicy(sizePolicy4)
        self.buttonMaximize.setMinimumSize(QSize(40, 40))
        self.buttonMaximize.setMaximumSize(QSize(40, 16777215))
        icon2 = QIcon()
        icon2.addFile(
            u":/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.buttonMaximize.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.buttonMaximize)

        self.buttonClose = QPushButton(self.windowTitleRightFrame)
        self.buttonClose.setObjectName(u"buttonClose")
        self.buttonClose.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.buttonClose.sizePolicy().hasHeightForWidth())
        self.buttonClose.setSizePolicy(sizePolicy4)
        self.buttonClose.setMinimumSize(QSize(40, 40))
        self.buttonClose.setMaximumSize(QSize(40, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonClose.setIcon(icon3)

        self.horizontalLayout_4.addWidget(self.buttonClose)

        self.horizontalLayout_3.addWidget(self.windowTitleRightFrame)

        self.verticalLayout.addWidget(self.windowTitleFrame)

        self.windowBodyFrame = QFrame(self.fullWindowFrame)
        self.windowBodyFrame.setObjectName(u"windowBodyFrame")
        sizePolicy1.setHeightForWidth(
            self.windowBodyFrame.sizePolicy().hasHeightForWidth()
        )
        self.windowBodyFrame.setSizePolicy(sizePolicy1)
        self.windowBodyFrame.setStyleSheet(
            u"QFrame {\n" "	background-color: rgb(33,33,33);\n" "}"
        )
        self.gridLayout = QGridLayout(self.windowBodyFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(0, 0, 12, 0)
        self.dataTableFrame = DatasetWidget(self.windowBodyFrame)
        self.dataTableFrame.setObjectName(u"dataTableFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(
            self.dataTableFrame.sizePolicy().hasHeightForWidth()
        )
        self.dataTableFrame.setSizePolicy(sizePolicy5)
        self.dataTableFrame.setMaximumSize(QSize(16777215, 140))
        self.dataTableFrame.setStyleSheet(u"")
        self.horizontalLayout_5 = QHBoxLayout(self.dataTableFrame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.dataTableView = TableView(self.dataTableFrame)
        self.dataTableView.setObjectName(u"dataTableView")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.dataTableView.sizePolicy().hasHeightForWidth()
        )
        self.dataTableView.setSizePolicy(sizePolicy6)
        self.dataTableView.setMinimumSize(QSize(0, 105))
        self.dataTableView.setMaximumSize(QSize(16777215, 105))
        self.dataTableView.setStyleSheet(
            u"QTableWidget {	\n"
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
            "}"
        )
        self.dataTableView.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_5.addWidget(self.dataTableView)

        self.gridLayout.addWidget(self.dataTableFrame, 1, 3, 1, 1)

        self.menu_frame = QFrame(self.windowBodyFrame)
        self.menu_frame.setObjectName(u"menu_frame")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy7)
        self.menu_frame.setMinimumSize(QSize(190, 0))
        self.menu_frame.setMaximumSize(QSize(190, 16777215))
        self.menu_frame.setStyleSheet(
            u"QFrame {\n"
            "	color: white;\n"
            "	background-color: rgb(18, 18, 18);\n"
            "}\n"
            "\n"
            "QPushButton {	\n"
            '	font: 57 11pt "Roboto Medium";\n'
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
            "}"
        )
        self.menu_frame.setFrameShape(QFrame.NoFrame)
        self.menu_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.menu_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(37, 0, 20, 0)
        self.modeTagButton = QPushButton(self.menu_frame)
        self.modeTagButton.setObjectName(u"modeTagButton")
        self.modeTagButton.setMinimumSize(QSize(120, 70))
        self.modeTagButton.setMaximumSize(QSize(120, 70))
        icon4 = QIcon()
        icon4.addFile(u":/icons/24x24/cil-list.png", QSize(), QIcon.Normal, QIcon.Off)
        self.modeTagButton.setIcon(icon4)
        self.modeTagButton.setIconSize(QSize(24, 24))
        self.modeTagButton.setCheckable(True)
        self.modeTagButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeTagButton, 2, 0, 1, 2)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_2.addItem(self.verticalSpacer_3, 5, 1, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.gridLayout_2.addItem(self.verticalSpacer_14, 0, 0, 1, 1)

        self.modeFitButton = QPushButton(self.menu_frame)
        self.modeFitButton.setObjectName(u"modeFitButton")
        self.modeFitButton.setMinimumSize(QSize(120, 70))
        self.modeFitButton.setMaximumSize(QSize(120, 70))
        icon5 = QIcon()
        icon5.addFile(
            u":/icons/24x24/cil-speedometer.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.modeFitButton.setIcon(icon5)
        self.modeFitButton.setIconSize(QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeFitButton, 4, 0, 1, 1)

        self.modeSelectButton = QPushButton(self.menu_frame)
        self.modeSelectButton.setObjectName(u"modeSelectButton")
        self.modeSelectButton.setMinimumSize(QSize(120, 70))
        self.modeSelectButton.setMaximumSize(QSize(16777215, 70))
        icon6 = QIcon()
        icon6.addFile(
            u":/icons/24x24/cil-location-pin.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.modeSelectButton.setIcon(icon6)
        self.modeSelectButton.setIconSize(QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setChecked(True)
        self.modeSelectButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeSelectButton, 1, 0, 1, 2)

        self.modePlotButton = QPushButton(self.menu_frame)
        self.modePlotButton.setObjectName(u"modePlotButton")
        self.modePlotButton.setMinimumSize(QSize(170, 70))
        self.modePlotButton.setMaximumSize(QSize(120, 70))
        icon7 = QIcon()
        icon7.addFile(
            u":/icons/24x24/cil-chart-line.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.modePlotButton.setIcon(icon7)
        self.modePlotButton.setIconSize(QSize(24, 24))
        self.modePlotButton.setCheckable(True)
        self.modePlotButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modePlotButton, 3, 0, 1, 2)

        self.gridLayout.addWidget(self.menu_frame, 0, 0, 3, 1)

        self.pagesStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.pagesStackedWidget.setObjectName(u"pagesStackedWidget")
        sizePolicy1.setHeightForWidth(
            self.pagesStackedWidget.sizePolicy().hasHeightForWidth()
        )
        self.pagesStackedWidget.setSizePolicy(sizePolicy1)
        self.pagesStackedWidget.setMaximumSize(QSize(420, 620))
        self.extractPointsWidget = DataExtractingWidget()
        self.extractPointsWidget.setObjectName(u"extractPointsWidget")
        self.verticalLayout_9 = QVBoxLayout(self.extractPointsWidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_8 = QFrame(self.extractPointsWidget)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(
            u"QPushButton {\n"
            '	font: 57 10pt "Roboto Medium";\n'
            "	color: rgb(170, 170, 170);\n"
            "	text-align: left;\n"
            "	border: none;\n"
            "}"
        )
        self.verticalLayout_12 = QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(20, 25, -1, -1)
        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(
            u"color: rgb(190, 130, 250);\n" 'font: 57 11pt "Roboto Medium";\n' ""
        )
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setMargin(3)

        self.verticalLayout_12.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_12.addItem(self.verticalSpacer)

        self.scrollArea = QScrollArea(self.frame_8)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 515))
        self.scrollArea.setMaximumSize(QSize(16777215, 700))
        self.scrollArea.setStyleSheet(u"background-color: rgb(33,33,33);")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(False)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 366, 700))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.coloringPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.coloringPushButton.setObjectName(u"coloringPushButton")
        icon8 = QIcon()
        icon8.addFile(
            u":/icons/16x16/cil-caret-right.png", QSize(), QIcon.Normal, QIcon.Off
        )
        icon8.addFile(
            u":/icons/16x16/cil-caret-bottom.png", QSize(), QIcon.Normal, QIcon.On
        )
        self.coloringPushButton.setIcon(icon8)
        self.coloringPushButton.setCheckable(True)
        self.coloringPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.coloringPushButton)

        self.colorGridGroupBox = QGroupBox(self.scrollAreaWidgetContents_4)
        self.colorGridGroupBox.setObjectName(u"colorGridGroupBox")
        sizePolicy8 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(
            self.colorGridGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.colorGridGroupBox.setSizePolicy(sizePolicy8)
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
        icon9 = QIcon()
        icon9.addFile(u":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon9, u"PuOr")
        icon10 = QIcon()
        icon10.addFile(u":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon10, u"RdYlBu")
        icon11 = QIcon()
        icon11.addFile(u":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon11, u"bwr")
        icon12 = QIcon()
        icon12.addFile(u":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon12, u"viridis")
        icon13 = QIcon()
        icon13.addFile(u":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon13, u"cividis")
        icon14 = QIcon()
        icon14.addFile(u":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon14, u"gray")
        self.colorComboBox.setObjectName(u"colorComboBox")
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(
            self.colorComboBox.sizePolicy().hasHeightForWidth()
        )
        self.colorComboBox.setSizePolicy(sizePolicy9)
        self.colorComboBox.setMinimumSize(QSize(0, 30))
        # if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(100, 10))
        self.colorComboBox.setFrame(True)

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

        self.verticalSpacer_2 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.gridLayout_9.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.verticalLayout_5.addWidget(self.colorGridGroupBox)

        self.bgndSubtractPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.bgndSubtractPushButton.setObjectName(u"bgndSubtractPushButton")
        self.bgndSubtractPushButton.setIcon(icon8)
        self.bgndSubtractPushButton.setCheckable(True)
        self.bgndSubtractPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.bgndSubtractPushButton)

        self.bgndSubtractQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.bgndSubtractQFrame.setObjectName(u"bgndSubtractQFrame")
        sizePolicy10 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(
            self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth()
        )
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy10)
        self.bgndSubtractQFrame.setMinimumSize(QSize(330, 0))
        self.gridLayout_8 = QGridLayout(self.bgndSubtractQFrame)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(7)
        self.gridLayout_8.setContentsMargins(-1, 4, -1, -1)
        self.bgndSubtractYCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractYCheckBox.setObjectName(u"bgndSubtractYCheckBox")
        # if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip(u"Background subtraction along Y")
        # endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText(u"ALONG Y AXIS")

        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 3, 1, 1, 1)

        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName(u"bgndSubtractXCheckBox")
        # if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip(u"Background subtraction along X")
        # endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setText(u"ALONG X AXIS")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 3, 0, 1, 1)

        self.verticalLayout_5.addWidget(self.bgndSubtractQFrame)

        self.verticalSpacer_13 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_13)

        self.filtersPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.filtersPushButton.setObjectName(u"filtersPushButton")
        self.filtersPushButton.setIcon(icon8)
        self.filtersPushButton.setCheckable(True)

        self.verticalLayout_5.addWidget(self.filtersPushButton)

        self.filterQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.filterQFrame.setObjectName(u"filterQFrame")
        self.horizontalLayout_7 = QHBoxLayout(self.filterQFrame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 4, -1, -1)
        self.topHatCheckBox = QCheckBox(self.filterQFrame)
        self.topHatCheckBox.setObjectName(u"topHatCheckBox")
        # if QT_CONFIG(tooltip)
        self.topHatCheckBox.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.topHatCheckBox.setText(u"TOP-HAT")

        self.horizontalLayout_7.addWidget(self.topHatCheckBox)

        self.edgeFilterCheckBox = QCheckBox(self.filterQFrame)
        self.edgeFilterCheckBox.setObjectName(u"edgeFilterCheckBox")
        # if QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setText(u"EDGE")

        self.horizontalLayout_7.addWidget(self.edgeFilterCheckBox)

        self.waveletCheckBox = QCheckBox(self.filterQFrame)
        self.waveletCheckBox.setObjectName(u"waveletCheckBox")
        # if QT_CONFIG(tooltip)
        self.waveletCheckBox.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.waveletCheckBox.setText(u"DENOISE")

        self.horizontalLayout_7.addWidget(self.waveletCheckBox)

        self.verticalLayout_5.addWidget(self.filterQFrame)

        self.verticalSpacer_4 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.dataGroupPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.dataGroupPushButton.setObjectName(u"dataGroupPushButton")
        self.dataGroupPushButton.setIcon(icon8)
        self.dataGroupPushButton.setCheckable(True)

        self.verticalLayout_5.addWidget(self.dataGroupPushButton)

        self.xyzDataGridFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.xyzDataGridFrame.setObjectName(u"xyzDataGridFrame")
        self.xyzDataGridFrame.setEnabled(True)
        sizePolicy10.setHeightForWidth(
            self.xyzDataGridFrame.sizePolicy().hasHeightForWidth()
        )
        self.xyzDataGridFrame.setSizePolicy(sizePolicy10)
        self.xyzDataGridFrame.setMinimumSize(QSize(330, 0))
        self.gridLayout_4 = QGridLayout(self.xyzDataGridFrame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.zComboBox = QComboBox(self.xyzDataGridFrame)
        self.zComboBox.setObjectName(u"zComboBox")
        self.zComboBox.setMinimumSize(QSize(250, 30))
        self.zComboBox.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.zComboBox.setFrame(True)

        self.gridLayout_4.addWidget(self.zComboBox, 2, 1, 1, 1)

        self.label_14 = QLabel(self.xyzDataGridFrame)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setText(u"AXIS 2")
        self.label_14.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 5, 0, 1, 1)

        self.label_13 = QLabel(self.xyzDataGridFrame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setText(u"Z")
        self.label_13.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

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
        self.label_12.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 4, 0, 1, 1)

        self.verticalLayout_5.addWidget(self.xyzDataGridFrame)

        self.verticalSpacer_5 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.calibrateGroupPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.calibrateGroupPushButton.setObjectName(u"calibrateGroupPushButton")
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.calibrateGroupPushButton.setFont(font2)
        self.calibrateGroupPushButton.setIcon(icon8)
        self.calibrateGroupPushButton.setCheckable(True)
        self.calibrateGroupPushButton.setChecked(False)

        self.verticalLayout_5.addWidget(self.calibrateGroupPushButton)

        self.calibrationQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.calibrationQFrame.setObjectName(u"calibrationQFrame")
        self.calibrationQFrame.setStyleSheet(
            u"QPushButton {\n"
            "	background-color: rgb(93, 93, 93);\n"
            "	border: 0px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	text-align: center;\n"
            "}"
        )
        self.verticalLayout_2 = QVBoxLayout(self.calibrationQFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.calibrateXGridFrame = QFrame(self.calibrationQFrame)
        self.calibrateXGridFrame.setObjectName(u"calibrateXGridFrame")
        sizePolicy10.setHeightForWidth(
            self.calibrateXGridFrame.sizePolicy().hasHeightForWidth()
        )
        self.calibrateXGridFrame.setSizePolicy(sizePolicy10)
        self.calibrateXGridFrame.setMinimumSize(QSize(330, 0))
        self.calibrateXGridFrame.setMaximumSize(QSize(320, 16777215))
        self.gridLayout_10 = QGridLayout(self.calibrateXGridFrame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setContentsMargins(-1, 9, -1, -1)
        self.label_17 = QLabel(self.calibrateXGridFrame)
        self.label_17.setObjectName(u"label_17")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy11)
        self.label_17.setText(
            u'<html><head/><body><p align="right">\u2192 X<span style=" vertical-align:sub;">1</span>\'</p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_17, 1, 3, 1, 1)

        self.calibrateX1Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX1Button.setObjectName(u"calibrateX1Button")
        self.calibrateX1Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateX1Button.setToolTip(
            u"Calibrate x1, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        icon15 = QIcon()
        icon15.addFile(u":/icons/16x16/cil-at.png", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrateX1Button.setIcon(icon15)

        self.gridLayout_10.addWidget(self.calibrateX1Button, 1, 0, 1, 1)

        self.calibrateX2Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX2Button.setObjectName(u"calibrateX2Button")
        self.calibrateX2Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateX2Button.setToolTip(
            u"Calibrate x2, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        self.calibrateX2Button.setIcon(icon15)

        self.gridLayout_10.addWidget(self.calibrateX2Button, 2, 0, 1, 1)

        self.label_15 = QLabel(self.calibrateXGridFrame)
        self.label_15.setObjectName(u"label_15")
        sizePolicy11.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy11)
        self.label_15.setText(
            u'<html><head/><body><p align="right">X<span style=" vertical-align:sub;">1</span></p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_15, 1, 1, 1, 1)

        self.label_18 = QLabel(self.calibrateXGridFrame)
        self.label_18.setObjectName(u"label_18")
        sizePolicy11.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy11)
        self.label_18.setText(
            u'<html><head/><body><p align="right">\u2192 X<span style=" vertical-align:sub;">2</span>\'</p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_18, 2, 3, 1, 1)

        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX2LineEdit.setObjectName(u"rawX2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawX2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawX2LineEdit.setSizePolicy(sizePolicy6)
        self.rawX2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawX2LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.rawX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.rawX2LineEdit, 2, 2, 1, 1)

        self.label_16 = QLabel(self.calibrateXGridFrame)
        self.label_16.setObjectName(u"label_16")
        sizePolicy11.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy11)
        self.label_16.setText(
            u'<html><head/><body><p align="right">X<span style=" vertical-align:sub;">2</span></p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_16, 2, 1, 1, 1)

        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX2LineEdit.setObjectName(u"mapX2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapX2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapX2LineEdit.setSizePolicy(sizePolicy6)
        self.mapX2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapX2LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.mapX2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX2LineEdit.setText(u"1.0")

        self.gridLayout_10.addWidget(self.mapX2LineEdit, 2, 4, 1, 1)

        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX1LineEdit.setObjectName(u"rawX1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawX1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawX1LineEdit.setSizePolicy(sizePolicy6)
        self.rawX1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawX1LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.rawX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.rawX1LineEdit, 1, 2, 1, 1)

        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX1LineEdit.setObjectName(u"mapX1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapX1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapX1LineEdit.setSizePolicy(sizePolicy6)
        self.mapX1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapX1LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.mapX1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapX1LineEdit.setText(u"0.0")

        self.gridLayout_10.addWidget(self.mapX1LineEdit, 1, 4, 1, 1)

        self.verticalLayout_2.addWidget(self.calibrateXGridFrame)

        self.calibrateYGridFrame = QFrame(self.calibrationQFrame)
        self.calibrateYGridFrame.setObjectName(u"calibrateYGridFrame")
        sizePolicy10.setHeightForWidth(
            self.calibrateYGridFrame.sizePolicy().hasHeightForWidth()
        )
        self.calibrateYGridFrame.setSizePolicy(sizePolicy10)
        self.calibrateYGridFrame.setMinimumSize(QSize(330, 0))
        self.calibrateYGridFrame.setMaximumSize(QSize(320, 16777215))
        # if QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.gridLayout_11 = QGridLayout(self.calibrateYGridFrame)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(-1, 15, -1, -1)
        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY1LineEdit.setObjectName(u"rawY1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawY1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawY1LineEdit.setSizePolicy(sizePolicy6)
        self.rawY1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 0, 2, 1, 1)

        self.label_19 = QLabel(self.calibrateYGridFrame)
        self.label_19.setObjectName(u"label_19")
        sizePolicy11.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy11)
        self.label_19.setText(
            u'<html><head/><body><p align="right">Y<span style=" vertical-align:sub;">1</span></p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridFrame)
        self.label_20.setObjectName(u"label_20")
        sizePolicy11.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy11)
        self.label_20.setText(
            u'<html><head/><body><p align="right">Y<span style=" vertical-align:sub;">2</span></p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_20, 1, 1, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridFrame)
        self.label_22.setObjectName(u"label_22")
        sizePolicy11.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy11)
        self.label_22.setText(
            u'<html><head/><body><p align="right">\u2192 Y<span style=" vertical-align:sub;">2</span>\'</p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_22, 1, 3, 1, 1)

        self.calibrateY1Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY1Button.setObjectName(u"calibrateY1Button")
        self.calibrateY1Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateY1Button.setToolTip(
            u"Calibrate y1, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        self.calibrateY1Button.setIcon(icon15)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 0, 0, 1, 1)

        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY2LineEdit.setObjectName(u"mapY2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapY2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapY2LineEdit.setSizePolicy(sizePolicy6)
        self.mapY2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 1, 4, 1, 1)

        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY2LineEdit.setObjectName(u"rawY2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawY2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawY2LineEdit.setSizePolicy(sizePolicy6)
        self.rawY2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.rawY2LineEdit.setText(u"1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 1, 2, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY1LineEdit.setObjectName(u"mapY1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapY1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapY1LineEdit.setSizePolicy(sizePolicy6)
        self.mapY1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet(u"background-color: rgb(47,47,47);")
        self.mapY1LineEdit.setText(u"0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 0, 4, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridFrame)
        self.label_21.setObjectName(u"label_21")
        sizePolicy11.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy11)
        self.label_21.setText(
            u'<html><head/><body><p align="right">\u2192 Y<span style=" vertical-align:sub;">1</span>\'</p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_21, 0, 3, 1, 1)

        self.calibrateY2Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY2Button.setObjectName(u"calibrateY2Button")
        self.calibrateY2Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateY2Button.setToolTip(
            u"Calibrate y2, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        self.calibrateY2Button.setIcon(icon15)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 1, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.calibrateYGridFrame)

        self.calibratedCheckBox = QCheckBox(self.calibrationQFrame)
        self.calibratedCheckBox.setObjectName(u"calibratedCheckBox")
        sizePolicy6.setHeightForWidth(
            self.calibratedCheckBox.sizePolicy().hasHeightForWidth()
        )
        self.calibratedCheckBox.setSizePolicy(sizePolicy6)
        self.calibratedCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.calibratedCheckBox.setText(u"TOGGLE CALIBRATION")

        self.verticalLayout_2.addWidget(self.calibratedCheckBox)

        self.verticalLayout_5.addWidget(self.calibrationQFrame)

        self.verticalSpacer_15 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_15)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_12.addWidget(self.scrollArea)

        self.verticalSpacer_12 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_12.addItem(self.verticalSpacer_12)

        self.verticalLayout_9.addWidget(self.frame_8)

        self.pagesStackedWidget.addWidget(self.extractPointsWidget)
        self.taggingWidget = DataTaggingWidget()
        self.taggingWidget.setObjectName(u"taggingWidget")
        self.verticalLayout_10 = QVBoxLayout(self.taggingWidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_9 = QFrame(self.taggingWidget)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(25, 25, -1, -1)
        self.label_5 = QLabel(self.frame_9)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(
            u"color: rgb(190, 130, 250);\n" 'font: 57 11pt "Roboto Medium";'
        )
        self.label_5.setMargin(3)

        self.verticalLayout_13.addWidget(self.label_5)

        self.verticalSpacer_6 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred
        )

        self.verticalLayout_13.addItem(self.verticalSpacer_6)

        self.tagChoicesFrame = QFrame(self.frame_9)
        self.tagChoicesFrame.setObjectName(u"tagChoicesFrame")
        self.tagChoicesFrame.setFrameShape(QFrame.NoFrame)
        self.tagChoicesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.tagChoicesFrame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.noTagRadioButton = QRadioButton(self.tagChoicesFrame)
        self.noTagRadioButton.setObjectName(u"noTagRadioButton")
        self.noTagRadioButton.setText(u"NO TAG")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.verticalLayout_4.addWidget(self.noTagRadioButton)

        self.verticalSpacer_7 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.label_23 = QLabel(self.tagChoicesFrame)
        self.label_23.setObjectName(u"label_23")
        # if QT_CONFIG(tooltip)
        self.label_23.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.label_23.setStyleSheet(u'font: 10pt "Roboto";')
        self.label_23.setText(u"DISPERSIVE TRANSITION")

        self.verticalLayout_4.addWidget(self.label_23)

        self.tagDispersiveBareRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveBareRadioButton.setObjectName(u"tagDispersiveBareRadioButton")
        # if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setText(u"BY BARE STATES")
        self.tagDispersiveBareRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveBareRadioButton)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveDressedRadioButton.setObjectName(
            u"tagDispersiveDressedRadioButton"
        )
        # if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveDressedRadioButton)

        self.verticalSpacer_8 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.label_24 = QLabel(self.tagChoicesFrame)
        self.label_24.setObjectName(u"label_24")
        # if QT_CONFIG(tooltip)
        self.label_24.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.label_24.setStyleSheet(u'font: 10pt "Roboto";')
        self.label_24.setText(u"AVOIDED CROSSING")

        self.verticalLayout_4.addWidget(self.label_24)

        self.tagCrossingRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingRadioButton.setObjectName(u"tagCrossingRadioButton")
        # if QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setText(u"INFER WHEN FITTING")
        self.tagCrossingRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingRadioButton)

        self.tagCrossingDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingDressedRadioButton.setObjectName(
            u"tagCrossingDressedRadioButton"
        )
        # if QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setText(u"BY DRESSED INDICES")
        self.tagCrossingDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingDressedRadioButton)

        self.verticalLayout_13.addWidget(self.tagChoicesFrame)

        self.verticalSpacer_9 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_13.addItem(self.verticalSpacer_9)

        self.tagDressedGroupBox = QGroupBox(self.frame_9)
        self.tagDressedGroupBox.setObjectName(u"tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
        # if QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setStyleSheet(
            u"QGroupBox {\n" '	font: 10pt "Roboto";\n' "}"
        )
        self.tagDressedGroupBox.setTitle(u"TAG BY DRESSED INDICES")
        self.gridLayout_13 = QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 27, -1, -1)
        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName(u"label_30")
        sizePolicy12 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy12)
        # if QT_CONFIG(tooltip)
        self.label_30.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.label_30.setText(u"INITIAL")
        self.label_30.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 0, 3, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName(u"label_29")
        sizePolicy12.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy12)
        # if QT_CONFIG(tooltip)
        self.label_29.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.label_29.setText(u"PHOTONS")

        self.gridLayout_13.addWidget(self.label_29, 0, 0, 1, 1)

        self.phNumberDressedSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setObjectName(u"phNumberDressedSpinBox")
        self.phNumberDressedSpinBox.setEnabled(True)
        sizePolicy6.setHeightForWidth(
            self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy6)
        self.phNumberDressedSpinBox.setMinimumSize(QSize(60, 0))
        self.phNumberDressedSpinBox.setMinimum(1)

        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_13.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.finalStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.finalStateSpinBox.setObjectName(u"finalStateSpinBox")
        sizePolicy6.setHeightForWidth(
            self.finalStateSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.finalStateSpinBox.setSizePolicy(sizePolicy6)
        self.finalStateSpinBox.setMinimumSize(QSize(60, 20))
        self.finalStateSpinBox.setValue(1)

        self.gridLayout_13.addWidget(self.finalStateSpinBox, 1, 4, 1, 1)

        self.initialStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setObjectName(u"initialStateSpinBox")
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy6.setHeightForWidth(
            self.initialStateSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.initialStateSpinBox.setSizePolicy(sizePolicy6)
        self.initialStateSpinBox.setMinimumSize(QSize(60, 20))

        self.gridLayout_13.addWidget(self.initialStateSpinBox, 0, 4, 1, 1)

        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName(u"label_31")
        # if QT_CONFIG(tooltip)
        self.label_31.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.label_31.setText(u"FINAL")
        self.label_31.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_31, 1, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 5, 1, 1)

        self.verticalLayout_13.addWidget(self.tagDressedGroupBox)

        self.verticalSpacer_10 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_13.addItem(self.verticalSpacer_10)

        self.tagBareGroupBox = QGroupBox(self.frame_9)
        self.tagBareGroupBox.setObjectName(u"tagBareGroupBox")
        self.tagBareGroupBox.setEnabled(True)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setStyleSheet(
            u"QGroupBox {\n" '	font: 10pt "Roboto";\n' "}"
        )
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
        sizePolicy12.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy12)
        self.label_25.setText(u"PHOTONS")

        self.gridLayout_12.addWidget(self.label_25, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

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
        self.finalStateLineEdit.setPlaceholderText(
            u"<level subsys 1>, <level subsys2>, ..."
        )

        self.gridLayout_12.addWidget(self.finalStateLineEdit, 2, 4, 1, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName(u"phNumberBareSpinBox")
        sizePolicy8.setHeightForWidth(
            self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy8)
        self.phNumberBareSpinBox.setMinimumSize(QSize(60, 20))
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 1, 1, 1, 1)

        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setObjectName(u"initialStateLineEdit")
        self.initialStateLineEdit.setMinimumSize(QSize(0, 30))
        self.initialStateLineEdit.setPlaceholderText(
            u"<level subsys 1>, <level subsys2>, ..."
        )

        self.gridLayout_12.addWidget(self.initialStateLineEdit, 1, 4, 1, 1)

        self.verticalLayout_13.addWidget(self.tagBareGroupBox)

        self.verticalSpacer_11 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_13.addItem(self.verticalSpacer_11)

        self.verticalLayout_10.addWidget(self.frame_9)

        self.pagesStackedWidget.addWidget(self.taggingWidget)

        self.gridLayout.addWidget(self.pagesStackedWidget, 0, 1, 1, 1)

        self.manageDatasetsWidget = ManageDatasetsWidget(self.windowBodyFrame)
        self.manageDatasetsWidget.setObjectName(u"manageDatasetsWidget")

        self.gridLayout.addWidget(self.manageDatasetsWidget, 1, 1, 1, 1)

        self.mplFigureCanvas = MplFigureCanvas(self.windowBodyFrame)
        self.mplFigureCanvas.setObjectName(u"mplFigureCanvas")
        sizePolicy.setHeightForWidth(
            self.mplFigureCanvas.sizePolicy().hasHeightForWidth()
        )
        self.mplFigureCanvas.setSizePolicy(sizePolicy)
        self.mplFigureCanvas.setMinimumSize(QSize(0, 60))
        self.mplFigureCanvas.setMaximumSize(QSize(16777215, 16777215))
        self.mplFigureCanvas.setStyleSheet(
            u"background-color: rgb(37, 37, 42);\n" "color: rgb(200, 200, 200);"
        )
        self.mplNavButtons = MplNavButtons(self.mplFigureCanvas)
        self.mplNavButtons.setObjectName(u"mplNavButtons")
        self.mplNavButtons.setGeometry(QRect(10, 20, 360, 60))

        self.gridLayout.addWidget(self.mplFigureCanvas, 0, 3, 1, 1)

        self.verticalLayout.addWidget(self.windowBodyFrame)

        self.windowBodyFrame.raise_()
        self.windowTitleFrame.raise_()

        self.verticalLayout_3.addWidget(self.fullWindowFrame)

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
        QWidget.setTabOrder(
            self.tagDispersiveBareRadioButton, self.tagDispersiveDressedRadioButton
        )
        QWidget.setTabOrder(
            self.tagDispersiveDressedRadioButton, self.tagCrossingRadioButton
        )
        QWidget.setTabOrder(
            self.tagCrossingRadioButton, self.tagCrossingDressedRadioButton
        )
        QWidget.setTabOrder(
            self.tagCrossingDressedRadioButton, self.initialStateSpinBox
        )
        QWidget.setTabOrder(self.initialStateSpinBox, self.finalStateSpinBox)
        QWidget.setTabOrder(self.finalStateSpinBox, self.phNumberDressedSpinBox)
        QWidget.setTabOrder(self.phNumberDressedSpinBox, self.subsysNamesLineEdit)
        QWidget.setTabOrder(self.subsysNamesLineEdit, self.phNumberBareSpinBox)
        QWidget.setTabOrder(self.phNumberBareSpinBox, self.initialStateLineEdit)
        QWidget.setTabOrder(self.initialStateLineEdit, self.finalStateLineEdit)

        self.retranslateUi(MainWindow)
        self.buttonClose.clicked.connect(MainWindow.close)
        self.buttonMaximize.clicked.connect(MainWindow.showMaximized)
        self.buttonMinimize.clicked.connect(MainWindow.showMinimized)
        self.dataGroupPushButton.toggled.connect(self.xyzDataGridFrame.setVisible)
        self.bgndSubtractPushButton.toggled.connect(self.bgndSubtractQFrame.setVisible)
        self.coloringPushButton.toggled.connect(self.colorGridGroupBox.setVisible)
        self.calibrateGroupPushButton.toggled.connect(self.calibrationQFrame.setVisible)
        self.filtersPushButton.toggled.connect(self.filterQFrame.setVisible)

        self.pagesStackedWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        self.toggleMenuButton.setText("")
        self.windowTitleText.setText(
            QCoreApplication.translate("MainWindow", u"qfit", None)
        )
        self.buttonMinimize.setText("")
        self.buttonMaximize.setText("")
        self.buttonClose.setText("")
        self.modeTagButton.setText(
            QCoreApplication.translate("MainWindow", u"   TAG", None)
        )
        self.modeFitButton.setText(
            QCoreApplication.translate("MainWindow", u"   FIT", None)
        )
        self.modeSelectButton.setText(
            QCoreApplication.translate("MainWindow", u"   EXTRACT", None)
        )
        self.modePlotButton.setText(
            QCoreApplication.translate("MainWindow", u"   PRE-FIT", None)
        )
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"EXTRACT", None))
        self.coloringPushButton.setText(
            QCoreApplication.translate("MainWindow", u"COLORING", None)
        )
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"MAX", None))

        self.colorComboBox.setCurrentText(
            QCoreApplication.translate("MainWindow", u"PuOr", None)
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MIN", None))
        self.bgndSubtractPushButton.setText(
            QCoreApplication.translate("MainWindow", u"BACKGROUND SUBTRACT", None)
        )
        self.filtersPushButton.setText(
            QCoreApplication.translate("MainWindow", u"FILTERS", None)
        )
        self.dataGroupPushButton.setText(
            QCoreApplication.translate("MainWindow", u"DATA", None)
        )
        self.zComboBox.setCurrentText("")
        self.calibrateGroupPushButton.setText(
            QCoreApplication.translate("MainWindow", u"CALIBRATE", None)
        )
        self.calibrateX1Button.setText("")
        self.calibrateX2Button.setText("")
        self.mapX1LineEdit.setInputMask("")
        self.calibrateY1Button.setText("")
        self.calibrateY2Button.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TAG", None))
        # if QT_CONFIG(statustip)
        self.tagDispersiveBareRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", u"RR", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(statustip)
        self.tagDispersiveDressedRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", u"RR", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(statustip)
        self.tagCrossingRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", u"RR", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(statustip)
        self.tagCrossingDressedRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", u"RR", None)
        )
        # endif // QT_CONFIG(statustip)
        pass

    # retranslateUi