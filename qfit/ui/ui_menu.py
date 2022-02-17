# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\menu.ui',
# licensing of '.\menu.ui' applies.
#
# Created: Thu Aug 19 07:06:14 2021
#      by: pyside2-uic  running on PySide6 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QFont

import qfit.ui.resources_rc


class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        MenuWidget.setObjectName("MenuWidget")
        MenuWidget.resize(225, 300)
        self.menuFrame = QtWidgets.QFrame(MenuWidget)
        self.menuFrame.setEnabled(True)
        self.menuFrame.setGeometry(QtCore.QRect(0, 0, 225, 300))
        self.menuFrame.setMinimumSize(QtCore.QSize(225, 300))
        self.menuFrame.setMaximumSize(QtCore.QSize(225, 300))
        self.menuFrame.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menuFrame.setAutoFillBackground(False)
        self.menuFrame.setStyleSheet(
            "QFrame {\n"
            "    background-color: rgb(18, 18, 18);\n"
            "}\n"
            "\n"
            "QPushButton {    \n"
            '    font: 57 11pt "Roboto Medium";\n'
            "    color: rgb(249, 249, 249);\n"
            "    background-color: rgb(18, 18, 18);\n"
            "    border: none;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(52, 59, 72);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(85, 170, 255);\n"
            "}\n"
            "\n"
            "QPushButton:checked {\n"
            "    border: 5px;\n"
            "    border-color: rgb(6, 50, 250);\n"
            "    border-right-style: inset;\n"
            "}"
        )
        self.menuFrame.setObjectName("menuFrame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.menuFrame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.menuOpenButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuOpenButton.sizePolicy().hasHeightForWidth()
        )
        self.menuOpenButton.setSizePolicy(sizePolicy)
        self.menuOpenButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuOpenButton.setFont(font)
        self.menuOpenButton.setObjectName("menuOpenButton")
        self.verticalLayout_8.addWidget(self.menuOpenButton)
        self.menuNewButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuNewButton.sizePolicy().hasHeightForWidth()
        )
        self.menuNewButton.setSizePolicy(sizePolicy)
        self.menuNewButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuNewButton.setFont(font)
        self.menuNewButton.setObjectName("menuNewButton")
        self.verticalLayout_8.addWidget(self.menuNewButton)
        self.menuSaveButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuSaveButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveButton.setSizePolicy(sizePolicy)
        self.menuSaveButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuSaveButton.setFont(font)
        self.menuSaveButton.setObjectName("menuSaveButton")
        self.verticalLayout_8.addWidget(self.menuSaveButton)
        self.menuSaveAsButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuSaveAsButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveAsButton.setSizePolicy(sizePolicy)
        self.menuSaveAsButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuSaveAsButton.setFont(font)
        self.menuSaveAsButton.setObjectName("menuSaveAsButton")
        self.verticalLayout_8.addWidget(self.menuSaveAsButton)
        self.menuQuitButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuQuitButton.sizePolicy().hasHeightForWidth()
        )
        self.menuQuitButton.setSizePolicy(sizePolicy)
        self.menuQuitButton.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuQuitButton.setFont(font)
        self.menuQuitButton.setObjectName("menuQuitButton")
        self.verticalLayout_8.addWidget(self.menuQuitButton)

        self.retranslateUi(MenuWidget)
        QtCore.QMetaObject.connectSlotsByName(MenuWidget)

    def retranslateUi(self, MenuWidget):
        MenuWidget.setWindowTitle(
            QtWidgets.QApplication.translate("MenuWidget", "Form", None, -1)
        )
        self.menuOpenButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "OPEN", None, -1)
        )
        self.menuNewButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "NEW", None, -1)
        )
        self.menuSaveButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "SAVE", None, -1)
        )
        self.menuSaveAsButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "SAVE AS", None, -1)
        )
        self.menuQuitButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "QUIT", None, -1)
        )
