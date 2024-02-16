# import_data.py
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

from PySide6.QtWidgets import QFileDialog, QMessageBox

from qfit.utils.helpers import StopExecution

from qfit.models.measurement_data import (
    ImageMeasurementData,
    NumericalMeasurementData,
)
from qfit.io_utils.measurement_file_readers import readMeasurementFile
from qfit.models.registry import Registry

from typing import Union

def importMeasurementData(
    parent,
    home = None,
) -> Union[ImageMeasurementData, NumericalMeasurementData]:
    if home is None:
        home = os.path.expanduser("~")

    while True:
        fileCategories = "Data files (*.h5 *.mat *.csv *.jpg *.jpeg *.png *.hdf5)"
        fileName, _ = QFileDialog.getOpenFileName(parent, "Open", home, fileCategories)
        if not fileName:
            parent.closeApp()
            raise StopExecution

        try:
            fileData = readMeasurementFile(fileName)
        except NotImplementedError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error opening file.")
            msg.setInformativeText(
                "The selected file format is not supported. Because: " + str(e)
            )
            msg.setWindowTitle("Error")
            _ = msg.exec_()
            continue
        except (ValueError, OSError, Exception) as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error opening file.")
            msg.setInformativeText(
                "The selected file format is supported, but heuristic inspection "
                "failed to identify suitable data inside the file."
            )
            msg.setWindowTitle("Error")
            _ = msg.exec_()
        else:
            break

    return fileData

def importProject(
    parent,
    home = None,
) -> Registry:
    if home is None:
        home = os.path.expanduser("~")

    while True:
        fileCategories = "Qfit project (*.qfit)"
        fileName, _ = QFileDialog.getOpenFileName(parent, "Open", home, fileCategories)
        if not fileName:
            parent.closeApp()
            raise StopExecution

        registry = Registry.fromFile(fileName)

        if registry is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error opening file.")
            msg.setInformativeText(
                "File is not found."
            )
            msg.setWindowTitle("Error")
            _ = msg.exec_()
        else:
            break

    return registry
