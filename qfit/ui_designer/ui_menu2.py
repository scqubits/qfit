# -*- coding: utf-8 -*-

# Form implementation generated from reading ui_designer file '.\menu2.ui_designer',
# licensing of '.\menu2.ui_designer' applies.
#
# Created: Thu Aug 19 06:28:23 2021
#      by: pyside2-uic  running on PySide6 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        MenuWidget.setObjectName("MenuWidget")
        MenuWidget.resize(198, 689)
        MenuWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        MenuWidget.setStyleSheet(
            "QWidget {\n"
            "    background-color: black;\n"
            "    color: white;\n"
            "    text-align: left;\n"
            '    font: 57 11pt "Roboto Medium";\n'
            "    border: none;\n"
            "}"
        )
        self.verticalLayout = QtWidgets.QVBoxLayout(MenuWidget)
        self.verticalLayout.setContentsMargins(14, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.menuFrame = QtWidgets.QFrame(MenuWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFrame.sizePolicy().hasHeightForWidth())
        self.menuFrame.setSizePolicy(sizePolicy)
        self.menuFrame.setMinimumSize(QtCore.QSize(180, 600))
        self.menuFrame.setMaximumSize(QtCore.QSize(180, 700))
        self.menuFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menuFrame.setObjectName("menuFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.menuFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.modeSelectButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.modeSelectButton.sizePolicy().hasHeightForWidth()
        )
        self.modeSelectButton.setSizePolicy(sizePolicy)
        self.modeSelectButton.setMinimumSize(QtCore.QSize(180, 70))
        self.modeSelectButton.setMaximumSize(QtCore.QSize(180, 70))
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/24x24/cil-location-pin.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.modeSelectButton.setIcon(icon)
        self.modeSelectButton.setIconSize(QtCore.QSize(24, 24))
        self.modeSelectButton.setCheckable(True)
        self.modeSelectButton.setChecked(True)
        self.modeSelectButton.setAutoExclusive(True)
        self.modeSelectButton.setObjectName("modeSelectButton")
        self.verticalLayout_2.addWidget(self.modeSelectButton)
        self.modeTagButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.modeTagButton.sizePolicy().hasHeightForWidth()
        )
        self.modeTagButton.setSizePolicy(sizePolicy)
        self.modeTagButton.setMinimumSize(QtCore.QSize(180, 70))
        self.modeTagButton.setMaximumSize(QtCore.QSize(180, 70))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/24x24/cil-list.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.modeTagButton.setIcon(icon1)
        self.modeTagButton.setIconSize(QtCore.QSize(24, 24))
        self.modeTagButton.setCheckable(True)
        self.modeTagButton.setAutoExclusive(True)
        self.modeTagButton.setObjectName("modeTagButton")
        self.verticalLayout_2.addWidget(self.modeTagButton)
        self.modePlotButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.modePlotButton.sizePolicy().hasHeightForWidth()
        )
        self.modePlotButton.setSizePolicy(sizePolicy)
        self.modePlotButton.setMinimumSize(QtCore.QSize(180, 70))
        self.modePlotButton.setMaximumSize(QtCore.QSize(180, 70))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/24x24/cil-chart-line.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.modePlotButton.setIcon(icon2)
        self.modePlotButton.setIconSize(QtCore.QSize(24, 24))
        self.modePlotButton.setCheckable(True)
        self.modePlotButton.setAutoExclusive(True)
        self.modePlotButton.setObjectName("modePlotButton")
        self.verticalLayout_2.addWidget(self.modePlotButton)
        self.modeFitButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.modeFitButton.sizePolicy().hasHeightForWidth()
        )
        self.modeFitButton.setSizePolicy(sizePolicy)
        self.modeFitButton.setMinimumSize(QtCore.QSize(180, 70))
        self.modeFitButton.setMaximumSize(QtCore.QSize(180, 70))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/24x24/cil-speedometer.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.modeFitButton.setIcon(icon3)
        self.modeFitButton.setIconSize(QtCore.QSize(24, 24))
        self.modeFitButton.setCheckable(True)
        self.modeFitButton.setAutoExclusive(True)
        self.modeFitButton.setObjectName("modeFitButton")
        self.verticalLayout_2.addWidget(self.modeFitButton)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.line = QtWidgets.QFrame(self.menuFrame)
        self.line.setStyleSheet("background-color: white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.menuOpenButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuOpenButton.sizePolicy().hasHeightForWidth()
        )
        self.menuOpenButton.setSizePolicy(sizePolicy)
        self.menuOpenButton.setMinimumSize(QtCore.QSize(180, 70))
        self.menuOpenButton.setMaximumSize(QtCore.QSize(180, 70))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuOpenButton.setFont(font)
        self.menuOpenButton.setStyleSheet("t")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/16x16/cil-folder-open.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.menuOpenButton.setIcon(icon4)
        self.menuOpenButton.setObjectName("menuOpenButton")
        self.verticalLayout_2.addWidget(self.menuOpenButton)
        self.menuNewButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuNewButton.sizePolicy().hasHeightForWidth()
        )
        self.menuNewButton.setSizePolicy(sizePolicy)
        self.menuNewButton.setMinimumSize(QtCore.QSize(180, 70))
        self.menuNewButton.setMaximumSize(QtCore.QSize(180, 70))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuNewButton.setFont(font)
        self.menuNewButton.setStyleSheet("t")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/20x20/cil-plus.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.menuNewButton.setIcon(icon5)
        self.menuNewButton.setObjectName("menuNewButton")
        self.verticalLayout_2.addWidget(self.menuNewButton)
        self.menuSaveButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuSaveButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveButton.setSizePolicy(sizePolicy)
        self.menuSaveButton.setMinimumSize(QtCore.QSize(180, 70))
        self.menuSaveButton.setMaximumSize(QtCore.QSize(180, 70))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuSaveButton.setFont(font)
        self.menuSaveButton.setStyleSheet("t")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/16x16/cil-file.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.menuSaveButton.setIcon(icon6)
        self.menuSaveButton.setObjectName("menuSaveButton")
        self.verticalLayout_2.addWidget(self.menuSaveButton)
        self.menuSaveAsButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuSaveAsButton.sizePolicy().hasHeightForWidth()
        )
        self.menuSaveAsButton.setSizePolicy(sizePolicy)
        self.menuSaveAsButton.setMinimumSize(QtCore.QSize(180, 70))
        self.menuSaveAsButton.setMaximumSize(QtCore.QSize(180, 70))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuSaveAsButton.setFont(font)
        self.menuSaveAsButton.setStyleSheet("t")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/16x16/cil-save.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.menuSaveAsButton.setIcon(icon7)
        self.menuSaveAsButton.setObjectName("menuSaveAsButton")
        self.verticalLayout_2.addWidget(self.menuSaveAsButton)
        self.menuQuitButton = QtWidgets.QPushButton(self.menuFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.menuQuitButton.sizePolicy().hasHeightForWidth()
        )
        self.menuQuitButton.setSizePolicy(sizePolicy)
        self.menuQuitButton.setMinimumSize(QtCore.QSize(180, 70))
        self.menuQuitButton.setMaximumSize(QtCore.QSize(180, 70))
        font = QtGui.QFont()
        font.setFamily("Roboto Medium")
        font.setPointSize(11)
        font.setWeight(QFont.Light)
        font.setItalic(False)
        font.setBold(False)
        self.menuQuitButton.setFont(font)
        self.menuQuitButton.setStyleSheet("t")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/16x16/cil-power-standby.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.menuQuitButton.setIcon(icon8)
        self.menuQuitButton.setObjectName("menuQuitButton")
        self.verticalLayout_2.addWidget(self.menuQuitButton)
        self.verticalLayout.addWidget(self.menuFrame)

        self.retranslateUi(MenuWidget)
        QtCore.QMetaObject.connectSlotsByName(MenuWidget)

    def retranslateUi(self, MenuWidget):
        MenuWidget.setWindowTitle(
            QtWidgets.QApplication.translate("MenuWidget", "Form", None, -1)
        )
        self.modeSelectButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   SELECT DATA", None, -1)
        )
        self.modeTagButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   TAG DATA", None, -1)
        )
        self.modePlotButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   PRE-FITTING", None, -1)
        )
        self.modeFitButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   FITTING", None, -1)
        )
        self.menuOpenButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   OPEN", None, -1)
        )
        self.menuNewButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   NEW", None, -1)
        )
        self.menuSaveButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   SAVE", None, -1)
        )
        self.menuSaveAsButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   SAVE AS", None, -1)
        )
        self.menuQuitButton.setText(
            QtWidgets.QApplication.translate("MenuWidget", "   QUIT", None, -1)
        )


import resources_rc