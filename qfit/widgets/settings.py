# menu.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QWidget
from typing import Union, Type

from dataclasses import dataclass

from qfit.ui_designer.settings_fit import Ui_fitSettingsWidget
from qfit.ui_designer.settings_numerical_spectrum import (
    Ui_numericalSpectrumSettingsWidget,
)
from qfit.ui_designer.settings_visual import Ui_visualSettingsWidget
from qfit.ui_designer.settings import Ui_settingsWidget


class SettingsWidgetBase(QWidget):
    """
    Base class for settings widgets.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mainwindow = parent
        self.move(350, 300)
        self.oldPos: Union[None, QPoint] = self.pos()
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


class SettingsWidget(SettingsWidgetBase):
    def __init__(self, parent):
        super(SettingsWidget, self).__init__(parent=parent)
        self.ui = Ui_settingsWidget()
        self.ui.setupUi(self)
