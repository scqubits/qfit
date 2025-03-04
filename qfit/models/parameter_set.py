from PySide6.QtCore import QObject, Signal, Slot, SignalInstance

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem
from scqubits.core.circuit import Circuit

from qfit.models.parameter_settings import ParameterType
from qfit.models.registry import RegistryEntry, Registrable
from qfit.models.parameter_settings import QSYS_PARAM_NAMES, DEFAULT_PARAM_MINMAX

from typing import (
    Dict,
    List,
    Union,
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
)

ParamCls = TypeVar("ParamCls", bound="ParamBase")
ParentType = Union[HilbertSpace, QuantumSystem]


class ParamSet(Registrable, Generic[ParamCls]):
    """
    A class to store all the parameters of a general model. The parameters are
    stored in a two-layer dictionary. The first layer is the parent system name
    and the second layer is the parameter name. The value of the second layer
    dictionary is a Parameter object.

    Parameters
    ----------
    paramCls: Type[ParamCls]
        The class of the parameter, which should be a subclass of ParamBase.
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

    def __repr__(self) -> str:
        return self.parameters.__repr__()

    def __str__(self) -> str:
        return self.parameters.__str__()

    def insertParam(
        self,
        parentName: str,
        paramName: str,
        param: ParamCls,
    ):
        """
        Insert a parameter to the parameter set. When the parent system is
        not in the parameter set, create a new entry for the parent system.

        Parameters
        ----------
        parentName: str
            The name of the parent system
        paramName: str
            The name of the parameter
        param: ParamCls
            The parameter object
        """
        assert param.__class__ == self.paramCls

        if parentName not in self.parameters.keys():
            self.parameters[parentName] = {}
        self.parameters[parentName][paramName] = param

    def paramNamesDict(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of parameter names for each parent system.

        Returns
        -------
        Dict[str, List[str]]
            Lists of parameter names for each parent system.
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
        Get an attribute of a parameter.

        Parameters
        ----------
        parentName: str
            The name of the parent system
        name: str
            The name of the parameter
        attr: str
            The name of the attribute

        Returns
        -------
            The attribute of the parameter
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
        Set the attribute of a parameter (and do nothing else for view / other models).

        Parameters
        ----------
        parent_system: str
            The name of the parent system
        name: str
            The name of the parameter
        attr: str
            The name of the attribute
        value: Union[int, float, str, None]
            The value of the attribute
        """
        try:
            para_dict = self[parentName]
        except KeyError:
            raise KeyError(
                f"Cannot find parent system {parentName} in the parameter set."
            )

        if attr not in para_dict[name].dataAttr:
            raise ValueError(
                f"Attribute {attr} is not in the data attribute list of "
                "the parameter {name}. Thus can't be set externally by "
                "calling setParameter."
            )

        try:
            setattr(para_dict[name], attr, value)
        except KeyError:
            raise KeyError(f"Cannot find parameter {name} in the parameter set.")

    def setParamByPA(
        self,
        paramAttr: ParamAttr,
    ):
        """
        Given a ParamAttr object, set the attribute of a parameter.
        """
        self.setParameter(
            paramAttr.parentName,
            paramAttr.name,
            paramAttr.attr,
            paramAttr.value,
        )

    def getFlattenedAttrDict(self, attribute: str = "value") -> Dict[str, Any]:
        """
        Provide a way to iterate through the parameter set via a single-layer
        dictionary. Used for fitting purposes.

        Parameters
        ----------
        attribute: str
            The name of the attribute to be extracted from the parameter object.

        Returns
        -------
        Dict[str, Any]
            A dictionary of all the parameters in the set.
            Keys: "<parent name>.<parameter name>"
            Values: The value of the attribute of the parameter.
        """
        paramval_dict = {}
        for parent_name, para_dict in self.parameters.items():
            for name, para in para_dict.items():
                if "." in parent_name:
                    raise ValueError(
                        "The parent name should not contain the character '.'."
                    )

                paramval_dict[f"{name}<br>({parent_name})"] = getattr(para, attribute)

        return paramval_dict

    def setByFlattenedAttrDict(
        self,
        paramval_dict: Union[Dict[str, float], Dict[str, int]],
        attribute: str = "value",
    ):
        """
        Set the whole parameter set by a single-layer dictionary of parameters.
        Used for fitting purposes.

        Parameters
        ----------
        paramval_dict: Dict[str, float]
            A dictionary of all the parameters in the set.
            Keys: "<parameter name><br>(<parent name>)"
            Values: The value of the attribute of the parameter.
        attribute: str
            The name of the attribute to be set for the parameter object.

        """
        for key, value in paramval_dict.items():
            splitted_key = key.split("<br>")
            parent_name = splitted_key[-1][1:-1]  # str between "(" and ")" after "<br>"
            name = "<br>".join(splitted_key[:-1])  # str before "<br>"
            self.setParameter(parent_name, name, attribute, value)

    def getFlattenedParamDict(self) -> Dict[str, ParamCls]:
        """
        Provide a way to iterate through the parameter set via a single-layer
        dictionary. Used for fitting purposes.

        Returns
        -------
        Dict[str, ParamCls]
            A dictionary of all the parameters in the set.
            Keys: "<parent name>.<parameter name>"
            Values: The parameter object
        """
        param_dict = {}
        for parent_name, para_dict in self.parameters.items():
            for name, para in para_dict.items():
                if "<br>" in parent_name:
                    raise ValueError(
                        "The parent name should not contain the character '<br>'."
                    )

                param_dict[f"{name}<br>({parent_name})"] = para

        return param_dict

    def setAttrByParamSet(
        self,
        paramSet: "ParamSet",
        attrsToUpdate: Optional[List[str]] = None,
        insertMissing: bool = False,
    ):
        """
        Set the whole parameter set by another parameter set, which should have
        the same structure as the parameters attribute of the current set.

        setParameter/insertParam is called to update the parameter set.

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set to be used to update the current parameter set.
        attrsToUpdate: List[str]
            The attributes to be updated. If None, all the dataAttr of the
            parameters will be updated.
        insertMissing: bool
            If True, insert the missing parameters in the paramSet to the
            current parameter set. If False, raise an error when the parameter
            is not in the current parameter set.
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
                    attrsToUpdate = param.dataAttr
                for attr in attrsToUpdate:
                    self.setParameter(parentName, paramName, attr, getattr(param, attr))


class HSParamSet(ParamSet[ParamCls], Generic[ParamCls]):
    """
    A class to store all the parameters of a HilbertSpace object. It has
    additional methods to identify the parameters of a HilbertSpace object and
    to update the HilbertSpace object based on the parameter set.

    Parameters
    ----------
    paramCls: Type[ParamCls]
        The class of the parameter, which should be a subclass of ParamBase.
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
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. For HSParamSet, it will
        insert all the parameters in the HilbertSpace object to the parameter
        set.

        Parameters
        ----------
        hilbertspace: HilbertSpace
            The HilbertSpace object
        included_parameter_type: List[ParameterType]
            When inserting parameters, only the parameters with the types in
            this list will be inserted.
        excluded_parameter_type: List[ParameterType]
            When inserting parameters, the parameters with the types in this
            list will be excluded.
        """
        self.hilbertspace = hilbertspace
        self._insertAllParams(
            included_parameter_type=included_parameter_type,
            excluded_parameter_type=excluded_parameter_type,
        )

    def _paramDictForCircuit(self, subsystem: Circuit) -> Dict[str, List[str]]:
        """
        The parameter dict is used to identify the parameters of a
        Circuit object, which serves as QSYS_PARAM_NAMES for the Circuit object.
            Keys: ParameterType for the Circuit object
            Values: a list of circuit parameter names for the given type
        """
        parameters = {}
        # check if the subsystem has symbolic circuit attribute
        if not hasattr(subsystem, "symbolic_circuit"):
            parameters["EJ"] = [
                param.name for param in list(subsystem.symbolic_params.keys())
            ]
        else:
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

    def _insertAllParams(
        self,
        included_parameter_type: Union[List[ParameterType], None] = None,
        excluded_parameter_type: Union[List[ParameterType], None] = None,
    ) -> None:
        """
        Add parameters to a HSParamSet. Those parameters that are supposed to
        be adjusted by using sliders or by using parameter sweeps.
        User may optionally specify parameter types that are excluded/included.

        Parameters:
        -----------
        included_parameter_type: List[ParameterType]
            Only the parameters with the types in this list will be inserted.
        excluded_parameter_type: List[ParameterType]
            The parameters with the types in this list will be excluded.
        """

        if self.parameters != {}:
            self.clear()

        if included_parameter_type is not None and excluded_parameter_type is not None:
            raise ValueError(
                "Only one of included_parameter_type or excluded_parameter_type can be specified."
            )

        # obtain all the parameters in the subsystems of the HilbertSpace object
        subsystems = self.hilbertspace.subsystem_list
        for parentSys in subsystems:
            # obtain the available parameters in the subsystem
            if isinstance(parentSys, Circuit):
                # for Circuit, we need to generate a lookup dict
                parameters = self._paramDictForCircuit(parentSys)
            else:
                parameters = QSYS_PARAM_NAMES[parentSys.__class__]

            # loop over different types of the parameters
            for parameter_type, parameter_names in parameters.items():
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
                    value = getattr(parentSys, parameter_name)

                    self._insertParamByArgs(
                        parent=parentSys,
                        paramName=parameter_name,
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
                    parent=self.hilbertspace,
                    paramName=f"g{interaction_term_index+1}",
                    paramType="interaction_strength",
                    value=value,
                    rangeDict=DEFAULT_PARAM_MINMAX["interaction_strength"],
                )

    @staticmethod
    def parentSystemNames(
        parent: ParentType,
        with_type: bool = False,
    ) -> str:
        """
        Get the name of the parent system.
        The name is a key in the parameter set.

        Parameters
        ----------
        parent: ParentType
            The parent system object
        with_type: bool = False
            If False, the name will be the id_str of the parent system.
            If True, the name will include the type of the parent system like
            "id_str (Fluxonium)".
        """
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
        An inverse function of parentSystemNames.
        """
        if with_type:
            return "".join(name.split(" ")[:-1])
        else:
            return name

    def _updateNameMap(self, parent: ParentType):
        """
        Maintain the name to object and object to name maps for the parent
        system.
        """
        name = self.parentSystemNames(parent)
        if name not in self.parentObjByName.keys():
            self.parentNameByObj[parent] = name
            self.parentObjByName[name] = parent

    def _insertParamByArgs(
        self,
        parent: ParentType,
        paramName: str,
        paramType: ParameterType,
        value: Union[int, float],
        rangeDict: Dict,
    ):
        """
        Create a Parameter object and add it to the parameter set.

        Parameters
        ----------
        parent: ParentType
            The parent system object
        paramName: str
            The name of the parameter
        paramType: ParameterType
            The type of the parameter
        value: Union[int, float]
            The value of the parameter
        rangeDict: Dict
            The range of the parameter, with keys "min" and "max"
        """
        # update the name map
        self._updateNameMap(parent)
        parentName = self.parentNameByObj[parent]

        # process the keyword arguments based on the needed arguments for the parameter class
        kwargs: Dict[str, Any] = {
            "name": paramName,
            "parent": parentName,
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
        self.insertParam(parentName, paramName, param)

    def clear(self):
        """
        Clear the parameter set.
        """
        super().clear()
        self.parentNameByObj = {}
        self.parentObjByName = {}

    def updateParamForHS(
        self,
        parentName: Optional[str] = None,
        paramName: Optional[str] = None,
    ):
        """
        Update the HilbertSpace object based on the parameter set.

        Parameters
        ----------
        parentName: Optional[str]
            The name of the parent system. If None, update all the parent
            systems' parameters.
        paramName: Optional[str]
            The name of the parameter. If None, update all the parameters.
        """
        for prtName, paramDict in self.items():
            if parentName is not None and parentName != prtName:
                continue
            parentSys = self.parentObjByName[prtName]

            for prName, param in paramDict.items():
                if paramName is not None and paramName != prName:
                    continue

                if isinstance(parentSys, HilbertSpace):
                    assert param.paramType == "interaction_strength"
                    interaction_index = int(param.name[1:]) - 1
                    interaction = parentSys.interaction_list[interaction_index]
                    interaction.g_strength = param.value
                else:
                    setattr(parentSys, param.name, param.value)


class SweepParamSet(HSParamSet[QMSweepParam]):
    """
    A class to store all the experimentally tunable parameters of a
    HilbertSpace, which we call sweep parameters.

    QMSweepParam stores calibration functions. The parameter set has additional
    methods to
    map the raw data to the parameter values and to update the HilbertSpace.
    """

    def __init__(self):
        super().__init__(QMSweepParam)

    @classmethod
    def initByHS(cls, hilbertSpace: HilbertSpace) -> "SweepParamSet":
        sweepParameterSet = SweepParamSet()
        sweepParameterSet.dynamicalInit(
            hilbertSpace,
            included_parameter_type=["ng", "flux"],
        )
        return sweepParameterSet

    def setByRawX(self, rawX: Dict[str, float]):
        for _, paramDictByParent in self.items():
            for _, param in paramDictByParent.items():
                # map rawX to the parameter values
                param.setValueWithCali(rawX)


DispParamCls = TypeVar("DispParamCls", bound="DispParamBase")


class ParamModelMixin(QObject, Generic[DispParamCls]):
    """
    When a parameter set is displayed in a view, it is promoted to a model.
    This class provides the methods to communicate with the view and register.
    """

    attrs: List[str] = ["value"]

    updateBox = Signal(ParamAttr)

    def _registrySetter(
        self,
        value: Dict[str, Dict[str, DispParamCls]],
        paramSet: ParamSet[DispParamCls],
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
        paramSet.parameters = value

        for parentName, paraDict in value.items():
            for paraName, para in paraDict.items():
                for attr in para.dataAttr:
                    self._emitUpdateBox(paramSet, parentName, paraName, attr)

    def _registerAll(
        self,
        paramSet: ParamSet[DispParamCls],
    ) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters in the parameter set.

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set
        """

        return {
            type(self).__name__: RegistryEntry(
                name=type(self).__name__,
                quantity_type="r+",
                getter=lambda: paramSet.parameters,
                setter=lambda value: self._registrySetter(value, paramSet),
            )
        }

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

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set
        signalToEmit: SignalInstance
            The signal to emit, which will be connected to the view
        parentName: str
            The name of the parent system. If None, emit the signals for all
            the parent systems.
        paramName: str
            The name of the parameter. If None, emit the signals for all the
            parameters.
        attr: str
            The name of the attribute. If None, emit the signals for
            all attribute names stored in self.attr.
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
        """
        Emit the updateBox signal to update the text box of the parameter.

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set
        parentName: str
            The name of the parent system
        paramName: str
            The name of the parameter
        attr: str
            The name of the attribute
        """
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
        """
        Store the attribute of the parameter to the parameter set from the view.

        Parameters
        ----------
        paramSet: ParamSet
            The parameter set
        paramAttr: ParamAttr
            The parameter attribute to be stored
        kwargs: Dict
            The other keyword arguments for the storeAttr method of the
            parameter
        """
        param = paramSet[paramAttr.parentName][paramAttr.name]
        param.storeAttr(paramAttr.attr, paramAttr.value, **kwargs)
