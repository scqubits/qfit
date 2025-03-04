import numpy as np

from PySide6.QtCore import Signal, Slot, QObject

from typing import (
    Dict,
    List,
    Union,
    Tuple,
    Callable,
    Literal,
    Optional,
    TYPE_CHECKING,
)

from qfit.models.data_structures import (
    SliderParam,
    FitParam,
    ParamAttr,
    CaliTableRowParam,
    Status,
)
from qfit.models.parameter_set import ParamSet, ParamModelMixin, SweepParamSet
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
    """
    Store calibration data for x and y axes, and provide methods to 
    transform between uncalibrated (raw) and calibrated (mapped) data.
    The transformation is either a complete one, where rawVecX is the
    experimental parameter (i.e. voltage) and mapVecX is the calibrated
    parameter (i.e. flux or ng). 
    
    If sufficient number of figures are provided, the full relation 
    between the two can be fully determined as follows:
        mapVecX = M @ rawVecX + offsetVecX
    assume mapVecX has N components, rawVecX has L components, then M
    is a N x L matrix and offsetVecX is a N-component vector. M and
    offsetVecX are determined by providing L+1 pairs of (rawVecX, mapVecX)
    data points. 

    If insufficient number of figures are provided, the calibration is
    partial. In this case, the calibration is done for each figure
    separately. For each figure, the relation between the rawVecX and 
    mapVecX is:
        rawVecX = rawVecX2 + tX * (rawVecX2 - rawVecX2)  \\
        mapVecX = mapVecX2 + tX * (mapVecX2 - mapVecX2)
    Here the rawVecX is the voltage vector in a figure that one wants to
    calibrate, and mapVecX is the calibrated vector. The tX is the
    parameter that determines the position of the rawVecX in the figure.
    The calibration is done by providing 2 pairs of (rawVecX, mapVecX) data
    points for each figure. 

    When the calibration is done, signals containing the calibration data
    will be emitted (xCaliUpdated, yCaliUpdated).

    The model also communicates with PrefitCaliModel as they share the same
    calibration data. The prefit model is used to fine-tune the calibration
    parameters. 

    Parameters
    ----------
    parent: QObject
        The parent object.
    """

    _figNames: List[str]
    _rawXVecNameList: List[str]
    _rawYName: str
    _sweepParamSet: SweepParamSet
    _sweepParamParentName: str
    _sweepParamName: str

    plotCaliPtExtractStart = Signal(str)
    plotCaliPtExtractFinished = Signal(str, dict)
    plotCaliPtExtractInterrupted = Signal()
    xCaliUpdated = Signal(object)
    yCaliUpdated = Signal(object, object)
    updatePrefitModel = Signal(ParamAttr)
    caliModelRawVecUpdatedForSwapXY = Signal()
    updateStatus = Signal(Status)
    # calibrationIsOn: Literal["CALI_X2", "CALI_X2", "CALI_Y2", "CALI_Y2", False]

    isFullCalibration: bool
    caliTableXRowNr: int
    _caliTableXRowIdxList: List[str]
    _caliTableYRowIdxList: List[str]
    _xRowIdxBySourceDict: Dict[str, List[str]]

    def __init__(
        self,
        parent: QObject,
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
        rawVecX = rawVecX2 + tX * (rawVecX2 - rawVecX2)
        mapVecX = mapVecX2 + tX * (mapVecX2 - mapVecX2)
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
        ParamModelMixin.__init__(self, parent)

        self.caliStatus = False

        self._caliTableYRowIdxList = ["Y1", "Y2"]
        self._xRowIdxBySourceDict = {}

    # initialize =======================================================
    def replaceHS(self, sweepParamSet: SweepParamSet):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It updates the
        HilbertSpace object.

        Parameters
        ----------
        sweepParamSet: SweepParamSet
            The sweep parameter set for the HilbertSpace.
        """
        self._sweepParamSet = sweepParamSet
        self._sweepParamParentName = list(self._sweepParamSet.keys())[0]
        self._sweepParamName = list(
            self._sweepParamSet[self._sweepParamParentName].keys()
        )[0]

    def replaceMeasData(
        self,
        figNames: List[str],
        rawXVecNameList: List[str],
        rawYNames: str,
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It replaces the figure
        names, determine the calibration mode, and reinitialize
        the calibration table entries.

        Note: For the moment, when the measurement data is updated, all of the
        properties will be re-initialized.

        Parameters
        ----------
        figName: List[str]
            The new figure names.
        rawXVecNameList: List[str]
            The new raw vector component names.
        rawYNames: str
            The new raw Y component name.
        """
        self._figNames = figNames
        self._rawXVecNameList = rawXVecNameList
        self._rawYName = rawYNames
        self._determineCaliMode(self.rawXVecDim, self.figNr)

    def dynamicalInit(
        self,
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It erase all the data
        input from the user and reinitialize the calibration table entries.
        """
        try:
            self._sweepParamSet
        except AttributeError:
            raise AttributeError(
                "HilbertSpace not yet inited. At the moment, "
                "this method should be called after replaceHS."
            )
        try:
            self._figNames
        except AttributeError:
            raise AttributeError(
                "Measurement data not yet inited. At the moment, "
                "this method should be called after replaceMeasData."
            )

        # initialize calibration table entries
        self._insertAllParams()
        self._updateXRowIdxBySourceDict()

    def _determineCaliMode(self, rawVecDim: int, figNr: int):
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
        self._caliTableXRowIdxList = [
            f"X{XRowIdx+1}" for XRowIdx in range(self.caliTableXRowNr)
        ]

    def _insertAllParams(self):
        """
        Insert all calibration table parameters as a part of the initialization.

        The calibration table parameters contains:
            - raw vector components, determined by the raw values from the two-tone data
            - mapped vector components, given by sweep parameters in the HilbertSpace
            - point pair source (if the raw vector comes from clicking on the plot)
        """
        if self.parameters != {}:
            self.clear()

        # insert calibration table parameters for each row for X
        for XRowIdx, XRowIdxName in enumerate(self._caliTableXRowIdxList):
            # loop over the raw vector components
            for rawVecCompIdx, rawVecCompName in enumerate(self._rawXVecNameList):
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
            for parentName, paramDictByParent in self._sweepParamSet.items():
                for paramName, param in paramDictByParent.items():
                    mapXValue = 1.0 if mapXVecIdx == (XRowIdx - 1) else 0.0
                    self._insertParamByArgs(
                        colName=f"{paramName}<br>({parentName})",
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
                    colName="DATA<br>SOURCE",
                    rowName=XRowIdxName,
                    paramType="data_source",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=None,
                )
            else:
                # value is the figure name
                self._insertParamByArgs(
                    colName="DATA<br>SOURCE",
                    rowName=XRowIdxName,
                    paramType="data_source",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=self._figNames[XRowIdx // 2],
                )
        # insert calibration table parameters for Y: raw vector,
        for YRowIdx, YRowIdxName in enumerate(self._caliTableYRowIdxList):
            # loop over 2 values only
            rawYValue = 0.0 if YRowIdx == 0 else 1.0
            mapYValue = rawYValue
            self._insertParamByArgs(
                colName=self._rawYName,
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
                colName="DATA<br>SOURCE",
                rowName=YRowIdxName,
                paramType="data_source",
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
        has a dual version in the SweepParamSet class.
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
        self.insertParam(rowName, colName, param)

    # property =========================================================
    @property
    def rawXVecDim(self) -> int:
        return len(self._rawXVecNameList)

    @property
    def figNr(self) -> int:
        return len(self._figNames)

    @property
    def sweepParamNr(self) -> int:
        return len(self._sweepParamSet)

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
        In prefit, the same calibration parameters can be tuned by
        sliders, and the min and max of the sliders are determined here.

        Parameters
        ----------
        rowName: str
            The row name of the parameter.
        colName: str
            The column name.
        scale: float = 0.2
            The scaling factor for the range.
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

        return (value + valRange / 2, value - valRange / 2)

    def toPrefitParams(
        self,
    ) -> ParamSet[SliderParam]:
        """
        Create a set of prefit parameters. It will be accepted by the
        prefitCaliParams using setAttrByParamDict method.

        Returns
        -------
        ParamSet[SliderParam]
            The prefit parameters with proper min, max, and value.
        """
        # create the prefit parameters
        paramSet = ParamSet[SliderParam](SliderParam)
        for rowName, paramDictByParent in self.items():
            for colName, param in paramDictByParent.items():
                if not self._prefitHas(rowName, colName):
                    continue

                value = param.value
                min, max = self._fitMinMaxByColName(rowName, colName, scale=0.2)

                # insert a prefit parameter
                prefitParam = SliderParam(
                    name=colName,
                    parent=param.parent,
                    paramType=param.paramType,
                    value=value,
                    min=min,
                    max=max,
                )
                paramSet.insertParam(rowName, colName, prefitParam)

        return paramSet

    def toFitParams(
        self,
    ) -> ParamSet[FitParam]:
        """
        Create a set of fit parameters. It will be accepted by the
        FitCaliParam using setAttrByParamDict method.

        Returns
        -------
        ParamSet[FitParam]
            The fit parameters with proper min, max, initValue and isFixed.
        """
        # create the prefit parameters
        paramSet = ParamSet[FitParam](FitParam)
        for rowName, paramDictByParent in self.items():
            for colName, param in paramDictByParent.items():
                if not self._prefitHas(rowName, colName):
                    continue

                value = param.value
                min, max = self._fitMinMaxByColName(rowName, colName, scale=0.1)

                # insert a prefit parameter
                fitParam = FitParam(
                    name=colName,
                    parent=param.parent,
                    paramType=param.paramType,
                    value=0,  # not used
                    min=min,
                    max=max,
                    initValue=value,
                    isFixed=True,
                )
                paramSet.insertParam(rowName, colName, fitParam)

        return paramSet

    # calibrate the raw vector to the mapped vector ====================
    def YCalibration(
        self,
    ) -> Union[Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]], Literal[False]]:
        """
        Generate a function that applies the calibration to the raw Y value.

        Returns
        -------
        Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]]
            The calibration function that maps the raw vector to the mapped vector.
        """
        alphaVec = self._getYAlphaVec()
        if alphaVec is False:
            return False
        else:

            def YCalibration(
                rawY: Union[float, np.ndarray]
            ) -> Union[float, np.ndarray]:
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

    def invYCalibration(
        self,
    ) -> Union[Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]], Literal[False]]:
        """
        Generate a function that applies the inverse calibration to the mapped Y value.

        Returns
        -------
        Callable[[Union[float, np.ndarray]], Union[float, np.ndarray]]
            The calibration function that maps the mapped vector to the raw vector.
        """
        alphaVec = self._getYAlphaVec()
        if alphaVec is False:
            return False
        else:

            def invYCalibration(
                mapY: Union[float, np.ndarray]
            ) -> Union[float, np.ndarray]:
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
                rawY = (mapY - alphaVec[0]) / alphaVec[1]
                return rawY

            return invYCalibration

    def _getYAlphaVec(self) -> Union[np.ndarray, Literal[False]]:
        """
        Solve the alpha vector for the Y calibration, which contains
        the offset and the slope of the calibration line.
        """
        # gather all the point pair raw value and construct the augmented rawMat
        augRawYMat = np.zeros((2, 2))
        for YRowIdx in range(2):
            augRawYMat[YRowIdx, 0] = 1
            augRawYMat[YRowIdx, 1] = self[f"Y{YRowIdx+1}"][self._rawYName].value
        # gather all the point pair mapped value and solve alphaVec by inversion
        mapCompVec = np.zeros(2)
        for YRowIdx in range(2):
            mapCompVec[YRowIdx] = self[f"Y{YRowIdx+1}"]["mappedY"].value

        try:
            alphaVec = np.linalg.solve(augRawYMat, mapCompVec)
        except np.linalg.LinAlgError:
            status = Status(
                statusSource="calibration",
                statusType="error",
                message="Invalid Y axes calibration parameters.",
            )
            self.updateStatus.emit(status)
            return False

        status = Status(
            statusSource="calibration",
            statusType="success",
            message="Y axes calibration parameters updated.",
        )

        return alphaVec

    def _fullXCalibration(self) -> Union[Dict[str, SweepParamSet], Literal[False]]:
        """
        Generate a function that applies the full calibration to the raw X vector.

        The full calibration takes the form of:
        mapVecComp = alphaVec . [1, rawVec]^T
        alphaVec is the "slope" and "offset" of the calibration line.
        To solve it, we need to gather all the point pairs of
        rawVec and construct the augmented rawMat, where [rawMat]_ji is
        the i-th component of the j-th vector [1, rawVec]. Then alphaVec
        can be solved by inverting the rawMat.

        Mapped vector components can be obtained by applying the calibration
        function to the raw vector components.

        Returns
        -------
        Dict[str, SweepParamSet]
            In each figure, the sweep parameter set contains the calibration
            function that maps the raw vector to the mapped vector.
        """
        # gather all the point pair rawVec and construct the augmented rawMat
        augRawXMat = np.zeros((self.caliTableXRowNr, self.rawXVecDim + 1))
        for XRowIdx, xRowName in enumerate(self._caliTableXRowIdxList):

            augRawXMat[XRowIdx, 0] = 1
            for colIdx, rawXVecCompName in enumerate(self._rawXVecNameList):
                augRawXMat[XRowIdx, colIdx + 1] = self[xRowName][rawXVecCompName].value

        # loop over sweep parameters
        # assemble sweep parameter set, add sweep parameters to the parameter set
        hasError = False
        sweepParamSetFromCali = SweepParamSet()
        for parentName, paramDictByParent in self._sweepParamSet.items():
            for paramName, param in paramDictByParent.items():
                # for each parameter,
                sweepParamSetFromCali._insertParamByArgs(
                    parent=self._sweepParamSet.parentObjByName[parentName],
                    paramName=paramName,
                    value=param.value,
                    paramType=param.paramType,
                    rangeDict={},  # not used
                )
                # gather all the point pair mapVec and solve alphaVec by inversion
                mapCompVec = np.zeros(self.caliTableXRowNr)
                for XRowIdx, xRowName in enumerate(self._caliTableXRowIdxList):
                    mapCompVec[XRowIdx] = self[xRowName][
                        f"{paramName}<br>({parentName})"
                    ].value
                try:
                    alphaVec = np.linalg.solve(augRawXMat, mapCompVec)
                except np.linalg.LinAlgError:
                    hasError = True
                    status = Status(
                        statusSource="calibration",
                        statusType="error",
                        message="Invalid calibration parameters.",
                    )
                    self.updateStatus.emit(status)
                    return False
                # generate the calibration function
                # first get the order of the raw vector components
                rawVecCompIdxDict = {
                    Idx: rawVecCompName
                    for Idx, rawVecCompName in enumerate(self._rawXVecNameList)
                }

                # _alphaVec added here to resolve the "late-binding closure" issue
                # so that whenever the function is defined, _alphaVec is set to alphaVec and is
                # a local variable with scope restricted to the function.
                def fullCalibration(
                    rawXVecDict: Dict[str, float],
                    _alphaVec=alphaVec,
                    _rawXVecDim=self.rawXVecDim,
                ) -> float:
                    """
                    The full calibration function that maps the raw vector to the mapped vector.
                    """
                    rawXVec = np.zeros(_rawXVecDim)
                    for rawXVecCompIdx in range(_rawXVecDim):
                        rawVecCompName = rawVecCompIdxDict[rawXVecCompIdx]
                        rawXVec[rawXVecCompIdx] = rawXVecDict[rawVecCompName]
                    # mapVecComp = alphaVec . [1, rawVec]^T
                    mapXVecComp = np.dot(_alphaVec, np.concatenate(([1], rawXVec)))
                    return mapXVecComp

                # set the calibration function
                sweepParamSetFromCali[parentName][param.name].setCalibrationFunc(
                    fullCalibration
                )

        sweepParamSetByFig: Dict[str, SweepParamSet] = {}
        for fig in self._figNames:
            sweepParamSetByFig[fig] = sweepParamSetFromCali

        if not hasError:
            status = Status(
                statusSource="calibration",
                statusType="success",
                message="X axes calibration parameters updated.",
            )
            self.updateStatus.emit(status)

        return sweepParamSetByFig

    def _partialXCalibration(self) -> Union[Dict[str, SweepParamSet], Literal[False]]:
        """
        Generate a function that applies the partial calibration to the raw X vector.

        The partial calibration takes the form of:
        mapVecComp = (mapVecComp2 - mapVecComp1)*x + mapVecComp1
        rawVecComp = (rawVecComp2 - rawVecComp1)*x + rawVecComp1
        Here x is the parameter that determines the position of the
        rawVecComp in the figure. The calibration is done by providing
        2 pairs of (rawVecComp, mapVecComp) data points for each figure.

        Mapped vector components can be obtained by applying the calibration
        function to the raw vector components.

        Returns
        -------
        Dict[str, SweepParamSet]
            In each figure, the sweep parameter set contains the calibration
            function that maps the raw vector to the mapped vector.
        """
        sweepParamSetByFig: Dict[str, SweepParamSet] = {}
        # loop over all the figures
        for fig in self._figNames:
            # get the row indices for the figure
            XRowIdxList = self._xRowIdxBySourceDict[fig]
            # this row index list should have length 2; extract the two rows
            rawXVecPairValues = {}
            for rawXVecCompName in self._rawXVecNameList:
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
            sweepParamSetFromCali = SweepParamSet()
            for parentName, paramDictByParent in self._sweepParamSet.items():
                for paramName, param in paramDictByParent.items():
                    # extract mapped vector pair values
                    mapXVecCompValue1 = self[XRowIdxList[0]][
                        f"{paramName}<br>({parentName})"
                    ].value
                    mapXVecCompValue2 = self[XRowIdxList[1]][
                        f"{paramName}<br>({parentName})"
                    ].value

                    # check if the denominator is zero
                    if (
                        rawXVecPairValues[maxDiffRawVecComp][0]
                        == rawXVecPairValues[maxDiffRawVecComp][1]
                    ):
                        status = Status(
                            statusSource="calibration",
                            statusType="error",
                            message="Invalid calibration parameters.",
                        )
                        self.updateStatus.emit(status)
                        return False
                    sweepParamSetFromCali._insertParamByArgs(
                        parent=self._sweepParamSet.parentObjByName[parentName],
                        paramName=paramName,
                        value=param.value,
                        paramType=param.paramType,
                        rangeDict={},  # not used
                    )

                    # generate the calibration function
                    # the underscored variables are workarounds for the late-binding issue
                    def partialCalibration(
                        rawXVecDict: Dict[str, float],
                        _mapXVecCompValue1=mapXVecCompValue1,
                        _mapXVecCompValue2=mapXVecCompValue2,
                        _maxDiffRawVecComp=maxDiffRawVecComp,
                        _rawXVecPairValues=rawXVecPairValues,
                    ) -> float:
                        """
                        The partial calibration function that maps the raw vector to the
                        mapped vector.
                        """
                        # first find x which is defined as
                        # rawVec = (rawVec2 - rawVec1)*x + rawVec1
                        x = (
                            rawXVecDict[_maxDiffRawVecComp]
                            - _rawXVecPairValues[_maxDiffRawVecComp][0]
                        ) / (
                            _rawXVecPairValues[_maxDiffRawVecComp][1]
                            - _rawXVecPairValues[_maxDiffRawVecComp][0]
                        )
                        # then calculate the specific individual component of the mapped vector
                        # mapVecComp = (mapVecComp2 - mapVecComp1)*x + mapVecComp1
                        mapXVecComp = (
                            _mapXVecCompValue2 - _mapXVecCompValue1
                        ) * x + _mapXVecCompValue1
                        return mapXVecComp

                    # set the calibration function
                    sweepParamSetFromCali[parentName][param.name].setCalibrationFunc(
                        partialCalibration
                    )
            sweepParamSetByFig[fig] = sweepParamSetFromCali
        return sweepParamSetByFig

    def XCalibration(self) -> Union[Dict[str, SweepParamSet], Literal[False]]:
        """
        Generate a function that applies the calibration to the raw X vector,
        based on the type of calibration.
        """
        if self.isFullCalibration:
            return self._fullXCalibration()
        else:
            return self._partialXCalibration()

    # slots & public interface ================================================
    @Slot()
    def updateStatusFromCaliView(self, status: Union[str, Literal[False]]):
        """
        When the user clicks the raw vector extraction button, the status
        will be updated.

        Parameters
        ----------
        status: Union[str, Literal[False]]
            The status of the calibration. If it's a string, calibration
            asis can be inferred from the first character (X or Y). If it's
            False, the calibration is off.
        """
        self.caliStatus = status
        if type(status) is str:
            if status[0] == "X":
                destination = "CALI_X"
            elif status[0] == "Y":
                destination = "CALI_Y"
            else:
                raise ValueError("Invalid status.")
            self.plotCaliPtExtractStart.emit(destination)
        else:
            self.plotCaliPtExtractInterrupted.emit()

    @Slot()
    def _updateXRowIdxBySourceDict(self):
        """
        Update the rowIdxSourceDict, which stores the row indices for each figure.
        """
        self._xRowIdxBySourceDict = {}

        for fig in self._figNames:
            self._xRowIdxBySourceDict[fig] = [
                XRowIdx
                for XRowIdx in self._caliTableXRowIdxList
                if fig == self[XRowIdx]["DATA<br>SOURCE"].value
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

        Parameters
        ----------
        rowIdx: str
            The row index of the parameter.
        colName: str
            The column name of the parameter.
        attr: str
            The attribute of the parameter.
        value: Union[int, float, str, None]
            The value to be set.
        """
        super().setParameter(rowIdx, colName, attr, value)

        self.emitUpdateBox(rowIdx, colName, attr)

        if self._xCaliDependOn(rowIdx, colName):
            self.sendXCaliFunc()
        elif self._yCaliDependOn(rowIdx, colName):
            self.sendYCaliFunc()

    def processSelectedPtFromPlot(self, data: Dict[str, float], figName: str):
        """
        Called by the canvas click event. Process and store the calibration data.

        Parameters
        ----------
        data: Dict[str, float]
            The raw vector data.
        figName: str
            The name of the figure.
        """
        # get current label
        caliLabel = self.caliStatus  # can be int or str
        # based on the current label, we know the row index to store the data
        # store the calibration data
        # if the current label is int, then it is for X
        if type(caliLabel) is str:
            if caliLabel[0] == "X":
                for rawXVecCompName in self._rawXVecNameList:
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
                    colName=self._rawYName,
                    attr="value",
                    value=data[self._rawYName],
                )
            # update source for the point pair
            self.setParameter(
                rowIdx=caliLabel, colName="DATA<br>SOURCE", attr="value", value=figName
            )
            self.plotCaliPtExtractFinished.emit(caliLabel, data)
            self.caliStatus = False

    @Slot()
    def interruptCali(self):
        """
        Interrupt the calibration process, it will be called either by the
        user clicking the calibration button again, or by other events like
        page change.
        """
        if self.caliStatus:
            self.caliStatus = False
            self.plotCaliPtExtractInterrupted.emit()

    def _registrySetter(
        self,
        value: Dict[str, Dict[str, CaliTableRowParam]],
        paramSet: ParamSet[CaliTableRowParam],
    ):
        """
        Set the parameter set by the value from the registry.

        Parameters
        ----------
        value: Dict[str, Dict[str, DispParamCls]]
            The value from the registry
        paramSet: ParamSet
            The parameter set
        """
        super()._registrySetter(value, paramSet)
        self.sendXCaliFunc()
        self.sendYCaliFunc()

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters in the model.
        """
        return self._registerAll(self)

    @Slot()
    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        """
        Store attr from view. It also updates the prefit model if the
        parameter is a prefit parameter.

        Parameters
        ----------
        paramAttr: ParamAttr
            The parameter attribute.
        kwargs: Dict[str, Any]
            The keyword arguments for setting the parameter attribute in
            view.storeAttr method.
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
                self.updatePrefitModel.emit(
                    ParamAttr(paramAttr.parentName, paramAttr.name, "min", min)
                )
                self.updatePrefitModel.emit(
                    ParamAttr(paramAttr.parentName, paramAttr.name, "max", max)
                )
                self.updatePrefitModel.emit(
                    ParamAttr(
                        paramAttr.parentName,
                        paramAttr.name,
                        paramAttr.attr,
                        self[paramAttr.parentName][paramAttr.name].value,
                    )
                )

    @Slot()
    def clearDataSourceInModel(self, paramAttr: ParamAttr):
        """
        Clear the data source in the model.
        """
        self.setParameter(paramAttr.parentName, paramAttr.name, paramAttr.attr, None)

    def updateCaliModelRawVecNameListForSwapXY(self):
        """
        Update the raw vector names for the calibration model when the XY data
        is swapped.
        """
        self._rawYName, self._rawXVecNameList = self._rawXVecNameList[0], [
            self._rawYName
        ]
        self._insertAllParams()
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

        oldX1RawValue = self.parameters["X1"][self._rawXVecNameList[0]].value
        oldX2RawValue = self.parameters["X2"][self._rawXVecNameList[0]].value
        oldX1MapValue = self.parameters["X1"][
            f"{self._sweepParamName}<br>({self._sweepParamParentName})"
        ].value
        oldX2MapValue = self.parameters["X2"][
            f"{self._sweepParamName}<br>({self._sweepParamParentName})"
        ].value
        oldY1RawValue = self.parameters["Y1"][self._rawYName].value
        oldY2RawValue = self.parameters["Y2"][self._rawYName].value
        oldY1MapValue = self.parameters["Y1"]["mappedY"].value
        oldY2MapValue = self.parameters["Y2"]["mappedY"].value
        self.setParameter(
            rowIdx="X1",
            colName=self._rawXVecNameList[0],
            attr="value",
            value=oldY1RawValue,
        )
        self.setParameter(
            rowIdx="X2",
            colName=self._rawXVecNameList[0],
            attr="value",
            value=oldY2RawValue,
        )
        self.setParameter(
            rowIdx="X1",
            colName=f"{self._sweepParamName}<br>({self._sweepParamParentName})",
            attr="value",
            value=oldY1MapValue,
        )
        self.setParameter(
            rowIdx="X2",
            colName=f"{self._sweepParamName}<br>({self._sweepParamParentName})",
            attr="value",
            value=oldY2MapValue,
        )
        self.setParameter(
            rowIdx="Y1", colName=self._rawYName, attr="value", value=oldX1RawValue
        )
        self.setParameter(
            rowIdx="Y2", colName=self._rawYName, attr="value", value=oldX2RawValue
        )
        self.setParameter(
            rowIdx="Y1", colName="mappedY", attr="value", value=oldX1MapValue
        )
        self.setParameter(
            rowIdx="Y2", colName="mappedY", attr="value", value=oldX2MapValue
        )

        self.blockSignals(False)

        self.emitUpdateBox()
        self.sendXCaliFunc()
        self.sendYCaliFunc()
        self.emitUpdatePrefitModel()

    def emitAllUpdateBoxes(self):
        """
        need to be updated in the future to cope with case where the data source
        is provided as a table entry.
        """
        for rowIdx, colDict in self.parameters.items():
            for colName, param in colDict.items():
                # if param.paramType not in ["data_source"]:
                self.emitUpdateBox(rowIdx, colName, "value")

    # signals ==========================================================
    def emitUpdateBox(
        self,
        rowIdx: Optional[str] = None,
        colName: Optional[str] = None,
        attr: Optional[str] = None,
    ):
        """
        Emit the signal to update the view.

        Parameters
        ----------
        rowIdx: Optional[str]
            The row index of the parameter.
        colName: Optional[str]
            The column name of the parameter.
        attr: Optional[str]
            The attribute of the parameter.
        """
        self._emitUpdateBox(self, parentName=rowIdx, paramName=colName, attr=attr)

    def sendXCaliFunc(self):
        """
        The function that updates the calibration function. Triggers when:
            - line editing acction triggers storeParamAttr
            - XY swap triggers swapXYData
            - entering raw X by clicking on the plot triggers processSelectedPtFromPlot
        """
        self.xCaliUpdated.emit(self.XCalibration())

    def sendYCaliFunc(self):
        """
        The function that updates the calibration function. Triggers when:
            - line editing acction triggers storeParamAttr
            - XY swap triggers swapXYData
            - entering raw Y by clicking on the plot triggers processSelectedPtFromPlot
        """
        self.yCaliUpdated.emit(self.YCalibration(), self.invYCalibration())

    def emitUpdatePrefitModel(self):
        """Update everything in prefit model"""
        for rowName, paramDictByParent in self.items():
            for colName, param in paramDictByParent.items():
                if self._prefitHas(rowName, colName):
                    # update min, max, value for the prefit model
                    min, max = self._fitMinMaxByColName(rowName, colName)
                    self.updatePrefitModel.emit(ParamAttr(rowName, colName, "min", min))
                    self.updatePrefitModel.emit(ParamAttr(rowName, colName, "max", max))
                    self.updatePrefitModel.emit(
                        ParamAttr(
                            rowName,
                            colName,
                            "value",
                            param.value,
                        )
                    )
