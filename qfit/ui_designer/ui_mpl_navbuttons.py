# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mpl_navbuttons.ui'
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
from PySide6.QtWidgets import QApplication, QFrame, QPushButton, QSizePolicy, QWidget
from . import resources_rc


class Ui_MplNavButtons(object):
    def setupUi(self, MplNavButtons):
        if not MplNavButtons.objectName():
            MplNavButtons.setObjectName(u"MplNavButtons")
        MplNavButtons.resize(360, 60)
        MplNavButtons.setStyleSheet(
            u"QFrame {\n"
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
        self.mplFigureButtons = QFrame(MplNavButtons)
        self.mplFigureButtons.setObjectName(u"mplFigureButtons")
        self.mplFigureButtons.setGeometry(QRect(0, 0, 361, 60))
        self.mplFigureButtons.setStyleSheet(
            u"QFrame {\n"
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
        self.resetViewButton.setObjectName(u"resetViewButton")
        self.resetViewButton.setGeometry(QRect(30, 10, 40, 40))
        # if QT_CONFIG(tooltip)
        self.resetViewButton.setToolTip(u"Reset plot area")
        # endif // QT_CONFIG(tooltip)
        icon = QIcon()
        icon.addFile(u":/icons/16x16/cil-reload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.resetViewButton.setIcon(icon)
        self.resetViewButton.setIconSize(QSize(24, 24))
        self.panViewButton = QPushButton(self.mplFigureButtons)
        self.panViewButton.setObjectName(u"panViewButton")
        self.panViewButton.setGeometry(QRect(90, 10, 40, 40))
        self.panViewButton.setCursor(QCursor(Qt.ArrowCursor))
        # if QT_CONFIG(tooltip)
        self.panViewButton.setToolTip(u"Pan mode: move plot region by dragging")
        # endif // QT_CONFIG(tooltip)
        icon1 = QIcon()
        icon1.addFile(u":/icons/16x16/cil-move.png", QSize(), QIcon.Normal, QIcon.Off)
        self.panViewButton.setIcon(icon1)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.zoomViewButton = QPushButton(self.mplFigureButtons)
        self.zoomViewButton.setObjectName(u"zoomViewButton")
        self.zoomViewButton.setGeometry(QRect(150, 10, 40, 40))
        self.zoomViewButton.setCursor(QCursor(Qt.ArrowCursor))
        # if QT_CONFIG(tooltip)
        self.zoomViewButton.setToolTip(u"Zoom mode: select a plot region to enlarge")
        # endif // QT_CONFIG(tooltip)
        icon2 = QIcon()
        icon2.addFile(
            u":/icons/16x16/cil-zoom-in.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.zoomViewButton.setIcon(icon2)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.selectViewButton = QPushButton(self.mplFigureButtons)
        self.selectViewButton.setObjectName(u"selectViewButton")
        self.selectViewButton.setGeometry(QRect(210, 10, 41, 41))
        self.selectViewButton.setCursor(QCursor(Qt.CrossCursor))
        # if QT_CONFIG(tooltip)
        self.selectViewButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        icon3 = QIcon()
        icon3.addFile(
            u":/icons/16x16/cil-location-pin.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.selectViewButton.setIcon(icon3)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.swapXYButton = QPushButton(self.mplFigureButtons)
        self.swapXYButton.setObjectName(u"swapXYButton")
        self.swapXYButton.setGeometry(QRect(270, 10, 71, 41))
        self.swapXYButton.setCursor(QCursor(Qt.CrossCursor))
        # if QT_CONFIG(tooltip)
        self.swapXYButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.swapXYButton.setStyleSheet(
            u"QPushButton {\n"
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

        self.retranslateUi(MplNavButtons)

        QMetaObject.connectSlotsByName(MplNavButtons)

    # setupUi

    def retranslateUi(self, MplNavButtons):
        MplNavButtons.setWindowTitle(
            QCoreApplication.translate("MplNavButtons", u"Form", None)
        )
        self.resetViewButton.setText("")
        self.panViewButton.setText("")
        self.zoomViewButton.setText("")
        self.selectViewButton.setText("")
        self.swapXYButton.setText(
            QCoreApplication.translate("MplNavButtons", u"X\u2194Y", None)
        )

    # retranslateUi
