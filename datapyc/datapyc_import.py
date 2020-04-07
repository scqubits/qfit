# datapyc_import.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import os

from PySide2.QtWidgets import QFileDialog, QMessageBox

import scqubits.utils.fitting as fit

from datapyc.core.inputdata_io import readFileData, ImageMeasurementData, NumericalMeasurementData
from datapyc.core.misc import OrderedDictMod


def importFile():
    home = os.path.expanduser("~")

    success = False
    while not success:
        fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"
        fileName, filter = QFileDialog.getOpenFileName(None, "Open", home, fileCategories)
        if not fileName:
            exit()

        fileData = readFileData(fileName)

        if fileData is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error opening file.")
            msg.setInformativeText("The selected file format is supported, but heuristic inspection "
                                   "failed to identify suitable data inside the file.")
            msg.setWindowTitle("Error")
            returnVal = msg.exec_()
        else:
            success = True

    if isinstance(fileData, fit.FitData):
        extractedData = fileData
        if fileData.image_data is not None:
            measurementData = ImageMeasurementData('image_data', fileData.image_data)

        else:
            measurementData = NumericalMeasurementData({'xData': fileData.x_data,
                                                        'yData': fileData.y_data,
                                                        'zData': fileData.z_data},
                                                       {'zData': fileData.z_data})
    else:
        measurementData = fileData
        extractedData = None

    return measurementData, extractedData
