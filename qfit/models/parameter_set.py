from abc import ABC, abstractmethod, abstractproperty
import numpy as np
from copy import deepcopy

from PySide6.QtCore import QObject, Signal, Slot, SignalInstance

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem
from scqubits.core.circuit import Circuit

from qfit.models.parameter_settings import ParameterType
from qfit.models.registry import RegistryEntry, Registrable
from qfit.widgets.grouped_sliders import SLIDER_RANGE
from qfit.models.parameter_settings import QSYS_PARAM_NAMES, DEFAULT_PARAM_MINMAX

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
    SliderParam,
    FitParam,
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

    def insertParam(
        self,
        parentName: str,
        paramName: str,
        param: ParamCls,
    ):
        """
        Insert a parameter to the parameter set. When the parent system is
        not in the parameter set, create a new entry for the parent system.
        """
        if parentName not in self.parameters.keys():
            self.parameters[parentName] = {}
        self.parameters[parentName][paramName] = param

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

        print(f"parentName: {parentName}, name: {name}, attr: {attr}")

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

    def setParamByPA(
        self,
        paramAttr: ParamAttr,
    ):
        self.setParameter(
            paramAttr.parentName,
            paramAttr.name,
            paramAttr.attr,
            paramAttr.value,
        )

    def toParamDict(self) -> Dict[str, ParamCls]:
        """
        Provide a way to iterate through the parameter set. Used for fitting purposes
        - as we need to provide a single-layer dictionary.

        Return a dictionary of all the parameters in the parameter set. Keys are "<parent name>.<parameter name>"
        """
        param_dict = {}
        for parent_name, para_dict in self.parameters.items():
            for name, para in para_dict.items():
                if "." in parent_name:
                    raise ValueError(
                        "The parent name should not contain the character '.'."
                    )
                
                param_dict[f"{parent_name}.{name}"] = para

        return param_dict

    def getAttrDict(self, attribute: str = "value") -> Dict[str, Any]:
        """
        Provide a way to iterate through the parameter set. Used for fitting purposes
        - as we need to provide a single-layer dictionary.

        Convert the parameter set to a dictionary. Keys are "<parent name>.<parameter name>"
        and values are the value of the parameter.

        Parameters
        ----------
        attribute: str
        """
        paramval_dict = {}
        for parent_name, para_dict in self.parameters.items():
            for name, para in para_dict.items():
                if "." in parent_name:
                    raise ValueError(
                        "The parent name should not contain the character '.'."
                    )

                paramval_dict[f"{parent_name}.{name}"] = getattr(para, attribute)

        return paramval_dict

    def setByAttrDict(
        self,
        paramval_dict: Union[Dict[str, float], Dict[str, int]],
        attribute: str = "value",
    ):
        """
        Provide a way to iterate through the parameter set. Used for fitting purposes
        - as we need to provide a single-layer dictionary.

        Update the parameter set from a dictionary. Keys are "<parent name>.<parameter name>"
        and values are the value of the parameter.
        """
        for key, value in paramval_dict.items():
            splitted_key = key.split(".")
            parent_name = splitted_key[0]   # str before the first "."
            name = ".".join(splitted_key[1:])   # str after the first "."
            self.setParameter(parent_name, name, attribute, value)

    def setAttrByParamDict(
        self,
        paramSet: "ParamSet",
        attrsToUpdate: Optional[List[str]] = None,
        insertMissing: bool = False,
    ):
        """
        Set the whole parameter set by a dictionary of parameters. The dictionary should
        have the same structure as the parameters attribute of the ParamSet object.
        setParameter/insertParam is called to update the parameter set.
        """
        if attrsToUpdate is not None and insertMissing:
            raise ValueError(
                "When insertMissing is True, attrsToUpdate should be None. "
                "Meaning that all of the attibutes of the parameters will "
                "be inserted for the missing parameter."
            )

        for parentName, paraDict in paramSet.items():
            # check if the parent system is in the parameter set
            if parentName not in self.parameters.keys():
                if insertMissing:
                    self.parameters[parentName] = {}
                else:
                    raise ValueError(
                        f"Parent system {parentName} is not in the parameter set."
                    )

            for paramName, param in paraDict.items():
                # check if the parameter is in the parameter set
                if paramName not in self.parameters[parentName].keys():
                    if insertMissing:
                        self.insertParam(parentName, paramName, param)
                        continue
                    else:
                        raise ValueError(
                            f"Parameter {paramName} is not in the parameter set."
                        )

                # update the parameter for all the attributes
                if attrsToUpdate is None:
                    attrsToUpdate = dir(param)
                for attr in attrsToUpdate:
                    if attr.startswith("_"):
                        continue
                    self.setParameter(parentName, paramName, attr, getattr(param, attr))


