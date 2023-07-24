from qfit.controllers.wrapped_optimizer import Optimization, OptTraj
from qfit.models.quantum_model_parameters import QuantumModelParameter

class NumericalFitting():
    def __init__(
        self,
    ):
        pass

    def _paramToDict(
        self,
        param,
    ):
        """turn QuantumModelParameter into a dictionary, keys are "parent.para_name" """
        pass

    def _dictToParam(
        self,
        param_dict,
    ):
        # turn dictionary into QuantumModelParameter type
        pass

    def _targetFunctionWrapper(
        self,
        param_dict,
    ):
        # turn param_dict into QuantumModelParameter type
        # call update hilbert space
        # calculate MSE
        pass

    def runOptimization(
        self,
    ):
        # once the user clicks the optimize button, run the optimization
        pass

