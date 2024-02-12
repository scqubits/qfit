from abc import ABC, abstractmethod, abstractproperty
import numpy as np

from PySide6.QtCore import QObject, Signal, Slot, SignalInstance

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem
from scqubits.core.circuit import Circuit

from qfit.models.data_structures import (
    ParamBase, QMSweepParam, DispParamBase, QMSliderParam, QMFitParam, ParamAttr
)
from qfit.models.parameter_settings import ParameterType
from qfit.models.registry import RegistryEntry, Registrable
from qfit.widgets.grouped_sliders import SLIDER_RANGE
from qfit.models.parameter_settings import QSYS_PARAM_NAMES, DEFAULT_PARAM_MINMAX

from typing import (
    Dict, List, Union, overload, Tuple, Callable, Literal, Any, 
    TypeVar, Generic, Optional, Type
)

ParentSystem = Union[QuantumSystem, HilbertSpace]
ParamCls = TypeVar("ParamCls", bound="ParamBase")


class CombinedMeta(type(QObject), type(Registrable)):
    pass


class ParamSet(QObject, Registrable, Generic[ParamCls], metaclass=CombinedMeta):
    """
    A class to store all the parameters of a quantum system
    """

    def __init__(self, hilbertspace: HilbertSpace, paramCls: Type[ParamCls]):
        QObject.__init__(self)

        self.hilbertspace = hilbertspace
        self.paramCls = paramCls

        self.parameters: Dict[
            ParentSystem,
            Dict[str, ParamCls],
        ] = {}

        self.parentNameByObj: Dict[ParentSystem, str] = {}
        self.parentObjByName: Dict[str, ParentSystem] = {}

    def keys(self):
        return self.parameters.keys()

    def values(self):
        return self.parameters.values()

    def items(self):
        return self.parameters.items()

    def __getitem__(self, key):
        return self.parameters[key]

    def __len__(self):
        return sum([len(para_dict) for para_dict in self.parameters.values()])

    @staticmethod
    def parentSystemNames(
        parent: ParentSystem,
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
        return ''.join(name.split(" ")[:-1])

    def _updateNameMap(self, parent: ParentSystem, with_type: bool = True):
        name = self.parentSystemNames(parent, with_type=with_type)
        self.parentNameByObj[parent] = name
        self.parentObjByName[name] = parent

    def paramNamesDict(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of parameter names for each parent system.
        """
        return {
            self.parentNameByObj[parent]: list(para_dict.keys()) 
            for parent, para_dict in self.parameters.items()
        }
    
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
                        paramName = parameter_name,
                        parent = subsystem,
                        paramType = parameter_type,
                        value = value,
                        rangeDict = range_dict,
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
                    paramName = f"g{interaction_term_index+1}",
                    parent = self.hilbertspace,
                    paramType = "interaction_strength",
                    value = value,
                    rangeDict = DEFAULT_PARAM_MINMAX["interaction_strength"],
                )
                    
    def _insertParamByArgs(
        self,
        paramName: str,
        parent: ParentSystem,
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
        if param.parent not in self.parameters:
            self.parameters[param.parent] = {}
            self._updateNameMap(param.parent)

        # add the parameter to the parameter set
        self.parameters[param.parent][param.name] = param

    def clean(self):
        """
        Clean the parameter set.
        """
        self.parameters = {}
        self.parentNameByObj = {}
        self.parentObjByName = {}

    @overload
    def getParameter(self, parent_system) -> Dict[str, float]:
        ...

    @overload
    def getParameter(self, parent_system, name: str) -> float:
        ...

    def getParameter(
        self,
        parent_system: Union[ParentSystem, str],
        name: Union[str, None] = None,
        attribute: str = "value",
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

        if isinstance(parent_system, str):
            try:
                parent_system = self.parentObjByName[parent_system]
            except KeyError:
                raise KeyError(
                    f"Cannot find parent system {parent_system} in the parameter set."
                )

        try:
            para_dict = self.parameters[parent_system]
        except KeyError:
            raise KeyError(
                f"Cannot find parent system {parent_system} in the parameter set."
            )

        name_dict = {name: getattr(para, attribute) for name, para in para_dict.items()}

        if name is None:
            return name_dict
        else:
            return name_dict[name]

    def setParameter(
        self,
        parentName: str,
        name: str,
        value: Union[int, float],
        attr: str = "value",
    ):
        """
        Set the value of the parameter of a parent system (either a QuantumSystem
        object or a HilbertSpace object).

        Parameters
        ----------
        parent_system: Union[QuantumSystem, HilbertSpace]
            The quantum model
        name: str
            The name of the parameter
        value: Union[float, int]
            The value of the parameter
        """

        try:
            parent = self.parentObjByName[parentName]
        except KeyError:
            raise KeyError(
                f"Cannot find parent system {parentName} in the parameter set."
            )

        try:
            para_dict = self.parameters[parent]
        except KeyError:
            raise KeyError(
                f"Cannot find parent system {parent} in the parameter set."
            )

        try:
            setattr(para_dict[name], attr, value)
        except KeyError:
            raise KeyError(f"Cannot find parameter {name} in the parameter set.")
        
    def toParamDict(self) -> Dict[str, ParamBase]:
        """
        Provide a way to iterate through the parameter set.

        Return a dictionary of all the parameters in the parameter set. Keys are "<parent name>.<parameter name>"
        """
        param_dict = {}
        for parent_system, para_dict in self.parameters.items():
            parent_name = self.parentNameByObj[parent_system]
            for name, para in para_dict.items():
                param_dict[f"{parent_name}.{name}"] = para

        return param_dict

    def exportAttrDict(
        self, attribute: str = "value"
    ) -> Union[Dict[str, float], Dict[str, int],]:
        """
        Convert the parameter set to a dictionary. Keys are "<parent name>.<parameter name>"
        and values are the value of the parameter.

        Parameters
        ----------
        attribute: str
        """
        paramval_dict = {}
        for parent_system, para_dict in self.parameters.items():
            parent_name = self.parentNameByObj[parent_system]
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
            self.setParameter(parent_name, name, value, attr=attribute)

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters in the parameter set
        """
        # start from an empty registry
        registry = {}
        for parent_system, para_dict in self.parameters.items():
            for para_name, para in para_dict.items():
                # loop over all parameters in parameter sets and create a registry entry
                # notice that internally, the method _toRegistryEntry is called. However,
                # the entry name is a string just like "EC", "EJ", "EL" etc. and very likely
                # repeated in different parameter sets. Therefore, we must update names for
                # each parameter.
                entry_dict = para.registerAll()

                # update the name of the parameter entry and the registry key to make it unique.
                # notice that the entry_dict is not returned directly.
                for attr_name, entry in entry_dict.items():
                    new_name = (
                        f"{self.name}"
                        f".{self.parentNameByObj[parent_system]}"
                        f".{para_name}"
                        f".{attr_name}"
                    )
                    entry.name = new_name
                    registry[new_name] = entry

        return registry
    

DispParamCls = TypeVar("DispParamCls", bound="DispParamBase")
    

class ParamModel(ParamSet[DispParamCls], Generic[DispParamCls]):
    attrs: List[str] = ["value"]

    updateBox = Signal(ParamAttr)
    hspaceUpdated = Signal(HilbertSpace)

    def setParameter(
        self, 
        parentName: str,
        name: str,
        value: Union[int, float],
        attr: str = "value",
    ):
        """
        Not only set the parameter, but also emit the signal to update the view.

        A key method in updating the model by the internal processes.
        """
        super().setParameter(parentName, name, value, attr)

        self.emitUpdateBox(parentName, name, attr)

    # Signals ==========================================================
    def _emitAttrByName(
        self, 
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
            parentDict2Iter = {
                self.parentNameByObj[prt]: prmDict for prt, prmDict in self.parameters.items()
            }
        else:
            parent = self.parentObjByName[parentName]
            parentDict2Iter = {parentName: self.parameters[parent]}
        
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
                        prtNm, prmNm, at, prm.exportAttr(
                        at, **kwargs
                    ))
                    signalToEmit.emit(paramAttr)

    def emitUpdateBox(
        self,
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
        attr: Optional[str] = None,
    ):
        self._emitAttrByName(
            self.updateBox,
            parentName=parentName,
            paramName=paramName,
            attr=attr
        )

    def emitHspaceUpdated(self):
        self.hspaceUpdated.emit(self.hilbertspace)

    # Slots ============================================================
    @Slot(ParamAttr)
    def storeParamAttr(
        self, 
        paramAttr: ParamAttr,
        updateHspace: bool = False,
        **kwargs,
    ):
        parent = self.parentObjByName[paramAttr.parantName]
        param = self[parent][paramAttr.name]
        param.storeAttr(paramAttr.attr, paramAttr.value, **kwargs)

        if updateHspace:
            param.setParameterForParent()
            self.emitHspaceUpdated()

    @Slot(str, str)
    def updateParent(
        self,
        parentName: str,
        paramName: str,
    ):
        parent = self.parentObjByName[parentName]
        param = self[parent][paramName]
        param.setParameterForParent()
        self.emitHspaceUpdated()


class PrefitParamModel(ParamModel[QMSliderParam]):
    updateSlider = Signal(ParamAttr)
    attrs = QMSliderParam.attrToRegister

    def setParameter(
        self, 
        parentName: str,
        name: str,
        value: Union[int, float],
        attr: str = "value",
    ):
        """
        Set the parameter, emit the signal to update the box and sliders.
        """
        super().setParameter(parentName, name, value, attr)

        self.emitUpdateSlider(parentName, name)

    def emitUpdateSlider(
        self, 
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
    ):
        self._emitAttrByName(
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
        super().storeParamAttr(
            paramAttr, 
            fromSlider=fromSlider
        )

        if paramAttr.attr == "value":
            if fromSlider:
                self.emitUpdateBox(
                    paramAttr.parantName, paramAttr.name, paramAttr.attr
                )
            elif not fromSlider:
                self.emitUpdateSlider(
                    paramAttr.parantName, paramAttr.name
                )
        elif paramAttr.attr in ["min", "max"]:
            self.emitUpdateSlider(
                paramAttr.parantName, paramAttr.name
            )


class FitParamModel(ParamModel[QMFitParam]):
    pass