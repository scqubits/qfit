# __main__.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import sys

import PySide2.QtCore

from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication

from datapyc.core.mainwindow import MainWindow
from datapyc.data.measurement_data import dummy_measurement_data
from datapyc.io_utils.import_data import importFile

if hasattr(PySide2.QtCore.Qt, "AA_EnableHighDpiScaling"):
    PySide2.QtWidgets.QApplication.setAttribute(
        PySide2.QtCore.Qt.AA_EnableHighDpiScaling, True
    )

if hasattr(PySide2.QtCore.Qt, "AA_UseHighDpiPixmaps"):
    PySide2.QtWidgets.QApplication.setAttribute(
        PySide2.QtCore.Qt.AA_UseHighDpiPixmaps, True
    )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("Roboto Medium")
    font.setPointSize(9)
    app.setFont(font)


    # fileData = readFileData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/00000_twotoneVsPowerTransmission.h5')
    # fileData = readFileData('C:/Users/drjen/Desktop/Spectroscopy.JPEG')
    # fileData = readFileData(r"C:\Users\drjen\PycharmProjects\datapyc\datapyc\scratch\aug_summary_4_1.hdf5")
    window = MainWindow(measurementData=dummy_measurement_data(),
                            extractedData=None)
    maxSize = QSize(app.primaryScreen().availableGeometry().size())
    window.resizeAndCenter(maxSize)
    window.show()
    window.openFile(initialize=True)
    sys.exit(app.exec_())