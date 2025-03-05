from PySide6.QtCore import (
    Slot, Signal, QObject, QRunnable, QThreadPool, SignalInstance
)

import numpy as np
from numpy import ndarray

import copy

import scqubits as scq
from scqubits.core.qubit_base import QuantumSystem
from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.param_sweep import ParameterSweep
from scqubits.core.storage import SpectrumData


from qfit.models.parameter_set import SweepParamSet
from qfit.models.data_structures import (
    QMSweepParam,
    FullExtr,
    ExtrTransition,
)
from qfit.models.data_structures import Tag, SpectrumElement, Status
import qfit.settings as settings

from typing import Dict, List, Tuple, Union, Callable, Any, Literal, Optional, Set


class SweepConfigForStandaloneCanvas(QObject):
    """
    Container for the data of a standalone canvas, as well as a signal to
    update the canvas.

    Parameters
    ----------
    pointsAdded: int, 
        number of sweep points
    xLim: Tuple[float, float], 
        x limits
    caliByFigName: str, 
        the calibration function used for this figure
        it must be the same as one of the figNames
    """
    readyToPlot = Signal(SpectrumElement)

    def __init__(
        self, 
        pointsAdded: int, 
        xLim: Tuple[float, float], 
        caliByFigName: str, 
        parent: QObject = None
    ):
        super().__init__(parent)
        self.pointsAdded = pointsAdded
        self.xLim = xLim
        self.caliByFigName = caliByFigName
        
    def cleanup(self):
        self.readyToPlot.disconnect()


