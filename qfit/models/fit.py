import numpy as np

from typing import List, Dict, Tuple, Callable, Union
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Slot

from scqubits.core.hilbert_space import HilbertSpace
from qfit.utils.wrapped_optimizer import Optimization, OptTraj
from qfit.models.parameter_set import (
    ParamSet,
    ParamModelMixin,
    ParamSet,
    HSParamSet,
)
from qfit.models.data_structures import FitParam, ParamAttr, SliderParam
from qfit.models.registry import RegistryEntry
from qfit.models.data_structures import Status


class FitParamModelMixin(ParamModelMixin[FitParam]):
    """
    A mixin class for the fit parameters, which turns a parameter set into 
    a model class. It provides methods to check the validity of the
    parameters, to extract the fixed parameters, free parameter ranges,
    initial parameters, and to convert the parameters to the initial
    parameters and prefit parameters. It also provides methods to store
    the parameter attributes, and to emit the signal to update the view.
    """
    updateStatus = Signal(Status)

    def _isValid(self, paramSet: ParamSet[FitParam]) -> bool:
        """
        Determine if the fit parameters are valid. The validity is determined
        by the following rules:
            - min < max
            - if the parameter is not fixed, the initial value should be
              within the range

        If the parameters are not valid, emit the signal to update the status
        and return False. Otherwise, return True.
        """
        for key, params in paramSet.getFlattenedParamDict().items():
            if not params.isFixed and params.min >= params.max:
                self.updateStatus.emit(
                    Status(
                        statusSource="fit",
                        statusType="error",
                        message=f"For {key}, min value is greater than or equal to max value.",
                    )
                )
                return False
            if not params.isFixed and (
                params.initValue < params.min or params.initValue > params.max
            ):
                self.updateStatus.emit(
                    Status(
                        statusSource="fit",
                        statusType="error",
                        message=f"For {key}, initial value is out of range.",
                    )
                )
                return False
        return True

    def _fixedParams(self, paramSet: ParamSet[FitParam]) -> Dict[str, float]:
        """
        Extract the fixed parameters from the parameter set.
        """
        return {
            key: params.initValue
            for key, params in paramSet.getFlattenedParamDict().items()
            if params.isFixed
        }

    def _freeParamRanges(self, paramSet: ParamSet[FitParam]) -> Dict[str, List[float]]:
        """
        Extract the free parameter ranges from the parameter set.
        """
        return {
            key: [params.min, params.max]
            for key, params in paramSet.getFlattenedParamDict().items()
            if not params.isFixed
        }

    def _initParams(self, paramSet: ParamSet[FitParam]) -> Dict[str, float]:
        """
        Extract the initial parameters from the parameter set.
        """
        return {
            key: params.initValue
            for key, params in paramSet.getFlattenedParamDict().items()
            if not params.isFixed
        }

    def _toInitParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[FitParam]:
        """
        Generate a new parameter set with the final value as the initial 
        value. This is used to accomplish the "result to fit" feature.
        """
        initParamSet = ParamSet[FitParam](FitParam)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                fitParam = FitParam(
                    name=paramName,  # useless
                    parent=param.parent,  # useless
                    paramType=param.paramType,  # useless
                    initValue=param.value,
                )
                initParamSet.insertParam(parentName, paramName, fitParam)

        return initParamSet

    def _toPrefitParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[SliderParam]:
        """
        Generate a new parameter set with the final value as the value. 
        This is used to accomplish the "result to
        prefit" feature.
        """
        prefitParamSet = ParamSet[SliderParam](SliderParam)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                sliderParam = SliderParam(
                    name=paramName,  # useless
                    parent=param.parent,  # useless
                    paramType=param.paramType,  # useless
                    value=param.value,
                    min=0,  # useless
                    max=1,  # useless
                )
                prefitParamSet.insertParam(parentName, paramName, sliderParam)

        return prefitParamSet
    
    def _initToFinalParams(self, paramSet: ParamSet[FitParam]) -> ParamSet[FitParam]:
        """
        Update the initial parameters to the final parameters.
        """
        finalParamSet = ParamSet[FitParam](FitParam)
        for parentName, parent in paramSet.items():
            for paramName, param in parent.items():
                fitParam = FitParam(
                    name=paramName,  # useless
                    parent=param.parent,  # useless
                    paramType=param.paramType,  # useless
                    value=param.initValue,
                )
                finalParamSet.insertParam(parentName, paramName, fitParam)

        return finalParamSet


class CombinedMeta(type(FitParamModelMixin), type(ParamSet)):
    pass


