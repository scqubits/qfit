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

from PySide2.QtCore import QSize
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QStyleFactory

from datapyc.core.measureddata_io import readMeasurementData
from datapyc.datapyc_engine import MainWindow



if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily('Segoe UI')
    font.setPointSize(9)
    app.setFont(font)

    # success = False
    # home = os.path.expanduser("~")
    # while not success:
    #     fileName, filter = QFileDialog.getOpenFileName(None, "Open", home,
    #                                                    "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)")
    #     if fileName:
    #         measurementData = readMeasurementData(fileName)
    #         success = measurementData.success
    #     else:
    #         exit()

    # measurementData = readMeasurementData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/00000_twotoneVsPowerTransmission.h5')
    # measurementData = readMeasurementData('C:/Users/drjen/PycharmProjects/DataSelector/scratch/spec_scan_flux_gate_20190629_v05.mat')
    measurementData = readMeasurementData('C:/Users/drjen/Desktop/Spectroscopy.JPEG')
    # measurementData = readMeasurementData(r"C:\Users\drjen\PycharmProjects\datapyc\datapyc\scratch\aug_summary_4_1.hdf5")

    window = MainWindow(measurementData)
    maxSize = QSize(app.desktop().availableGeometry().size())
    window.resizeAndCenter(maxSize)
    window.show()
    sys.exit(app.exec_())
