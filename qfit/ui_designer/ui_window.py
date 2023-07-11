# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window-2022-v2.ui'
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
from qfit.widgets.data_extracting import (
    DataExtractingWidget,
    DatasetWidget,
    ListView,
    ManageDatasetsWidget,
    TableView,
)
from qfit.widgets.data_tagging import (
    DataTaggingWidget,
    IntTupleLineEdit,
    StrTupleLineEdit,
)
from qfit.widgets.mpl_canvas import MplFigureCanvas, MplNavButtons
from . import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(909, 990)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies(["Roboto"])
        font.setPointSize(9)
        MainWindow.setFont(font)
        MainWindow.setWindowTitle("qfit")
        MainWindow.setWindowOpacity(1.000000000000000)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(
            "QMainWindow {\n"
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
        self.centralWidget.setObjectName("centralWidget")
        sizePolicy.setHeightForWidth(
            self.centralWidget.sizePolicy().hasHeightForWidth()
        )
        self.centralWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.fullWindowFrame = QFrame(self.centralWidget)
        self.fullWindowFrame.setObjectName("fullWindowFrame")
        self.fullWindowFrame.setMaximumSize(QSize(16777215, 16777215))
        self.fullWindowFrame.setFrameShape(QFrame.NoFrame)
        self.fullWindowFrame.setFrameShadow(QFrame.Raised)
        self.fullWindowFrame.setLineWidth(1)
        self.verticalLayout = QVBoxLayout(self.fullWindowFrame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.windowTitleFrame = QFrame(self.fullWindowFrame)
        self.windowTitleFrame.setObjectName("windowTitleFrame")
        self.windowTitleFrame.setMaximumSize(QSize(16777215, 40))
        self.windowTitleFrame.setFrameShape(QFrame.NoFrame)
        self.windowTitleFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.windowTitleFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.windowTitleLeftFrame = QFrame(self.windowTitleFrame)
        self.windowTitleLeftFrame.setObjectName("windowTitleLeftFrame")
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
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.toggleMenuButton = QPushButton(self.windowTitleLeftFrame)
        self.toggleMenuButton.setObjectName("toggleMenuButton")
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
            "QPushButton {	\n"
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
        icon.addFile(":/icons/20x20/cil-menu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toggleMenuButton.setIcon(icon)

        self.verticalLayout_7.addWidget(self.toggleMenuButton)

        self.horizontalLayout_3.addWidget(self.windowTitleLeftFrame)

        self.windowTitleMidFrame = QFrame(self.windowTitleFrame)
        self.windowTitleMidFrame.setObjectName("windowTitleMidFrame")
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
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.windowTitleText = QLabel(self.windowTitleMidFrame)
        self.windowTitleText.setObjectName("windowTitleText")
        self.windowTitleText.setStyleSheet(
            'color: rgb(255, 255, 255); font: 10pt "Roboto";'
        )
        self.windowTitleText.setLineWidth(0)

        self.horizontalLayout_6.addWidget(self.windowTitleText)

        self.horizontalLayout_3.addWidget(self.windowTitleMidFrame)

        self.windowTitleRightFrame = QFrame(self.windowTitleFrame)
        self.windowTitleRightFrame.setObjectName("windowTitleRightFrame")
        self.windowTitleRightFrame.setStyleSheet(
            "QPushButton {	\n"
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
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.buttonMinimize = QPushButton(self.windowTitleRightFrame)
        self.buttonMinimize.setObjectName("buttonMinimize")
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
            ":/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.buttonMinimize.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.buttonMinimize)

        self.buttonMaximize = QPushButton(self.windowTitleRightFrame)
        self.buttonMaximize.setObjectName("buttonMaximize")
        self.buttonMaximize.setEnabled(True)
        sizePolicy4.setHeightForWidth(
            self.buttonMaximize.sizePolicy().hasHeightForWidth()
        )
        self.buttonMaximize.setSizePolicy(sizePolicy4)
        self.buttonMaximize.setMinimumSize(QSize(40, 40))
        self.buttonMaximize.setMaximumSize(QSize(40, 16777215))
        icon2 = QIcon()
        icon2.addFile(
            ":/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.buttonMaximize.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.buttonMaximize)

        self.buttonClose = QPushButton(self.windowTitleRightFrame)
        self.buttonClose.setObjectName("buttonClose")
        self.buttonClose.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.buttonClose.sizePolicy().hasHeightForWidth())
        self.buttonClose.setSizePolicy(sizePolicy4)
        self.buttonClose.setMinimumSize(QSize(40, 40))
        self.buttonClose.setMaximumSize(QSize(40, 16777215))
        icon3 = QIcon()
        icon3.addFile(":/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.buttonClose.setIcon(icon3)

        self.horizontalLayout_4.addWidget(self.buttonClose)

        self.horizontalLayout_3.addWidget(self.windowTitleRightFrame)

        self.verticalLayout.addWidget(self.windowTitleFrame)

        self.windowBodyFrame = QFrame(self.fullWindowFrame)
        self.windowBodyFrame.setObjectName("windowBodyFrame")
        sizePolicy1.setHeightForWidth(
            self.windowBodyFrame.sizePolicy().hasHeightForWidth()
        )
        self.windowBodyFrame.setSizePolicy(sizePolicy1)
        self.windowBodyFrame.setStyleSheet(
            "QFrame {\n" "	background-color: rgb(33,33,33);\n" "}"
        )
        self.gridLayout = QGridLayout(self.windowBodyFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setContentsMargins(0, 0, 12, 0)
        self.allDatasetsFrame = ManageDatasetsWidget(self.windowBodyFrame)
        self.allDatasetsFrame.setObjectName("allDatasetsFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(
            self.allDatasetsFrame.sizePolicy().hasHeightForWidth()
        )
        self.allDatasetsFrame.setSizePolicy(sizePolicy5)
        self.allDatasetsFrame.setMaximumSize(QSize(16777215, 140))
        self.horizontalLayout_2 = QHBoxLayout(self.allDatasetsFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(15, -1, 15, -1)
        self.allDatasetsButtonsFrame = QFrame(self.allDatasetsFrame)
        self.allDatasetsButtonsFrame.setObjectName("allDatasetsButtonsFrame")
        self.allDatasetsButtonsFrame.setStyleSheet(
            "QPushButton {\n"
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
            "}"
        )
        self.verticalLayout_6 = QVBoxLayout(self.allDatasetsButtonsFrame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.newRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.newRowButton.setObjectName("newRowButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.newRowButton.sizePolicy().hasHeightForWidth()
        )
        self.newRowButton.setSizePolicy(sizePolicy6)
        self.newRowButton.setMinimumSize(QSize(100, 30))
        # if QT_CONFIG(tooltip)
        self.newRowButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.newRowButton.setText("NEW   ")
        icon4 = QIcon()
        icon4.addFile(":/icons/16x16/cil-plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.newRowButton.setIcon(icon4)

        self.verticalLayout_6.addWidget(self.newRowButton)

        self.deleteRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.deleteRowButton.setObjectName("deleteRowButton")
        sizePolicy6.setHeightForWidth(
            self.deleteRowButton.sizePolicy().hasHeightForWidth()
        )
        self.deleteRowButton.setSizePolicy(sizePolicy6)
        self.deleteRowButton.setMinimumSize(QSize(100, 30))
        # if QT_CONFIG(tooltip)
        self.deleteRowButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.deleteRowButton.setText("DELETE  ")
        icon5 = QIcon()
        icon5.addFile(":/icons/16x16/cil-minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteRowButton.setIcon(icon5)

        self.verticalLayout_6.addWidget(self.deleteRowButton)

        self.clearAllButton = QPushButton(self.allDatasetsButtonsFrame)
        self.clearAllButton.setObjectName("clearAllButton")
        sizePolicy6.setHeightForWidth(
            self.clearAllButton.sizePolicy().hasHeightForWidth()
        )
        self.clearAllButton.setSizePolicy(sizePolicy6)
        self.clearAllButton.setMinimumSize(QSize(100, 30))
        # if QT_CONFIG(tooltip)
        self.clearAllButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.clearAllButton.setText("CLEAR ALL")

        self.verticalLayout_6.addWidget(self.clearAllButton)

        self.horizontalLayout_2.addWidget(self.allDatasetsButtonsFrame)

        self.datasetListView = ListView(self.allDatasetsFrame)
        self.datasetListView.setObjectName("datasetListView")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(
            self.datasetListView.sizePolicy().hasHeightForWidth()
        )
        self.datasetListView.setSizePolicy(sizePolicy7)
        self.datasetListView.setMinimumSize(QSize(0, 100))
        self.datasetListView.setMaximumSize(QSize(230, 100))
        self.datasetListView.setStyleSheet("background-color: rgb(47, 47, 47)")
        self.datasetListView.setFrameShape(QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_2.addWidget(self.datasetListView)

        self.gridLayout.addWidget(self.allDatasetsFrame, 1, 1, 1, 1)

        self.mplFigureCanvas = MplFigureCanvas(self.windowBodyFrame)
        self.mplFigureCanvas.setObjectName("mplFigureCanvas")
        sizePolicy.setHeightForWidth(
            self.mplFigureCanvas.sizePolicy().hasHeightForWidth()
        )
        self.mplFigureCanvas.setSizePolicy(sizePolicy)
        self.mplFigureCanvas.setMinimumSize(QSize(0, 60))
        self.mplFigureCanvas.setMaximumSize(QSize(16777215, 16777215))
        self.mplFigureCanvas.setStyleSheet(
            "background-color: rgb(37, 37, 42);\n" "color: rgb(200, 200, 200);"
        )
        self.mplFigureButtons = MplNavButtons(self.mplFigureCanvas)
        self.mplFigureButtons.setObjectName("mplFigureButtons")
        self.mplFigureButtons.setGeometry(QRect(20, 20, 361, 60))
        self.mplFigureButtons.setStyleSheet(
            "QFrame {\n"
            "	background-color: transparent;\n"
            "}\n"
            "\n"
            "QPushButton {\n"
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
            "}"
        )
        self.resetViewButton = QPushButton(self.mplFigureButtons)
        self.resetViewButton.setObjectName("resetViewButton")
        self.resetViewButton.setGeometry(QRect(30, 0, 40, 40))
        # if QT_CONFIG(tooltip)
        self.resetViewButton.setToolTip("Reset plot area")
        # endif // QT_CONFIG(tooltip)
        icon6 = QIcon()
        icon6.addFile(":/icons/16x16/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon6)
        self.resetViewButton.setIconSize(QSize(24, 24))
        self.panViewButton = QPushButton(self.mplFigureButtons)
        self.panViewButton.setObjectName("panViewButton")
        self.panViewButton.setGeometry(QRect(90, 0, 40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
        # if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip("Pan mode: move plot region by dragging")
        # endif // QT_CONFIG(tooltip)
        icon7 = QIcon()
        icon7.addFile(":/icons/16x16/cil-move.png", QSize(), QIcon.Normal, QIcon.Off)
        self.panViewButton.setIcon(icon7)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.zoomViewButton = QPushButton(self.mplFigureButtons)
        self.zoomViewButton.setObjectName("zoomViewButton")
        self.zoomViewButton.setGeometry(QRect(150, 0, 40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
        # if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip("Zoom mode: select a plot region to enlarge")
        # endif // QT_CONFIG(tooltip)
        icon8 = QIcon()
        icon8.addFile(":/icons/16x16/cil-zoom-in.png", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomViewButton.setIcon(icon8)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.selectViewButton = QPushButton(self.mplFigureButtons)
        self.selectViewButton.setObjectName("selectViewButton")
        self.selectViewButton.setGeometry(QRect(210, 0, 41, 41))
        self.selectViewButton.setCursor(QCursor(Qt.CrossCursor))
        # if QT_CONFIG(tooltip)
        self.selectViewButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        icon9 = QIcon()
        icon9.addFile(
            ":/icons/16x16/cil-location-pin.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.selectViewButton.setIcon(icon9)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.swapXYButton = QPushButton(self.mplFigureButtons)
        self.swapXYButton.setObjectName("swapXYButton")
        self.swapXYButton.setGeometry(QRect(270, 0, 71, 41))
        self.swapXYButton.setCursor(QCursor(Qt.CrossCursor))
        # if QT_CONFIG(tooltip)
        self.swapXYButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.swapXYButton.setStyleSheet(
            "QPushButton {\n"
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
            "}"
        )
        self.swapXYButton.setCheckable(True)
        self.swapXYButton.setChecked(True)
        self.swapXYButton.setAutoExclusive(True)

        self.gridLayout.addWidget(self.mplFigureCanvas, 0, 3, 1, 1)

        self.menu_frame = QFrame(self.windowBodyFrame)
        self.menu_frame.setObjectName("menu_frame")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy8)
        self.menu_frame.setMinimumSize(QSize(190, 0))
        self.menu_frame.setMaximumSize(QSize(190, 16777215))
        self.menu_frame.setStyleSheet(
            "QFrame {\n"
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
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(37, 0, 20, 0)
        self.modeTagButton = QPushButton(self.menu_frame)
        self.modeTagButton.setObjectName("modeTagButton")
        self.modeTagButton.setMinimumSize(QSize(120, 70))
        self.modeTagButton.setMaximumSize(QSize(120, 70))
        icon10 = QIcon()
        icon10.addFile(":/icons/24x24/cil-list.png", QSize(), QIcon.Normal, QIcon.Off)
        self.modeTagButton.setIcon(icon10)
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
        self.modeFitButton.setObjectName("modeFitButton")
        self.modeFitButton.setMinimumSize(QSize(120, 70))
        self.modeFitButton.setMaximumSize(QSize(120, 70))
        icon11 = QIcon()
        icon11.addFile(
            ":/icons/24x24/cil-speedometer.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.modeFitButton.setIcon(icon11)
        self.modeFitButton.setIconSize(QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeFitButton, 4, 0, 1, 1)

        self.modeSelectButton = QPushButton(self.menu_frame)
        self.modeSelectButton.setObjectName("modeSelectButton")
        self.modeSelectButton.setMinimumSize(QSize(120, 70))
        self.modeSelectButton.setMaximumSize(QSize(16777215, 70))
        icon12 = QIcon()
        icon12.addFile(
            ":/icons/24x24/cil-location-pin.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.modeSelectButton.setIcon(icon12)
        self.modeSelectButton.setIconSize(QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setChecked(True)
        self.modeSelectButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modeSelectButton, 1, 0, 1, 2)

        self.modePlotButton = QPushButton(self.menu_frame)
        self.modePlotButton.setObjectName("modePlotButton")
        self.modePlotButton.setMinimumSize(QSize(170, 70))
        self.modePlotButton.setMaximumSize(QSize(120, 70))
        icon13 = QIcon()
        icon13.addFile(
            ":/icons/24x24/cil-chart-line.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.modePlotButton.setIcon(icon13)
        self.modePlotButton.setIconSize(QSize(24, 24))
        self.modePlotButton.setCheckable(True)
        self.modePlotButton.setAutoExclusive(True)

        self.gridLayout_2.addWidget(self.modePlotButton, 3, 0, 1, 2)

        self.gridLayout.addWidget(self.menu_frame, 0, 0, 3, 1)

        self.dataTableFrame = DatasetWidget(self.windowBodyFrame)
        self.dataTableFrame.setObjectName("dataTableFrame")
        sizePolicy5.setHeightForWidth(
            self.dataTableFrame.sizePolicy().hasHeightForWidth()
        )
        self.dataTableFrame.setSizePolicy(sizePolicy5)
        self.dataTableFrame.setMaximumSize(QSize(16777215, 140))
        self.dataTableFrame.setStyleSheet("")
        self.horizontalLayout_5 = QHBoxLayout(self.dataTableFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.dataTableView = TableView(self.dataTableFrame)
        self.dataTableView.setObjectName("dataTableView")
        sizePolicy6.setHeightForWidth(
            self.dataTableView.sizePolicy().hasHeightForWidth()
        )
        self.dataTableView.setSizePolicy(sizePolicy6)
        self.dataTableView.setMinimumSize(QSize(0, 105))
        self.dataTableView.setMaximumSize(QSize(16777215, 105))
        self.dataTableView.setStyleSheet(
            "QTableWidget {	\n"
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

        self.pagesStackedWidget = QStackedWidget(self.windowBodyFrame)
        self.pagesStackedWidget.setObjectName("pagesStackedWidget")
        sizePolicy1.setHeightForWidth(
            self.pagesStackedWidget.sizePolicy().hasHeightForWidth()
        )
        self.pagesStackedWidget.setSizePolicy(sizePolicy1)
        self.pagesStackedWidget.setMaximumSize(QSize(420, 620))
        self.extractPointsWidget = DataExtractingWidget()
        self.extractPointsWidget.setObjectName("extractPointsWidget")
        self.verticalLayout_9 = QVBoxLayout(self.extractPointsWidget)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.frame_8 = QFrame(self.extractPointsWidget)
        self.frame_8.setObjectName("frame_8")
        self.frame_8.setStyleSheet(
            "QPushButton {\n"
            '	font: 57 10pt "Roboto Medium";\n'
            "	color: rgb(170, 170, 170);\n"
            "	text-align: left;\n"
            "	border: none;\n"
            "}"
        )
        self.verticalLayout_12 = QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(20, 25, -1, -1)
        self.label_4 = QLabel(self.frame_8)
        self.label_4.setObjectName("label_4")
        font1 = QFont()
        font1.setFamilies(["Roboto Medium"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(
            "color: rgb(190, 130, 250);\n" 'font: 57 11pt "Roboto Medium";\n' ""
        )
        self.label_4.setFrameShape(QFrame.NoFrame)
        self.label_4.setMargin(3)

        self.verticalLayout_12.addWidget(self.label_4)

        self.verticalSpacer = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_12.addItem(self.verticalSpacer)

        self.scrollArea = QScrollArea(self.frame_8)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 515))
        self.scrollArea.setMaximumSize(QSize(16777215, 700))
        self.scrollArea.setStyleSheet("background-color: rgb(33,33,33);")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(False)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 366, 700))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.coloringPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.coloringPushButton.setObjectName("coloringPushButton")
        icon14 = QIcon()
        icon14.addFile(
            ":/icons/16x16/cil-caret-right.png", QSize(), QIcon.Normal, QIcon.Off
        )
        icon14.addFile(
            ":/icons/16x16/cil-caret-bottom.png", QSize(), QIcon.Normal, QIcon.On
        )
        self.coloringPushButton.setIcon(icon14)
        self.coloringPushButton.setCheckable(True)
        self.coloringPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.coloringPushButton)

        self.colorGridGroupBox = QGroupBox(self.scrollAreaWidgetContents_4)
        self.colorGridGroupBox.setObjectName("colorGridGroupBox")
        sizePolicy9 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(
            self.colorGridGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.colorGridGroupBox.setSizePolicy(sizePolicy9)
        self.colorGridGroupBox.setMinimumSize(QSize(330, 0))
        self.colorGridGroupBox.setTitle("")
        self.gridLayout_9 = QGridLayout(self.colorGridGroupBox)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.rangeSliderMin = QSlider(self.colorGridGroupBox)
        self.rangeSliderMin.setObjectName("rangeSliderMin")
        self.rangeSliderMin.setMinimumSize(QSize(0, 18))
        self.rangeSliderMin.setMaximum(99)
        self.rangeSliderMin.setSingleStep(1)
        self.rangeSliderMin.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMin, 2, 0, 1, 1)

        self.label_3 = QLabel(self.colorGridGroupBox)
        self.label_3.setObjectName("label_3")

        self.gridLayout_9.addWidget(self.label_3, 4, 1, 1, 1)

        self.colorComboBox = QComboBox(self.colorGridGroupBox)
        icon15 = QIcon()
        icon15.addFile(":/icons/PuOr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon15, "PuOr")
        icon16 = QIcon()
        icon16.addFile(":/icons/RdYlBu.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon16, "RdYlBu")
        icon17 = QIcon()
        icon17.addFile(":/icons/bwr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon17, "bwr")
        icon18 = QIcon()
        icon18.addFile(":/icons/viridis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon18, "viridis")
        icon19 = QIcon()
        icon19.addFile(":/icons/cividis.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon19, "cividis")
        icon20 = QIcon()
        icon20.addFile(":/icons/gray.png", QSize(), QIcon.Normal, QIcon.Off)
        self.colorComboBox.addItem(icon20, "gray")
        self.colorComboBox.setObjectName("colorComboBox")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(
            self.colorComboBox.sizePolicy().hasHeightForWidth()
        )
        self.colorComboBox.setSizePolicy(sizePolicy10)
        self.colorComboBox.setMinimumSize(QSize(0, 30))
        # if QT_CONFIG(tooltip)
        self.colorComboBox.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.colorComboBox.setIconSize(QSize(100, 10))
        self.colorComboBox.setFrame(True)

        self.gridLayout_9.addWidget(self.colorComboBox, 1, 0, 1, 1)

        self.logScaleCheckBox = QCheckBox(self.colorGridGroupBox)
        self.logScaleCheckBox.setObjectName("logScaleCheckBox")
        self.logScaleCheckBox.setLayoutDirection(Qt.LeftToRight)
        self.logScaleCheckBox.setAutoFillBackground(False)
        self.logScaleCheckBox.setText("LOG")
        self.logScaleCheckBox.setChecked(False)

        self.gridLayout_9.addWidget(self.logScaleCheckBox, 1, 1, 1, 1)

        self.rangeSliderMax = QSlider(self.colorGridGroupBox)
        self.rangeSliderMax.setObjectName("rangeSliderMax")
        self.rangeSliderMax.setMinimumSize(QSize(0, 18))
        self.rangeSliderMax.setMaximum(99)
        self.rangeSliderMax.setValue(99)
        self.rangeSliderMax.setSliderPosition(99)
        self.rangeSliderMax.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.rangeSliderMax, 4, 0, 1, 1)

        self.label_2 = QLabel(self.colorGridGroupBox)
        self.label_2.setObjectName("label_2")

        self.gridLayout_9.addWidget(self.label_2, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.gridLayout_9.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.verticalLayout_5.addWidget(self.colorGridGroupBox)

        self.bgndSubtractPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.bgndSubtractPushButton.setObjectName("bgndSubtractPushButton")
        self.bgndSubtractPushButton.setIcon(icon14)
        self.bgndSubtractPushButton.setCheckable(True)
        self.bgndSubtractPushButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.bgndSubtractPushButton)

        self.bgndSubtractQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.bgndSubtractQFrame.setObjectName("bgndSubtractQFrame")
        sizePolicy11 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(
            self.bgndSubtractQFrame.sizePolicy().hasHeightForWidth()
        )
        self.bgndSubtractQFrame.setSizePolicy(sizePolicy11)
        self.bgndSubtractQFrame.setMinimumSize(QSize(330, 0))
        self.gridLayout_8 = QGridLayout(self.bgndSubtractQFrame)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(0)
        self.gridLayout_8.setVerticalSpacing(7)
        self.gridLayout_8.setContentsMargins(-1, 4, -1, -1)
        self.bgndSubtractYCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractYCheckBox.setObjectName("bgndSubtractYCheckBox")
        # if QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setToolTip("Background subtraction along Y")
        # endif // QT_CONFIG(tooltip)
        self.bgndSubtractYCheckBox.setText("ALONG Y AXIS")

        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 3, 1, 1, 1)

        self.bgndSubtractXCheckBox = QCheckBox(self.bgndSubtractQFrame)
        self.bgndSubtractXCheckBox.setObjectName("bgndSubtractXCheckBox")
        # if QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setToolTip("Background subtraction along X")
        # endif // QT_CONFIG(tooltip)
        self.bgndSubtractXCheckBox.setText("ALONG X AXIS")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)

        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 3, 0, 1, 1)

        self.verticalLayout_5.addWidget(self.bgndSubtractQFrame)

        self.verticalSpacer_13 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_13)

        self.filtersPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.filtersPushButton.setObjectName("filtersPushButton")
        self.filtersPushButton.setIcon(icon14)
        self.filtersPushButton.setCheckable(True)

        self.verticalLayout_5.addWidget(self.filtersPushButton)

        self.filterQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.filterQFrame.setObjectName("filterQFrame")
        self.horizontalLayout_7 = QHBoxLayout(self.filterQFrame)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 4, -1, -1)
        self.topHatCheckBox = QCheckBox(self.filterQFrame)
        self.topHatCheckBox.setObjectName("topHatCheckBox")
        # if QT_CONFIG(tooltip)
        self.topHatCheckBox.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.topHatCheckBox.setText("TOP-HAT")

        self.horizontalLayout_7.addWidget(self.topHatCheckBox)

        self.edgeFilterCheckBox = QCheckBox(self.filterQFrame)
        self.edgeFilterCheckBox.setObjectName("edgeFilterCheckBox")
        # if QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.edgeFilterCheckBox.setText("EDGE")

        self.horizontalLayout_7.addWidget(self.edgeFilterCheckBox)

        self.waveletCheckBox = QCheckBox(self.filterQFrame)
        self.waveletCheckBox.setObjectName("waveletCheckBox")
        # if QT_CONFIG(tooltip)
        self.waveletCheckBox.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.waveletCheckBox.setText("DENOISE")

        self.horizontalLayout_7.addWidget(self.waveletCheckBox)

        self.verticalLayout_5.addWidget(self.filterQFrame)

        self.verticalSpacer_4 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.dataGroupPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.dataGroupPushButton.setObjectName("dataGroupPushButton")
        self.dataGroupPushButton.setIcon(icon14)
        self.dataGroupPushButton.setCheckable(True)

        self.verticalLayout_5.addWidget(self.dataGroupPushButton)

        self.xyzDataGridFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.xyzDataGridFrame.setObjectName("xyzDataGridFrame")
        self.xyzDataGridFrame.setEnabled(True)
        sizePolicy11.setHeightForWidth(
            self.xyzDataGridFrame.sizePolicy().hasHeightForWidth()
        )
        self.xyzDataGridFrame.setSizePolicy(sizePolicy11)
        self.xyzDataGridFrame.setMinimumSize(QSize(330, 0))
        self.gridLayout_4 = QGridLayout(self.xyzDataGridFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.zComboBox = QComboBox(self.xyzDataGridFrame)
        self.zComboBox.setObjectName("zComboBox")
        self.zComboBox.setMinimumSize(QSize(250, 30))
        self.zComboBox.setStyleSheet("background-color: rgb(47,47,47);")
        self.zComboBox.setFrame(True)

        self.gridLayout_4.addWidget(self.zComboBox, 2, 1, 1, 1)

        self.label_14 = QLabel(self.xyzDataGridFrame)
        self.label_14.setObjectName("label_14")
        self.label_14.setText("AXIS 2")
        self.label_14.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_14, 5, 0, 1, 1)

        self.label_13 = QLabel(self.xyzDataGridFrame)
        self.label_13.setObjectName("label_13")
        self.label_13.setText("Z")
        self.label_13.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)

        self.xComboBox = QComboBox(self.xyzDataGridFrame)
        self.xComboBox.setObjectName("xComboBox")
        self.xComboBox.setMinimumSize(QSize(250, 30))
        self.xComboBox.setStyleSheet("background-color: rgb(47,47,47);")

        self.gridLayout_4.addWidget(self.xComboBox, 4, 1, 1, 1)

        self.yComboBox = QComboBox(self.xyzDataGridFrame)
        self.yComboBox.setObjectName("yComboBox")
        self.yComboBox.setMinimumSize(QSize(250, 30))
        self.yComboBox.setStyleSheet("background-color: rgb(47,47,47);")

        self.gridLayout_4.addWidget(self.yComboBox, 5, 1, 1, 1)

        self.label_12 = QLabel(self.xyzDataGridFrame)
        self.label_12.setObjectName("label_12")
        self.label_12.setText("AXIS 1")
        self.label_12.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_12, 4, 0, 1, 1)

        self.verticalLayout_5.addWidget(self.xyzDataGridFrame)

        self.verticalSpacer_5 = QSpacerItem(
            20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.calibrateGroupPushButton = QPushButton(self.scrollAreaWidgetContents_4)
        self.calibrateGroupPushButton.setObjectName("calibrateGroupPushButton")
        font2 = QFont()
        font2.setFamilies(["Roboto Medium"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.calibrateGroupPushButton.setFont(font2)
        self.calibrateGroupPushButton.setIcon(icon14)
        self.calibrateGroupPushButton.setCheckable(True)
        self.calibrateGroupPushButton.setChecked(False)

        self.verticalLayout_5.addWidget(self.calibrateGroupPushButton)

        self.calibrationQFrame = QFrame(self.scrollAreaWidgetContents_4)
        self.calibrationQFrame.setObjectName("calibrationQFrame")
        self.calibrationQFrame.setStyleSheet(
            "QPushButton {\n"
            "	background-color: rgb(93, 93, 93);\n"
            "	border: 0px solid rgb(52, 59, 72);\n"
            "	border-radius: 5px;	\n"
            "	text-align: center;\n"
            "}"
        )
        self.verticalLayout_2 = QVBoxLayout(self.calibrationQFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.calibrateXGridFrame = QFrame(self.calibrationQFrame)
        self.calibrateXGridFrame.setObjectName("calibrateXGridFrame")
        sizePolicy11.setHeightForWidth(
            self.calibrateXGridFrame.sizePolicy().hasHeightForWidth()
        )
        self.calibrateXGridFrame.setSizePolicy(sizePolicy11)
        self.calibrateXGridFrame.setMinimumSize(QSize(330, 0))
        self.calibrateXGridFrame.setMaximumSize(QSize(320, 16777215))
        self.gridLayout_10 = QGridLayout(self.calibrateXGridFrame)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_10.setVerticalSpacing(8)
        self.gridLayout_10.setContentsMargins(-1, 9, -1, -1)
        self.label_17 = QLabel(self.calibrateXGridFrame)
        self.label_17.setObjectName("label_17")
        sizePolicy12 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy12)
        self.label_17.setText(
            '<html><head/><body><p align="right">\u2192 X<span style=" vertical-align:sub;">1</span>\'</p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_17, 1, 3, 1, 1)

        self.calibrateX1Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX1Button.setObjectName("calibrateX1Button")
        self.calibrateX1Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateX1Button.setToolTip(
            "Calibrate x1, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        icon21 = QIcon()
        icon21.addFile(":/icons/16x16/cil-at.png", QSize(), QIcon.Normal, QIcon.Off)
        self.calibrateX1Button.setIcon(icon21)

        self.gridLayout_10.addWidget(self.calibrateX1Button, 1, 0, 1, 1)

        self.calibrateX2Button = QPushButton(self.calibrateXGridFrame)
        self.calibrateX2Button.setObjectName("calibrateX2Button")
        self.calibrateX2Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateX2Button.setToolTip(
            "Calibrate x2, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        self.calibrateX2Button.setIcon(icon21)

        self.gridLayout_10.addWidget(self.calibrateX2Button, 2, 0, 1, 1)

        self.label_15 = QLabel(self.calibrateXGridFrame)
        self.label_15.setObjectName("label_15")
        sizePolicy12.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy12)
        self.label_15.setText(
            '<html><head/><body><p align="right">X<span style=" vertical-align:sub;">1</span></p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_15, 1, 1, 1, 1)

        self.label_18 = QLabel(self.calibrateXGridFrame)
        self.label_18.setObjectName("label_18")
        sizePolicy12.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy12)
        self.label_18.setText(
            '<html><head/><body><p align="right">\u2192 X<span style=" vertical-align:sub;">2</span>\'</p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_18, 2, 3, 1, 1)

        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX2LineEdit.setObjectName("rawX2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawX2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawX2LineEdit.setSizePolicy(sizePolicy6)
        self.rawX2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawX2LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.rawX2LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.rawX2LineEdit.setText("1.0")

        self.gridLayout_10.addWidget(self.rawX2LineEdit, 2, 2, 1, 1)

        self.label_16 = QLabel(self.calibrateXGridFrame)
        self.label_16.setObjectName("label_16")
        sizePolicy12.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy12)
        self.label_16.setText(
            '<html><head/><body><p align="right">X<span style=" vertical-align:sub;">2</span></p></body></html>'
        )

        self.gridLayout_10.addWidget(self.label_16, 2, 1, 1, 1)

        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX2LineEdit.setObjectName("mapX2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapX2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapX2LineEdit.setSizePolicy(sizePolicy6)
        self.mapX2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapX2LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.mapX2LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.mapX2LineEdit.setText("1.0")

        self.gridLayout_10.addWidget(self.mapX2LineEdit, 2, 4, 1, 1)

        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.rawX1LineEdit.setObjectName("rawX1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawX1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawX1LineEdit.setSizePolicy(sizePolicy6)
        self.rawX1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawX1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawX1LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.rawX1LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.rawX1LineEdit.setText("0.0")

        self.gridLayout_10.addWidget(self.rawX1LineEdit, 1, 2, 1, 1)

        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridFrame)
        self.mapX1LineEdit.setObjectName("mapX1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapX1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapX1LineEdit.setSizePolicy(sizePolicy6)
        self.mapX1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapX1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapX1LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.mapX1LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.mapX1LineEdit.setText("0.0")

        self.gridLayout_10.addWidget(self.mapX1LineEdit, 1, 4, 1, 1)

        self.verticalLayout_2.addWidget(self.calibrateXGridFrame)

        self.calibrateYGridFrame = QFrame(self.calibrationQFrame)
        self.calibrateYGridFrame.setObjectName("calibrateYGridFrame")
        sizePolicy11.setHeightForWidth(
            self.calibrateYGridFrame.sizePolicy().hasHeightForWidth()
        )
        self.calibrateYGridFrame.setSizePolicy(sizePolicy11)
        self.calibrateYGridFrame.setMinimumSize(QSize(330, 0))
        self.calibrateYGridFrame.setMaximumSize(QSize(320, 16777215))
        # if QT_CONFIG(tooltip)
        self.calibrateYGridFrame.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.gridLayout_11 = QGridLayout(self.calibrateYGridFrame)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_11.setVerticalSpacing(8)
        self.gridLayout_11.setContentsMargins(-1, 15, -1, -1)
        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY1LineEdit.setObjectName("rawY1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawY1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawY1LineEdit.setSizePolicy(sizePolicy6)
        self.rawY1LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawY1LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.rawY1LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.rawY1LineEdit.setText("0.0")

        self.gridLayout_11.addWidget(self.rawY1LineEdit, 0, 2, 1, 1)

        self.label_19 = QLabel(self.calibrateYGridFrame)
        self.label_19.setObjectName("label_19")
        sizePolicy12.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy12)
        self.label_19.setText(
            '<html><head/><body><p align="right">Y<span style=" vertical-align:sub;">1</span></p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)

        self.label_20 = QLabel(self.calibrateYGridFrame)
        self.label_20.setObjectName("label_20")
        sizePolicy12.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy12)
        self.label_20.setText(
            '<html><head/><body><p align="right">Y<span style=" vertical-align:sub;">2</span></p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_20, 1, 1, 1, 1)

        self.label_22 = QLabel(self.calibrateYGridFrame)
        self.label_22.setObjectName("label_22")
        sizePolicy12.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy12)
        self.label_22.setText(
            '<html><head/><body><p align="right">\u2192 Y<span style=" vertical-align:sub;">2</span>\'</p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_22, 1, 3, 1, 1)

        self.calibrateY1Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY1Button.setObjectName("calibrateY1Button")
        self.calibrateY1Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateY1Button.setToolTip(
            "Calibrate y1, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        self.calibrateY1Button.setIcon(icon21)

        self.gridLayout_11.addWidget(self.calibrateY1Button, 0, 0, 1, 1)

        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY2LineEdit.setObjectName("mapY2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapY2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapY2LineEdit.setSizePolicy(sizePolicy6)
        self.mapY2LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapY2LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.mapY2LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.mapY2LineEdit.setText("1.0")

        self.gridLayout_11.addWidget(self.mapY2LineEdit, 1, 4, 1, 1)

        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.rawY2LineEdit.setObjectName("rawY2LineEdit")
        sizePolicy6.setHeightForWidth(
            self.rawY2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawY2LineEdit.setSizePolicy(sizePolicy6)
        self.rawY2LineEdit.setMinimumSize(QSize(80, 30))
        self.rawY2LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.rawY2LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.rawY2LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.rawY2LineEdit.setText("1.0")

        self.gridLayout_11.addWidget(self.rawY2LineEdit, 1, 2, 1, 1)

        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridFrame)
        self.mapY1LineEdit.setObjectName("mapY1LineEdit")
        sizePolicy6.setHeightForWidth(
            self.mapY1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapY1LineEdit.setSizePolicy(sizePolicy6)
        self.mapY1LineEdit.setMinimumSize(QSize(80, 30))
        self.mapY1LineEdit.setMaximumSize(QSize(200, 16777215))
        # if QT_CONFIG(tooltip)
        self.mapY1LineEdit.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.mapY1LineEdit.setStyleSheet("background-color: rgb(47,47,47);")
        self.mapY1LineEdit.setText("0.0")

        self.gridLayout_11.addWidget(self.mapY1LineEdit, 0, 4, 1, 1)

        self.label_21 = QLabel(self.calibrateYGridFrame)
        self.label_21.setObjectName("label_21")
        sizePolicy12.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy12)
        self.label_21.setText(
            '<html><head/><body><p align="right">\u2192 Y<span style=" vertical-align:sub;">1</span>\'</p></body></html>'
        )

        self.gridLayout_11.addWidget(self.label_21, 0, 3, 1, 1)

        self.calibrateY2Button = QPushButton(self.calibrateYGridFrame)
        self.calibrateY2Button.setObjectName("calibrateY2Button")
        self.calibrateY2Button.setMinimumSize(QSize(30, 30))
        # if QT_CONFIG(tooltip)
        self.calibrateY2Button.setToolTip(
            "Calibrate y2, allows selection of coordinate inside plot"
        )
        # endif // QT_CONFIG(tooltip)
        self.calibrateY2Button.setIcon(icon21)

        self.gridLayout_11.addWidget(self.calibrateY2Button, 1, 0, 1, 1)

        self.verticalLayout_2.addWidget(self.calibrateYGridFrame)

        self.calibratedCheckBox = QCheckBox(self.calibrationQFrame)
        self.calibratedCheckBox.setObjectName("calibratedCheckBox")
        sizePolicy6.setHeightForWidth(
            self.calibratedCheckBox.sizePolicy().hasHeightForWidth()
        )
        self.calibratedCheckBox.setSizePolicy(sizePolicy6)
        self.calibratedCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.calibratedCheckBox.setText("TOGGLE CALIBRATION")

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
        self.taggingWidget.setObjectName("taggingWidget")
        self.verticalLayout_10 = QVBoxLayout(self.taggingWidget)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_9 = QFrame(self.taggingWidget)
        self.frame_9.setObjectName("frame_9")
        self.frame_9.setStyleSheet("")
        self.verticalLayout_13 = QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(25, 25, -1, -1)
        self.label_5 = QLabel(self.frame_9)
        self.label_5.setObjectName("label_5")
        self.label_5.setStyleSheet(
            "color: rgb(190, 130, 250);\n" 'font: 57 11pt "Roboto Medium";'
        )
        self.label_5.setMargin(3)

        self.verticalLayout_13.addWidget(self.label_5)

        self.verticalSpacer_6 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred
        )

        self.verticalLayout_13.addItem(self.verticalSpacer_6)

        self.tagChoicesFrame = QFrame(self.frame_9)
        self.tagChoicesFrame.setObjectName("tagChoicesFrame")
        self.tagChoicesFrame.setFrameShape(QFrame.NoFrame)
        self.tagChoicesFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.tagChoicesFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.noTagRadioButton = QRadioButton(self.tagChoicesFrame)
        self.noTagRadioButton.setObjectName("noTagRadioButton")
        self.noTagRadioButton.setText("NO TAG")
        self.noTagRadioButton.setIconSize(QSize(16, 16))
        self.noTagRadioButton.setChecked(True)

        self.verticalLayout_4.addWidget(self.noTagRadioButton)

        self.verticalSpacer_7 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.label_23 = QLabel(self.tagChoicesFrame)
        self.label_23.setObjectName("label_23")
        # if QT_CONFIG(tooltip)
        self.label_23.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.label_23.setStyleSheet('font: 10pt "Roboto";')
        self.label_23.setText("DISPERSIVE TRANSITION")

        self.verticalLayout_4.addWidget(self.label_23)

        self.tagDispersiveBareRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveBareRadioButton.setObjectName("tagDispersiveBareRadioButton")
        # if QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.tagDispersiveBareRadioButton.setText("BY BARE STATES")
        self.tagDispersiveBareRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveBareRadioButton)

        self.tagDispersiveDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveDressedRadioButton.setObjectName(
            "tagDispersiveDressedRadioButton"
        )
        # if QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.tagDispersiveDressedRadioButton.setText("BY DRESSED INDICES")
        self.tagDispersiveDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagDispersiveDressedRadioButton)

        self.verticalSpacer_8 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.label_24 = QLabel(self.tagChoicesFrame)
        self.label_24.setObjectName("label_24")
        # if QT_CONFIG(tooltip)
        self.label_24.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.label_24.setStyleSheet('font: 10pt "Roboto";')
        self.label_24.setText("AVOIDED CROSSING")

        self.verticalLayout_4.addWidget(self.label_24)

        self.tagCrossingRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingRadioButton.setObjectName("tagCrossingRadioButton")
        # if QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.tagCrossingRadioButton.setText("INFER WHEN FITTING")
        self.tagCrossingRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingRadioButton)

        self.tagCrossingDressedRadioButton = QRadioButton(self.tagChoicesFrame)
        self.tagCrossingDressedRadioButton.setObjectName(
            "tagCrossingDressedRadioButton"
        )
        # if QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.tagCrossingDressedRadioButton.setText("BY DRESSED INDICES")
        self.tagCrossingDressedRadioButton.setIconSize(QSize(16, 16))

        self.verticalLayout_4.addWidget(self.tagCrossingDressedRadioButton)

        self.verticalLayout_13.addWidget(self.tagChoicesFrame)

        self.verticalSpacer_9 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.verticalLayout_13.addItem(self.verticalSpacer_9)

        self.tagDressedGroupBox = QGroupBox(self.frame_9)
        self.tagDressedGroupBox.setObjectName("tagDressedGroupBox")
        self.tagDressedGroupBox.setEnabled(True)
        # if QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.tagDressedGroupBox.setStyleSheet(
            "QGroupBox {\n" '	font: 10pt "Roboto";\n' "}"
        )
        self.tagDressedGroupBox.setTitle("TAG BY DRESSED INDICES")
        self.gridLayout_13 = QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_13.setContentsMargins(-1, 27, -1, -1)
        self.label_30 = QLabel(self.tagDressedGroupBox)
        self.label_30.setObjectName("label_30")
        sizePolicy13 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy13)
        # if QT_CONFIG(tooltip)
        self.label_30.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.label_30.setText("INITIAL")
        self.label_30.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_30, 0, 3, 1, 1)

        self.label_29 = QLabel(self.tagDressedGroupBox)
        self.label_29.setObjectName("label_29")
        sizePolicy13.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy13)
        # if QT_CONFIG(tooltip)
        self.label_29.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.label_29.setText("PHOTONS")

        self.gridLayout_13.addWidget(self.label_29, 0, 0, 1, 1)

        self.phNumberDressedSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.phNumberDressedSpinBox.setObjectName("phNumberDressedSpinBox")
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
        self.finalStateSpinBox.setObjectName("finalStateSpinBox")
        sizePolicy6.setHeightForWidth(
            self.finalStateSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.finalStateSpinBox.setSizePolicy(sizePolicy6)
        self.finalStateSpinBox.setMinimumSize(QSize(60, 20))
        self.finalStateSpinBox.setValue(1)

        self.gridLayout_13.addWidget(self.finalStateSpinBox, 1, 4, 1, 1)

        self.initialStateSpinBox = QSpinBox(self.tagDressedGroupBox)
        self.initialStateSpinBox.setObjectName("initialStateSpinBox")
        self.initialStateSpinBox.setEnabled(True)
        sizePolicy6.setHeightForWidth(
            self.initialStateSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.initialStateSpinBox.setSizePolicy(sizePolicy6)
        self.initialStateSpinBox.setMinimumSize(QSize(60, 20))

        self.gridLayout_13.addWidget(self.initialStateSpinBox, 0, 4, 1, 1)

        self.label_31 = QLabel(self.tagDressedGroupBox)
        self.label_31.setObjectName("label_31")
        # if QT_CONFIG(tooltip)
        self.label_31.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.label_31.setText("FINAL")
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
        self.tagBareGroupBox.setObjectName("tagBareGroupBox")
        self.tagBareGroupBox.setEnabled(True)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setStyleSheet(
            "QGroupBox {\n" '	font: 10pt "Roboto";\n' "}"
        )
        self.tagBareGroupBox.setTitle("TAG BY BARE STATES")
        self.tagBareGroupBox.setFlat(False)
        self.gridLayout_12 = QGridLayout(self.tagBareGroupBox)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_12.setContentsMargins(-1, 27, -1, -1)
        self.subsysNamesLineEdit = StrTupleLineEdit(self.tagBareGroupBox)
        self.subsysNamesLineEdit.setObjectName("subsysNamesLineEdit")
        self.subsysNamesLineEdit.setMinimumSize(QSize(0, 30))
        self.subsysNamesLineEdit.setText("")
        self.subsysNamesLineEdit.setPlaceholderText(" <subsystem name 1>, ...")
        self.subsysNamesLineEdit.setClearButtonEnabled(True)

        self.gridLayout_12.addWidget(self.subsysNamesLineEdit, 0, 0, 1, 5)

        self.label_25 = QLabel(self.tagBareGroupBox)
        self.label_25.setObjectName("label_25")
        sizePolicy13.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy13)
        self.label_25.setText("PHOTONS")

        self.gridLayout_12.addWidget(self.label_25, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_12.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.label_28 = QLabel(self.tagBareGroupBox)
        self.label_28.setObjectName("label_28")
        self.label_28.setText("INITIAL")

        self.gridLayout_12.addWidget(self.label_28, 1, 3, 1, 1)

        self.label_26 = QLabel(self.tagBareGroupBox)
        self.label_26.setObjectName("label_26")
        self.label_26.setText("FINAL")

        self.gridLayout_12.addWidget(self.label_26, 2, 3, 1, 1)

        self.finalStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setObjectName("finalStateLineEdit")
        self.finalStateLineEdit.setMinimumSize(QSize(0, 30))
        self.finalStateLineEdit.setPlaceholderText(
            "<level subsys 1>, <level subsys2>, ..."
        )

        self.gridLayout_12.addWidget(self.finalStateLineEdit, 2, 4, 1, 1)

        self.phNumberBareSpinBox = QSpinBox(self.tagBareGroupBox)
        self.phNumberBareSpinBox.setObjectName("phNumberBareSpinBox")
        sizePolicy9.setHeightForWidth(
            self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy9)
        self.phNumberBareSpinBox.setMinimumSize(QSize(60, 20))
        self.phNumberBareSpinBox.setAlignment(Qt.AlignCenter)
        self.phNumberBareSpinBox.setMinimum(1)

        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 1, 1, 1, 1)

        self.initialStateLineEdit = IntTupleLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setObjectName("initialStateLineEdit")
        self.initialStateLineEdit.setMinimumSize(QSize(0, 30))
        self.initialStateLineEdit.setPlaceholderText(
            "<level subsys 1>, <level subsys2>, ..."
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
        QWidget.setTabOrder(self.finalStateLineEdit, self.resetViewButton)
        QWidget.setTabOrder(self.resetViewButton, self.panViewButton)
        QWidget.setTabOrder(self.panViewButton, self.zoomViewButton)
        QWidget.setTabOrder(self.zoomViewButton, self.selectViewButton)
        QWidget.setTabOrder(self.selectViewButton, self.swapXYButton)

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
            QCoreApplication.translate("MainWindow", "qfit", None)
        )
        self.buttonMinimize.setText("")
        self.buttonMaximize.setText("")
        self.buttonClose.setText("")
        self.resetViewButton.setText("")
        self.panViewButton.setText("")
        self.zoomViewButton.setText("")
        self.selectViewButton.setText("")
        self.swapXYButton.setText(
            QCoreApplication.translate("MainWindow", "X\u2194Y", None)
        )
        self.modeTagButton.setText(
            QCoreApplication.translate("MainWindow", "   TAG", None)
        )
        self.modeFitButton.setText(
            QCoreApplication.translate("MainWindow", "   FIT", None)
        )
        self.modeSelectButton.setText(
            QCoreApplication.translate("MainWindow", "   EXTRACT", None)
        )
        self.modePlotButton.setText(
            QCoreApplication.translate("MainWindow", "   PRE-FIT", None)
        )
        self.label_4.setText(QCoreApplication.translate("MainWindow", "EXTRACT", None))
        self.coloringPushButton.setText(
            QCoreApplication.translate("MainWindow", "COLORING", None)
        )
        self.label_3.setText(QCoreApplication.translate("MainWindow", "MAX", None))

        self.colorComboBox.setCurrentText(
            QCoreApplication.translate("MainWindow", "PuOr", None)
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "MIN", None))
        self.bgndSubtractPushButton.setText(
            QCoreApplication.translate("MainWindow", "BACKGROUND SUBTRACT", None)
        )
        self.filtersPushButton.setText(
            QCoreApplication.translate("MainWindow", "FILTERS", None)
        )
        self.dataGroupPushButton.setText(
            QCoreApplication.translate("MainWindow", "DATA", None)
        )
        self.zComboBox.setCurrentText("")
        self.calibrateGroupPushButton.setText(
            QCoreApplication.translate("MainWindow", "CALIBRATE", None)
        )
        self.calibrateX1Button.setText("")
        self.calibrateX2Button.setText("")
        self.mapX1LineEdit.setInputMask("")
        self.calibrateY1Button.setText("")
        self.calibrateY2Button.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", "TAG", None))
        # if QT_CONFIG(statustip)
        self.tagDispersiveBareRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", "RR", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(statustip)
        self.tagDispersiveDressedRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", "RR", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(statustip)
        self.tagCrossingRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", "RR", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(statustip)
        self.tagCrossingDressedRadioButton.setStatusTip(
            QCoreApplication.translate("MainWindow", "RR", None)
        )
        # endif // QT_CONFIG(statustip)
        pass

    # retranslateUi
