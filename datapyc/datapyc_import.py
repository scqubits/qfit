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


def importFile():
    """
    Opens a standard file dialog box for the user to select a file to be opened. Supported files types are
    - .h5 / .hdf5  (generic h5, Labber, datapyc)
    - .mat (Matlab file)
    - .csv
    - .jpg, .png

    Data is inspected and categorized as data specifying the two axes (xData, yData) and spectroscopy measurement data
    (zData). In the case of a datapyc .h5 file, additional data containing the extracted fit data points as well as
    calibration data is obtained and returned alongside.

    Returns
    -------
    MeasurementData, FitData
    """
    home = os.path.expanduser("~")

    success = False
    while not success:
        fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"
        fileName, fileFilter = QFileDialog.getOpenFileName(None, "Open", home, fileCategories)
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
            _ = msg.exec_()
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