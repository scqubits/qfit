from PySide6.QtCore import Slot, Signal, QObject, QRunnable, QThreadPool

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
from qfit.models.data_structures import Tag, SpectrumElement

from qfit.models.data_structures import Status

from typing import Dict, List, Tuple, Union, Callable, Any, Literal, Optional


class QuantumModel(QObject):
    """
    Generate and manipulate a parameter sweep for a quantum model.

    Parameters
    ----------
    hilbertspace: HilbertSpace
    """

    _sweeps: Dict[str, ParameterSweep]

    readyToPlot = Signal(SpectrumElement)
    mseReadyToFit = Signal(float)

    updateStatus = Signal(Status)

    # options

    def __init__(
        self,
        parent: QObject,
    ):
        super().__init__(parent)

        self._sweepThreadPool = QThreadPool()
        SweepRunner.signalHost.sweepFinished.connect(self._postSweepInThread)

    def dynamicalInit(self, hilbertspace: HilbertSpace, figNames: List[str]):
        self.hilbertspace = hilbertspace
        self._figNames = figNames
        self._currentFigName = self._figNames[0]

        self._initializeSweepIngredients()

    def _initializeSweepIngredients(self):
        # extracted data
        self._fullExtr = FullExtr()

        # calibration
        self._sweepParamSets: Dict[str, SweepParamSet] = {
            figName: SweepParamSet() for figName in self._figNames
        }
        self._yCaliFunc: Callable = lambda x: x
        self._yInvCaliFunc: Callable = lambda x: x

        # options when generating the parameter sweep
        self._evalsCount: int = np.min([10, self.hilbertspace.dimension])
        self._pointsAdded: int = 10
        self._rawXByX: Dict[str, Callable[[float], Dict[str, float]]] = {
            figName: lambda x: {} for figName in self._figNames
        }
        self._xLim: Tuple[float, float] = (0, 1)

        # options when plotting the spectrum
        self._subsysToPlot: QuantumSystem = self.hilbertspace.subsystem_list[0]
        self._initialState: Union[int, Tuple[int, ...], None] = None
        self._photons: int = 1

        # options when running
        self._autoRun: bool = True
        self.sweepUsage: Literal[
            "none", "prefit", "fit", "fit-result"
        ] = "none"

    # Signals and Slots ========================================================
    @Slot(str)
    def switchFig(self, figName: str):
        self._currentFigName = figName
        self.updateCalc()

    @Slot(HilbertSpace)
    def updateHilbertSpace(
        self, 
        hilbertspace: HilbertSpace,
    ):
        """
        Update the HilbertSpace object.

        Parameters
        ----------
        hilbertspace: HilbertSpace
        """
        self.hilbertspace = hilbertspace

        self.updateCalc()

    @Slot(FullExtr)
    def updateExtractedData(self, fullExtr: FullExtr):
        """
        Update the extracted data.

        Parameters
        ----------
        dataNames: List[str]
        data: List[ndarray]
        tags: List[Tag]
        """
        self._fullExtr = fullExtr
        # at the moment we don't update the calculation after the extracted data is updated

    @Slot(dict)
    def updateRawXMap(self, rawXByX: Dict[str, Callable[[float], Dict[str, float]]]):
        """
        Update the rawXByX dictionary.

        Parameters
        ----------
        rawXByX: Dict[str, ndarray]
        """
        self._rawXByX = rawXByX

    @Slot(dict)
    def updateXCaliFunc(self, sweepParamSets: Dict[str, SweepParamSet]):
        """
        Update the parameter sets for the sweeps.

        Parameters
        ----------
        sweepParamSets: Dict[str, SweepParamSet]
        """
        self._sweepParamSets = sweepParamSets

        self.updateCalc()

    @Slot(object, object)  # can't use Callable here in the initialization
    # because Argument of type "type[Callable]" cannot be assigned to parameter of type "type"
    def updateYCaliFunc(self, yCaliFunc: Callable, invYCaliFunc: Callable):
        """
        Update the y calibration function.

        Parameters
        ----------
        yCaliFunc: Callable
        """
        self._yCaliFunc = yCaliFunc
        self._yInvCaliFunc = invYCaliFunc
        self.sweep2SpecMSE()

    @Slot(str, Any)
    def storeSweepOption(
        self,
        attrName: Literal[
            "subsysToPlot",
            "initialState",
            "photons",
            "evalsCount",
            "pointsAdded",
            "autoRun",
        ],
        value: Any,
    ):
        """
        Set the sweep options.

        Parameters
        ----------
        attrName: str
            The name of the attribute to be set.
        value: Any
            The value to be set.
        """
        # process the raw value from UI
        if attrName == "subsysToPlot":
            id_str = SweepParamSet.parentSystemIdstrByName(value)
            value = self.hilbertspace.subsys_by_id_str(id_str)
        elif attrName == "initialState":
            value = self._stateStr2Label(value)
        elif attrName == "photons":
            value = int(value)
        elif attrName == "evalsCount":
            value = int(value)
        elif attrName == "pointsAdded":
            value = int(value)
        elif attrName == "autoRun":
            value = bool(value)

        # set the value
        setattr(self, "_" + attrName, value)

        if attrName in ["subsysToPlot", "initialState", "photons"]:
            self.sweep2SpecMSE()
        elif attrName in ["evalsCount", "pointsAdded", "autoRun"]:
            self.updateCalc()

    @Slot(np.ndarray, np.ndarray)
    def relimX(self, x: np.ndarray, y: np.ndarray):
        self._xLim = (np.min(x), np.max(x))

    def exportSweepOption(self) -> Dict[str, Any]:
        """
        Export the sweep options to view

        Returns
        -------
        A tuple of the attribute name and the value.
        """
        if isinstance(self._initialState, tuple):
            initStateStr = str(self._initialState)[1:-1]  # remove the parentheses
        elif isinstance(self._initialState, int):
            initStateStr = str(self._initialState)
        else:
            initStateStr = ""

        return {
            "subsysToPlot": SweepParamSet.parentSystemNames(self._subsysToPlot),
            "initialState": initStateStr,
            "photons": self._photons,
            "evalsCount": str(self._evalsCount),
            "pointsAdded": str(self._pointsAdded),
            "autoRun": self._autoRun,
        }

    @Slot(str)
    def updateModeOnPageChange(
        self, currentPage: Literal["calibrate", "extract", "prefit", "fit"]
    ):
        """
        Update the disableSweep attribute when the page changes.
        """
        if currentPage == "prefit":
            self.sweepUsage = currentPage
        elif currentPage == "fit":
            self.sweepUsage = currentPage
        else:
            self.sweepUsage = "none"

    # signals =================================================================
    def emitReadyToPlot(self):
        # since we always specify the subsystems to plot, we need change the
        # default setting for initial state: None means (0, 0, ...)
        if self._initialState is None:
            initialState = (0,) * self.hilbertspace.subsystem_count
        else:
            initialState = self._initialState

        # spectrum data for highlighting
        highlight_specdata = self._currentSweep.transitions(
            as_specdata=True,
            subsystems=self._subsysToPlot,
            initial=initialState,
            final=None,
            sidebands=False,
            photon_number=self._photons,
            make_positive=False,
        )

        # overall data
        overall_specdata = copy.deepcopy(
            self._currentSweep[(slice(None),)].dressed_specdata
        )
        overall_specdata.energy_table -= highlight_specdata.subtract

        # scale the spectrum data accordingly, based on the calibration
        self._invCaliSpec(overall_specdata)
        self._invCaliSpec(highlight_specdata)

        # emit the spectrum data to the plot view
        spectrum_element = SpectrumElement(
            "spectrum",
            overall_specdata,
            highlight_specdata,
        )
        self.readyToPlot.emit(spectrum_element)

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

        return True
    
    # tools ===================================================================
    def _stateStr2Label(self, state_str: str):
        # convert string to state label

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

    def _invCaliSpec(self, specData: SpectrumData):
        """
        scale the spectrum data accordingly, based on the calibration
        this step is carried out based on the inverse calibration function
        in the calibration data
        """
        specData.energy_table = self._yInvCaliFunc(specData.energy_table)

    # generate sweep ==========================================================
    def _prefitSweptX(self, addPoints: bool = True) -> Dict[str, np.ndarray]:
        """
        Generate a list of x coordinates for the prefit. The x coordinates are
        currently made of (1) a uniformly distributed list of x coordinates in
        between the min and max of the x-coordinates of the extracted data, and
        (2) the x-coordinates of the extracted data.
        """
        sweptX = {}
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
        for figName, sweepParamSet in self._sweepParamSets.items():
            rawXByX = self._rawXByX[figName]

            def updateHilbertspace(x: float) -> None:
                # map x to the rawX (voltage vector)
                rawX = rawXByX(x)
                sweepParamSet.setByRawX(rawX)
                sweepParamSet.updateParamForHS()

            updateHSDict[figName] = updateHilbertspace

        return updateHSDict

    def _subsysUpdateInfo(self) -> Dict[str, List]:
        """
        Return a dictionary that maps the figure names to the list of subsystems
        that need to be updated when the x-coordinate is changed.
        """
        return {
            figName: list(set(sweepParamSet.parentObjByName[
                key
            ] for key in sweepParamSet.keys()))
            for figName, sweepParamSet in self._sweepParamSets.items()
        }

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
        x_coordinate_list: ndarray
            The x coordinate of the transition plot.
        sweep_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object.
            All the parameters in the parameter set must have the calibration_func attribute.

        Returns
        -------
        A ParameterSweep object.
        """
        sweeps = {}

        for figName, x_coordinate in sweptX.items():
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
                num_cpus=1,  # change this later to connect to the number from the view
            )
            sweeps[figName] = param_sweep

        return sweeps

    def _newSweep(self) -> None:
        """
        Create a new ParameterSweep object based on the stored data.
        """
        try:
            self._sweeps = self._generateSweep(
                sweptX=self._prefitSweptX(
                    addPoints=(self.sweepUsage in ["prefit", "fit-result"])
                ),
                updateHS=self._updateHSForSweep(),
                subsysUpdateInfo=self._subsysUpdateInfo(),
            )
        except Exception as e:
            # TODO: emit error message
            status = Status(
                statusSource=self.sweepUsage,
                statusType="error",
                message=f"{e}",
            )
            self.updateStatus.emit(status)
            raise e

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
        """
        for sweep in self._sweeps.values():
            # manually turn off the warning message
            sweep._out_of_sync_warning_issued = True
            try:
                sweep.run()
            except Exception as e:
                status = Status(
                    statusSource=self.sweepUsage,
                    statusType="error",
                    message=f"{e}",
                )
                self.updateStatus.emit(status)

    def _sweepInThread(self):
        """
        Run sweep in a separate thread. After finished, _postSweepInThread 
        will be called, which will handle errors and call sweep2SpecMSE.
        """
        runner = SweepRunner(self._sweeps)
        self._sweepThreadPool.start(runner)

    @Slot(object)
    def _postSweepInThread(
        self, 
        result: Union[Dict[str, ParameterSweep], str]
    ):
        if isinstance(result, str):
            status = Status(
                statusSource=self.sweepUsage,
                statusType="error",
                message=result,
            )
            self.updateStatus.emit(status)
        else:
            self._sweeps = result
            self.sweep2SpecMSE()

    # public methods ===========================================================
    @Slot()
    def sweep2SpecMSE(self, forced: bool = False) -> float:
        """
        It is connected to the signal emitted by the UI when the user clicks the plot button
        for the prefit stage. It make use of the existing sweep object to
        get a spectrum data and MSE.
        """
        if self.sweepUsage != "prefit" and not forced:
            # only in prefit mode, this method will be activated as a slot
            # function
            return 0.0
        
        try:
            self._sweeps
        except AttributeError:
            try:
                self._newSweep()
            except Exception as e:
                status = Status(
                    statusSource=self.sweepUsage,
                    statusType="error",
                    message=f"{e}",
                )
                self.updateStatus.emit(status)
                raise e

        if self.sweepUsage in ["prefit", "fit-result"]:
            self.emitReadyToPlot()

        # mse calculation
        mse = self._calculateMSE()
        return mse

    @Slot()
    def updateCalc(self, forced: bool = False) -> Union[None, float]:
        """
        newSweep + sweep2SpecMSE (when autoRun is on / fit / called by plot button)

        It is connected to the signal emitted by the UI when the user changes the slider
        of a parameter. It receives a QuantumModelParameterSet object and updates the
        the HilbertSpace object. If auto run is on, it will also compute the spectrum
        and MSE.
        """
        if self.sweepUsage != "prefit" and not forced:
            # only in prefit mode, this method will be activated as a slot
            # function
            return
        
        if self._autoRun and self.sweepUsage == "prefit":
            self._newSweep()
            self._sweepInThread()

        elif forced and self.sweepUsage in ["prefit", "fit-result"]:
            self._newSweep()
            self._sweepInThread()

        elif forced and self.sweepUsage == "fit":
            self._newSweep()
            self._runSweep()
            return self.sweep2SpecMSE(forced=forced)

    # calculate MSE ===========================================================
    @staticmethod
    def _closestTransFreq(
        dataFreq: float,
        evals: ndarray,
        initial: Optional[int] = None,
        final: Optional[int] = None,
    ) -> float:
        """
        Given a list of eigenenergies, find the closest transition frequency.
        """
        if initial is not None and final is not None:
            assert initial < final
            return evals[final] - evals[initial]

        elif initial is not None and final is None:
            possible_transitions = evals[initial + 1 :] - evals[initial]

        elif initial is None and final is not None:
            possible_transitions = evals[final] - evals[:final]

        else:
            # enumerate all possible transitions starting from all different states
            possible_transitions = np.array(
                [
                    evals[final] - evals[initial]
                    for initial in range(len(evals))
                    for final in range(initial + 1, len(evals))
                ]
            )

        closest_idx = (np.abs(possible_transitions - dataFreq)).argmin()

        return possible_transitions[closest_idx]

    def _numericalSpecByTag(
        self,
        x_coord: float,
        sweep: ParameterSweep,
        tag: Tag,
        dataFreq: float,
    ) -> Tuple[
        float,
        Literal[
            "SUCCESS",
            "DRESSED_OUT_OF_RANGE",
            "NO_TAG",
            "NO_MATCHED_BARE_INITIAL",
            "NO_MATCHED_BARE_FINAL",
            "NO_MATCHED_BARE_INITIAL_AND_FINAL",
        ],
    ]:
        """
        Obtain the cooresponding transition frequency provided by the tag from a ParameterSweep
        instance. If the tag is not provided or can not identify states,
        the closest transition frequency is returned.
        """
        eigenenergies = sweep["evals"]["x":x_coord]

        # if provided dressed label
        if tag.tagType == "NO_TAG":
            status = "NO_TAG"
            availableLabels = {}

        elif tag.tagType == "DISPERSIVE_DRESSED":
            # if the state is above evals_count, terminate the computation and return error status
            if sweep.dressed_evals_count() < max(tag.initial, tag.final):
                status = "DRESSED_OUT_OF_RANGE"
                return np.nan, status
            else:
                status = "SUCCESS"
                availableLabels = {"initial": tag.initial, "final": tag.final}

        # if provided bare label
        elif tag.tagType == "DISPERSIVE_BARE":
            initial_energy = sweep.energy_by_bare_index(tag.initial)["x":x_coord]
            final_energy = sweep.energy_by_bare_index(tag.final)["x":x_coord]

            # when we can identify both initial and final states
            if not np.isnan(initial_energy) and not np.isnan(final_energy):
                simulation_freq = final_energy - initial_energy
                status = "SUCCESS"
                return simulation_freq, status

            # when some of the states are not identifiable
            elif np.isnan(initial_energy) and not np.isnan(final_energy):
                status = "NO_MATCHED_BARE_INITIAL"
                final_energy_dressed_label = sweep.dressed_index(tag.final)["x":x_coord]
                availableLabels = {"final": final_energy_dressed_label}

            elif not np.isnan(initial_energy) and np.isnan(final_energy):
                status = "NO_MATCHED_BARE_FINAL"
                initial_energy_dressed_label = sweep.dressed_index(tag.initial)[
                    "x":x_coord
                ]
                availableLabels = {"initial": initial_energy_dressed_label}

            else:
                status = "NO_MATCHED_BARE_INITIAL_AND_FINAL"
                availableLabels = {}

        simulation_freq = self._closestTransFreq(
            dataFreq=dataFreq,
            evals=eigenenergies,
            **availableLabels,
        )
        return simulation_freq, status

    def _MSEByTransition(
        self,
        sweep: ParameterSweep,
        transition: ExtrTransition,
        dataNameWOlabel: List[str],
    ) -> float:
        """
        Calculate the mean square error between the extracted data and the simulated data.
        """
        mse = 0.0

        tag = transition.tag

        for xData, yData in transition.data.T:
            # obtain the transition frequency from the transition data
            yData = self._yCaliFunc(yData)
            (
                transition_freq,
                get_transition_freq_status,
            ) = self._numericalSpecByTag(
                x_coord=xData,
                sweep=sweep,
                tag=tag,
                dataFreq=yData,
            )

            # process the status
            # if the transition_freq is None, return directly with a mse of None
            if get_transition_freq_status == "DRESSED_OUT_OF_RANGE":
                statusType = "error"
                statusText = (
                    f"The {tag.tagType} tag {tag.initial}->{tag.final} includes"
                    " state label(s) that exceed evals count."
                )
                # emit error message
                status = Status(
                    statusSource=self.sweepUsage,
                    statusType=statusType,
                    message=statusText,
                )
                self.updateStatus.emit(status)
                return np.nan
            # if the return status is not SUCCESS, add a warning message and set status type to WARNING
            if get_transition_freq_status != "SUCCESS":
                if transition.name not in dataNameWOlabel:
                    dataNameWOlabel.append(transition.name)

            # finish the calculation
            photons = 1 if tag.photons is None else tag.photons
            transition_freq /= photons
            mse += (yData - transition_freq) ** 2

        return mse

    def _calculateMSE(self) -> float:
        """
        Calculate the mean square error between the extracted data and the simulated data
        from the parameter sweep. Currently, the MSE is calculated from the transition
        spectrum of the self.sweep attribute (i.e. the ParameterSweep object is stored in
        the controller). This method is supposed to be called after running the parameter
        sweep.

        """
        if self._fullExtr.count() == 0:
            return 0.0

        mse = 0
        dataNameWOlabel = []

        for figName, extrSpec in self._fullExtr.items():
            sweep = self._sweeps[figName]
            for transition in extrSpec:
                mse += self._MSEByTransition(sweep, transition, dataNameWOlabel)

        # normalize the MSE
        mse /= self._fullExtr.count()

        # if in fit mode, return the mse directly, the status message will be
        # handled in the fit model instead
        if self.sweepUsage in ["fit", "fit-result"]:
            return mse
        # otherwise, add to the status text if there is any unidentifiable tag
        # and send out the status
        else:
            if dataNameWOlabel != []:
                statusType = "warning"
                message = (
                    f"Data sets {dataNameWOlabel} have unidentifiable state "
                    "labels or are untagged. "
                    "Selected transition frequencies are matched to the closest ones in the model, "
                    "starting from the ground state.\n"
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
                message = "MSE calculation successful."
                status = Status(
                    statusSource=self.sweepUsage,
                    message=message,
                    statusType=statusType,
                    mse=mse,
                )
                self.updateStatus.emit(status)
            return mse


class sweepSignalHost(QObject):
    sweepFinished = Signal(object)


class SweepRunner(QRunnable):

    signalHost = sweepSignalHost()

    def __init__(self, sweeps: Dict[str, ParameterSweep]):
        super().__init__()
        self.sweeps = sweeps

    def run(self):
        for sweep in self.sweeps.values():
            # manually turn off the warning message
            sweep._out_of_sync_warning_issued = True
            try:
                sweep.run()
            except Exception as e:
                self.signalHost.sweepFinished.emit(str(e))

        self.signalHost.sweepFinished.emit(self.sweeps)