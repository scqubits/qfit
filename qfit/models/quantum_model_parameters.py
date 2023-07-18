import numpy as np

from scqubits import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem

from qfit.models.parameter_settings import ParameterType

from typing import Dict, List, Union, overload, Tuple, Callable

class QuantumModelSliderParameter:
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

    def __init__(
        self,
        name: str,
        parent: Union[QuantumSystem, HilbertSpace],
        min: Union[int, float],
        max: Union[int, float],
        param_type: ParameterType,
    ):
        self.name = name
        self.parent = parent
        self.min = min
        self.max = max
        self.param_type = param_type
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

    def _toInt(self, value: Union[int, float]) -> Union[int, float]:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.param_type in ["cutoff", "truncated_dim"]:
            return np.round(value).astype(int)
        else:
            return value
        
    def _toIntString(self, value: Union[int, float]) -> str:
        """
        Convert the value to an integer if the parameter type is cutoff or truncated_dim.
        """
        if self.param_type in ["cutoff", "truncated_dim"]:
            return f"{value:.0f}"
        else:
            return f"{value:.2f}"

    def _normalizeValue(self, value: Union[int, float]) -> int:
        """
        Normalize the value of the parameter to a value between 0 and 100.
        """
        normalizedValue = (value - self.min) / (
            self.max - self.min
        ) * 100
        return np.round(normalizedValue).astype(int)
    
    def _denormalizeValue(self, value: int) -> Union[int, float]:
        """
        Denormalize the value of the parameter to a value between min and max.
        """
        denormalizedValue = self.min + value / 100 * (
            self.max - self.min
        )

        return self._toInt(denormalizedValue)

    def _onSliderValueChanged(self, *args, **kwargs):
        """
        When the value of the slider is changed, update the value of the box
        """
        sliderValue = self.sliderValueCallback()

        print("sliderValue", sliderValue)

        denormalizedValue = self._denormalizeValue(sliderValue)

        if np.abs(denormalizedValue - float(self.boxValueCallback())) < 1e-14:
            return
        
        self.boxValueSetter(self._toIntString(denormalizedValue))

    def _onBoxValueChanged(self, *args, **kwargs):
        """
        When the value of the box is changed, update the value of the slider
        """
        boxValue = self.boxValueCallback()

        if boxValue == "":
            return

        print("boxValue", boxValue)

        normalizedValue = self._normalizeValue(float(boxValue))

        if normalizedValue == self.sliderValueCallback():
            return
        self.sliderValueSetter(normalizedValue)

    def _getUiValue(self) -> Union[int, float]:
        """
        Get the value of the parameter from the box. We should trust the number in the
        box more than the number on the slider, because the number on the box is directly 
        input by the user, while the number on the slider is calculated and may be rounded.

        Returns
        -------
        The value of the parameter
        """
        
        boxValue = self.boxValueCallback()
        return self._toInt(boxValue)

    @property
    def value(self):
        return self._getUiValue()


class QuantumModelParameter:
    """
    A class for parameters that are not adjustable by a slider.
    """

    def __init__(
        self,
        name: str,
        parent: Union[QuantumSystem, HilbertSpace],
        value: Union[float, int],
        param_type: ParameterType,
    ):
        self.name = name
        self.parent = parent
        self.value = value
        self.param_type = param_type


class QuantumModelParameterSet:
    """
    A class to store all the parameters of a quantum system
    """

    def __init__(self):
        self.parameters: Dict[
            Union[HilbertSpace, QuantumSystem],
            Dict[str, Union[QuantumModelSliderParameter, QuantumModelParameter]],
        ] = {}

    def keys(self):
        return self.parameters.keys()
    
    def values(self):
        return self.parameters.values()
    
    def items(self):
        return self.parameters.items()
    
    def __getitem__(self, key):
        return self.parameters[key]
    
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

    def add_parameter(
        self,
        name: str,
        parent_system,
        param_type,
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
        if (
            (minmax_not_provided and value is None) 
            or (minmax_provided and value is not None)
        ):
            raise ValueError(
                "Either minmax or value need to be provided, but not both."
            )
    
        # if the parent system is not in the parameter set, add it and set its value to
        # an empty list
        if parent_system not in self.parameters:
            self.parameters[parent_system] = {}
        # if the parameter is not a slider parameter, add it to the parameter set
        if minmax_not_provided:
            self.parameters[parent_system][name] = QuantumModelParameter(
                name = name, 
                parent = parent_system, 
                value = value, 
                param_type = param_type
            )
        # if the parameter is a slider parameter, add it to the parameter set
        else:
            self.parameters[parent_system][name] = QuantumModelSliderParameter(
                name = name, 
                parent = parent_system, 
                min = min,
                max = max, 
                param_type = param_type,
            )

    def clean(self):
        """
        Clean the parameter set.
        """
        self.parameters = {}

    @overload
    def getParameters(self, parent_system) -> Dict[str, float]:
        ...

    @overload
    def getParameters(self, parent_system, name: str) -> float:
        ...

    def getParameters(
        self,
        parent_system: Union[QuantumSystem, HilbertSpace],
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

        # TODO: we may want to add a check to see if the parent_system is in the parameter set
        # generate a dict with keys being the parameter names and values being the parameter
        name_dict = {
            parameter.name: parameter.value
            for parameter in self.parameters[parent_system]
        }
        if name is None:
            return name_dict
        else:
            return name_dict[name]
