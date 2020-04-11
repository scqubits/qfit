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

from PySide2.QtCore import QSize
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication

from datapyc.io.import_data import importFile
from datapyc.core.mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily('Segoe UI')
    font.setPointSize(9)
    app.setFont(font)

    measurementData, extractedData = importFile()

    # fileData = readFileData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/00000_twotoneVsPowerTransmission.h5')
    # fileData = readFileData('C:/Users/drjen/Desktop/Spectroscopy.JPEG')
    # fileData = readFileData(r"C:\Users\drjen\PycharmProjects\datapyc\datapyc\scratch\aug_summary_4_1.hdf5")

    window = MainWindow(measurementData=measurementData, extractedData=extractedData)
    maxSize = QSize(app.desktop().availableGeometry().size())
    window.resizeAndCenter(maxSize)
    window.show()
    sys.exit(app.exec_())
