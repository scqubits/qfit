from abc import ABC, abstractmethod, abstractproperty
import numpy as np

from scqubits import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem

from qfit.models.parameter_settings import ParameterType
from qfit.io_utils.registry import RegistryEntry
from qfit.widgets.grouped_sliders import SLIDER_RANGE

from typing import Dict, List, Union, overload, Tuple, Callable, Literal, Any

ParentSystem = Union[QuantumSystem, HilbertSpace]

class ParameterBase(ABC):

    intergerParameterTypes = ["cutoff", "truncated_dim"]
    attrToRegister: List[str] = ["value"]

    def __init__(
        self,
        name: str,
        parent: ParentSystem,
        param_type: ParameterType,
    ):
        self.name = name
        self.parent = parent
        self.param_type = param_type

    def setParameterForParent(self):
        """
        Set the parameter for the parent
        """
        # TODO: include more "special" parameter types here in future
        if self.param_type == "interaction_strength":
            interaction_index = int(self.name[1:]) - 1
            interaction = self.parent.interaction_list[interaction_index]
            interaction.g_strength = self.value
        else:
            setattr(self.parent, self.name, self.value)

    def _toInt(self, value: Union[int, float]) -> Union[int, float]:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.param_type in self.intergerParameterTypes:
            return np.round(value).astype(int)
        else:
            return value

    @abstractproperty
    def value(self):
        """
        Get the value of the parameter
        """
        pass
        

    @value.setter
    def value(self, value):
        """
        Set the value of the parameter
        """
        pass

    def _toRegistryEntry(self, attribute: str = "value") -> RegistryEntry:
        """
        Convert the parameter to a RegistryEntry object. The name of the
        RegistryEntry object is not complete, and should be updated later.
        """

        def setter_func(value):
            setattr(self, attribute, value)
            # self.setParameterForParent()

        return RegistryEntry(
            name = self.name,
            quantity_type = "r+",
            getter = lambda: getattr(self, attribute),
            setter = setter_func,
        )
    
    def registerAll(self,) -> Dict[str, RegistryEntry]:
        """
        Register all the attributes of the parameter
        """
        return {attr: self._toRegistryEntry(attribute=attr) 
                for attr in self.attrToRegister}
        

class DisplayedParameterBase(ParameterBase):

    min: float

    def _toIntString(self, value: Union[int, float], precision=4) -> str:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.

        For now, if the value has higher precision, the code breaks. We may want to fix this.
        """
        if self.param_type in self.intergerParameterTypes:
            return f"{value:.0f}"
        else:
            return f"{value:.{precision}f}".rstrip("0").rstrip(".")


class QuantumModelParameter(ParameterBase):
    """
    A class for parameters that are not adjustable by a slider. Primarily used for
    ng and flux parameters in qubits.

    Parameters
    ----------
    name: str
        The name of the parameter
    parent: Union[QuantumSystem, HilbertSpace]
        The parent of the parameter
    value: Union[float, int]
        The value of the parameter
    param_type: ParameterType
        The type of the parameter
    """

    attrToRegister = ["value"]

    def __init__(
        self,
        name: str,
        parent: ParentSystem,
        value: Union[float, int],
        param_type: ParameterType,
    ):
        super().__init__(name=name, parent=parent, param_type=param_type)

        self._value = value
        self.calibration_func = None

    def setCalibrationFunc(self, func):
        """
        Set the calibration function for the parameter
        """
        self.calibration_func = func

    @property
    def value(self) -> Union[int, float]:
        """
        Get the value of the parameter
        """
        return self._value
    
    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter. Will update the both the parameter stored and the 
        parent object.
        """
        self._value = self._toInt(value)


