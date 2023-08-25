# __init__.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import sys

from copy import deepcopy

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

import matplotlib

matplotlib.use("qtagg")

from qfit.core.mainwindow import MainWindow
from qfit.models.measurement_data import dummy_measurement_data
from qfit.controllers.numerical_model import test_hilbert_space


class qfit:
    def __init__(self, hilbert_space):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        QFontDatabase.addApplicationFont(":/fonts/Roboto-Regular.ttf")
        font = QFontDatabase.font("Roboto", "", 10)
        font.setWeight(QFont.Normal)
        self.app.setFont(font)

        _hilbert_space = deepcopy(hilbert_space)
        self.window = MainWindow(
            measurementData=dummy_measurement_data(),
            hilbert_space=_hilbert_space,
            extractedData=None,
        )

        self.window.show()
        self.window.openFile(initialize=True)
