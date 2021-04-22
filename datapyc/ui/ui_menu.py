# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        if not MenuWidget.objectName():
            MenuWidget.setObjectName(u"MenuWidget")
        MenuWidget.resize(225, 300)
        self.menuFrame = QFrame(MenuWidget)
        self.menuFrame.setObjectName(u"menuFrame")
        self.menuFrame.setEnabled(True)
        self.menuFrame.setGeometry(QRect(0, 0, 225, 300))
        self.menuFrame.setMinimumSize(QSize(225, 300))
        self.menuFrame.setMaximumSize(QSize(225, 300))
        self.menuFrame.setFocusPolicy(Qt.NoFocus)
        self.menuFrame.setAutoFillBackground(False)
        self.menuFrame.setStyleSheet(u"background-color: rgb(18, 18, 18);")
        self.verticalLayout_8 = QVBoxLayout(self.menuFrame)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.menuOpenButton = QPushButton(self.menuFrame)
        self.menuOpenButton.setObjectName(u"menuOpenButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuOpenButton.sizePolicy().hasHeightForWidth()
        )
        self.menuOpenButton.setSizePolicy(sizePolicy)
        self.menuOpenButton.setMinimumSize(QSize(0, 40))
        font = QFont()
        font.setFamily(u"Roboto")
        font.setPointSize(10)
        self.menuOpenButton.setFont(font)
        self.menuOpenButton.setStyleSheet(
            u"QPushButton {	\n"
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

        self.verticalLayout_8.addWidget(self.menuOpenButton)

        self.menuNewButton = QPushButton(self.menuFrame)
        self.menuNewButton.setObjectName(u"menuNewButton")
        sizePolicy.setHeightForWidth(
            self.menuNewButton.sizePolicy().hasHeightForWidth()
        )
        self.menuNewButton.setSizePolicy(sizePolicy)
        self.menuNewButton.setMinimumSize(QSize(0, 40))
        self.menuNewButton.setFont(font)
        self.menuNewButton.setStyleSheet(
            u"QPushButton {	\n"
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

        self.verticalLayout_8.addWidget(self.menuNewButton)

        self.menuSaveButton = QPushButton(self.menuFrame)
        self.menuSaveButton.setObjectName(u"menuSaveButton")
        sizePolicy.setHeightForWidth(
            self.menuSaveButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveButton.setSizePolicy(sizePolicy)
        self.menuSaveButton.setMinimumSize(QSize(0, 40))
        self.menuSaveButton.setFont(font)
        self.menuSaveButton.setStyleSheet(
            u"QPushButton {	\n"
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

        self.verticalLayout_8.addWidget(self.menuSaveButton)

        self.menuSaveAsButton = QPushButton(self.menuFrame)
        self.menuSaveAsButton.setObjectName(u"menuSaveAsButton")
        sizePolicy.setHeightForWidth(
            self.menuSaveAsButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveAsButton.setSizePolicy(sizePolicy)
        self.menuSaveAsButton.setMinimumSize(QSize(0, 40))
        self.menuSaveAsButton.setFont(font)
        self.menuSaveAsButton.setStyleSheet(
            u"QPushButton {	\n"
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

        self.verticalLayout_8.addWidget(self.menuSaveAsButton)

        self.menuQuitButton = QPushButton(self.menuFrame)
        self.menuQuitButton.setObjectName(u"menuQuitButton")
        sizePolicy.setHeightForWidth(
            self.menuQuitButton.sizePolicy().hasHeightForWidth()
        )
        self.menuQuitButton.setSizePolicy(sizePolicy)
        self.menuQuitButton.setMinimumSize(QSize(0, 40))
        self.menuQuitButton.setFont(font)
        self.menuQuitButton.setStyleSheet(
            u"QPushButton {	\n"
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

        self.verticalLayout_8.addWidget(self.menuQuitButton)

        self.retranslateUi(MenuWidget)

        QMetaObject.connectSlotsByName(MenuWidget)

    # setupUi

    def retranslateUi(self, MenuWidget):
        MenuWidget.setWindowTitle(
            QCoreApplication.translate("MenuWidget", u"Form", None)
        )
        self.menuOpenButton.setText(
            QCoreApplication.translate("MenuWidget", u"OPEN", None)
        )
        self.menuNewButton.setText(
            QCoreApplication.translate("MenuWidget", u"NEW", None)
        )
        self.menuSaveButton.setText(
            QCoreApplication.translate("MenuWidget", u"SAVE", None)
        )
        self.menuSaveAsButton.setText(
            QCoreApplication.translate("MenuWidget", u"SAVE AS", None)
        )
        self.menuQuitButton.setText(
            QCoreApplication.translate("MenuWidget", u"QUIT", None)
        )

    # retranslateUi
