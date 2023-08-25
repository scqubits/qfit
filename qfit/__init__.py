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

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

import matplotlib

matplotlib.use("qtagg")

from qfit.core.mainwindow import MainWindow
from qfit.models.measurement_data import dummy_measurement_data
from qfit.controllers.numerical_model import test_hilbert_space


def qfit():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app = QApplication.instance()
    QFontDatabase.addApplicationFont(":/fonts/Roboto-Regular.ttf")
    font = QFontDatabase.font("Roboto", "", 10)
    font.setWeight(QFont.Normal)
    app.setFont(font)

    window = MainWindow(
        measurementData=dummy_measurement_data(),
        hilbert_space=test_hilbert_space(),
        extractedData=None,
    )

    window.show()
    window.openFile(initialize=True)