class FitHSParams(
    HSParamSet[FitParam],
    FitParamModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    """
    A model class for the fit parameters in the HilbertSpace. It inherits
    from HSParamSet and FitParamModelMixin. It provides methods to check the
    validity of the parameters, to extract the fixed parameters, free
    parameter ranges, initial parameters, and to convert the parameters to
    the initial parameters and prefit parameters. It also provides methods
    to store the parameter attributes, and to emit the signal to update the
    view.

    Parameters
    ----------
    parent : QObject
        The parent object of the model.
    """
    attrs = FitParam.dataAttr

    # mixin methods ====================================================
    def __init__(self, parent: QObject):
        # ordering matters here
        HSParamSet.__init__(self, FitParam)
        FitParamModelMixin.__init__(self, parent)

    def replaceHS(self, hilbertspace: HilbertSpace):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It overrides the parent 
        method and won't initialize the parameters.

        Parameters
        ----------
        hilbertspace : HilbertSpace
            The HilbertSpace object.
        """
        self.hilbertspace = hilbertspace

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Not only set the parameter, but also emit the signal to update the 
        text box.

        A key method in updating the model by the internal processes.

        Parameters
        ----------
        parentName : str
            The name of the parent object.
        name : str
            The name of the parameter.
        attr : str
            The attribute of the parameter. 
        value : Union[int, float]
            The value to be set.
        """
        super().setParameter(parentName, name, attr, value)

        self._emitUpdateBox(self, parentName=parentName, paramName=name, attr=attr)

    @property
    def isValid(self) -> bool:
        return self._isValid(self)

    @property
    def fixedParams(self) -> Dict[str, float]:
        return self._fixedParams(self)

    @property
    def freeParamRanges(self) -> Dict[str, List[float]]:
        return self._freeParamRanges(self)

    @property
    def initParams(self) -> Dict[str, float]:
        return self._initParams(self)

    def toInitParams(self) -> ParamSet[FitParam]:
        """
        Generate a new parameter set with the final value as the initial
        value. This is used to accomplish the "result to fit" feature.
        """
        return self._toInitParams(self)

    def toPrefitParams(self) -> ParamSet[SliderParam]:
        """
        Generate a new parameter set with the final value as the value.
        This is used to accomplish the "result to prefit" feature.
        """
        return self._toPrefitParams(self)
    
    def initToFinalParams(self) -> ParamSet[FitParam]:
        """
        Update the final parameters (to be optimized) using the initial parameters.
        """
        return self._initToFinalParams(self)

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """Register all the parameters."""
        return self._registerAll(self)

    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        """Store the parameter attributes from the view."""
        super()._storeParamAttr(self, paramAttr, **kwargs)

    def emitUpdateBox(
        self,
        parentName: str | None = None,
        paramName: str | None = None,
        attr: str | None = None,
    ):
        """Emit the signal to update the text box."""
        self._emitUpdateBox(self, parentName, paramName, attr)

    # hilbert space related methods ====================================
    def updateParamForHS(
        self, parentName: str | None = None, paramName: str | None = None
    ):
        """Update the parameter for the HilbertSpace."""
        super().updateParamForHS(parentName, paramName)


class FitCaliParams(
    ParamSet[FitParam],
    FitParamModelMixin,  # ordering matters
    metaclass=CombinedMeta,
):
    """
    A model class for the fit parameters in the calibration. It inherits
    from ParamSet and FitParamModelMixin. It provides methods to check the
    validity of the parameters, to extract the fixed parameters, free
    parameter ranges, initial parameters, and to convert the parameters to
    the initial parameters and prefit parameters. It also provides methods
    to store the parameter attributes, and to emit the signal to update the
    view.

    Parameters
    ----------
    parent : QObject
        The parent object of the model.
    """
    attrs = FitParam.dataAttr

    # mixin methods ====================================================
    def __init__(self, parent: QObject):
        # ordering matters here
        ParamSet.__init__(self, FitParam)
        ParamModelMixin.__init__(self, parent)

    def setParameter(
        self,
        parentName: str,
        name: str,
        attr: str,
        value: Union[int, float],
    ):
        """
        Not only set the parameter, but also emit the signal to update the
        text box.

        A key method in updating the model by the internal processes.
        """
        super().setParameter(parentName, name, attr, value)

        self._emitUpdateBox(self, parentName=parentName, paramName=name, attr=attr)

    @property
    def isValid(self) -> bool:
        return self._isValid(self)

    @property
    def fixedParams(self) -> Dict[str, float]:
        return self._fixedParams(self)

    @property
    def freeParamRanges(self) -> Dict[str, List[float]]:
        return self._freeParamRanges(self)

    @property
    def initParams(self) -> Dict[str, float]:
        return self._initParams(self)

    def toInitParams(self) -> ParamSet[FitParam]:
        """
        Generate a new parameter set with the final value as the initial
        value. This is used to accomplish the "result to fit" feature.
        """
        return self._toInitParams(self)

    def toPrefitParams(self) -> ParamSet[SliderParam]:
        """
        Generate a new parameter set with the final value as the value.
        This is used to accomplish the "result to prefit" feature.
        """
        return self._toPrefitParams(self)
    
    def initToFinalParams(self) -> ParamSet[FitParam]:
        """
        Update the final parameters (to be optimized) using the initial parameters.
        """
        return self._initToFinalParams(self)

    def registerAll(
        self,
    ) -> Dict[str, RegistryEntry]:
        """Register all the parameters."""
        return self._registerAll(self)

    def storeParamAttr(
        self,
        paramAttr: ParamAttr,
        **kwargs,
    ):
        """Store the parameter attributes from the view."""
        super()._storeParamAttr(self, paramAttr, **kwargs)
        
    def emitUpdateBox(
        self,
        parentName: str | None = None,
        paramName: str | None = None,
        attr: str | None = None,
    ):
        """Emit the signal to update the text box."""
        self._emitUpdateBox(self, parentName, paramName, attr)


class FitModel(QObject):
    """
    A model class for the fit. It provides methods to set up the optimization,
    to run the optimization, and to update the optimization parameters. It
    also provides methods to emit the signal to update the view.

    Parameters
    ----------
    parent : QObject
        The parent object of the model.
    """

    optFinished = Signal()  # signal to notify the controller
    updateStatus = Signal(Status)   # signal to update the status bar
    
    optimizer: str
    tol: float
    HSParamNames: List[str]
    iteration: int
    status: Status

    def __init__(self, parent: QObject):
        super().__init__(parent)
        
        self._fitThreadPool = QThreadPool()

        self.optimizer = "L-BFGS-B"
        self.tol = 1e-6
        
        self.HSParamNames = []
        self.iteration = 0
        
    # signal & slots ===================================================
    @Slot()
    def updateOptimizer(self, optimizer: str):
        self.optimizer = optimizer

    @Slot()
    def updateTol(self, tol: str):
        self.tol = float(tol)

    @Slot()
    def resetIteration(self):
        self.iteration = 0

    # optimization setup ===============================================
    def _costWrapper(
        self,
        func: Callable[[Dict[str, float], Dict[str, float]], float],
    ):
        """
        The optimization class requires the cost function to have only one
        input parameter. This wrapper function is used to separate the HS
        parameters and calibration parameters, and to pass them to the
        original cost function.

        Parameters
        ----------
        func : Callable[[Dict[str, float], Dict[str, float]], float]
            The original cost function, which takes two dictionaries as
            input parameters. The first dictionary contains the HilbertSpace
            parameters, and the second dictionary contains the calibration
            parameters.

        Returns
        -------
        Callable[[Dict[str, float]], float]
            The wrapped cost function, which takes only one dictionary as
            input parameter.
        """
        def wrappedCostFunc(
            paramDict: Dict[str, float],
        ) -> float:
            HSParams = {
                key: value
                for key, value in paramDict.items()
                if key in self.HSParamNames
            }
            caliParams = {
                key: value
                for key, value in paramDict.items()
                if key not in self.HSParamNames
            }

            return func(HSParams, caliParams)

        return wrappedCostFunc

    def _callbackWrapper(
        self,
        callback: Callable,
    ) -> Callable:
        """
        Return a wrapped callback function which is used to update the status
        """

        def wrappedCallback(*args, **kwargs):
            mse = callback(*args, **kwargs)
            self.iteration += 1
            # status update; during the optimization, the status is always computing
            status = Status(
                statusSource="fit",
                statusType="computing",
                message="",
                mse=mse,  # a dummy value
            )
            self.updateStatus.emit(status)

        return wrappedCallback

    def setupOptimization(
        self,
        HSFixedParams: Dict[str, float],
        HSFreeParamRanges: Dict[str, List[float]],
        caliFixedParams: Dict[str, float],
        caliFreeParamRanges: Dict[str, List[float]],
        costFunction: Callable[[Dict[str, float], Dict[str, float]], float],
    ) -> bool:
        """
        Set up the optimization with the following parameters:

        Parameters
        ----------
        HSFixedParams : Dict[str, float]
            The fixed parameters in the HilbertSpace.
        HSFreeParamRanges : Dict[str, List[float]]
            The free parameter ranges in the HilbertSpace.
        caliFixedParams : Dict[str, float]
            The fixed parameters in the calibration.
        caliFreeParamRanges : Dict[str, List[float]]
            The free parameter ranges in the calibration.
        costFunction : Callable[[Dict[str, float], Dict[str, float]], float]
            The cost function, which takes two dictionaries as input
            parameters. The first dictionary contains the HilbertSpace
            parameters, and the second dictionary contains the calibration
            parameters.
        """
        # distinguish between HS and cali parameters
        self.HSParamNames = list(HSFixedParams.keys()) + list(HSFreeParamRanges.keys())

        # set up the optimization
        try:
            self.opt = Optimization(
                HSFixedParams | caliFixedParams,
                HSFreeParamRanges | caliFreeParamRanges,
                self._costWrapper(costFunction),
                optimizer=self.optimizer,
                opt_options={
                    "disp": False,
                    "tol": self.tol,
                },
            )
        except Exception as e:
            status = Status(
                statusSource="fit",
                statusType="error",
                message="Fail to set up the optimization. Due to the "
                        "following reason: " + str(e),
                mse=np.nan,
            )
            return False

        return True

    def _paramHitBound(self, traj: OptTraj) -> bool:
        """
        Check if the optimized parameters hit the bound.
        """
        finalParam = traj.final_para
        for key, value in finalParam.items():
            freeRange = self.opt.free_variables[key]
            if value == freeRange[0] or value == freeRange[1]:
                return True
        return False

    @Slot(OptTraj)
    def _postOptimization(self, result: Union[OptTraj, str]):
        """
        After the optimization is finished, process the result. If the
        optimization is successful, emit the signal to notify the
        controller, and update the status.
        """
        self.optFinished.emit()
        # reset iteration
        self.iteration = 0

        if isinstance(result, str):
            if result == "Opt terminated by the user.":
                status = Status(
                    statusSource="fit",
                    statusType="warning",
                    message="The optimization is terminated by the user.",
                    mse=np.nan,
                )
                self.updateStatus.emit(status)
                return

            status = Status(
                statusSource="fit",
                statusType="error",
                message=(
                    "Optimization was interrupted. Due to the following reason: "
                    + result
                ),
                mse=np.nan,
            )
            self.updateStatus.emit(status)
            return
        
        if self._paramHitBound(result):
            status = Status(
                statusSource="fit",
                statusType="warning",
                message="The optimized parameters may hit the bound.",
                mse=result.final_target,
            )
            self.updateStatus.emit(status)
            return

        status = Status(
            statusSource="fit",
            statusType="success",
            message="Successfully optimized the parameter.",
            mse=result.final_target,
        )
        self.updateStatus.emit(status)

    def runOptimization(
        self,
        initParam: Dict[str, float],
        callback: Callable,
    ):
        """
        Once the user clicks the optimize button, run the optimization in a
        separate thread.
        """
        # initial parameter & calculate the current MSE
        try:
            initMSE = self.opt.target_func(initParam)
        except Exception as e:
            self._postOptimization(
                "Fail to calculate the MSE. Due to the following reason: " 
                + str(e)
            )
            return
        
        # status update
        status = Status(
            statusSource="fit",
            statusType="initializing",
            message="",
            mse=initMSE,
        )
        self.updateStatus.emit(status)

        runner = FitRunner(
            self.opt,
            initParam,
            self._callbackWrapper(callback),
        )
        runner.signalHost.optFinished.connect(self._postOptimization)
        
        self._fitThreadPool.start(runner)


class fitSignalHost(QObject):
    optFinished = Signal(OptTraj)


class FitRunner(QRunnable):
    """
    A worker class to run the optimization in a separate thread.

    Parameters
    ----------
    opt : Optimization
        The optimization object.
    initParam : Dict[str, float]
        The initial parameters.
    callback : Callable
        The callback function.
    """

    def __init__(
        self,
        opt: Optimization,
        initParam: Dict[str, float],
        callback: Callable,
    ):
        super().__init__()

        self.opt = opt
        self.initParam = initParam
        self.callback = callback
        self.signalHost = fitSignalHost()

    def run(self):
        """
        Run the optimization and emit the signal to notify the controller
        the optimization result.
        """
        try:
            traj = self.opt.run(init_x=self.initParam, callback=self.callback)
            self.signalHost.optFinished.emit(traj)
        except Exception as e:
            self.signalHost.optFinished.emit(str(e))