class HSParamSet(ParamSet[ParamCls], Generic[ParamCls]):
    """
    A class to store all the parameters of a HilbertSpace object
    """

    hilbertspace: HilbertSpace

    def __init__(self, paramCls: Type[ParamCls]):
        super().__init__(paramCls)

        self.parentNameByObj: Dict[ParentType, str] = {}
        self.parentObjByName: Dict[str, ParentType] = {}

    def dynamicalInit(
        self,
        hilbertspace: HilbertSpace,
        included_parameter_type: Union[List[ParameterType], None] = None,
        excluded_parameter_type: Union[List[ParameterType], None] = None,
    ):
        self.hilbertspace = hilbertspace
        self.insertAllParams(
            included_parameter_type=included_parameter_type,
            excluded_parameter_type=excluded_parameter_type,
        )

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

    def insertAllParams(
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
        with_type: bool = False,
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
    def parentSystemIdstrByName(name: str, with_type: bool = False) -> str:
        """
        An inverse function of parentSystemNames
        """
        if with_type:
            return "".join(name.split(" ")[:-1])
        else:
            return name

    def _updateNameMap(self, parent: ParentType):
        name = self.parentSystemNames(parent)
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

        if self.paramCls is SliderParam:
            kwargs["value"] = value
            kwargs.update(rangeDict)

        elif self.paramCls is QMSweepParam:
            kwargs["value"] = value

        elif self.paramCls is FitParam:
            pass

        else:
            raise ValueError("The parameter class is not supported.")

        # create the parameter object
        param = self.paramCls(**kwargs)

        # insert the parameter object to the parameter set
        self._updateNameMap(param.parent)
        parentName = self.parentNameByObj[param.parent]

        self.insertParam(parentName, paramName, param)

    def clear(self):
        """
        Clean the parameter set.
        """
        super().clear()
        self.parentNameByObj = {}
        self.parentObjByName = {}

    @classmethod
    def sweepSetByHS(cls, hilbertSpace: HilbertSpace) -> "ParamSet[QMSweepParam]":
        sweepParameterSet = HSParamSet(QMSweepParam)
        sweepParameterSet.dynamicalInit(
            hilbertSpace,
            included_parameter_type=["ng", "flux"],
        )
        return sweepParameterSet


DispParamCls = TypeVar("DispParamCls", bound="DispParamBase")


class ParamModelMixin(QObject, Generic[DispParamCls]):
    attrs: List[str] = ["value"]

    updateBox = Signal(ParamAttr)

    # def _registerAttr(
    #     self,
    #     paramSet: ParamSet[DispParamCls],
    #     parentName: str,
    #     paramName: str,
    #     attr: str,
    # ) -> RegistryEntry:
    #     """
    #     This method set
    #     """
    #     entryName = ".".join([type(self).__name__, parentName, paramName, attr])

    #     return RegistryEntry(
    #         name=entryName,
    #         quantity_type="r+",
    #         getter=lambda: paramSet.getParameter(parentName, paramName, attr),
    #         setter=lambda value: paramSet.setParameter(
    #             parentName, paramName, attr, value
    #         ),
    #     )

    # def _registerAll(
    #     self,
    #     paramSet: ParamSet[DispParamCls],
    # ) -> Dict[str, RegistryEntry]:
    #     """
    #     Register all the parameters in the parameter set
    #     """
    #     # start from an empty registry
    #     registry = {}
    #     for parentName, paraDict in paramSet.items():
    #         for paraName, para in paraDict.items():
    #             for attr in para.attrToRegister:
    #                 print(f"parentName: {parentName}, paraName: {paraName}, attr: {attr}")
    #                 entry = self._registerAttr(paramSet, parentName, paraName, attr)
    #                 registry[entry.name] = entry
    #     return registry

    def _registrySetter(
        self, 
        value: Dict[str, Dict[str, DispParamCls]],
        paramSet: ParamSet[DispParamCls]
    ):
        paramSet.parameters = value

        for parentName, paraDict in value.items():
            for paraName, para in paraDict.items():
                for attr in para.attrToRegister:
                    self._emitUpdateBox(paramSet, parentName, paraName, attr)
    
    def _registerAll(
        self,
        paramSet: ParamSet[DispParamCls],
    ) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters in the parameter set
        """

        return {type(self).__name__: RegistryEntry(
            name=type(self).__name__,
            quantity_type="r+",
            getter=lambda: paramSet.parameters,
            setter=lambda value: self._registrySetter(value, paramSet),
        )}


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
        Emit the signals to update the view. When the parentName, paramName,
        and attr are not provided, emit the signals for all the parameters.
        Especially, when the attr is not provided, emit the signals for all the
        attributes (usually attr_to_register) of the parameter.
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
        param = paramSet[paramAttr.parentName][paramAttr.name]
        param.storeAttr(paramAttr.attr, paramAttr.value, **kwargs)

