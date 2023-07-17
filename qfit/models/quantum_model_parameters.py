from typing import Dict, List, Union, overload, Tuple
from qfit.models.parameter_settings import ParameterType

from scqubits import HilbertSpace
from scqubits.core.qubit_base import QuantumSystem


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
    minmax: Union[Tuple[int, int], Tuple[float, float]]
        The range of the parameter
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

    def __init__(
        self,
        name: str,
        parent: Union[QuantumSystem, HilbertSpace],
        minmax: Union[Tuple[int, int], Tuple[float, float]],
        param_type: ParameterType,
    ):
        self.name = name
        self.parent = parent
        self.minmax = minmax
        self.param_type = param_type
        # a placeholder for the callback function that returns the value of the slider
        # this callback function is set by the UI
        self.sliderValueCallback = None

    # TODO: in future, we may wish to let user specify the min and max of parameters in the slider,
    # do we want to store minmax by then? If so, we may need:
    # self.minmaxCallback = lambda x: minmax # not yet implemented

    def _get_value_from_slider(self) -> Union[int, float]:
        """
        Get the value of the parameter from the slider.

        Returns
        -------
        The value of the parameter
        """
        # obtain the value of the slider
        sliderValue = self.sliderValueCallback()
        # convert the slider value to the parameter value, sliderValue is in [0, 100]
        currentValue = self.minmax[0] + sliderValue / 100 * (
            self.minmax[1] - self.minmax[0]
        )
        if self.param_type in ["cutoff", "truncated_dim"]:
            return int(currentValue)
        else:
            return currentValue

    @property
    def value(self):
        return self._get_value_from_slider()


class QuantumModelParameter:
    """
    A class for parameters that are not adjustable by a slider.
    """

    def __init__(
        self,
        name: str,
        parent: Union[QuantumSystem, HilbertSpace],
        value: float,
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
            List[Union[QuantumModelSliderParameter, QuantumModelParameter]],
        ] = {}

    @overload
    def add_parameter(
        self,
        name: str,
        parent_system: Union[QuantumSystem, HilbertSpace],
        param_type: ParameterType,
        minmax: Union[Tuple[int], Tuple[float]],
    ):
        ...

    @overload
    def add_parameter(
        self,
        name: str,
        parent_system: Union[QuantumSystem, HilbertSpace],
        param_type: ParameterType,
        value: Union[float, int],
    ):
        ...

    def add_parameter(
        self,
        name,
        parent_system,
        param_type,
        minmax: Union[Tuple[int], Tuple[float], None] = None,
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
        if (minmax is None and value is None) or (
            minmax is not None and value is not None
        ):
            raise ValueError(
                "Either minmax or value need to be provided, but not both."
            )
        # if the parent system is not in the parameter set, add it and set its value to
        # an empty list
        if parent_system not in self.parameters:
            self.parameters[parent_system] = []
        # if the parameter is not a slider parameter, add it to the parameter set
        if minmax is None:
            self.parameters[parent_system].append(
                QuantumModelParameter(name, parent_system, param_type, value)
            )
        # if the parameter is a slider parameter, add it to the parameter set
        else:
            self.parameters[parent_system].append(
                QuantumModelSliderParameter(name, parent_system, param_type, minmax)
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
