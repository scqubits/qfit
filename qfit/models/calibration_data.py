# calibration_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

from typing import Dict, List, Optional, Tuple, Union
from typing_extensions import Literal

import numpy as np

from PySide6.QtCore import QObject, Signal, Slot

from qfit.models.registry import Registrable, RegistryEntry


class CombinedMeta(type(QObject), type(Registrable)):
    pass


class CalibrationData(QObject, Registrable, metaclass=CombinedMeta):
    plotCaliOn = Signal(str)
    plotCaliOff = Signal()
    caliClicked = Signal(str, float)

    calibrationIsOn: Literal["CALI_X1", "CALI_X2", "CALI_Y1", "CALI_Y2", False]

    def __init__(
        self,
        rawVec1: Tuple[float, float] = (0.0, 0.0),
        rawVec2: Tuple[float, float] = (1.0, 1.0),
        mapVec1: Tuple[float, float] = (0.0, 0.0),
        mapVec2: Tuple[float, float] = (1.0, 1.0),
    ):
        """
        Store calibration data for x and y axes, and provide methods to transform between uncalibrated and calibrated
        data.

        Parameters
        ----------
        rawVec1, rawVec2, mapVec1, mapVec2: ndarray
            Each of these is a two component vector (x,y) marking a point. The calibration maps rawVec1 -> mapVec1,
            rawVec2 -> mapVec2 with an affine-linear transformation:   mapVecN = alphaMat . rawVecN + bVec.
        """
        super().__init__()
        self.rawVec1 = rawVec1
        self.rawVec2 = rawVec2
        self.mapVec1 = mapVec1
        self.mapVec2 = mapVec2
        self.bVec = None
        self.alphaMat = None

        if rawVec1 and rawVec2 and mapVec1 and mapVec2:
            self.setCalibration(rawVec1, rawVec2, mapVec1, mapVec2)
        else:
            self.resetCalibration()
        self.applyCalibration = False

        self.calibrationIsOn = False

    def resetCalibration(self):
        self.setCalibration((0.0, 0.0), (1.0, 1.0), (0.0, 0.0), (1.0, 1.0))
        self.applyCalibration = False

    def toggleCalibration(self):
        self.applyCalibration = not self.applyCalibration

    def calibrationOn(self, label):
        self.calibrationIsOn = label
        self.plotCaliOn.emit(label)

    def calibrationOff(self):
        self.calibrationIsOn = False
        self.plotCaliOff.emit()

    def acceptCalibration(self, label: Literal[
        "CALI_X1", "CALI_X2", "CALI_Y1", "CALI_Y2"
    ], data):
        """
        Called by the canvas click event to accept the calibration data.
        """
        if label == "CALI_X1":
            self.rawVec1 = (data, self.rawVec1[1])
        elif label == "CALI_X2":
            self.rawVec1 = (self.rawVec1[0], data)
        elif label == "CALI_Y1":
            self.rawVec2 = (data, self.rawVec2[1])
        elif label == "CALI_Y2":
            self.rawVec2 = (self.rawVec2[0], data)
        
        self.calibrationOff()
        self.caliClicked.emit(label, data)  # update the calibration view

    def setCalibration(
        self,
        rVec1: Tuple[float, float],
        rVec2: Tuple[float, float],
        mVec1: Tuple[float, float],
        mVec2: Tuple[float, float],
    ):
        x1, y1 = rVec1
        x2, y2 = rVec2
        x1p, y1p = mVec1
        x2p, y2p = mVec2

        alphaX = (x1p - x2p) / (x1 - x2)
        alphaY = (y1p - y2p) / (y1 - y2)

        self.bVec = np.asarray([x1p - alphaX * x1, y1p - alphaY * y1])
        self.alphaMat = np.asarray([[alphaX, 0.0], [0.0, alphaY]])
        self.rawVec1, self.rawVec2, self.mapVec1, self.mapVec2 = (
            rVec1,
            rVec2,
            mVec1,
            mVec2,
        )

    def allCalibrationVecs(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        return self.rawVec1, self.rawVec2, self.mapVec1, self.mapVec2

    def calibrateDataset(
        self,
        array: np.ndarray,
        calibration_axis: Literal["xy", "x", "y"] = "xy",
    ):
        return np.apply_along_axis(
            self.calibrateDataPoint,
            axis=0,
            arr=array,
            **{"calibration_axis": calibration_axis},
        )

    def inverseCalibrateDataset(
        self,
        array: np.ndarray,
        inverse_calibration_axis: Literal["xy", "x", "y"] = "xy",
    ):
        return np.apply_along_axis(
            self.inverseCalibrateDataPoint,
            axis=0,
            arr=array,
            **{"inverse_calibration_axis": inverse_calibration_axis},
        )

    def calibrateDataPoint(
        self,
        rawVec: Union[List[float], np.ndarray],
        calibration_axis: Literal["xy", "x", "y"] = "xy",
    ) -> np.ndarray:
        """
        Apply the calibration to a single (or multiple) data point(s). The form of the rawVec can be either a
        list [x,y] or a list of [x,y] coordinates.

        Parameters
        ----------
        rawVec: list or ndarray
            A single data point or a list of data points. Each data point is a list of two floats [x,y].

        Returns
        -------
        mVec: ndarray
            The calibrated data point(s). If rawVec is a list of data points, mVec is a list of calibrated data points.
        """
        if isinstance(rawVec, list):
            rawVec = np.asarray(rawVec)
        mVec = np.matmul(self.alphaMat, rawVec) + self.bVec
        # set the x- or y-data to be the uncalibrated one, depending on calibration_axis
        if calibration_axis == "x":
            mVec[..., 1] = rawVec[..., 1]
        elif calibration_axis == "y":
            mVec[..., 0] = rawVec[..., 0]
        return mVec

    def inverseCalibrateDataPoint(
        self,
        mapVec: Union[List[float], np.ndarray],
        inverse_calibration_axis: Literal["xy", "x", "y"] = "xy",
    ) -> np.ndarray:
        """
        Apply the inverse calibration to a single (or multiple) data point(s) that are in the calibrated units.
        The form of the mapVec can be either a list [x,y] or a list of [x,y] coordinates.

        Parameters
        ----------
        mapVec: list or ndarray
            A single calibrated data point or a list of calibrated data points. Each calibrated data point is a list
            of two floats [x,y].

        Returns
        -------
        rawVec: ndarray
            The uncalibrated data point(s). If mapVec is a list of calibrated data points, rawVec is a list of
            uncalibrated data points.
        """
        if isinstance(mapVec, list):
            mapVec = np.asarray(mapVec)
        rawVec = np.matmul(np.linalg.inv(self.alphaMat), mapVec - self.bVec)
        if inverse_calibration_axis == "x":
            rawVec[..., 1] = mapVec[..., 1]
        elif inverse_calibration_axis == "y":
            rawVec[..., 0] = mapVec[..., 0]
        return rawVec

    def adaptiveConversionFunc(self) -> callable:
        if not self.applyCalibration:
            return lambda vec: vec
        return self.calibrateDataPoint

    def registerAll(self) -> Dict[str, RegistryEntry]:
        def setter(initdata):
            # set calibration data
            self.setCalibration(
                initdata[0],
                initdata[1],
                initdata[2],
                initdata[3],
            )

        def getter():
            return self.allCalibrationVecs()

        registry_entry = RegistryEntry(
            name="CalibrationData",
            quantity_type="r+",
            getter=getter,
            setter=setter,
        )
        registry = {"CalibrationData": registry_entry}
        return registry
