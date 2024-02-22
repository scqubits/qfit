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


from PySide6.QtWidgets import QWidget

from qfit.ui_designer.settings_fit import Ui_fitSettingsWidget
from qfit.ui_designer.settings_numerical_spectrum import (
    Ui_numericalSpectrumSettingsWidget,
)
from qfit.ui_designer.settings_visual import Ui_visualSettingsWidget


class FitSettingsWidget(QWidget):
    def __init__(self, parent):
        super(FitSettingsWidget, self).__init__(parent=parent)
        self.mainwindow = parent
        self.ui = Ui_fitSettingsWidget()
        self.ui.setupUi(self)

        self.move(80, 80)
        self.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


class NumericalSpectrumSettingsWidget(QWidget):
    def __init__(self, parent):
        super(NumericalSpectrumSettingsWidget, self).__init__(parent=parent)
        self.mainwindow = parent
        self.ui = Ui_numericalSpectrumSettingsWidget()
        self.ui.setupUi(self)

        self.move(80, 80)
        self.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


class VisualSettingsWidget(QWidget):
    def __init__(self, parent):
        super(VisualSettingsWidget, self).__init__(parent=parent)
        self.mainwindow = parent
        self.ui = Ui_visualSettingsWidget()
        self.ui.setupUi(self)

        self.move(80, 80)
        self.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
