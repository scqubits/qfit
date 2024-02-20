from abc import ABC, abstractmethod, abstractproperty
import numpy as np

from PySide6.QtCore import QObject, Signal, Slot, SignalInstance

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem
from scqubits.core.circuit import Circuit

from qfit.models.parameter_settings import ParameterType
from qfit.models.registry import RegistryEntry, Registrable
from qfit.widgets.grouped_sliders import SLIDER_RANGE
from qfit.models.parameter_settings import QSYS_PARAM_NAMES, DEFAULT_PARAM_MINMAX
from qfit.utils.helpers import sweepParamByHS

from typing import (
    Dict,
    List,
    Union,
    overload,
    Tuple,
    Callable,
    Literal,
    Any,
    TypeVar,
    Generic,
    Optional,
    Type,
)

from qfit.models.data_structures import (
    ParamBase,
    QMSweepParam,
    DispParamBase,
    QMSliderParam,
    QMFitParam,
    ParamAttr,
    CaliTableRowParam,
    ParentType,
)

ParamCls = TypeVar("ParamCls", bound="ParamBase")


class ParamSet(Registrable, Generic[ParamCls]):
    """
    A class to store all the parameters of a general model
    """

    def __init__(self, paramCls: Type[ParamCls]):
        self.paramCls = paramCls

        self.parameters: Dict[
            str,
            Dict[str, ParamCls],
        ] = {}

    def keys(self):
        return self.parameters.keys()

    def values(self):
        return self.parameters.values()

    def items(self):
        return self.parameters.items()

    def __getitem__(self, key: str):
        return self.parameters[key]

    def __len__(self):
        return sum([len(para_dict) for para_dict in self.parameters.values()])

    def paramNamesDict(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of parameter names for each parent system.
        """
        return {
            parentName: list(para_dict.keys())
            for parentName, para_dict in self.parameters.items()
        }

    def clear(self):
        """
        Clean the parameter set.
        """
        self.parameters = {}

    def getParameter(
        self,
        parentName: str,
        name: str,
        attr: str = "value",
    ) -> Union[Dict[str, Any], Any]:
        """
        Get the value of the parameters of a parent system (either a QuantumSystem
        object or a HilbertSpace object). If the name is of the parameter is not
        provided, then return a dictionary of all the parameters of the parent system.

        Parameters
        ----------
        parent_system: Union[QuantumSystem, HilbertSpace]
            The quantum model
        name: str
            The name of the parameter

        Returns
        -------
        The value of the parameter(s)
        """

        try:
            para_dict = self[parentName]
        except KeyError:
            raise KeyError(
                f"Cannot find parent system {parentName} in the parameter set."
            )

        return getattr(para_dict[name], attr)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float, str, None],
    ):
        """
        Set the value of the parameter of a parent system.

        Parameters
        ----------
        parent_system: str
            The parent
        name: str
            The name of the parameter
        value: Union[float, int]
            The value of the parameter
        """

        try:
            para_dict = self[parentName]
        except KeyError:
            raise KeyError(
                f"Cannot find parent system {parentName} in the parameter set."
            )

        try:
            setattr(para_dict[name], attr, value)
        except KeyError:
            raise KeyError(f"Cannot find parameter {name} in the parameter set.")

    def toParamDict(self) -> Dict[str, ParamCls]:
        """
        Provide a way to iterate through the parameter set.

        Return a dictionary of all the parameters in the parameter set. Keys are "<parent name>.<parameter name>"
        """
        param_dict = {}
        for parent_name, para_dict in self.parameters.items():
            for name, para in para_dict.items():
                param_dict[f"{parent_name}.{name}"] = para

        return param_dict

    def exportAttrDict(self, attribute: str = "value") -> Dict[str, Any]:
        """
        Convert the parameter set to a dictionary. Keys are "<parent name>.<parameter name>"
        and values are the value of the parameter.

        Parameters
        ----------
        attribute: str
        """
        paramval_dict = {}
        for parent_name, para_dict in self.parameters.items():
            for name, para in para_dict.items():
                paramval_dict[f"{parent_name}.{name}"] = getattr(para, attribute)

        return paramval_dict

    def loadAttrDict(
        self,
        paramval_dict: Union[Dict[str, float], Dict[str, int]],
        attribute: str = "value",
    ):
        """
        Provide a way to iterate through the parameter set.

        Update the parameter set from a dictionary. Keys are "<parent name>.<parameter name>"
        and values are the value of the parameter.
        """
        for key, value in paramval_dict.items():
            parent_name, name = key.split(".")
            self.setParameter(parent_name, name, attribute, value)


class HSParamSet(ParamSet[ParamCls], Generic[ParamCls]):
    """
    A class to store all the parameters of a HilbertSpace object
    """

    def __init__(self, hilbertspace: HilbertSpace, paramCls: Type[ParamCls]):
        super().__init__(paramCls)

        self.hilbertspace = hilbertspace
        self.parentNameByObj: Dict[ParentType, str] = {}
        self.parentObjByName: Dict[str, ParentType] = {}

    def _generateParamDictForCircuit(self, subsystem: Circuit) -> Dict[str, List[str]]:
        """
        generate parameter dict for a Circuit instance, conforming with those stored in
        QSYS_PARAM_NAMES
        """
        parameters = {}
        # loop over branches to search for symbolic EJ, EC, EL
        branches = subsystem.symbolic_circuit.branches
        EJ_list = []
        EC_list = []
        EL_list = []
        for branch in branches:
            if branch.type == "L":
                # check if the EL parameter is a symbol
                if type(branch.parameters["EL"]) is not float:
                    # get the parameter string
                    param_name = branch.parameters["EL"].name
                    # if the parameter is not in the list, append to the EL list
                    if param_name not in EL_list:
                        EL_list.append(param_name)
            elif branch.type == "C":
                if type(branch.parameters["EC"]) is not float:
                    param_name = branch.parameters["EC"].name
                    if param_name not in EC_list:
                        EC_list.append(param_name)
            elif branch.type == "JJ":
                if type(branch.parameters["ECJ"]) is not float:
                    param_name = branch.parameters["ECJ"].name
                    if param_name not in EC_list:
                        EC_list.append(param_name)
                if type(branch.parameters["EJ"]) is not float:
                    param_name = branch.parameters["EJ"].name
                    if param_name not in EJ_list:
                        EJ_list.append(param_name)
        parameters["EL"] = EL_list
        parameters["EJ"] = EJ_list
        parameters["EC"] = EC_list
        parameters["flux"] = [
            external_flux.name for external_flux in subsystem.external_fluxes
        ]
        parameters["ng"] = [
            offset_charge.name for offset_charge in subsystem.offset_charges
        ]
        parameters["cutoff"] = subsystem.cutoff_names
        parameters["truncated_dim"] = ["truncated_dim"]
        return parameters

    def insertParamToSet(
        self,
        included_parameter_type: Union[List[ParameterType], None] = None,
        excluded_parameter_type: Union[List[ParameterType], None] = None,
    ) -> None:
        """
        Add parameters to a QuantumModelParameterSet object for the HilbertSpace object
        for parameters that are supposed to be adjusted by using sliders or by using parameter sweeps.
        User may optionally specify parameter types that are excluded/included.

        Parameters:
        -----------
        parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object.
        parameter_type: Literal["slider", "sweep", "fit"]
            The type of the parameter.
        included_parameter_type: List[ParameterType]
            A list of parameter types that are included in the returned parameter set.
        excluded_parameter_type: List[ParameterType]
            A list of parameter types that are excluded in the returned parameter set.
        """

        if self.parameters != {}:
            self.clear()

        if included_parameter_type is not None and excluded_parameter_type is not None:
            raise ValueError(
                "Only one of included_parameter_type or excluded_parameter_type can be specified."
            )

        # obtain all the parameters in the subsystems of the HilbertSpace object
        subsystems = self.hilbertspace.subsystem_list
        for subsystem in subsystems:
            # obtain the available parameters in the subsystem
            subsystem_type = subsystem.__class__
            # if the subsystem is not a Circuit instance, look up parameters from
            # QSYS_PARAM_NAMES
            if subsystem_type is not Circuit:
                parameters = QSYS_PARAM_NAMES[subsystem_type]
            # else, generate parameter lookup dict for the circuit
            else:
                parameters = self._generateParamDictForCircuit(subsystem)

            # loop over different types of the parameters
            for parameter_type, parameter_names in parameters.items():
                # check if the parameter type is included or excluded
                if (
                    (included_parameter_type is not None)
                    and (parameter_type not in included_parameter_type)
                ) or (
                    (excluded_parameter_type is not None)
                    and (parameter_type in excluded_parameter_type)
                ):
                    continue

                # for each parameter type, loop over the parameters
                for parameter_name in parameter_names:
                    range_dict = DEFAULT_PARAM_MINMAX[parameter_type]
                    # value = range_dict["min"] * 4/5 + range_dict["max"] * 1/5
                    value = getattr(subsystem, parameter_name)

                    self._insertParamByArgs(
                        paramName=parameter_name,
                        parent=subsystem,
                        paramType=parameter_type,
                        value=value,
                        rangeDict=range_dict,
                    )

        #  add interaction strengths to the parameter set
        if (
            (included_parameter_type is not None)
            and ("interaction_strength" not in included_parameter_type)
        ) or (
            (excluded_parameter_type is not None)
            and ("interaction_strength" in excluded_parameter_type)
        ):
            pass
        else:
            interactions = self.hilbertspace.interaction_list
            for interaction_term_index in range(len(interactions)):
                value = interactions[interaction_term_index].g_strength

                if isinstance(value, complex):
                    raise ValueError(
                        "The interaction strength is complex. "
                        "The current implementation does not support complex interaction strength."
                    )

                self._insertParamByArgs(
                    paramName=f"g{interaction_term_index+1}",
                    parent=self.hilbertspace,
                    paramType="interaction_strength",
                    value=value,
                    rangeDict=DEFAULT_PARAM_MINMAX["interaction_strength"],
                )

    @staticmethod
    def parentSystemNames(
        parent: ParentType,
        with_type: bool = True,
    ) -> str:
        if isinstance(parent, HilbertSpace):
            return "Interactions"
        elif isinstance(parent, QuantumSystem):
            parent_name = f"{parent.id_str}"
            if with_type:
                parent_name += f" ({parent.__class__.__name__})"
            return parent_name
        else:
            raise ValueError(
                f"Parent of parameter {parent} is not a QuantumSystem or HilbertSpace object."
            )

    @staticmethod
    def parentSystemIdstrByName(name: str) -> str:
        """
        An inverse function of parentSystemNames
        """
        return "".join(name.split(" ")[:-1])

    def _updateNameMap(self, parent: ParentType, with_type: bool = True):
        name = self.parentSystemNames(parent, with_type=with_type)
        if name not in self.parentObjByName.keys():
            self.parentNameByObj[parent] = name
            self.parentObjByName[name] = parent

    def _insertParamByArgs(
        self,
        paramName: str,
        parent: ParentType,
        paramType: str,
        value: Union[int, float],
        rangeDict: Dict,
    ):
        """
        Create a Parameter object and add it to the parameter set.
        """

        # process the keyword arguments based on the needed arguments for the parameter class
        kwargs = {
            "name": paramName,
            "parent": parent,
            "paramType": paramType,
        }

        if self.paramCls is QMSliderParam:
            kwargs["value"] = value
            kwargs.update(rangeDict)

        elif self.paramCls is QMSweepParam:
            kwargs["value"] = value

        elif self.paramCls is QMFitParam:
            pass

        else:
            raise ValueError("The parameter class is not supported.")

        # create the parameter object
        param = self.paramCls(**kwargs)

        # insert the parameter object to the parameter set
        self._updateNameMap(param.parent)
        parentName = self.parentNameByObj[param.parent]
        if parentName not in self.parameters.keys():
            self.parameters[parentName] = {}

        # add the parameter to the parameter set
        self[parentName][param.name] = param

    def clear(self):
        """
        Clean the parameter set.
        """
        super().clear()
        self.parentNameByObj = {}
        self.parentObjByName = {}


DispParamCls = TypeVar("DispParamCls", bound="DispParamBase")


class ParamModelMixin(QObject, Generic[DispParamCls]):
    attrs: List[str] = ["value"]

    updateBox = Signal(ParamAttr)

    def _registerAttr(
        self,
        paramSet: ParamSet[DispParamCls],
        parentName: str,
        paramName: str,
        attr: str,
    ) -> RegistryEntry:
        """
        This method set
        """
        entryName = ".".join([type(self).__name__, parentName, paramName, attr])

        return RegistryEntry(
            name=entryName,
            quantity_type="r+",
            getter=lambda: paramSet.getParameter(parentName, paramName, attr),
            setter=lambda value: paramSet.setParameter(
                parentName, paramName, attr, value
            ),
        )

    def _registerAll(
        self,
        paramSet: ParamSet[DispParamCls],
    ) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters in the parameter set
        """
        # start from an empty registry
        registry = {}
        for parentName, paraDict in paramSet.items():
            for paraName, para in paraDict.items():
                for attr in para.attrToRegister:
                    entry = self._registerAttr(paramSet, parentName, paraName, attr)
                    registry[entry.name] = entry
        return registry

    # Signals ==========================================================
    def _emitAttrByName(
        self,
        paramSet: ParamSet[DispParamCls],
        signalToEmit: SignalInstance,
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
        attr: Optional[str] = None,
        **kwargs,
    ):
        """
        Emit the signals to update the view.
        """
        # select the parent system
        if parentName is None:
            parentDict2Iter = paramSet
        else:
            parentDict2Iter = {parentName: paramSet[parentName]}

        # iterate through the parent systems
        for prtNm, prmDict in parentDict2Iter.items():
            # select the parameter
            if paramName is None:
                paramDict2Iter = prmDict
            else:
                paramDict2Iter = {paramName: prmDict[paramName]}

            # iterate through the parameters
            for prmNm, prm in paramDict2Iter.items():
                # select the attribute
                if attr is None:
                    attrs2Iter = self.attrs
                else:
                    attrs2Iter = [attr]

                # iterate through the attributes
                for at in attrs2Iter:
                    paramAttr = ParamAttr(
                        prtNm, prmNm, at, prm.exportAttr(at, **kwargs)
                    )
                    signalToEmit.emit(paramAttr)

    def _emitUpdateBox(
        self,
        paramSet: ParamSet[DispParamCls],
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
        attr: Optional[str] = None,
    ):
        self._emitAttrByName(
            paramSet,
            self.updateBox,
            parentName=parentName,
            paramName=paramName,
            attr=attr,
        )

    # Slots ============================================================
    @Slot(ParamAttr)
    def _storeParamAttr(
        self,
        paramSet: ParamSet[DispParamCls],
        paramAttr: ParamAttr,
        **kwargs,
    ):
        param = paramSet[paramAttr.parantName][paramAttr.name]
        param.storeAttr(paramAttr.attr, paramAttr.value, **kwargs)


class CombinedMeta(type(ParamModelMixin), type(ParamSet)):
    pass


class HSParamModel(
    HSParamSet[DispParamCls],
    ParamModelMixin[DispParamCls],  # ordering matters
    Generic[DispParamCls],
    metaclass=CombinedMeta,
):
    hspaceUpdated = Signal(HilbertSpace)

    def __init__(self, hilbertspace: HilbertSpace, paramCls: Type[DispParamCls]):
        # ordering matters here
        HSParamSet.__init__(self, hilbertspace, paramCls)
        ParamModelMixin.__init__(self)
        attrs = self.paramCls.attrToRegister

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Not only set the parameter, but also emit the signal to update the view.

        A key method in updating the model by the internal processes.
        """
        super().setParameter(parentName, name, attr, value)

        self.emitUpdateBox(parentName, name, attr)

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        return self._registerAll(self)

    # Signals ==========================================================
    def emitUpdateBox(
        self,
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
        attr: Optional[str] = None,
    ):
        self._emitUpdateBox(self, parentName=parentName, paramName=paramName, attr=attr)

    def emitHspaceUpdated(self):
        self.hspaceUpdated.emit(self.hilbertspace)

    # Slots ============================================================
    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        super()._storeParamAttr(self, paramAttr, **kwargs)

    @Slot(str, str)
    def updateParent(
        self,
        parentName: str,
        paramName: str,
    ):
        param = self[parentName][paramName]
        param.setParameterForParent()
        self.emitHspaceUpdated()


class PrefitParamModel(HSParamModel[QMSliderParam]):
    updateSlider = Signal(ParamAttr)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Set the parameter, emit the signal to update the box and sliders.
        """
        super().setParameter(parentName, name, attr, value)

        self.emitUpdateSlider(parentName, name)

    def emitUpdateSlider(
        self,
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
    ):
        self._emitAttrByName(
            self,
            self.updateSlider,
            parentName=parentName,
            paramName=paramName,
            attr="value",
            toSlider=True,
        )

    @Slot()
    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        fromSlider: bool = False,
    ):
        """
        Store the data from the view
        """
        super().storeParamAttr(paramAttr, fromSlider=fromSlider)

        if paramAttr.attr == "value":
            if fromSlider:
                self.emitUpdateBox(paramAttr.parantName, paramAttr.name, paramAttr.attr)
            elif not fromSlider:
                self.emitUpdateSlider(paramAttr.parantName, paramAttr.name)
        elif paramAttr.attr in ["min", "max"]:
            self.emitUpdateSlider(paramAttr.parantName, paramAttr.name)


