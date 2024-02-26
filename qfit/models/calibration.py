import numpy as np

from PySide6.QtCore import Signal, Slot

from typing import (
    Dict, List, Union, Tuple, Callable, Literal, Optional, TYPE_CHECKING,
)

from qfit.models.data_structures import (
    QMSweepParam, SliderParam, FitParam, ParamAttr, CaliTableRowParam,
)
from qfit.models.parameter_set import ParamSet, ParamModelMixin, HSParamSet
from qfit.models.registry import RegistryEntry

if TYPE_CHECKING:
    from scqubits.core.hilbert_space import HilbertSpace


class CombinedMeta(type(ParamModelMixin), type(ParamSet)):
    pass


class CaliParamModel(
    ParamSet[CaliTableRowParam],
    ParamModelMixin[CaliTableRowParam],  # ordering matters
    metaclass=CombinedMeta,
):
    plotCaliPtExtractStart = Signal(str)
    plotCaliPtExtractFinished = Signal(str, dict)
    plotCaliPtExtractInterrupted = Signal()
    xCaliUpdated = Signal(dict)
    yCaliUpdated = Signal(object, object)
    updatePrefitModel = Signal(ParamAttr)
    caliModelRawVecUpdatedForSwapXY = Signal()
    # calibrationIsOn: Literal["CALI_X1", "CALI_X2", "CALI_Y1", "CALI_Y2", False]

    isFullCalibration: bool
    caliTableXRowNr: int
    caliTableXRowIdxList: List[str]
    caliTableYRowIdxList: List[str] = ["Y0", "Y1"]
    xRowIdxBySourceDict: Dict[str, List[str]] = {}

    parameters: Dict[str, Dict[str, CaliTableRowParam]]

    def __init__(
        self,
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
        # ordering matters here
        ParamSet.__init__(self, CaliTableRowParam)
        ParamModelMixin.__init__(self)

        self.applyCaliToAxis = False
        self.caliStatus = False

        # the following will be called separately outside of the class
        # self.dynamicalInit(
        #     hilbertSpace,
        #     rawXVecNameList,
        #     rawYName,
        #     figName,
        #     sweepParamSet,
        # )

    # initialize =======================================================
    def dynamicalInit(
        self,
        hilbertSpace: "HilbertSpace",
        rawXVecNameList: List[str],
        rawYName: str,
        figName: List[str],
    ):
        self.hilbertSpace = hilbertSpace
        self.rawXVecNameList = rawXVecNameList
        self.rawYName = rawYName
        self.figName = figName
        self.sweepParamSet = HSParamSet.sweepSetByHS(hilbertSpace)
        self.sweepParamParentName = list(self.sweepParamSet.keys())[0]
        self.sweepParamName = list(
            self.sweepParamSet[self.sweepParamParentName].keys()
        )[0]

        # determine total calibration table row number and if the calibration is a complete one

        self._isSufficientForFullCalibration(self.rawXVecDim, self.figNr)

        # initialize calibration table entries
        self.insertAllParams()

        self._updateXRowIdxBySourceDict()
        # self.paramDict = self.toParamDict()

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
            self.caliTableXRowNr = figNr * 2
        else:
            self.isFullCalibration = True
            self.caliTableXRowNr = pointsRequired
        self.caliTableXRowIdxList = [
            f"X{XRowIdx}" for XRowIdx in range(self.caliTableXRowNr)
        ]

    def insertAllParams(self):
        if self.parameters != {}:
            self.clear()

        # insert calibration table parameters for each row for X
        for XRowIdx, XRowIdxName in enumerate(self.caliTableXRowIdxList):
            # loop over the raw vector components
            for rawVecCompIdx, rawVecCompName in enumerate(self.rawXVecNameList):
                rawXValue = 1.0 if rawVecCompIdx == (XRowIdx - 1) else 0.0
                self._insertParamByArgs(
                    colName=rawVecCompName,
                    rowName=XRowIdxName,
                    paramType="raw_X_vec_component",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=rawXValue,
                )
            # loop over the mapped vector components (given by sweep parameters)
            mapXVecIdx = 0
            for parentName, paramDictByParent in self.sweepParamSet.items():
                for paramName, param in paramDictByParent.items():
                    mapXValue = 1.0 if mapXVecIdx == (XRowIdx - 1) else 0.0
                    self._insertParamByArgs(
                        colName=f"{parentName}.{paramName}",
                        rowName=XRowIdxName,
                        paramType=param.paramType,
                        sweepParamName=paramName,
                        value=mapXValue,
                        parentSystemName=parentName,
                    )
                    mapXVecIdx += 1
            # insert the point pair source
            if self.isFullCalibration:
                self._insertParamByArgs(
                    colName="pointPairSource",
                    rowName=XRowIdxName,
                    paramType="point_pair_source",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=None,
                )
            else:
                # value is the figure name
                self._insertParamByArgs(
                    colName="pointPairSource",
                    rowName=XRowIdxName,
                    paramType="point_pair_source",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=self.figName[int(XRowIdxName[1:]) // 2],
                )
        # insert calibration table parameters for Y: raw vector,
        for YRowIdx, YRowIdxName in enumerate(self.caliTableYRowIdxList):
            # loop over 2 values only
            rawYValue = 0.0 if YRowIdx == 0 else 1.0
            mapYValue = rawYValue
            self._insertParamByArgs(
                colName=self.rawYName,
                rowName=YRowIdxName,
                paramType="raw_Y",
                parentSystemName=None,
                sweepParamName=None,
                value=rawYValue,
            )
            self._insertParamByArgs(
                colName="mappedY",
                rowName=YRowIdxName,
                paramType="mapped_Y",
                sweepParamName=None,
                value=mapYValue,
                parentSystemName=None,
            )
            self._insertParamByArgs(
                colName="pointPairSource",
                rowName=YRowIdxName,
                paramType="point_pair_source",
                sweepParamName=None,
                value=None,
                parentSystemName=None,
            )

    def _insertParamByArgs(
        self,
        colName: str,
        rowName: str,
        paramType: str,
        parentSystemName: Optional[str],
        sweepParamName: Optional[str],
        value: Optional[Union[int, float, str]],
    ):
        """
        Create a Parameter object and add it to the parameter set. Notice that this method
        has a dual version in the HSParamSet class.
        """

        # process the keyword arguments (if needed)
        kwargs = {
            "colName": colName,
            "rowIdx": rowName,
            "paramType": paramType,
            "parentSystemName": parentSystemName,
            "sweepParamName": sweepParamName,
            "value": value,
        }

        # create the parameter object
        param = CaliTableRowParam(**kwargs)

        # add the parameter to the parameter set
        if rowName not in self.parameters.keys():
            self.parameters[rowName] = {}
        self.parameters[rowName][colName] = param

    # property =========================================================
    @property
    def rawXVecDim(self) -> int:
        return len(self.rawXVecNameList)

    @property
    def figNr(self) -> int:
        return len(self.figName)

    @property
    def sweepParamNr(self) -> int:
        return len(self.sweepParamSet)

    def _prefitHas(self, rowName: str, colName: str) -> bool:
        """
        Check if the prefit parameter is in the prefit parameter set.
        """
        param = self.parameters[rowName][colName]
        return param.paramType in ["flux", "ng", "mapped_Y"]

    def _xCaliDependOn(self, rowName: str, colName: str) -> bool:
        """
        Check if the mapped X value depends on the raw X value.
        """
        param = self.parameters[rowName][colName]
        return param.paramType in ["raw_X_vec_component", "ng", "flux"]

    def _yCaliDependOn(self, rowName: str, colName: str) -> bool:
        """
        Check if the mapped Y value depends on the raw Y value.
        """
        param = self.parameters[rowName][colName]
        return param.paramType in ["raw_Y", "mapped_Y"]
    
    def _fitMinMaxByColName(
        self, 
        rowName: str, 
        colName: str,
        scale: float = 0.2,
    ) -> Tuple[float, float]:
        """
        Prefit parameters' min and max are determined by the range of the 
        existed mapped values, for fine-tuning the cali parameters.
        """
        # obtain a list of values that has the same column name
        existedValue = []
        for rowNameIter, paramDictByParent in self.items():
            for colNameIter, param in paramDictByParent.items():
                if colNameIter != colName:
                    continue

                # filter out the parameters that are not updated by the slider
                if not self._prefitHas(rowNameIter, colName):
                    raise ValueError(
                        "This method should be only used for prefit parameters."
                    )
                
                existedValue.append(param.value)

        # using the min & max of the list, determine the range
        valRange = (np.max(existedValue) - np.min(existedValue)) * scale
        value = self[rowName][colName].value
        if valRange > 0:   
            # accept the range if it is not zero
            pass
        elif value != 0:
            valRange = np.abs(value) * scale * 2
        else:
            valRange = 1

        return (value + valRange/2, value - valRange/2)
    
    def toPrefitParams(self,) -> ParamSet[SliderParam]:
        # create the prefit parameters
        paramSet = ParamSet[SliderParam](SliderParam)
        for rowName, paramDictByParent in self.items():
            for colName, param in paramDictByParent.items():
                if not self._prefitHas(rowName, colName):
                    continue
                
                value = param.value
                min, max = self._fitMinMaxByColName(
                    rowName, colName, scale=0.2
                )

                # insert a prefit parameter
                prefitParam = SliderParam(
                    name = colName,
                    parent = param.parent,
                    paramType = param.paramType,
                    value = value,
                    min = min,
                    max = max,
                )
                paramSet.insertParam(rowName, colName, prefitParam)

        return paramSet
    
    def toFitParams(self,) -> ParamSet[FitParam]:
        # create the prefit parameters
        paramSet = ParamSet[FitParam](FitParam)
        for rowName, paramDictByParent in self.items():
            for colName, param in paramDictByParent.items():
                if not self._prefitHas(rowName, colName):
                    continue
                
                value = param.value
                min, max = self._fitMinMaxByColName(
                    rowName, colName, scale=0.1
                )

                # insert a prefit parameter
                fitParam = FitParam(
                    name = colName,
                    parent = param.parent,
                    paramType = param.paramType,
                    value = value,
                    min = min,
                    max = max,
                    initValue = value,
                    isFixed = True,
                )
                paramSet.insertParam(rowName, colName, fitParam)

        return paramSet

    # calibrate the raw vector to the mapped vector ====================
    def YCalibration(self) -> Callable:
        """
        Generate a function that applies the calibration to the raw Y value.
        """
        alphaVec = self._getYAlphaVec()

        def YCalibration(rawY: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
            """
            The full calibration function that maps the raw vector to the mapped vector.

            Parameters
            ----------
            rawY: Union[float, np.ndarray]
                The raw Y value, can either be an array of Y, or a single Y value.

            Returns
            -------
            The mapped Y value.
            """
            # mapY = alphaVec[0] + alphaVec[1]*rawY
            mapY = alphaVec[0] + alphaVec[1] * rawY
            return mapY

        return YCalibration

    def invYCalibration(self) -> Callable:
        """
        Generate a function that applies the inverse calibration to the mapped Y value.
        """
        alphaVec = self._getYAlphaVec()

        def invYCalibration(mapY: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
            """
            The full calibration function that maps the raw vector to the mapped vector.

            Parameters
            ----------
            mapY: Union[float, np.ndarray]
                The mapped Y value, can either be an array of Y, or a single Y value.

            Returns
            -------
            The raw Y value.
            """
            # rawY = (mapY - alphaVec[0])/alphaVec[1]
            rawY = (mapY - alphaVec[0]) / alphaVec[1]
            return rawY

        return invYCalibration

    def _getYAlphaVec(self) -> np.ndarray:
        """
        Solve the alpha vector for the Y calibration.
        """
        # gather all the point pair raw value and construct the augmented rawMat
        augRawYMat = np.zeros((2, 2))
        for YRowIdx in range(2):
            augRawYMat[YRowIdx, 0] = 1
            augRawYMat[YRowIdx, 1] = self[f"Y{YRowIdx}"][self.rawYName].value
        # gather all the point pair mapped value and solve alphaVec by inversion
        mapCompVec = np.zeros(2)
        for YRowIdx in range(2):
            mapCompVec[YRowIdx] = self[f"Y{YRowIdx}"]["mappedY"].value
        alphaVec = np.linalg.solve(augRawYMat, mapCompVec)
        return alphaVec

    def _fullXCalibration(self) -> Dict[str, HSParamSet[QMSweepParam]]:
        """
        Generate a function that applies the full calibration to the raw X vector.

        The full calibration takes form of
        mapVecComp = alphaVec . [1, rawVec]^T
        for each mapped vector component. To solve for alphaVec, we need to gather all the
        point pair rawVec and construct the augmented rawMat ([rawMat]_ji = i-th
        component of the j-th vector [1, rawVec]). For each mapped vector component, we
        gather all the point pair mapVec and solve alphaVec by inversion.
        """
        # gather all the point pair rawVec and construct the augmented rawMat
        augRawXMat = np.zeros((self.caliTableXRowNr, self.rawXVecDim + 1))
        for XRowIdx, xRowName in enumerate(self.caliTableXRowIdxList):

            augRawXMat[XRowIdx, 0] = 1
            for colIdx, rawXVecCompName in enumerate(self.rawXVecNameList):
                augRawXMat[XRowIdx, colIdx + 1] = self[xRowName][rawXVecCompName].value
        # loop over sweep parameters
        # assemble sweep parameter set, add sweep parameters to the parameter set

        sweepParamSetFromCali = HSParamSet[QMSweepParam](QMSweepParam)
        for parentName, paramDictByParent in self.sweepParamSet.items():
            for paramName, param in paramDictByParent.items():
                sweepParamSetFromCali._insertParamByArgs(
                    paramName=paramName,
                    parent=param.parent,
                    value=param.value,
                    paramType=param.paramType,
                    rangeDict={},  # not used
                )
                # gather all the point pair mapVec and solve alphaVec by inversion
                mapCompVec = np.zeros(self.caliTableXRowNr)
                for XRowIdx, xRowName in enumerate(self.caliTableXRowIdxList):
                    mapCompVec[XRowIdx] = self[xRowName][
                        f"{parentName}.{paramName}"
                    ].value
                alphaVec = np.linalg.solve(augRawXMat, mapCompVec)
                # generate the calibration function
                # first get the order of the raw vector components
                rawVecCompIdxDict = {
                    Idx: rawVecCompName
                    for Idx, rawVecCompName in enumerate(self.rawXVecNameList)
                }

                def fullCalibration(rawXVecDict: Dict[str, float]) -> float:
                    """
                    The full calibration function that maps the raw vector to the mapped vector.
                    """
                    rawXVec = np.zeros(self.rawXVecDim)
                    for rawXVecCompIdx in range(self.rawXVecDim):
                        rawVecCompName = rawVecCompIdxDict[rawXVecCompIdx]
                        rawXVec[rawXVecCompIdx] = rawXVecDict[rawVecCompName]
                    # mapVecComp = alphaVec . [1, rawVec]^T
                    mapXVecComp = np.dot(alphaVec, np.concatenate(([1], rawXVec)))
                    return mapXVecComp

                # set the calibration function
                sweepParamSetFromCali[parentName][param.name].setCalibrationFunc(
                    fullCalibration
                )
        sweepParamSetByFig: Dict[str, HSParamSet[QMSweepParam]] = {}
        for fig in self.figName:
            sweepParamSetByFig[fig] = sweepParamSetFromCali
        return sweepParamSetByFig

    def _partialXCalibration(self) -> Dict[str, HSParamSet[QMSweepParam]]:
        """
        Generate a function that applies the partial calibration to the raw vector.
        """
        sweepParamSetByFig: Dict[str, HSParamSet[QMSweepParam]] = {}
        # loop over all the figures
        for fig in self.figName:
            # get the row indices for the figure
            XRowIdxList = self.xRowIdxBySourceDict[fig]
            # this row index list should have length 2; extract the two rows
            rawXVecPairValues = {}
            for rawXVecCompName in self.rawXVecNameList:
                rawXVecCompValue1 = self[XRowIdxList[0]][rawXVecCompName].value
                rawXVecCompValue2 = self[XRowIdxList[1]][rawXVecCompName].value
                rawXVecPairValues[rawXVecCompName] = [
                    rawXVecCompValue1,
                    rawXVecCompValue2,
                ]
            # find the raw vector component that has the largest difference
            maxDiffRawVecComp = max(
                rawXVecPairValues,
                key=lambda k: abs(rawXVecPairValues[k][0] - rawXVecPairValues[k][1]),
            )
            # assemble sweep parameter set, add sweep parameters to the parameter set
            sweepParamSetFromCali = HSParamSet[QMSweepParam](QMSweepParam)
            for parentName, paramDictByParent in self.sweepParamSet.items():
                for paramName, param in paramDictByParent.items():
                    # extract mapped vector pair values
                    mapXVecCompValue1 = self[XRowIdxList[0]][
                        f"{parentName}.{paramName}"
                    ].value
                    mapXVecCompValue2 = self[XRowIdxList[1]][
                        f"{parentName}.{paramName}"
                    ].value
                    sweepParamSetFromCali._insertParamByArgs(
                        paramName=paramName,
                        parent=param.parent,
                        value=param.value,
                        paramType=param.paramType,
                        rangeDict={},  # not used
                    )

                    # generate the calibration function
                    def partialCalibration(rawXVecDict: Dict[str, float]) -> float:
                        """
                        The partial calibration function that maps the raw vector to the
                        mapped vector.
                        """
                        # first find x which is defined as
                        # rawVec = (rawVec2 - rawVec1)*x + rawVec1
                        x = (
                            rawXVecDict[maxDiffRawVecComp]
                            - rawXVecPairValues[maxDiffRawVecComp][0]
                        ) / (
                            rawXVecPairValues[maxDiffRawVecComp][1]
                            - rawXVecPairValues[maxDiffRawVecComp][0]
                        )
                        # then calculate the specific individual component of the mapped vector
                        # mapVecComp = (mapVecComp2 - mapVecComp1)*x + mapVecComp1
                        mapXVecComp = (
                            mapXVecCompValue2 - mapXVecCompValue1
                        ) * x + mapXVecCompValue1
                        return mapXVecComp

                    # set the calibration function
                    sweepParamSetFromCali[parentName][param.name].setCalibrationFunc(
                        partialCalibration
                    )
            sweepParamSetByFig[fig] = sweepParamSetFromCali
        return sweepParamSetByFig
    
    def XCalibration(self) -> Dict[str, HSParamSet[QMSweepParam]]:
        if self.isFullCalibration:
            return self._fullXCalibration()
        else:
            return self._partialXCalibration()

    # slots & public interface ================================================
    @Slot()
    def updateStatusFromCaliView(self, status: Union[str, Literal[False]]):
        self.caliStatus = status
        if type(status) is str:
            if status[0] == "X":
                destination = "CALI_X"
            elif status[0] == "Y":
                destination = "CALI_Y"
            self.plotCaliPtExtractStart.emit(destination)
        else:
            self.plotCaliPtExtractInterrupted.emit()

    @Slot()
    def _updateXRowIdxBySourceDict(self):
        """
        Update the rowIdxSourceDict, which stores the row indices for each figure.
        """
        self.xRowIdxBySourceDict = {}

        for fig in self.figName:
            self.xRowIdxBySourceDict[fig] = [
                XRowIdx
                for XRowIdx in self.caliTableXRowIdxList
                if fig == self[XRowIdx]["pointPairSource"].value
            ]

    def setParameter(
        self,
        rowIdx: str,
        colName: str,
        attr: str,
        value: Union[int, float, str, None],
    ):
        """
        Not only set the parameter, but also emit the signal to update the view.

        A key method in updating the model by the internal processes.
        """
        super().setParameter(rowIdx, colName, attr, value)

        self.emitUpdateBox(rowIdx, colName, attr)

        if self._xCaliDependOn(rowIdx, colName):
            self.sendXCaliFunc()
        elif self._yCaliDependOn(rowIdx, colName):
            self.sendYCaliFunc()
            # self.sendInvYCaliFunc()

    def processSelectedPtFromPlot(self, data: Dict[str, float], figName: str):
        """
        Called by the canvas click event. Process and store the calibration data.
        """
        # get current label
        caliLabel = self.caliStatus  # can be int or str
        # based on the current label, we know the row index to store the data
        # store the calibration data
        # if the current label is int, then it is for X
        if type(caliLabel) is str:
            if caliLabel[0] == "X":
                for rawXVecCompName in self.rawXVecNameList:
                    # this contains updatebox
                    self.setParameter(
                        rowIdx=caliLabel,
                        colName=rawXVecCompName,
                        attr="value",
                        value=data[rawXVecCompName],
                    )
            elif caliLabel[0] == "Y":
                # this contains updatebox
                self.setParameter(
                    rowIdx=caliLabel,
                    colName=self.rawYName,
                    attr="value",
                    value=data[self.rawYName],
                )
            # update source for the point pair
            self.setParameter(
                rowIdx=caliLabel, colName="pointPairSource", attr="value", value=figName
            )
            self.plotCaliPtExtractFinished.emit(caliLabel, data)
            self.caliStatus = False

    def toggleAxisCaliRep(self):
        self.applyCaliToAxis = not self.applyCaliToAxis

    @Slot()
    def interruptCali(self):
        self.caliStatus = False
        self.plotCaliPtExtractInterrupted.emit()

        # if self.caliStatus:
        #     self.caliStatus = False
        #     self.plotCaliPtExtractEnd.emit()
        # else:
        #     # if the calibration is not on, it's likely triggered by
        #     # other events like page change,
        #     # we should not trigger the plotCaliPtExtractEnd signal in this case
        #     pass

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        return self._registerAll(self)

    @Slot()
    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        """
        Store attr from view. 

        It also updates the prefit model if the parameter is a prefit parameter.
        """
        super()._storeParamAttr(self, paramAttr, **kwargs)
        rowIdx = paramAttr.parentName
        colName = paramAttr.name

        if paramAttr.attr == "value":
            if self._xCaliDependOn(rowIdx, colName):
                self.sendXCaliFunc()
            elif self._yCaliDependOn(rowIdx, colName):
                self.sendYCaliFunc()
                # self.sendInvYCaliFunc()

            if self._prefitHas(rowIdx, colName):
                # update min, max, value for the prefit model
                min, max = self._fitMinMaxByColName(rowIdx, colName)
                self.updatePrefitModel.emit(ParamAttr(
                    paramAttr.parentName, 
                    paramAttr.name, 
                    "min", 
                    min
                ))
                self.updatePrefitModel.emit(ParamAttr(
                    paramAttr.parentName, 
                    paramAttr.name, 
                    "max", 
                    max
                ))
                self.updatePrefitModel.emit(ParamAttr(
                    paramAttr.parentName, 
                    paramAttr.name, 
                    paramAttr.attr, 
                    self[paramAttr.parentName][paramAttr.name].value
                ))

    def updateCaliModelRawVecNameListForSwapXY(self):
        self.rawYName, self.rawXVecNameList = self.rawXVecNameList[0], [self.rawYName]
        self.insertAllParams()
        self._updateXRowIdxBySourceDict()
        self.caliModelRawVecUpdatedForSwapXY.emit()

    @Slot()
    def swapXYData(self):
        """
        Finalize the XY swap: swap the value of the X and Y data for both raw and
        mapped vectors, and update calibration functions.
        """
        # signals will be sent by these setParameter methods
        # if we don't block the signals, the signals will be sent multiple times
        # will send the signals after the swap is done
        self.blockSignals(True)

        oldX0RawValue = self.parameters["X0"][self.rawXVecNameList[0]].value
        oldX1RawValue = self.parameters["X1"][self.rawXVecNameList[0]].value
        oldX0MapValue = self.parameters["X0"][
            f"{self.sweepParamParentName}.{self.sweepParamName}"
        ].value
        oldX1MapValue = self.parameters["X1"][
            f"{self.sweepParamParentName}.{self.sweepParamName}"
        ].value
        oldY0RawValue = self.parameters["Y0"][self.rawYName].value
        oldY1RawValue = self.parameters["Y1"][self.rawYName].value
        oldY0MapValue = self.parameters["Y0"]["mappedY"].value
        oldY1MapValue = self.parameters["Y1"]["mappedY"].value
        self.setParameter(
            rowIdx="X0",
            colName=self.rawXVecNameList[0],
            attr="value",
            value=oldY0RawValue,
        )
        self.setParameter(
            rowIdx="X1",
            colName=self.rawXVecNameList[0],
            attr="value",
            value=oldY1RawValue,
        )
        self.setParameter(
            rowIdx="X0",
            colName=f"{self.sweepParamParentName}.{self.sweepParamName}",
            attr="value",
            value=oldY0MapValue,
        )
        self.setParameter(
            rowIdx="X1",
            colName=f"{self.sweepParamParentName}.{self.sweepParamName}",
            attr="value",
            value=oldY1MapValue,
        )
        self.setParameter(
            rowIdx="Y0", colName=self.rawYName, attr="value", value=oldX0RawValue
        )
        self.setParameter(
            rowIdx="Y1", colName=self.rawYName, attr="value", value=oldX1RawValue
        )
        self.setParameter(
            rowIdx="Y0", colName="mappedY", attr="value", value=oldX0MapValue
        )
        self.setParameter(
            rowIdx="Y1", colName="mappedY", attr="value", value=oldX1MapValue
        )

        self.blockSignals(False)

        self.emitUpdateBox()
        self.sendXCaliFunc()
        self.sendYCaliFunc()

    def updateAllBoxes(self):
        """
        need to be updated in the future to cope with case where the data source
        is provided as a table entry.
        """
        for rowIdx, colDict in self.parameters.items():
            for colName, param in colDict.items():
                if param.paramType not in ["point_pair_source"]:
                    self.emitUpdateBox(rowIdx, colName, "value")

    # signals ==========================================================
    def emitUpdateBox(
        self,
        rowIdx: Optional[str] = None,
        colName: Optional[str] = None,
        attr: Optional[str] = None,
    ):
        self._emitUpdateBox(self, parentName=rowIdx, paramName=colName, attr=attr)

    def sendXCaliFunc(self):
        """
        The function that updates the calibration function. Triggers when:
        * line editing acction triggers storeParamAttr
        * XY swap triggers swapXYData
        * entering raw X by clicking on the plot triggers processSelectedPtFromPlot
        """
        self.xCaliUpdated.emit(self.XCalibration())

    def sendYCaliFunc(self):
        """
        The function that updates the calibration function. Triggers when:
        * line editing acction triggers storeParamAttr
        * XY swap triggers swapXYData
        * entering raw Y by clicking on the plot triggers processSelectedPtFromPlot
        """
        self.yCaliUpdated.emit(self.YCalibration(), self.invYCalibration())

