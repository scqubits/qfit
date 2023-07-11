# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_menu3.ui'
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
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        if not MenuWidget.objectName():
            MenuWidget.setObjectName("MenuWidget")
        MenuWidget.resize(211, 389)
        MenuWidget.setAutoFillBackground(True)
        MenuWidget.setStyleSheet(
            "QWidget {\n"
            "	background-color: rgb(18, 18, 18);\n"
            "}\n"
            "\n"
            "QPushButton {	\n"
            '	font: 57 11pt "Roboto Medium";\n'
            "	color: rgb(249, 249, 249);\n"
            "	background-color: rgb(18, 18, 18);\n"
            "	border: none;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(85, 170, 255);\n"
            "}\n"
            "\n"
            "QPushButton:checked {\n"
            "	border: 5px;\n"
            "	border-color: rgb(6, 50, 250);\n"
            "	border-right-style: inset;\n"
            "}"
        )
        self.verticalLayout = QVBoxLayout(MenuWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.menuNewButton = QPushButton(MenuWidget)
        self.menuNewButton.setObjectName("menuNewButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuNewButton.sizePolicy().hasHeightForWidth()
        )
        self.menuNewButton.setSizePolicy(sizePolicy)
        self.menuNewButton.setMinimumSize(QSize(0, 45))
        self.menuNewButton.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setFamilies(["Roboto Medium"])
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.menuNewButton.setFont(font)

        self.verticalLayout.addWidget(self.menuNewButton)

        self.menuOpenButton = QPushButton(MenuWidget)
        self.menuOpenButton.setObjectName("menuOpenButton")
        sizePolicy.setHeightForWidth(
            self.menuOpenButton.sizePolicy().hasHeightForWidth()
        )
        self.menuOpenButton.setSizePolicy(sizePolicy)
        self.menuOpenButton.setMinimumSize(QSize(0, 45))
        self.menuOpenButton.setMaximumSize(QSize(16777215, 50))
        self.menuOpenButton.setFont(font)

        self.verticalLayout.addWidget(self.menuOpenButton)

        self.menuSaveButton = QPushButton(MenuWidget)
        self.menuSaveButton.setObjectName("menuSaveButton")
        sizePolicy.setHeightForWidth(
            self.menuSaveButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveButton.setSizePolicy(sizePolicy)
        self.menuSaveButton.setMinimumSize(QSize(0, 45))
        self.menuSaveButton.setMaximumSize(QSize(16777215, 50))
        self.menuSaveButton.setFont(font)

        self.verticalLayout.addWidget(self.menuSaveButton)

        self.menuSaveAsButton = QPushButton(MenuWidget)
        self.menuSaveAsButton.setObjectName("menuSaveAsButton")
        sizePolicy.setHeightForWidth(
            self.menuSaveAsButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveAsButton.setSizePolicy(sizePolicy)
        self.menuSaveAsButton.setMinimumSize(QSize(0, 45))
        self.menuSaveAsButton.setMaximumSize(QSize(16777215, 50))
        self.menuSaveAsButton.setFont(font)

        self.verticalLayout.addWidget(self.menuSaveAsButton)

        self.menuQuitButton = QPushButton(MenuWidget)
        self.menuQuitButton.setObjectName("menuQuitButton")
        sizePolicy.setHeightForWidth(
            self.menuQuitButton.sizePolicy().hasHeightForWidth()
        )
        self.menuQuitButton.setSizePolicy(sizePolicy)
        self.menuQuitButton.setMinimumSize(QSize(0, 45))
        self.menuQuitButton.setMaximumSize(QSize(16777215, 50))
        self.menuQuitButton.setFont(font)

        self.verticalLayout.addWidget(self.menuQuitButton)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.retranslateUi(MenuWidget)

        QMetaObject.connectSlotsByName(MenuWidget)

    # setupUi

    def retranslateUi(self, MenuWidget):
        MenuWidget.setWindowTitle("")
        self.menuNewButton.setText(
            QCoreApplication.translate("MenuWidget", "NEW", None)
        )
        self.menuOpenButton.setText(
            QCoreApplication.translate("MenuWidget", "OPEN", None)
        )
        self.menuSaveButton.setText(
            QCoreApplication.translate("MenuWidget", "SAVE", None)
        )
        self.menuSaveAsButton.setText(
            QCoreApplication.translate("MenuWidget", "SAVE AS", None)
        )
        self.menuQuitButton.setText(
            QCoreApplication.translate("MenuWidget", "QUIT", None)
        )

    # retranslateUi