class CaliParamModel(
    ParamSet[CaliTableRowParam],
    ParamModelMixin[CaliTableRowParam],  # ordering matters
    metaclass=CombinedMeta,
):
    plotCaliPtExtractStart = Signal(str)
    plotCaliPtExtractFinished = Signal()
    plotCaliPtExtractInterrupted = Signal()
    issueNewXCaliFunc = Signal(object)
    issueNewYCaliFunc = Signal(object)
    issueNewInvYCaliFunc = Signal(object)
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
        hilbertSpace: HilbertSpace,
        rawXVecNameList: List[str],
        rawYName: str,
        figName: List[str],
    ):
        self._hilbertSpace = hilbertSpace
        self.rawXVecNameList = rawXVecNameList
        self.rawYName = rawYName
        self.figName = figName
        self.sweepParamSet = sweepParamByHS(hilbertSpace)

        # determine total calibration table row number and if the calibration is a complete one
        
        self._isSufficientForFullCalibration(self.rawXVecDim, self.figNr)

        # initialize calibration table entries
        self.insertParamToSet()

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

    def insertParamToSet(self):
        if self.parameters != {}:
            self.clear()

        # insert calibration table parameters for each row for X
        for XRowIdx in self.caliTableXRowIdxList:
            # loop over the raw vector components
            for rawVecCompName in self.rawXVecNameList:
                self._insertParamByArgs(
                    colName=rawVecCompName,
                    rowIdx=XRowIdx,
                    paramType="raw_X_vec_component",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=0,
                )
            # loop over the mapped vector components (given by sweep parameters)
            for parentName, paramDictByParent in self.sweepParamSet.items():
                for paramName, param in paramDictByParent.items():
                    self._insertParamByArgs(
                        colName=f"{parentName}.{paramName}",
                        rowIdx=XRowIdx,
                        paramType=param.paramType,
                        sweepParamName=paramName,
                        value=0,
                        parentSystemName=parentName,
                    )
            # insert the point pair source
            if self.isFullCalibration:
                self._insertParamByArgs(
                    colName="pointPairSource",
                    rowIdx=XRowIdx,
                    paramType="point_pair_source",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=None,
                )
            else:
                # value is the figure name
                self._insertParamByArgs(
                    colName="pointPairSource",
                    rowIdx=XRowIdx,
                    paramType="point_pair_source",
                    parentSystemName=None,
                    sweepParamName=None,
                    value=self.figName[int(XRowIdx[1:]) // 2],
                )
        # insert calibration table parameters for Y: raw vector,
        for YRowIdx in self.caliTableYRowIdxList:
            self._insertParamByArgs(
                colName=self.rawYName,
                rowIdx=YRowIdx,
                paramType="raw_Y",
                parentSystemName=None,
                sweepParamName=None,
                value=0,
            )
            self._insertParamByArgs(
                colName="mappedY",
                rowIdx=YRowIdx,
                paramType="mapped_Y",
                sweepParamName=None,
                value=0,
                parentSystemName=None,
            )
            self._insertParamByArgs(
                colName="pointPairSource",
                rowIdx=YRowIdx,
                paramType="point_pair_source",
                sweepParamName=None,
                value=None,
                parentSystemName=None,
            )

    def _insertParamByArgs(
        self,
        colName: str,
        rowIdx: str,
        paramType: str,
        parentSystemName: Optional[str],
        sweepParamName: Optional[str],
        value: Optional[Union[int, float, str]],
    ):
        """
        Create a Parameter object and add it to the parameter set. Notice that this method
        has a dual version in the HSParamSet class.
        """

        # process the keyword arguments based on the needed arguments for the parameter class
        kwargs = {
            "colName": colName,
            "rowIdx": rowIdx,
            "paramType": paramType,
            "parentSystemName": parentSystemName,
            "sweepParamName": sweepParamName,
            "value": value,
        }

        # create the parameter object
        param = CaliTableRowParam(**kwargs)

        # add the parameter to the parameter set
        if rowIdx not in self.parameters.keys():
            self.parameters[rowIdx] = {}
        self.parameters[rowIdx][colName] = param

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


    # calibrate the raw vector to the mapped vector ====================
    def _YCalibration(self) -> Callable:
        """
        Generate a function that applies the calibration to the raw Y value.
        """
        alphaVec = self._getAlphaVec()

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

    def _invYCalibration(self) -> Callable:
        """
        Generate a function that applies the inverse calibration to the mapped Y value.
        """
        alphaVec = self._getAlphaVec()

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

    def _getAlphaVec(self) -> np.ndarray:
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
        for XRowIdx in self.caliTableXRowIdxList:
            augRawXMat[XRowIdx, 0] = 1
            for colIdx, rawXVecCompName in enumerate(self.rawXVecNameList):
                augRawXMat[XRowIdx, colIdx + 1] = self[XRowIdx][rawXVecCompName].value
        # loop over sweep parameters
        # assemble sweep parameter set, add sweep parameters to the parameter set

        sweepParamSetFromCali = HSParamSet[QMSweepParam](
            self.hilbertSpace, QMSweepParam
        )
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
                for XRowIdx in self.caliTableXRowIdxList:
                    mapCompVec[XRowIdx] = self[XRowIdx][
                        f"{param.parent}.{param.name}"
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
            sweepParamSetFromCali = HSParamSet[QMSweepParam](
                self.hilbertSpace, QMSweepParam
            )
            for parentName, paramDictByParent in self.sweepParamSet.items():
                for paramName, param in paramDictByParent.items():
                    # extract mapped vector pair values
                    mapXVecCompValue1 = self[XRowIdxList[0]][
                        f"{param.parent}.{param.name}"
                    ].value
                    mapXVecCompValue2 = self[XRowIdxList[1]][
                        f"{param.parent}.{param.name}"
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
    
    # slots & public interface ================================================
    @Slot()
    def updateStatusFromCaliView(self, status: Union[str, Literal[False]]):
        self.caliStatus = status
        if status != False:
            if type(status) is int:
                destination = "CALI_X"
            else:
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

    def processSelectedPtFromPlot(self, data: Dict[str, float], figName: str):
        """
        Called by the canvas click event. Process and store the calibration data.
        """
        # get current label
        caliLabel = self.caliStatus  # can be int or str
        # based on the current label, we know the row index to store the data
        # store the calibration data
        # if the current label is int, then it is for X
        if caliLabel is not False:
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
        super()._storeParamAttr(self, paramAttr, **kwargs)
    
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
        The function that updates the calibration function.
        """
        if self.isFullCalibration:
            self.issueNewXCaliFunc.emit(self._fullXCalibration)
        else:
            self.issueNewXCaliFunc.emit(self._partialXCalibration)

    def sendYCaliFunc(self):
        """
        The function that updates the calibration function.
        """
        self.issueNewYCaliFunc.emit(self._YCalibration)

    def sendInvYCaliFunc(self):
        """
        The function that updates the calibration function.
        """
        self.issueNewInvYCaliFunc.emit(self._invYCalibration)
