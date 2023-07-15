from typing import Dict, Union, overload

EL_range = {"min": 1e-5, "max": 10.0}
EJ_range = {"min": 1e-5, "max": 70.0}
EC_range = {"min": 1e-5, "max": 10.0}
flux_range = {"min": 0.0, "max": 1.0}
ng_range = {"min": 0.0, "max": 1.0}
int_range = {"min": 1, "max": 30}
float_range = {"min": 0.0, "max": 30.0}
ncut_range = {"min": 10, "max": 50}


class QuantumSystemParameter:
    """
    A class to store the parameters of a quantum system.
    """

    def __init__(self, name, parent, minmax, is_int):
        pass

class QuantumSystemParameterSlider(QuantumSystemParameter):
    """
    Parameter that is connected to a slider.
    """
    def __init__(self, name, parent, minmax, is_int):
        super().__init__(name, parent, minmax, is_int)

        self.sliderValueCallback = None
        # TODO: do we want to store minmax?
        # self.minmaxCallback = lambda x: minmax # not yet implemented

    # @property
    # def minmax(self):
    #     return self.minmaxCallback()

    def get_value_from_slider(self):
        sliderValue = self.sliderValueCallback()
        currentValue = self.minmax[0] + sliderValue / 100 * (
            self.minmax[1] - self.minmax[0]
        )
        if self.is_int:
            return int(currentValue)
        else:
            return currentValue


class QuantumSystemParameterSet:
    """
    A class to store all the parameters of a quantum system
    """

    def __init__(self):
        self.parameters = {}

    def add_parameter(self, name, parent, currentvalue, range, is_int):
        self.parameters[name] = QuantumSystemParameter(
            name, parent, currentvalue, range, is_int
        )

    def clean(self):
        self.parameters = {}

    @overload
    def getParameters(self, quantumsystem) -> Dict[str, float]:
        ...

    @overload
    def getParameters(self, quantumsystem, name: str) -> float:
        ...

    def getParameters(
        self, quantumsystem, name: Union[str, None] = None
    ) -> Union[Dict[str, float], float]:
        name_dict = {
            parameter.name: parameter.get_value_from_slider()
            for parameter in self.parameters[quantumsystem]
        }
        if name is None:
            return name_dict
        else:
            return name_dict[name]

    def _update_parameter(self, name, parent, newvalue):
        return self.parameters[name]
