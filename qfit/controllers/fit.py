from typing import List, Dict, Tuple, Callable, Union

from qfit.controllers.wrapped_optimizer import Optimization, OptTraj
from qfit.models.extracted_data import AllExtractedData
from qfit.models.quantum_model_parameters import (
    QuantumModelFittingParameter,
    QuantumModelParameterSet,
)

class NumericalFitting():
    opt: Optimization

    def __init__(
        self,
    ):
        return

    def setupUICallbacks(self):
        # set up callbacks for the UI
        return

    def _targetFunctionWrapper(
        self,
        paramDict: Dict[str, float],
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        extractedData: AllExtractedData,
    ):
        parameterSet.loadAttrDict(paramDict)
        return MSE(parameterSet, extractedData)
    
    def setupOptimization(
        self,
        parameterSet: QuantumModelParameterSet,
        MSE: Callable,
        extractedData: AllExtractedData,
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
                "extractedData": extractedData,
            },
        )

    def _optCallback(
        self,
        freeParams: Dict[str, float],
        targetValue: float,
        parameterSet: QuantumModelParameterSet,
        extractedData: AllExtractedData,
    ):
        # update the free parameters in the parameter set and display the target value

        parameterSet.loadAttrDict(freeParams, "value")

        print(targetValue)

        
    def runOptimization(
        self,
        parameterSet: QuantumModelParameterSet,
        extractedData: AllExtractedData,
    ):
        """once the user clicks the optimize button, run the optimization"""


        # disable all the line edits, sliders, etc
        

        # initial parameter
        init_param_ui = parameterSet.exportAttrDict("initValue")
        init_param = {key: value for key, value in init_param_ui.items() 
                      if key not in self.opt.fixed_variables.keys()}

        try:
            traj = self.opt.run(
                init_x = init_param,
                callback = self._optCallback,
                callback_kwargs = {
                    "parameterSet": parameterSet,
                    "extractedData": extractedData,
                    },
                # file_name = ...,
            )
        except AttributeError:
            # the optimization hasn't been set up yet
            pass

        # display the results, optimizer's termination message
        # enable all the line edits, sliders, etc



