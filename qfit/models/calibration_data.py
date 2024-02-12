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

from typing import Dict, List, Optional, Tuple, Union, Callable
from typing_extensions import Literal

import numpy as np

from PySide6.QtCore import QObject, Signal, Slot

from qfit.models.registry import Registrable, RegistryEntry

from qfit.models.data_structures import (
    CalibrationRawMapPair,
    CaliTableParam,
    CaliTableRow,
)
from qfit.models.quantum_model_parameters import ParamSet, QMSweepParam


class CombinedMeta(type(QObject), type(Registrable)):
    pass


class CalibrationData(QObject, Registrable, metaclass=CombinedMeta):
    plotCaliOn = Signal(str)
    plotCaliOff = Signal()
    caliClicked = Signal(str, float)

    calibrationIsOn: Literal["CALI_X1", "CALI_X2", "CALI_Y1", "CALI_Y2", False]

    def __init__(
        self,
        rawVecName: List[str],
        figName: List[str],
        sweepParamSet: ParamSet[QMSweepParam],
        rawVec1: Tuple[float, float] = (0.0, 0.0),
        rawVec2: Tuple[float, float] = (1.0, 1.0),
        mapVec1: Tuple[float, float] = (0.0, 0.0),
        mapVec2: Tuple[float, float] = (1.0, 1.0),
    ):
        """
        Store calibration data for x and y axes, and provide methods to transform between uncalibrated and calibrated
        data.

        The transformation is either a complete one, where rawVecX is the experimental parameter (i.e. voltage)
        and mapVecX is the calibrated parameter (i.e. flux or ng). If sufficient number of figures are provided, the
        full relation between the two can be fully determined as follows:
        mapVecX = MMat @ rawVecX + offsetVecX
        assume mapVecX has N components, rawVecX has L components, then MMat is a N x L matrix and offsetVecX is a
        N-component vector. MMat and offsetVecX are determined by providing L+1 pairs of (rawVecX, mapVecX) data points.

        If insufficient number of figures are provided, the calibration is partial. In this case, the calibration
        is done for each figure separately. Assume we have F figures, then for each figure, the relation between the
        rawVecX and mapVecX is:
        rawVecX = rawVecX1 + tX * (rawVecX2 - rawVecX1)
        mapVecX = mapVecX1 + tX * (mapVecX2 - mapVecX1)
        here the rawVecX is the voltage vector in a figure that one wants to calibrate, and mapVecX is the calibrated
        vector. The tX is the parameter that determines the position of the rawVecX in the figure. The calibration
        is done by providing 2 pairs of (rawVecX, mapVecX) data points for each figure.
        When a rawVecX is provided, the tX is first determined by using polyfit, then the mapVecX is determined with the
        formula above.

        The calibration function is supposed to take in rawVecX (and figName if using partial calibration) and return 
        mapVecX. rawVecX is a dictionary of {rawVecName: value} and mapVecX is a sweep parameter set.

        Parameters
        ----------
        rawVec1, rawVec2, mapVec1, mapVec2: ndarray
            Each of these is a two component vector (x,y) marking a point. The calibration maps rawVec1 -> mapVec1,
            rawVec2 -> mapVec2 with an affine-linear transformation:   mapVecN = MMat . rawVecN + bVec.
        """
        super().__init__()
        self.rawVecName = rawVecName
        self.rawVecDim = len(rawVecName)
        self.figName = figName
        self.figNr = len(figName)
        self.sweepParamSet = sweepParamSet
        self.sweepParamNr = len(sweepParamSet)

        # determine total calibration table row number and if the calibration is a complete one
        self.isFullCalibration: bool
        self.caliTableRowNr: int
        self._isSufficientForFullCalibration(self.rawVecDim, self.figNr)

        self.caliTable: List[CaliTableRow]
        self._initializeCaliTable()

        # only used for full calibration
        self.MMat: Optional[np.ndarray] = None
        self.offsetVec: Optional[np.ndarray]= None

        # only used for partial calibration
        self.rawVecX1Dict: Optional[Dict[str, Dict[str, float]]] = None # {figureName: {rawVecName: value}}
        self.rawVecX2Dict: Optional[Dict[str, Dict[str, float]]] = None
        self.mapVecX1Dict: Optional[Dict[str, Dict[str, float]]] = None # {figureName: {rawVecName: value}}
        self.mapVecX2Dict: Optional[Dict[str, Dict[str, float]]] = None

        # self.rawVec1 = rawVec1
        # self.rawVec2 = rawVec2
        # self.mapVec1 = mapVec1
        # self.mapVec2 = mapVec2
        # self.bVec = None
        # self.alphaMat = None

        # if rawVec1 and rawVec2 and mapVec1 and mapVec2:
        #     self.setCalibration(rawVec1, rawVec2, mapVec1, mapVec2)
        # else:
        #     self.resetCalibration()
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
        if self.calibrationIsOn:
            self.calibrationIsOn = False
            self.plotCaliOff.emit()
        else:
            # if the calibration is not on, it's likely triggered by 
            # other events like page change,
            # we should not trigger the plotCaliOff signal in this case 
            pass

    def acceptCalibration(
        self, label: Literal["CALI_X1", "CALI_X2", "CALI_Y1", "CALI_Y2"], data
    ):
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
    ) -> Tuple[
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
        Tuple[float, float],
    ]:
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

    def _isSufficientForFullCalibration(self, rawVecDim: int, figNr: int):
        """
        Determine if the calibration data is sufficient for a full calibration. For a full
        calibration, the number of points required is equal to the number of voltages + 1.
        If we restrict user to select max 2 points in each figure, the minimum number of
        figures required is (voltageNumber+1)/2, round up. However this number does not check
        for the case when the user provides scans for voltages along the same direction.

        Parameters
        ----------
        rawVecDim: int
            The raw vector dimension (number of voltages) used in the scan. Obtained from the two-tone data.
        figNr: int
            The number of figures imported.
        """
        pointsRequired = rawVecDim + 1
        if pointsRequired > figNr * 2:
            self.isFullCalibration = False
            self.caliTableRowNr = figNr * 2
        else:
            self.isFullCalibration = True
            self.caliTableRowNr = pointsRequired

    def rawToMappedX(self, rawVec: np.ndarray, figName: Union[str, None]) -> np.ndarray:
        """
        Map the raw vector to the mapped vector using the calibration data.
        """
        if self.isFullCalibration:
            return self._fullXCalibration(rawVec)
        else:
            if figName is None:
                raise ValueError(
                    "The figure name must be provided for partial calibration."
                )
            return self._partialXCalibration(rawVec, figName)

    def _fullXCalibration(self, rawVec: Dict[str, float]) -> ParamSet[QMSweepParam]:
        """
        Apply the full calibration to the raw vector.
        """

        return self.calibrateDataPoint(rawVec)

    def _partialXCalibration(self, rawVec: np.ndarray, figName: str) -> np.ndarray:
        pass

    def _initializeCaliTable(self):
        self.caliTable = []
        defaultMapVec = self.defaultMapVec()
        defaultParamSet = self.defaultCaliTableRowParamSet()
        for rowIdx in range(self.caliTableRowNr):
            if self.isFullCalibration:
                caliTableRow = CaliTableRow(
                    rawVec=defaultMapVec,
                    mapVec=defaultParamSet,
                    pointPairSource=None,
                )
            else:
                caliTableRow = CaliTableRow(
                    rawVec=defaultMapVec,
                    mapVec=defaultParamSet,
                    pointPairSource=self.figName[rowIdx // 2],
                )
            self.caliTable.append(caliTableRow)

    def defaultMapVec(self) -> Dict[str, float]:
        """
        Return the default mapped vector for the calibration table.
        """
        defaultMapVec = {name: 0.0 for name in self.rawVecName}
        return defaultMapVec

    def defaultCaliTableRowParamSet(self) -> List[ParamSet]:
        """
        Return the default parameter set for the calibration table.
        """
        # the idea: extract parameter set info from the sweep parameter set
        defaultParamSet = ParamSet[CaliTableParam](name="caliTableParamSet")
        for paramDictByParent in list(self.sweepParamSet.values()):
            for param in list(paramDictByParent.values()):
                defaultParamSet.addParameter(
                    CaliTableParam(
                        name=param.name,
                        value=param.value,
                        parent=param.parent,
                        param_type=param.param_type,
                    )
                )
        return defaultParamSet

    @Slot()
    def updateRawVec(
        self, row: int, newRawValue: Dict[str, float], figName: Union[str, None]
    ):
        """
        The function that updates raw vector for calibration
        """
        for name, value in newRawValue.items():
            self.caliTable[row].rawVec[name] = value

    @Slot()
    def updateMapVec(self, row: int, newMapValue: Tuple[str, str, float]):
        """
        The function that updates mapped vector for calibration

        Parameters
        ----------
        row: int
            The row index of the calibration table.
        newMapValue: Tuple[str, str, float]
            [parent name, parameter name, value]
        """
        parentName, parameterName, value = newMapValue
        self.caliTable[row].mapVec.setParameter(
            parent_system=parentName, name=parameterName, value=value
        )

    @Slot()
    def updateCaliFunc(self) -> Callable:
        """
        The function that updates the calibration function.
        """
        if self.isFullCalibration:
            return self._fullXCalibration
        else:
            return self._partialXCalibration
