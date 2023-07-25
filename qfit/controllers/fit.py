from typing import List, Dict, Tuple, Callable, Union

from qfit.controllers.wrapped_optimizer import Optimization, OptTraj
from qfit.models.quantum_model_parameters import QuantumModelParameter



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
        paramDict,
        parameterSet,
        MSE,
        # any other models needed when calculating the MSE
    ):
        parameterSet.fromDict(paramDict)
        return MSE(parameterSet)
    
    def _fixedParameters(self) -> Dict[str, float]:
        return {}
    
    def _freeParameterRanges(self) -> Dict[str, List[float]]:
        return {}
    
    def setUpObtimization(
        self,
        parameterSet,
        MSE,
        # any other models needed when fitting
    ):
        self.opt = Optimization(
            self._fixedParameters(),
            self._freeParameterRanges(),
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
    ):
        # update the free parameters in the parameter set and display the target value
        pass
        
    def runOptimization(
        self,
    ):
        """once the user clicks the optimize button, run the optimization"""
        # disable all the line edits, sliders, etc
        # run the optimization
        # display the results, optimizer's termination message
        # enable all the line edits, sliders, etc

        self.opt.run()



