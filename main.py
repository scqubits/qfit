# main.py
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
import os

from PySide2.QtCore import QSize
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QFileDialog, QMessageBox

from datapyc.core.inputdata_io import readFileData
from datapyc.datapyc_mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily('Segoe UI')
    font.setPointSize(9)
    app.setFont(font)

    success = False
    home = os.path.expanduser("~")
    while not success:
        fileName, filter = QFileDialog.getOpenFileName(None, "Open", home,
                                                       "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)")
        if fileName:
            fileData = readFileData(fileName)
            success = fileData is not None
            if not success:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Error opening file.")
                msg.setInformativeText("The selected file format is supported, but heuristic inspection "
                                       "failed to identify suitable data inside the file.")
                msg.setWindowTitle("Error")
                returnVal = msg.exec_()
        else:
            exit()

    # fileData = readFileData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/00000_twotoneVsPowerTransmission.h5')
    # fileData = readFileData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/spec_scan_flux_gate_20190629_v05.mat')
    # fileData = readFileData('C:/Users/drjen/Desktop/Spectroscopy.JPEG')
    # fileData = readFileData(r"C:\Users\drjen\PycharmProjects\datapyc\datapyc\scratch\aug_summary_4_1.hdf5")

    window = MainWindow(fileData)
    maxSize = QSize(app.desktop().availableGeometry().size())
    window.resizeAndCenter(maxSize)
    window.show()
    sys.exit(app.exec_())