class QuantumModelSliderParameter(DisplayedParameterBase):
    """
    A class for parameters that are connected to a slider. The slider value is stored elsewhere,
    and this method stores the name of the parameter, the parent object, the min and max of parameters,
    and parameter types.

    Parameters
    ----------
    name: str
        Name of the parameter
    parent: Union[QuantumSystem, HilbertSpace]
        The parent object of the parameter
    min: Union[int, float]
        The minimum value of the parameter
    max: Union[int, float]
        The maximum value of the parameter
    param_type: Literal[
        "EC",
        "EJ",
        "EL",
        "E_osc",
        "l_osc",
        "ng",
        "flux",
        "cutoff",
        "interaction_strength",
        "truncated_dim",
    ]
        The type of the parameter
    """

    sliderValueCallback: Callable
    sliderValueSetter: Callable
    boxValueCallback: Callable
    boxValueSetter: Callable
    overallValueSetter: Callable

    attrToRegister = ["value"]

    def __init__(
        self,
        name: str,
        parent: ParentSystem,
        min: Union[int, float],
        max: Union[int, float],
        param_type: ParameterType,
    ):
        super().__init__(name=name, parent=parent, param_type=param_type)
        
        self.min = min
        self.max = max
        # a placeholder for the callback function that returns the value of the slider
        # this callback function is set by the UI

    # TODO: in future, we may wish to let user specify the min and max of parameters in the slider,
    # do we want to store minmax by then? If so, we may need:
    # self.minmaxCallback = lambda x: minmax # not yet implemented

    def setupUICallbacks(
        self,
        sliderValueCallback,
        sliderValueSetter,
        boxValueCallback,
        boxValueSetter,
    ):
        self.sliderValueCallback = sliderValueCallback
        self.sliderValueSetter = sliderValueSetter
        self.boxValueCallback = boxValueCallback
        self.boxValueSetter = boxValueSetter

    def _normalizeValue(self, value: Union[int, float]) -> int:
        """
        Normalize the value of the parameter to a value between 0 and SLIDER_RANGE.
        """
        normalizedValue = (value - self.min) / (self.max - self.min) * SLIDER_RANGE
        return np.round(normalizedValue).astype(int)

    def _denormalizeValue(self, value: int) -> Union[int, float]:
        """
        Denormalize the value of the parameter to a value between min and max.
        """
        denormalizedValue = self.min + value / SLIDER_RANGE * (self.max - self.min)

        return self._toInt(denormalizedValue)

    def sliderValueToBox(self, *args, **kwargs):
        """
        When the value of the slider is changed, update the value of the box
        """
        sliderValue = self.sliderValueCallback()

        denormalizedValue = self._denormalizeValue(sliderValue)

        self.boxValueSetter(self._toIntString(denormalizedValue))

    def boxValueToSlider(self, *args, **kwargs):
        """
        When the value of the box is changed, update the value of the slider
        """
        try:
            boxValue = float(self.boxValueCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        normalizedValue = self._normalizeValue(boxValue)

        self.sliderValueSetter(normalizedValue)

    def onBoxEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.boxValueCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.boxValueSetter(self._toIntString(boxValue))

    @property
    def value(self) -> Union[int, float]:
        """
        Special note: Will raise a ValueError if user input is not a number. Should be
        taken care of by the UI/controller.
        """
        boxValue = float(self.boxValueCallback())   # will raise a ValueError if user input is not a number

        return self._toInt(boxValue)
    
    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter. Will update both value of the UI and the controller.
        """
        value = self._toInt(value)

        self.boxValueSetter(self._toIntString(value))
        self.sliderValueSetter(self._normalizeValue(value))

    def initialize(self):
        # for test only
        self.value = (self.max + self.min) / 5 + self.min


class QuantumModelFittingParameter(DisplayedParameterBase):

    initValueCallback: Callable
    initValueSetter: Callable
    valueCallback: Callable
    valueSetter: Callable
    minCallback: Callable
    minSetter: Callable
    maxCallback: Callable
    maxSetter: Callable
    fixCallback: Callable
    fixSetter: Callable

    attrToRegister = ["initValue", "value", "min", "max", "isFixed"]
    
    def __init__(
        self,
        name: str,
        parent: ParentSystem,
        param_type: ParameterType,
    ):
        super().__init__(name=name, parent=parent, param_type=param_type)
        self._initValue = None
        self._value = None

    def setupUICallbacks(
        self,
        initValueCallback,
        initValueSetter,
        valueCallback,
        valueSetter,
        minCallback,
        minSetter,
        maxCallback,
        maxSetter,
        fixCallback,
        fixSetter,
    ):
        self.initValueCallback = initValueCallback
        self.initValueSetter = initValueSetter
        self.valueCallback = valueCallback
        self.valueSetter = valueSetter
        self.minCallback = minCallback
        self.minSetter = minSetter
        self.maxCallback = maxCallback
        self.maxSetter = maxSetter
        self.fixCallback = fixCallback
        self.fixSetter = fixSetter

    @property
    def min(self) -> Union[int, float]:
        """
        Get the minimum value of the parameter from the UI
        """
        return float(self.minCallback())    # will raise a ValueError if user input is not a number
        
    @min.setter
    def min(self, value: Union[int, float]):
        """
        Set the minimum value of the parameter in the UI
        """
        self.minSetter(self._toIntString(value))

    def onMinEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the min box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.minCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.min = boxValue

    @property
    def max(self) -> Union[int, float]:
        """
        Get the maximum value of the parameter from the UI
        """
        return float(self.maxCallback())    # will raise a ValueError if user input is not a number

    @max.setter
    def max(self, value: Union[int, float]):    
        """
        Set the maximum value of the parameter in the UI
        """
        self.maxSetter(self._toIntString(value))

    def onMaxEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the max box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.maxCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.max = boxValue

    @property
    def initValue(self) -> Union[int, float]:
        """
        Get the initial value of the parameter from the UI
        """
        if self._initValue is None:
            # self._initValue = float(self.initValueCallback())
            raise ValueError("Initial value of fitting parameter is not set yet.")

        return self._initValue
    
    @initValue.setter
    def initValue(self, value: Union[int, float]):
        """
        Set the initial value of the parameter in the UI
        """
        self._initValue = value
        self.initValueSetter(self._toIntString(value))

    def onInitValueEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the value box, update the value of the box and make the
        value consistent with the parameter type.

        """
        try:
            boxValue = float(self.initValueCallback())
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.initValue = boxValue

    @property
    def value(self) -> Union[int, float]:
        """
        Get the value of the parameter from the UI
        """
        if self._value is None:
            # self._value = float(self.valueCallback())
            raise ValueError("Initial value of fitting parameter is not set yet.")

        return self._value

    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter in the UI
        """
        self._value = value
        self.valueSetter(self._toIntString(value))

    @property
    def isFixed(self) -> bool:
        """
        Check if the parameter is fixed
        """
        return self.fixCallback()

    @isFixed.setter
    def isFixed(self, value: bool):
        """
        Set the parameter to be fixed or not
        """
        self.fixSetter(value)

    def initialize(self):
        # for test only
        self.min = 0
        self.max = 1
        self.initValue = self.min
        self.value = self.initValue
        self.isFixed = False

    def valueToInitial(self):
        """
        Set the value of the parameter to the initial value
        """
        self.value = self.initValue


class QuantumModelParameterSet:
    """
    A class to store all the parameters of a quantum system
    """

    def __init__(self, name):

        self.name = name

        self.parameters: Dict[
            ParentSystem,
            Dict[str, ParameterBase],
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
        return name.split(" ")[0]
        
    def _updateNameMap(self, parent: ParentSystem, with_type: bool = True):
        name = self.parentSystemNames(parent, with_type=with_type)
        self.parentNameByObj[parent] = name
        self.parentObjByName[name] = parent
    
    # @overload
    # def add_parameter(
    #     self,
    #     name: str,
    #     parent_system: Union[QuantumSystem, HilbertSpace],
    #     param_type: ParameterType,
    #     minmax: Union[Tuple[int], Tuple[float]],
    # ):
    #     ...

    # @overload
    # def add_parameter(
    #     self,
    #     name: str,
    #     parent_system: Union[QuantumSystem, HilbertSpace],
    #     param_type: ParameterType,
    #     value: Union[float, int],
    # ):
    #     ...

    def addParameter(
        self,
        name: str,
        parent_system: ParentSystem,
        param_type: ParameterType,
        param_usage: Literal["slider", "static", "fitting"],
        min: Union[float, int, None] = None,
        max: Union[float, int, None] = None,
        value: Union[float, int, None] = None,
    ):
        """
        Add a QuantumModelParameter or a QuantumModelSliderParameter object to
        the parameter set. When a QuantumModelSliderParameter object is added,
        minmax need to be provided, otherwise the value need to be provided.

        Parameters
        ----------
        name: str
            Name of the parameter
        parent_system: Union[QuantumSystem, HilbertSpace]
            The parent system of the parameter
        param_type: Literal[
            "EC",
            "EJ",
            "EL",
            "E_osc",
            "l_osc",
            "ng",
            "flux",
            "cutoff",
            "interaction_strength",
            "truncated_dim",
        ]
            The type of the parameter
        minmax: Union[Tuple[int], Tuple[float], None]
            The range of the parameter, only needed when a QuantumModelSliderParameter
            object is added
        value: Union[float, int, None]
            The value of the parameter, only needed when a QuantumModelParameter
            object is added
        """

        # if the parent system is not in the parameter set, create a new entry
        if parent_system not in self.parameters:
            self.parameters[parent_system] = {}
            self._updateNameMap(parent_system)

        # if the parameter is not a slider parameter, add it to the parameter set
        if param_usage == "static":
            # check if the value is provided
            if value is None:
                raise ValueError(
                    f"Value of parameter {name} is not provided for a static parameter."
                )
            self.parameters[parent_system][name] = QuantumModelParameter(
                name=name, parent=parent_system, value=value, param_type=param_type
            )

        # if the parameter is a slider parameter, add it to the parameter set
        elif param_usage == "slider":
            # check if minmax is provided
            if min is None or max is None:
                raise ValueError(
                    f"Min or max of parameter {name} is not provided for a slider parameter."
                )
            self.parameters[parent_system][name] = QuantumModelSliderParameter(
                name=name,
                parent=parent_system,
                min=min,
                max=max,
                param_type=param_type,
            )
        elif param_usage == "fitting":
            # check if minmax and value are provided
            if min is None or max is None or value is None:
                raise ValueError(
                    f"Min, max, or value of parameter {name} is not provided for a fitting parameter."
                )
            self.parameters[parent_system][name] = QuantumModelFittingParameter(
                name=name,
                parent=parent_system,
                param_type=param_type,
            )
        else:
            raise ValueError(f"Unknown parameter usage {param_usage}.")

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
                raise KeyError(f"Cannot find parent system {parent_system} in the parameter set.")
        
        try:
            para_dict = self.parameters[parent_system]
        except KeyError:
            raise KeyError(f"Cannot find parent system {parent_system} in the parameter set.")

        name_dict = {
            name: getattr(para, attribute) for name, para in para_dict.items()
        }

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
                raise KeyError(f"Cannot find parent system {parent_system} in the parameter set.")

        try:
            para_dict = self.parameters[parent_system]
        except KeyError:
            raise KeyError(f"Cannot find parent system {parent_system} in the parameter set.")

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
        
    def exportAttrDict(self, attribute: str = "value") -> Union[
        Dict[str, float], 
        Dict[str, int], 
    ]:
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
        attribute: str = "value"
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

    def update(self, param_set: "QuantumModelParameterSet", attribute: Union[str, List[str]] = "value"):
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

    def registerAll(self,) -> Dict[str, RegistryEntry]:
        """
        Register all the parameters in the parameter set
        """
        registry = {}
        for parent_system, para_dict in self.parameters.items():
            for para_name, para in para_dict.items():
                entry_dict = para.registerAll()

                # update the name of the parameter
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