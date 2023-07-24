from abc import ABC, abstractmethod, abstractproperty
import numpy as np

from scqubits import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem

from qfit.models.parameter_settings import ParameterType
from qfit.widgets.grouped_sliders import SLIDER_RANGE

from typing import Dict, List, Union, overload, Tuple, Callable, Literal

ParentSystem = Union[QuantumSystem, HilbertSpace]

class ParameterBase(ABC):

    intergerParameterTypes = ["cutoff", "truncated_dim"]

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
    def value(self) -> Union[int, float]:
        pass

    @value.setter
    def value(self, value):
        pass


class QuantumModelSliderParameter(ParameterBase):
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
        overallValueSetter,
    ):
        self.sliderValueCallback = sliderValueCallback
        self.sliderValueSetter = sliderValueSetter
        self.boxValueCallback = boxValueCallback
        self.boxValueSetter = boxValueSetter
        self.overallValueSetter = overallValueSetter

    def _strToFloat(self, value: str) -> float:
        """
        Convert the string value to float. When failed, return the minimum value of the
        parameter.
        """
        try:
            return float(value)
        except ValueError:
            return self.min

    def _toIntString(self, value: Union[int, float], precision=4) -> str:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.

        For now, if the value has higher precision, the code breaks. We may want to fix this.
        """
        if isinstance(value, str):
            value = self._strToFloat(value)

        if self.param_type in self.intergerParameterTypes:
            return f"{value:.0f}"
        else:
            return f"{value:.{precision}f}".rstrip("0").rstrip(".")

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

    def _sliderValueToBox(self, *args, **kwargs):
        """
        When the value of the slider is changed, update the value of the box
        """
        sliderValue = self.sliderValueCallback()

        denormalizedValue = self._denormalizeValue(sliderValue)

        self.boxValueSetter(self._toIntString(denormalizedValue))

    def _boxValueToSlider(self, *args, **kwargs):
        """
        When the value of the box is changed, update the value of the slider
        """
        boxValue = self.boxValueCallback()

        if boxValue == "":
            return

        try:
            normalizedValue = self._normalizeValue(self._strToFloat(boxValue))
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.sliderValueSetter(normalizedValue)

    def _onBoxEditingFinished(self, *args, **kwargs):
        """
        When the user is done editing the box, update the value of the box and make the
        value consistent with the parameter type.

        Special note: Will not take care of the case when the user input is not a number.
        """
        boxValue = self.boxValueCallback()

        if boxValue == "":
            return

        try:
            float_boxValue = float(boxValue)
        except ValueError:
            # cannot convert the box value to float, do nothing
            return

        self.boxValueSetter(self._toIntString(float_boxValue))

    def _getUiValue(self) -> Union[int, float]:
        """
        Get the value of the parameter from the box. We should trust the number in the
        box more than the number on the slider, because the number on the box is directly
        input by the user, while the number on the slider is calculated and may be rounded.

        Special note: Will raise a ValueError if user input is not a number. Should be
        taken care of by the UI/controller.

        Returns
        -------
        The value of the parameter
        """

        boxValue = self.boxValueCallback()

        if boxValue == "":
            raise ValueError("Box is empty.")

        try:
            float_boxValue = float(boxValue)
        except ValueError:
            raise ValueError(f"Cannot convert {boxValue} to float.")

        return self._toInt(float_boxValue)

    @property
    def value(self):
        """
        Special note: Will raise a ValueError if user input is not a number. Should be
        taken care of by the UI/controller.
        """
        return self._getUiValue()
    
    @value.setter
    def value(self, value: Union[int, float]):
        """
        Set the value of the parameter. Will update both value of the UI and the controller.
        """
        value = self._toInt(value)
        self.overallValueSetter(value)
        self.setParameterForParent()


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
        self.setParameterForParent()


class QuantumModelParameterSet:
    """
    A class to store all the parameters of a quantum system
    """

    def __init__(self):
        self.parameters: Dict[
            ParentSystem,
            Dict[str, Union[QuantumModelSliderParameter, QuantumModelParameter]],
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
    
    def _parentSystemNames(
        self, 
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
        
    def _updateNameMap(self, parent: ParentSystem, with_type: bool = True):
        name = self._parentSystemNames(parent, with_type=with_type)
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
        # only one of minmax and value can be provided

        minmax_provided = min is not None and max is not None
        minmax_not_provided = min is None or max is None
        if (minmax_not_provided and value is None) or (
            minmax_provided and value is not None
        ):
            raise ValueError(
                "Either minmax or value need to be provided, but not both."
            )

        # if the parent system is not in the parameter set, add it and set its value to
        # an empty dictionary
        if parent_system not in self.parameters:
            self.parameters[parent_system] = {}
        # if the parameter is not a slider parameter, add it to the parameter set
        if minmax_not_provided:
            self.parameters[parent_system][name] = QuantumModelParameter(
                name=name, parent=parent_system, value=value, param_type=param_type
            )
        # if the parameter is a slider parameter, add it to the parameter set
        else:
            self.parameters[parent_system][name] = QuantumModelSliderParameter(
                name=name,
                parent=parent_system,
                min=min,
                max=max,
                param_type=param_type,
            )

        self._updateNameMap(parent_system)

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
    ) -> Union[Dict[str, float], float]:
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
            name: para.value for name, para in para_dict.items()
        }

        if name is None:
            return name_dict
        else:
            return name_dict[name]
        
    def setParameter(
        self, 
        parent_system: Union[ParentSystem, str], 
        name: str, 
        value: Union[int, float]
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
            para_dict[name].value = value
        except KeyError:
            raise KeyError(f"Cannot find parameter {name} in the parameter set.")