from abc import ABC, abstractmethod, abstractproperty
import numpy as np

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem

from qfit.models.data_structures import (
    ParamBase, QMSweepParam, QMSliderParam, QMFitParam,
)
from qfit.models.parameter_settings import ParameterType
from qfit.models.registry import RegistryEntry, Registrable
from qfit.widgets.grouped_sliders import SLIDER_RANGE

from typing import (
    Dict, List, Union, overload, Tuple, Callable, Literal, Any, 
    TypeVar, Generic
)

ParentSystem = Union[QuantumSystem, HilbertSpace]
ParamCls = TypeVar("ParamCls", bound="ParamBase")


class ParamSet(Registrable, Generic[ParamCls]):
    """
    A class to store all the parameters of a quantum system
    """

    def __init__(self, name):
        self.name = name

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

    def addParameter(
        self,
        parameter: ParamCls,
    ):
        """
        Add a QuantumModelParameter or a QuantumModelSliderParameter object to
        the parameter set.

        Parameters
        ----------
        parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
            The parameter to add
        """

        # if the parent system is not in the parameter set, create a new entry
        if parameter.parent not in self.parameters:
            self.parameters[parameter.parent] = {}
            self._updateNameMap(parameter.parent)

        # add the parameter to the parameter set
        self.parameters[parameter.parent][parameter.name] = parameter

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
        parent_system: Union[ParentSystem, str],
        name: str,
        value: Union[int, float],
        attribute: str = "value",
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

        try:
            setattr(para_dict[name], attribute, value)
        except KeyError:
            raise KeyError(f"Cannot find parameter {name} in the parameter set.")

    def toParamDict(self) -> Dict[str, ParameterBase]:
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
            parent_system = self.parentObjByName[parent_name]
            self.setParameter(parent_system, name, value, attribute=attribute)

    def update(
        self,
        param_set: "ParamSet",
        attribute: Union[str, List[str]] = "value",
    ):
        """
        Update the parameter set from another parameter set. Only affect the parameters
        that exist in both parameter sets.

        Parameters
        ----------
        param_set: QuantumModelParameterSet
            The parameter set to update from

        attribute: Union[str, List[str]]
            The attribute(s) to update
        """
        if isinstance(attribute, str):
            attribute = [attribute]

        for parent_system, para_dict in param_set.items():
            for name, para in para_dict.items():
                try:
                    for attr in attribute:
                        self.setParameter(
                            parent_system,
                            name,
                            getattr(para, attr),
                            attribute=attr,
                        )
                except KeyError:
                    continue

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


