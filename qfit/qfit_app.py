# qfit_app.py
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

import PySide6.QtCore

from PySide6.QtCore import QSize
from PySide6.QtGui import QFont, QScreen
from PySide6.QtWidgets import QApplication

import matplotlib

matplotlib.use("qtagg")

from qfit.core.mainwindow import MainWindow
from qfit.models.measurement_data import dummy_measurement_data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("Roboto Medium")
    font.setPointSize(9)
    app.setFont(font)

    # fileData = readFileData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/00000_twotoneVsPowerTransmission.h5')
    # fileData = readFileData('C:/Users/drjen/Desktop/Spectroscopy.JPEG')
    # fileData = readFileData(r"C:\Users\drjen\PycharmProjects\qfit\qfit\scratch\aug_summary_4_1.hdf5")
    window = MainWindow(measurementData=dummy_measurement_data(), extractedData=None)
    # window.resizeAndCenter(maxSize)

    window.show()
    window.openFile(initialize=True)
    sys.exit(app.exec())