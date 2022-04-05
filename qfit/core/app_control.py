# app_control.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

from enum import Enum, auto, unique

from PySide6 import QtCore
from PySide6.QtCore import Signal

from qfit.core.data_structures import Database


@unique
class State(Enum):
    SELECT = auto()
    ZOOM = auto()
    PAN = auto()
    CALIBRATE_X1 = auto()
    CALIBRATE_X2 = auto()
    CALIBRATE_Y1 = auto()
    CALIBRATE_Y2 = auto()


class ApplicationCentral(QtCore.QObject):
    state = State.SELECT
    updatePlotSignal = Signal()

    def __init__(self):
        self.canvas = None
        self.allDatasetsView = None
        self.allDatasetsModel = None
        self.currentDatasetView = None
        self.currentDatasetModel = None
        self.tagDatasetView = None
        self.tagDatasetModel = None
        self.calibrationDataView = None
        self.calibrationDataModel = None

    def initialize(self,
                   canvas,
                   allDatasetsView,
                   allDatasetsModel,
                   currentDatasetView,
                   currentDatasetModel,
                   tagDatasetView,
                   tagDatasetModel,
                   calibrationDataView,
                   calibrationDataModel):
        self.canvas = canvas
        self.allDatasetsView = allDatasetsView
        self.allDatasetsModel = allDatasetsModel
        self.currentDatasetView = currentDatasetView
        self.currentDatasetModel = currentDatasetModel
        self.tagDatasetView = tagDatasetView
        self.tagDatasetModel = tagDatasetModel
        self.calibrationDataView = calibrationDataView
        self.calibrationDataModel = calibrationDataModel

        self.updatePlotSignal.connect(self.canvas.updatePlot)


CENTRAL = ApplicationCentral()
DATA = Database()