class QuantumModel(QObject):
    """
    QuantumModel updates the HilbertSpace object, the extracted data, the calibration data and
    the sweep options whenever they are updated. Using these ingedients,
    QuantumModel generates a ParameterSweep object and calculates the
    mean square error between the extracted data and the simulated data.

    QuantumModel has three modes (sweepUsage):
    - "prefit": the sweep is automatically calculated once the ingredients are updated
    - "fit": the sweep can be manually calculated during the fitting process
    - "fit-result": calculate a one-time sweep after the fitting process is finished

    Parameters
    ----------
    parent: QObject
    """

    _sweeps: Dict[str, ParameterSweep]

    readyToPlotMainCanvas = Signal(SpectrumElement)
    mseReadyToFit = Signal(float)

    updateStatus = Signal(Status)

    def __init__(
        self,
        parent: QObject,
    ):
        super().__init__(parent)
        self._figNames: List[str] = []
        
        # standalone canvases and their configurations
        self._sweepConfigsForStandaloneCanvas: Dict[
            str, SweepConfigForStandaloneCanvas
        ] = {}

        self._sweepThreadPool = QThreadPool()

    def replaceHS(self, hilbertspace: HilbertSpace):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method.

        Parameters
        ----------
        hilbertspace: HilbertSpace
            HilbertSpace object
        """
        self.hilbertspace = hilbertspace

    def replaceMeasData(self, figNames: List[str]):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method.

        Parameters
        ----------
        figNames: List[str]
            The names of the figures to be plotted.
        """
        self._figNames = figNames

    def dynamicalInit(self):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method.

        Parameters
        ----------
        hilbertspace: HilbertSpace
            HilbertSpace object
        figNames: List[str]
            The names of the figures to be plotted.
        """
        if self._figNames == []:
            raise AttributeError("Should call replaceMeasData first.")
        try:
            self.hilbertspace
        except AttributeError:
            raise AttributeError("Should call replaceHS first.")

        self._currentFigName = self._figNames[0]
        self._initializeSweepIngredients()

    def _initializeSweepIngredients(self):
        """
        Initialize the ingredients for the sweep:
        - extracted data
        - calibration
        - options when generating the parameter sweep
        - options when plotting the spectrum
        - option and status when running
        """
        # extracted data
        self._fullExtr = FullExtr()

        # calibration
        self._sweepParamSets: Dict[str, SweepParamSet] | Literal[False] = False
        self._yCaliFunc: Callable | Literal[False] = False
        self._yInvCaliFunc: Callable | Literal[False] = False

        # options when generating the parameter sweep
        self._evalsCount: int = np.min([10, self.hilbertspace.dimension])
        self._pointsAdded: int = 10
        self._numCPUs: int = 1
        self._rawXByX: Dict[str, Callable[[float], Dict[str, float]]] = {
            figName: lambda x: {} for figName in self._figNames
        }
        self._xLim: Tuple[float, float] = (0, 1)

        # options when plotting the spectrum
        self._subsysToPlot: QuantumSystem = self.hilbertspace.subsystem_list[0]
        self._initialStates: List[Union[int, Tuple[int, ...], None]] = [None]
        self._photons: int = 1

        # options when running
        self._autoRun: bool = True
        self.sweepUsage: Literal["none", "prefit", "fit", "fit-result"] = "none"

    # Signals and Slots ========================================================
    @Slot(str)
    def switchFig(self, figName: str):
        """
        Switch the current figure name.
        """
        if figName not in self._figNames:
            # this happens in the data importing stage, where the model is
            # not fully initialized by the measurement data
            return

        self._currentFigName = figName
        self.updateCalc(forced=True)

    @Slot(HilbertSpace)
    def updateHilbertSpace(
        self,
        hilbertspace: HilbertSpace,
    ):
        """
        Update the HilbertSpace object and update the calculation.

        Parameters
        ----------
        hilbertspace: HilbertSpace
        """
        self.hilbertspace = hilbertspace

        self.updateCalc()

    @Slot(FullExtr)
    def updateExtractedData(self, fullExtr: FullExtr):
        """
        Update the extracted data and update the calculation.

        Parameters
        ----------
        fullExtr: FullExtr
            Full extracted data for all figures.
        """
        self._fullExtr = fullExtr
        # at the moment we don't update the calculation after the extracted data is updated

    @Slot(dict)
    def updateRawXMap(self, rawXByX: Dict[str, Callable[[float], Dict[str, float]]]):
        """
        Update the rawXByX dictionary. For each figure, there is a function
        which maps the extracted x coordinate
        to the raw x (all of the control knobs) coordinates.

        Parameters
        ----------
        rawXByX: Dict[str, Callable[[float], Dict[str, float]]]
            Key: figure name
            Value: a function that maps the extracted x coordinate to the raw x
            coordinate
        """
        self._rawXByX = rawXByX

    @Slot(object)
    def updateXCaliFunc(self, sweepParamSets: Dict[str, SweepParamSet] | Literal[False]):
        """
        Update the x calibration function that is stored in the sweepParamSets.
        It also updates the calculation.

        Parameters
        ----------
        sweepParamSets: Dict[str, SweepParamSet]
            Key: figure name
            Value: SweepParamSet
        """
        self._sweepParamSets = sweepParamSets
        self.updateCalc()

    @Slot(object, object)  # can't use Callable here in the initialization
    # because Argument of type "type[Callable]" cannot be assigned to parameter of type "type"
    def updateYCaliFunc(
        self, 
        yCaliFunc: Callable | Literal[False], 
        invYCaliFunc: Callable | Literal[False]
    ):
        """
        Update the y calibration function.

        Parameters
        ----------
        yCaliFunc: Callable
            The calibration function that maps the raw y to the calibrated
            y.
        invYCaliFunc: Callable
            The inverse calibration function that maps the calibrated y to the
            raw y.
        """
        self._yCaliFunc = yCaliFunc
        self._yInvCaliFunc = invYCaliFunc
        self.sweep2SpecMSE(sweepUsage=self.sweepUsage)

    @Slot(str, object)
    def storeSweepOption(
        self,
        attrName: Literal[
            "subsysToPlot",
            "initialStates",
            "photons",
            "evalsCount",
            "pointsAdded",
            "numCPUs",
            "autoRun",
        ],
        value: Any,
    ):
        """
        Set the sweep options including the subsystems to plot, the initial state,
        the photon number, the number of eigenenergies to be calculated, the number
        of points added to the x coordinate, and the auto run option.

        Parameters
        ----------
        attrName: str
            The name of the attribute to be set.
        value: Any
            The value to be set.
        """
        # process the raw value from UI
        if attrName == "subsysToPlot":
            if value != "None Selected":
                id_str = SweepParamSet.parentSystemIdstrByName(value)
                value = self.hilbertspace.subsys_by_id_str(id_str)
        elif attrName == "initialStates":
            value = self._multiStateStr2Label(value)
        elif attrName == "photons":
            value = int(value)
        elif attrName == "evalsCount":
            value = int(value)
        elif attrName == "pointsAdded":
            value = int(value)
        elif attrName == "numCPUs":
            value = int(value)
        elif attrName == "autoRun":
            value = bool(value)

        # set the value
        setattr(self, "_" + attrName, value)

        if attrName in ["subsysToPlot", "initialStates", "photons"]:
            self.sweep2SpecMSE(sweepUsage=self.sweepUsage)
        elif attrName in ["evalsCount", "pointsAdded", "autoRun"]:
            self.updateCalc()

    @Slot(np.ndarray, np.ndarray)
    def relimX(self, x: np.ndarray, y: np.ndarray):
        """
        Update the x limit of the plot, so that the sweep runs from one
        end to the other.
        """
        self._xLim = (np.min(x), np.max(x))

    def exportSweepOption(self) -> Dict[str, Any]:
        """
        Export the sweep options to view.

        Returns
        -------
        A tuple of the attribute name and the value.
        """
        initStatesStr = ""
        for state in self._initialStates:
            if isinstance(state, tuple):
                initStatesStr += str(state)[1:-1] + ";"  # remove the parentheses
            elif isinstance(state, int):
                initStatesStr += str(state) + ";"
            else:
                initStatesStr += ""
        initStatesStr = initStatesStr[:-1]  # remove the last semicolon

        return {
            "subsysToPlot": SweepParamSet.parentSystemNames(self._subsysToPlot),
            "initialState": initStatesStr,
            "photons": self._photons,
            "evalsCount": str(self._evalsCount),
            "pointsAdded": str(self._pointsAdded),
            "numCPUs": str(self._numCPUs),
            "autoRun": self._autoRun,
        }

    @Slot(str)
    def updateModeOnPageChange(
        self, currentPage: Literal["setup", "calibrate", "extract", "prefit", "fit"]
    ):
        """
        Update the mode of the sweep based on the current page.
        """
        if currentPage == "prefit":
            self.sweepUsage = currentPage
        elif currentPage == "fit":
            self.sweepUsage = currentPage
        else:
            self.sweepUsage = "none"

    # signals =================================================================
    def emitReadyToPlot(
        self,
        sweepToPlot: str | None = None,
        signalToEmit: SignalInstance | None = None,
    ):
        """
        Emit the signal to update the spectrum plot.
        """
        if sweepToPlot is None:
            sweep = self._currentSweep
        else:
            sweep = self._sweeps[sweepToPlot]
            
        if sweep is None:
            # this will only happen during the fit stage, where no sweep
            # is generated for an empty figure
            return
        
        if signalToEmit is None:
            signalToEmit = self.readyToPlotMainCanvas
        
        # compute the spectrum data for each initial state
        overall_specdata_list = []
        highlight_specdata_list = []
        for initState in self._initialStates:
            overall_specdata, highlight_specdata = self._specDataBySweep(
                sweep,
                initState,
            )
            overall_specdata_list.append(overall_specdata)
            highlight_specdata_list.append(highlight_specdata)

        # emit the spectrum data to the plot view
        spectrum_element = SpectrumElement(
            "spectrum",
            overall_specdata_list,
            highlight_specdata_list,
        )
        signalToEmit.emit(spectrum_element)

    # properties ==============================================================
    @property
    def _currentSweep(self) -> ParameterSweep:
        return self._sweeps[self._currentFigName]

    @property
    def readyToOpt(self) -> bool:
        if self._fullExtr.count() == 0:
            status = Status(
                statusSource=self.sweepUsage,
                statusType="error",
                message="No extracted data is available for fitting.",
            )
            self.updateStatus.emit(status)
            return False
        
        if not self.ingredientsReady():
            return False

        return True

    # tools ===================================================================
    def _stateStr2Label(self, state_str: str) -> int | Tuple[int, ...] | None:
        """
        Convert a label in string (something like "0, 1, 2")
        to a numerical label, which is a tuple or an integer.
        """
        # empty string means None
        if state_str == "":
            return None

        # comma separated string means tuple
        if "," in state_str:
            label_str = state_str.split(",")

            if len(label_str) != self.hilbertspace.subsystem_count:
                raise ValueError(
                    f"The state label length {len(label_str)} does not match the subsystem "
                    f"count {self.hilbertspace.subsystem_count}."
                )

            try:
                return tuple(
                    int(x) for x in label_str if x != ""
                )  # delete '' in the tuple
            except ValueError:
                raise ValueError(
                    f"Cannot convert {state_str} to a state label. Please check the format."
                )

        # otherwise, try to interpret it as an integer
        try:
            return int(state_str)
        except ValueError:
            raise ValueError(
                f"Cannot convert {state_str} to a state label. Please check the format."
            )
            
    def _multiStateStr2Label(self, state_str: str) -> List[int | Tuple[int, ...] | None]:
        """
        Convert a multi-state label in string (something like "0, 1, 2; 1, 2, 3")
        to a list of numerical labels, which is a list of tuples or integers.
        """
        states = []
        for state_str in state_str.split(";"):
            states.append(self._stateStr2Label(state_str))
        return states
            
    def _invCaliSpec(self, specData: SpectrumData):
        """
        scale the spectrum data accordingly, based on the calibration
        this step is carried out based on the inverse calibration function
        in the calibration data
        """
        specData.energy_table = self._yInvCaliFunc(specData.energy_table)

    def _specDataBySweep(
        self,
        sweep: ParameterSweep,
        initState: int | Tuple[int, ...] | None,
    ) -> Tuple[SpectrumData, SpectrumData]:
        """
        Calculate the spectrum data by the sweep.
        """
        # since we always specify the subsystems to plot, we need change the
        # default setting for initial state: None means (0, 0, ...)
        if initState is None:
            initState = (0,) * self.hilbertspace.subsystem_count

        # spectrum data for highlighting
        if self._subsysToPlot == "None Selected":
            subsystems = None
        else:
            subsystems = self._subsysToPlot

        highlight_specdata = sweep.transitions(
            as_specdata=True,
            subsystems=subsystems,
            initial=initState,
            final=None,
            sidebands=True,
            photon_number=self._photons,
            make_positive=True,
        )

        # overall data
        overall_specdata = copy.deepcopy(
            sweep[(slice(None),)].dressed_specdata
        )
        overall_specdata.energy_table -= highlight_specdata.subtract

        # scale the spectrum data accordingly, based on the calibration
        self._invCaliSpec(overall_specdata)
        self._invCaliSpec(highlight_specdata)
        
        return overall_specdata, highlight_specdata

    def ingredientsReady(self) -> bool:
        """
        Determine whether the calibration data exists and emit the error message
        if it does not exist.
        """
        if self._sweepParamSets is False:
            status = Status(
                statusSource=self.sweepUsage,
                statusType="error",
                message="X calibration data is invalid.",
            )
            self.updateStatus.emit(status)
            return False
        if self._yCaliFunc is False or self._yInvCaliFunc is False:
            status = Status(
                statusSource=self.sweepUsage,
                statusType="error",
                message="Y calibration data is invalid.",
            )
            self.updateStatus.emit(status)
            return False
        
        return True
    
    # generate sweep ==========================================================
    def _sweptX(self, addPoints: bool = True) -> Dict[str, np.ndarray]:
        """
        Generate a list of x coordinates for the prefit. The x coordinates are
        currently made of
        1. a uniformly distributed list of x coordinates in
        between the min and max of the x-coordinates of the extracted data
        2. the x-coordinates of the extracted data.
        
        For the standalone canvas, the x-coordinates are uniformly distributed
        according to the sweepConfigForStandaloneCanvas.
        """
        sweptX = {}
        
        # for each figure
        for figName, extracted_data_set in self._fullExtr.items():
            extrX = extracted_data_set.distinctSortedX()

            if figName == self._currentFigName and addPoints:
                # add uniformly distributed x coordinates if current figure
                # is being plotted
                x_coordinates_uniform = np.linspace(*self._xLim, self._pointsAdded)
                x_coordinates_all = np.concatenate([extrX, x_coordinates_uniform])
                sweptX[figName] = np.sort(x_coordinates_all)
            else:
                # only calculate the spectrum for the extracted data x coordinates
                sweptX[figName] = extrX
                
        # for each standalone canvas
        for name, config in self._sweepConfigsForStandaloneCanvas.items():
            sweptX[name] = np.linspace(
                *config.xLim, 
                config.pointsAdded if addPoints else 0
            )
                
        return sweptX

    def _updateHSForSweep(
        self,
    ) -> Dict[str, Callable[[float], None]]:
        """
        Update the HilbertSpace object with the values of parameters and coupling coefficients
        received from the UI when the sweep is running. This method returns a callable for
        `update_hilbertspace` that is passed to the ParameterSweep object.
        """
        updateHSDict = {}
        
        # for each figure
        for figName, sweepParamSet in self._sweepParamSets.items():
            rawXByX = self._rawXByX[figName]

            def updateHilbertspace(
                x: float,
                sweepParamSet = sweepParamSet,
                rawXByX = rawXByX,
            ) -> None:
                # map x to the rawX (voltage vector)
                rawX = rawXByX(x)
                sweepParamSet.setByRawX(rawX)
                sweepParamSet.updateParamForHS()

            updateHSDict[figName] = updateHilbertspace
            
        # for each standalone canvas
        for name, config in self._sweepConfigsForStandaloneCanvas.items():
            caliByFigName = config.caliByFigName
            updateHSDict[name] = updateHSDict[caliByFigName]

        return updateHSDict

    def _subsysUpdateInfo(self) -> Dict[str, List]:
        """
        Return a dictionary that maps the figure names to the list of subsystems
        that need to be updated when the x-coordinate is changed.
        """
        # for each figure
        info = {
            figName: list(
                set(sweepParamSet.parentObjByName[key] for key in sweepParamSet.keys())
            )
            for figName, sweepParamSet in self._sweepParamSets.items()
        }
        
        # for each standalone canvas
        for name, config in self._sweepConfigsForStandaloneCanvas.items():
            caliByFigName = config.caliByFigName
            info[name] = info[caliByFigName]
            
        return info

    def _generateSweep(
        self,
        sweptX: Dict[str, np.ndarray],
        updateHS: Dict[str, Callable[[float], None]],
        subsysUpdateInfo: Dict[str, List],
    ) -> Dict[str, ParameterSweep]:
        """
        Generate a ParameterSweep object from the HilbertSpace object.

        Parameters
        ----------
        sweptX: Dict[str, np.ndarray]
            Key: figure name
            Value: a list of x coordinates for sweeping, which is a direct
            argument to the ParameterSweep object.
        updateHS: Dict[str, Callable[[float], None]]
            Key: figure name
            Value: a function that updates the HilbertSpace object, which
            is a direct argument to the ParameterSweep object.
        subsysUpdateInfo: Dict[str, List]
            Key: figure name
            Value: a list of subsystems that need to be updated when the
            x-coordinate is changed, which is a direct argument to the
            ParameterSweep object.

        Returns
        -------
        Dict[str, ParameterSweep]
            Key: figure name
            Value: ParameterSweep object for each figure.
        """
        sweeps = {}

        for figName, x_coordinate in sweptX.items():
            if x_coordinate.size == 0:
                # It happens when the user doesn't extract any date
                # Either in the fit mode or the figure is not being plotted
                sweeps[figName] = None
                continue
            
            paramvals_by_name = {"x": x_coordinate}
            update_hilbertspace = updateHS[figName]
            subsys_update_info = {"x": subsysUpdateInfo[figName]}

            param_sweep = ParameterSweep(
                hilbertspace=self.hilbertspace,
                paramvals_by_name=paramvals_by_name,
                update_hilbertspace=update_hilbertspace,
                evals_count=self._evalsCount,
                subsys_update_info=subsys_update_info,
                autorun=False,
                num_cpus=self._numCPUs,  # change this later to connect to the number from the view
            )
            sweeps[figName] = param_sweep
            
        if all([sweep is None for sweep in sweeps.values()]):
            raise ValueError("No extracted data is available to generate a parameter sweep.")

        return sweeps

    def _newSweep(self) -> None:
        """
        Create a new ParameterSweep object based on the stored data.
        """
        try:
            self._sweeps = self._generateSweep(
                sweptX=self._sweptX(
                    addPoints=(self.sweepUsage in ["prefit", "fit-result"])
                ),
                updateHS=self._updateHSForSweep(),
                subsysUpdateInfo=self._subsysUpdateInfo(),
            )
        except Exception as e:
            if self.sweepUsage == "fit":
                # interrupt the fit process by the cost function, and such error
                # will be handled in the fit model
                raise e
            else:
                status = Status(
                    statusSource=self.sweepUsage,
                    statusType="error",
                    message=f"Fail to generate sweep due to: {e}",
                )
                self.updateStatus.emit(status)

        # only issue computing status in the prefit stage
        # for fit, new sweep is generated at every iteration, so we don't issue the
        # computing status here
        if self.sweepUsage == "prefit":
            status = Status(
                statusSource=self.sweepUsage,
                statusType="computing",
                message="",
            )
            self.updateStatus.emit(status)

    def _runSweep(self) -> None:
        """
        Run the existing sweeps. This method must be called after calling
        the _newSweep method.

        Note that there is a twin method _runSweepInThread. If this method is
        updated, the other method should be updated as well.
        """
        for sweep in self._sweeps.values():
            # if there is no extracted data: do not run the sweep
            if sweep is None:
                continue

            # manually turn off the warning message
            sweep._out_of_sync_warning_issued = True
            try:
                sweep.run()
            except Exception as e:
                if self.sweepUsage == "fit":
                    # interrupt the fit process by the cost function, and such error
                    # will be handled in the fit model
                    raise e
                else:
                    status = Status(
                        statusSource=self.sweepUsage,
                        statusType="error",
                        message=f"{e}",
                    )
                    self.updateStatus.emit(status)

    def _runSweepInThread(
        self, forced: bool = False, sweepUsage: str = "prefit"
    ) -> None:
        """
        Run sweep in a separate thread. After finished, _postSweepInThread
        will be called, which will handle errors and call sweep2SpecMSE.

        Parameters
        ----------
        forced: bool
            If True, the sweep will be run and the spectrum will be calculated
            regardless of the sweepUsage and autoRun settings.
        sweepUsage: str
            The usage of the sweep. It can be "prefit", "fit", or "fit-result".
            It helps to determine how and whether the spectrum will be calculated.
            It's not used in the running process, but it's passed to the
            _postSweepInThread method.
        """
        runner = SweepRunner(self._sweeps, forced=forced, sweepUsage=sweepUsage)
        runner.signalHost.sweepFinished.connect(self._postSweepInThread)  
        self._sweepThreadPool.start(runner)

    @Slot(object, bool, str)
    def _postSweepInThread(
        self,
        result: Union[Dict[str, ParameterSweep], str],
        forced: bool,
        sweepUsage: str,
    ):
        """
        This method is called after the sweep in the thread is finished. It
        handles errors and calls sweep2SpecMSE if the sweep is successful.

        Parameters
        ----------
        result: Union[Dict[str, ParameterSweep], str]
            The result of the sweep. If it's a string, it's an error message.
            If it's a dictionary, it's the sweep object.
        forced: bool
            It's passed to the sweep2SpecMSE method, so that the spectrum will
            be calculated if it's True regardless of the sweepUsage and autoRun.
        sweepUsage: str
            The usage of the sweep. It's passed to the sweep2SpecMSE method.
        """
        if isinstance(result, str):
            if self.sweepUsage == "fit":
                # interrupt the fit process by the cost function, and such error
                # will be handled in the fit model
                raise Exception(result)
            else:
                status = Status(
                    statusSource=sweepUsage,
                    statusType="error",
                    message=result,
                )
                self.updateStatus.emit(status)
        else:
            self._sweeps = result
            self.sweep2SpecMSE(forced=forced, sweepUsage=sweepUsage)

    # public methods ===========================================================
    @Slot(bool, str)
    def sweep2SpecMSE(self, forced: bool = False, sweepUsage: str = "prefit") -> float:
        """
        Given the existing sweeps, calculate and emit the spectrum and the
        mean square error
        between the extracted data and the simulated data.

        Parameters
        ----------
        forced: bool
            If True, the spectrum will be calculated regardless of the sweepUsage
            and autoRun settings.
        sweepUsage: str
            The usage of the sweep. It can be "prefit", "fit", or "fit-result".
            It helps to determine how and whether the spectrum will be calculated.

        Returns
        -------
        float
            The mean square error between the extracted data and the simulated data.
        """
        if not self.ingredientsReady():
            return 0.0
        
        if sweepUsage != "prefit" and not forced:
            # only in prefit mode, this method will be activated as a slot
            # function
            return 0.0

        try:
            self._sweeps
        except AttributeError:
            self._newSweep()

        if sweepUsage in ["prefit", "fit-result"]:
            self.emitReadyToPlot()
            
            for name, config in self._sweepConfigsForStandaloneCanvas.items():
                self.emitReadyToPlot(
                    sweepToPlot=name,
                    signalToEmit=config.readyToPlot,
                )

        # mse calculation
        mse = self._calculateMSE()
        return mse

    @Slot()
    def updateCalc(self, forced: bool = False) -> Union[None, float]:
        """
        newSweep + sweep2SpecMSE. This method is called when the ingredients
        for the sweep are updated. It will generate a new sweep and calculate
        the spectrum and the mean square error between the extracted data and
        the simulated data.

        Parameters
        ----------
        forced: bool
            If True, the spectrum will be calculated regardless of the sweepUsage
            and autoRun settings.
        """
        if not self.ingredientsReady():
            return
        
        if (self.sweepUsage != "prefit") and (not forced):
            # only in prefit mode, this method will be activated as a slot
            # function
            return

        if self._autoRun and (self.sweepUsage == "prefit"):
            self._newSweep()
            self._runSweepInThread(forced=forced, sweepUsage=self.sweepUsage)
        elif forced and (self.sweepUsage in ["prefit", "fit-result"]):
            self._newSweep()
            self._runSweepInThread(forced=forced, sweepUsage=self.sweepUsage)
        elif forced and (self.sweepUsage == "fit"):
            self._newSweep()
            self._runSweep()
            return self.sweep2SpecMSE(forced=forced, sweepUsage=self.sweepUsage)

    # calculate MSE ===========================================================
    @staticmethod
    def _thermalInitialStates(
        evals: ndarray,
    ) -> List[int]:
        """
        Given the eigenenergies, find the possible initial states of the 
        transition that is below POSSIBLE_INIT_STATE_FREQUENCY.
        """
        assert evals.ndim == 1, "evals must be a 1D array"
        diff_evals = evals - evals[0]
        return list(np.where(diff_evals < settings.POSSIBLE_INIT_STATE_FREQUENCY)[0])
    
    @staticmethod
    def _closestTransFreq(
        dataFreq: float,
        evals: ndarray,
        initial: List[int] | None = None,
        final: List[int] | None = None,
    ) -> float:
        """
        Given a list of eigenenergies, find the closest transition frequency,
        starting from the selected initial and ending at the selected final states.

        Parameters
        ----------
        dataFreq: float
            The transition frequency from the extracted data. With that,
            we can find the closest transition frequency if the initial 
            and final states are uncertain.
        evals: ndarray
            The eigenenergies of the system. (1D array)
        initial: List[int] | None
            The initial state indices. If None, transitions starting
            every state will be used.
        final: List[int]
            The final state indices. If None, transitions ending
            every state will be used.
        """
        # compute all possible transition frequencies
        # first index is the initial state, second index is the final state
        allToAllFreqs = np.subtract.outer(evals, evals).T
        # slice the possible transitions
        if initial is not None and final is not None:
            slc = np.ix_(initial, final)
        elif initial is not None and final is None:
            slc = (initial, slice(None))
        elif initial is None and final is not None:
            slc = (slice(None), final)
        else:
            slc = (slice(None), slice(None))
        possibleTransitions = allToAllFreqs[slc]
        possibleTransitions = possibleTransitions.flatten()
        
        # find the closest transition frequency
        closestIdx = np.abs(np.abs(possibleTransitions) - dataFreq).argmin()
        return possibleTransitions[closestIdx]
    
    def _numericalSpecByTag(
        self,
        xData: float,
        yDataFreq: float,
        tag: Tag,
        sweep: ParameterSweep,
        takeAbsFreq: bool = True,
    ) -> Tuple[
        float,
        Literal[
            "SUCCESS",
            "DRESSED_OUT_OF_RANGE",
            "NO_TAG",
            "BARE_OUT_OF_RANGE",
            "INCOMPLETE_TAG",
            "BARE_UNIDENTIFIABLE",
        ],
    ]:
        """
        Given ONE extractred data point, obtain the cooresponding transition frequency
        provided by the tag from a ParameterSweep instance. If the tag is not
        provided or we can not identify dressed states' bare label via overlap,
        the closest transition frequency starting from the ground state will be
        returned.

        Parameters
        ----------
        xData: float
            The x coordinate of the extracted data.
        yDataFreq: float
            The transition frequency (y coordinate) of the extracted data.
        tag: Tag
            The tag of the extracted data - user's input on which transition
            to calculate.
        sweep: ParameterSweep
            The parameter sweep object, which stores the eigenenergies and the
            labels of the dressed states.

        Returns
        -------
        float
            The transition frequency that matches the tag.
        Literal[
            "SUCCESS",
            "LABEL_OUT_OF_RANGE",
            "NO_TAG",
            "INCOMPLETE_TAG",
            "BARE_UNIDENTIFIABLE",
        ]
            The status of the calculation.
        """
        eigenenergies = sweep["evals"]["x":xData]
        status = "SUCCESS"

        if tag.tagType == "NO_TAG":
            status = "NO_TAG"
            # fiting to all possible transitions starting from the ground state
            # and the any excited state that is below POSSIBLE_INIT_STATE_FREQUENCY
            availableLabels = {
                "initial": self._thermalInitialStates(eigenenergies),
                "final": None,
            }

        elif tag.tagType == "DISPERSIVE_DRESSED":
            # if the state is above evals_count, terminate the computation and return error status
            
            if None in tag.initial:
                status = "INCOMPLETE_TAG"
                initial = self._thermalInitialStates(eigenenergies)
            elif sweep.dressed_evals_count() < max(tag.initial):
                status = "LABEL_OUT_OF_RANGE"
                return np.nan, status
            else:
                initial = tag.initial
                
            if None in tag.final:
                status = "INCOMPLETE_TAG"
                final = None
            elif sweep.dressed_evals_count() < max(tag.final):
                status = "LABEL_OUT_OF_RANGE"
                return np.nan, status
            else:
                final = tag.final
            
            availableLabels = {"initial": initial, "final": final}

        # if provided bare label
        elif tag.tagType == "DISPERSIVE_BARE":
            if None in tag.initial:
                status = "INCOMPLETE_TAG"
                initial = self._thermalInitialStates(eigenenergies)
            elif not all([idx < tuple(self.hilbertspace.subsystem_dims) for idx in tag.initial]):
                status = "LABEL_OUT_OF_RANGE"
                return np.nan, status
            else:
                initial = [sweep.dressed_index(idx)["x":xData] for idx in tag.initial]  
                if None in initial:
                    status = "BARE_UNIDENTIFIABLE"
                    # when there is unidentifiable initial state,
                    # remove the nan index, and add the thermal initial states
                    initial = [idx for idx in initial if idx is not None]
                    thermal_initial = self._thermalInitialStates(eigenenergies)
                    initial = list(set(initial + thermal_initial))
                
            if None in tag.final:
                status = "INCOMPLETE_TAG"
                final = None
            elif not all([idx < tuple(self.hilbertspace.subsystem_dims) for idx in tag.final]):
                status = "LABEL_OUT_OF_RANGE"
                return np.nan, status
            else:
                final = [sweep.dressed_index(idx)["x":xData] for idx in tag.final]
                if None in final:
                    status = "BARE_UNIDENTIFIABLE"
                    # when there is unidentifiable final state,
                    # we just compare it with the full eigenenergies
                    final = None
                
            availableLabels = {"initial": initial, "final": final}

        simulationFreq = self._closestTransFreq(
            dataFreq=yDataFreq,
            evals=eigenenergies,
            **availableLabels,
        )
        if takeAbsFreq:
            simulationFreq = np.abs(simulationFreq)
        return simulationFreq, status

    def _MSEByTransition(
        self,
        sweep: ParameterSweep,
        transition: ExtrTransition,
    ) -> Tuple[float, set[Literal[
        "SUCCESS",
        "INCOMPLETE_TAG",
        "BARE_UNIDENTIFIABLE",
        "NO_TAG",
    ]]]:
        """
        Calculate the mean square error for a single transition.

        Parameters
        ----------
        sweep: ParameterSweep
            The parameter sweep object.
        transition: ExtrTransition
            The extracted transition data.
        """
        mse = 0.0
        mseCalcStatus = set()
        tag = transition.tag

        for xData, yData in transition.data.T:
            # obtain the transition frequency from the transition data
            yData = self._yCaliFunc(yData)
            (
                transitionFreq,
                getTransitionFreqStatus,
            ) = self._numericalSpecByTag(
                xData=xData,
                yDataFreq=yData,
                tag=tag,
                sweep=sweep,
            )

            # process the status
            # if the transition_freq is None, return directly with a mse of None
            if getTransitionFreqStatus == "LABEL_OUT_OF_RANGE":
                raise ValueError(
                    f"The tag {tag.initial} -> {tag.final} includes "
                    "state indices that exceed the evaluated eigenvalue count."
                )
                
            # for now, we just summarize them as LABEL_CORRECTED
            mseCalcStatus.add(getTransitionFreqStatus)
            
            # finish the calculation
            photons = 1 if tag.photons is None else tag.photons
            transitionFreq /= photons
            mse += (yData - transitionFreq) ** 2

        return mse, mseCalcStatus

    def _calculateMSE(self) -> float:
        """
        Calculate the mean square error between the extracted data and the simulated data
        from the parameter sweep. It is calculated for each transition
        and then averaged.

        """
        if self._fullExtr.count() == 0:
            status = Status(
                statusSource=self.sweepUsage,
                message="Successful spectrum calculation, while no extracted data is available.",
                statusType="success",
                mse=np.nan,
            )
            self.updateStatus.emit(status)
            return np.nan

        mse = 0

        overallMseCalcStatus = set()
        for figName, extrSpec in self._fullExtr.items():
            sweep = self._sweeps[figName]
            # if there is no extracted data: do not calculate the MSE
            if sweep is None:
                continue

            # manually turn off the warning message
            sweep._out_of_sync_warning_issued = True

            for transition in extrSpec:
                try:
                    newMse, mseCalcStatus = self._MSEByTransition(
                        sweep, transition
                    )
                    overallMseCalcStatus.update(mseCalcStatus)
                    mse += newMse
                except Exception as e:
                    statusType = "error"
                    statusText = (
                        f"MSE calculation failed for <{transition.name}> in <{figName}>'s "
                        f" due to: {e}"
                    )
                    # emit error message
                    status = Status(
                        statusSource=self.sweepUsage,
                        statusType=statusType,
                        message=statusText,
                    )
                    self.updateStatus.emit(status)
                    return np.nan

        # normalize the MSE
        mse /= self._fullExtr.count()

        # if in fit mode, return the mse directly, the status message will be
        # handled in the fit model instead
        if self.sweepUsage in ["fit", "fit-result"]:
            return mse
        
        # otherwise, add to the status text if there is any unidentifiable tag
        # and send out the status
        if overallMseCalcStatus != set(["SUCCESS"]):
            problems = []
            if "INCOMPLETE_TAG" in overallMseCalcStatus:
                problems.append("incomplete")
            if "BARE_UNIDENTIFIABLE" in overallMseCalcStatus:
                problems.append("unidentifiable")
            if "NO_TAG" in overallMseCalcStatus:
                problems.append("no")
            problemsStr = " or ".join(problems)
                
            statusType = "warning"
            message = (
                f"Found extracted transitions with {problemsStr} labels. "
                "Any missing initial state label will be replaced by the "
                "lowest-lying states, and any missing final state label will "
                "be replaced by the all possible eigenstates."
            )
            status = Status(
                statusSource=self.sweepUsage,
                statusType=statusType,
                message=message,
                mse=mse,
            )
            self.updateStatus.emit(status)

        # else, send out the success status with the MSE
        else:
            statusType = "success"
            message = "Successful spectrum and MSE calculation."
            status = Status(
                statusSource=self.sweepUsage,
                message=message,
                statusType=statusType,
                mse=mse,
            )
            self.updateStatus.emit(status)
        
        return mse
        
    # Plotting to a standalone canvas
    # ==================================================================
    def _newStandaloneCanvas(
        self, 
        name: str,
        pointsAdded: int,
        xLim: Tuple[float, float],
        caliByFigName: str,
    ):
        """
        Initialize a standalone canvas.
        
        Parameters
        ----------
        name: str
            The name of the standalone canvas.
        pointsAdded: int
            The number of points for the sweep.
        xLim: Tuple[float, float]
            The x limits of the canvas, range of the sweeped x-axis.
        caliByFigName: str
            Calibration function. For a standalone canvas, it must contain the 
            x, y axis that are colinear, so any of the calibration function 
            associated with a figName in the canvas can be used.
        """
        assert caliByFigName in self._figNames, "Calibration function not found"
        assert name not in self._sweepConfigsForStandaloneCanvas, "Canvas already exists"
        assert name not in self._figNames, "Canvas (Main canvas) already exists"
        
        self._sweepConfigsForStandaloneCanvas[name] = SweepConfigForStandaloneCanvas(
            pointsAdded=pointsAdded,
            xLim=xLim,
            caliByFigName=caliByFigName,
        )
        
    def _removeSweepForStandaloneCanvas(self, name: str):
        """
        Garbage collection for removed standalone canvas.
        """
        self._sweepConfigsForStandaloneCanvas[name].cleanup()
        self._sweepConfigsForStandaloneCanvas.pop(name)
        
        if name in self._sweeps:
            self._sweeps.pop(name)
        


class sweepSignalHost(QObject):
    sweepFinished = Signal(object, bool, str)


class SweepRunner(QRunnable):
    """
    A QRunnable class that runs the sweep in a separate thread. It emits the
    signal when the sweep is finished.

    Parameters
    ----------
    sweeps: Dict[str, ParameterSweep]
        The parameter sweep objects.
    forced: bool
        It will be passed to the _postSweepInThread method.
    """


    def __init__(
        self,
        sweeps: Dict[str, ParameterSweep],
        forced: bool = False,
        sweepUsage: str = "prefit",
    ):
        super().__init__()
        self.sweeps = sweeps
        self.forced = forced
        self.sweepUsage = sweepUsage
        self.signalHost = sweepSignalHost()

    def run(self):
        for sweep in self.sweeps.values():
            # if there is no extracted data: do not run the sweep
            if sweep is None:
                continue

            # manually turn off the warning message
            sweep._out_of_sync_warning_issued = True
            try:
                sweep.run()
            except Exception as e:
                self.signalHost.sweepFinished.emit(str(e), self.forced, self.sweepUsage)

        self.signalHost.sweepFinished.emit(self.sweeps, self.forced, self.sweepUsage)
