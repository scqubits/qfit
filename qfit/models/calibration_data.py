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

from typing import List, Optional, Tuple, Union

import numpy as np

from PySide6.QtCore import QObject

import qfit.io_utils.file_io_serializers as serializers


class CalibrationData(serializers.Serializable):
    def __init__(
        self,
        rawVec1: Optional[np.ndarray] = None,
        rawVec2: Optional[np.ndarray] = None,
        mapVec1: Optional[np.ndarray] = None,
        mapVec2: Optional[np.ndarray] = None,
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

    def resetCalibration(self):
        self.setCalibration((1.0, 0.0), (0.0, 1.0), (1.0, 0.0), (0.0, 1.0))
        self.applyCalibration = False

    def toggleCalibration(self):
        self.applyCalibration = not self.applyCalibration

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
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return self.rawVec1, self.rawVec2, self.mapVec1, self.mapVec2

    def calibrateDataset(self, array: np.ndarray):
        return np.apply_along_axis(self.calibrateDataPoint, axis=0, arr=array)

    def calibrateDataPoint(self, rawVec: Union[List[float], np.ndarray]) -> np.ndarray:
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
        return mVec

    def adaptiveConversionFunc(self) -> callable:
        if not self.applyCalibration:
            return lambda vec: vec
        return self.calibrateDataPoint
