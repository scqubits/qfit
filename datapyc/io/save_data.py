# save_data.py
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

from PySide2.QtWidgets import QFileDialog

import scqubits.utils.fitting as fit
from datapyc.io.io_readers import ImageMeasurementData


def saveFile(parent):
    home = os.path.expanduser("~")
    fileCategories = "scQubits file (*.h5);;Data file (*.csv)"
    fileName, _ = QFileDialog.getSaveFileName(parent, "Save Extracted Data", home, fileCategories)

    if isinstance(parent.measurementData, ImageMeasurementData):
        imageData = parent.measurementData.currentZ.data
    else:
        imageData = None

    fitData = fit.FitData(
        datanames=parent.allDatasetsModel.dataNames,
        datalist=parent.allDatasetsModel.allDataSorted(applyCalibration=True),
        x_data=parent.measurementData.currentX.data,
        y_data=parent.measurementData.currentY.data,
        z_data=parent.measurementData.currentZ.data,
        image_data=imageData,
        calibration_data=parent.calibrationModel
    )
    fitData.filewrite(fileName)