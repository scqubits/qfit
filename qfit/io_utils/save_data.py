# save_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import os

from PySide6.QtWidgets import QFileDialog

import qfit.models.qfit_data as fit

from qfit.io_utils.measurement_file_readers import ImageMeasurementData


def saveFile(parent):
    home = os.path.expanduser("~")
    fileCategories = "scQubits file (*.h5);;Data file (*.csv)"
    fileName, _ = QFileDialog.getSaveFileName(
        parent, "Save Extracted Data", home, fileCategories
    )

    if not fileName:
        return False

    if isinstance(parent.measurementData, ImageMeasurementData):
        imageData = parent.measurementData.currentZ.data
    else:
        imageData = None

    fitData = fit.QfitData(
        datanames=parent.allDatasetsModel.dataNames,
        datalist=parent.allDatasetsModel.allDataSorted(applyCalibration=False),
        x_data=parent.measurementData.currentX.data,
        y_data=parent.measurementData.currentY.data,
        z_data=parent.measurementData.currentZ.data if imageData is None else None,
        image_data=imageData,
        calibration_data=parent.calibrationModel,
        tag_data=parent.allDatasetsModel.assocTagList,
    )
    fitData.filewrite(fileName)
    return True
