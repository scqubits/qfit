from typing import List, Dict, Tuple, Callable, Union

from qfit.controllers.wrapped_optimizer import Optimization, OptTraj
from qfit.models.quantum_model_parameters import (
    QuantumModelFittingParameter,
    QuantumModelParameterSet,
)

class NumericalFitting():
    opt: Optimization

    def __init__(
        self,
    ):
        pass

    def setupUICallbacks(self):
        # set up callbacks for the UI
        pass

    def _targetFunctionWrapper(
        self,
        paramDict: Dict[str, float],
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        # any other models needed when calculating the MSE
    ):
        parameterSet.fromAttrDict(paramDict)
        return MSE(parameterSet)
    
    def setUpObtimization(
        self,
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        # any other models needed when fitting
    ):
        # generate the fixed parameters and free parameter ranges
        fixed_params = {}
        free_param_ranges = {}
        param_dict = parameterSet.toParamDict()
        for key, params in param_dict.items():
            params: QuantumModelFittingParameter
            if params.isFixed:
                fixed_params[key] = params.initValue
            else:
                free_param_ranges[key] = [params.min, params.max]

        # set up the optimization
        self.opt = Optimization(
            fixed_params,
            free_param_ranges,
            self._targetFunctionWrapper,
            target_kwargs={
                "parameterSet": parameterSet,
                "MSE": MSE,
            },
        )

    def _optCallback(
        self,
        freeParams: Dict[str, float],
        targetValue: float,
        parameterSet: QuantumModelParameterSet,
    ):
        # update the free parameters in the parameter set and display the target value

        parameterSet.fromAttrDict(freeParams)



        
    def runOptimization(
        self,
        parameterSet: QuantumModelParameterSet,
    ):
        """once the user clicks the optimize button, run the optimization"""


        # disable all the line edits, sliders, etc
        

        # initial parameter

        try:
            traj = self.opt.run(
                init_x = parameterSet.toAttrDict("initValue"),
                callback = self._optCallback,
                callback_kwargs = {"parameterSet": parameterSet},
                # file_name = ...,
            )
        except AttributeError:
            # the optimization hasn't been set up yet
            pass


        # display the results, optimizer's termination message
        # enable all the line edits, sliders, etc



