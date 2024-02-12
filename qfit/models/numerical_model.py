from PySide6.QtCore import Slot, Signal, QObject

import numpy as np

from numpy import ndarray

from typing import overload
import copy

import scqubits as scq
from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.param_sweep import ParameterSweep
from scqubits.core.storage import SpectrumData

from typing import Dict, List, Tuple, Union, Callable
from typing_extensions import Literal

from qfit.models.parameter_settings import ParameterType

from qfit.models.quantum_model_parameters import (
    ParamSet,
)
from qfit.models.data_structures import (
    ParamBase, QMSliderParam, QMSweepParam, QMFitParam
)
from qfit.models.status import StatusModel
from qfit.models.numerical_spectrum_data import CalculatedSpecData
from qfit.models.calibration_data import CalibrationData
from qfit.models.extracted_data import AllExtractedData
from qfit.models.data_structures import Tag, SpectrumElement

def dummy_hilbert_space():
    resonator = scq.Oscillator(
        E_osc=6.0, l_osc=1.0, truncated_dim=4, id_str="resonator"
    )

    fluxonium = scq.Fluxonium(
        EJ=5.0, EC=1, EL=0.1, flux=0.0, cutoff=100, truncated_dim=5, id_str="fluxonium"
    )

    hilbertspace = scq.HilbertSpace([resonator, fluxonium])

    hilbertspace.add_interaction(
        g=0.01,
        op1=resonator.n_operator,
        op2=fluxonium.n_operator,
        add_hc=False,
        id_str="res-qubit",
    )

    return hilbertspace


class QuantumModel(QObject):
    """
    Class for handling the HilbertSpace object, including: (1) identifying parameters in each subsystem of the Hamiltonian
    and coupling coefficients of the interaction terms, (2) receiving updated values of parameters and coupling coefficients
    from the UI and reflect changes in the HilbertSpace object, (3) generating a ParameterSweep object, (4) compute the relevant
    transition spectrum. Primarily designed for prefit.

    Parameters
    ----------
    hilbertspace: HilbertSpace
    """

    readyToPlot = Signal(SpectrumElement)

    def __init__(
        self,
        hilbertspace: HilbertSpace,
    ):
        super().__init__()
        self.hilbertspace: HilbertSpace = hilbertspace

    def setupPlotUICallbacks(
        self,
        subsystemNameCallback: Callable,
        initialStateCallback: Callable,
        photonsCallback: Callable,
        evalsCountCallback: Callable,
        pointsAddCallback: Callable,
    ):
        """
        Obtain information from plot option UI including:
        * plot options
        * ...
        """

        # for test only
        # ------------------------------------------------------------------------------
        self.subsystem_names_to_plot = lambda: (
            ParamSet.parentSystemIdstrByName(subsystemNameCallback())
        )
        self.initialStateCallback = initialStateCallback
        self.photonsCallback = photonsCallback
        self.evalCountCallback = evalsCountCallback
        self.pointsAddCallback = pointsAddCallback
        # ------------------------------------------------------------------------------

    def setupAutorunCallbacks(
        self,
        autorun_callback: Callable,
    ):
        """
        Obtain information from autorun UI including
        """
        # set autorun callback
        self.autorun_callback = autorun_callback

    def subsystems_to_plot(self):
        subsys_names = self.subsystem_names_to_plot()

        if isinstance(subsys_names, str):
            return self.hilbertspace.subsys_by_id_str(subsys_names)

        # elif isinstance(subsys_names, list):
        #     return [self.hilbertspace.subsys_by_id_str(name) for name in subsys_names]

        else:
            raise TypeError(
                f"subsystem_names_to_plot() should give a string, not {type(subsys_names)}."
            )

    def _state_str_2_label(self, state_str: str):
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

    def initial_state(self):
        return self._state_str_2_label(self.initialStateCallback())

    def photons(self):
        return self.photonsCallback()

    # @overload
    # def generateParameterSets(
    #     self,
    #     included_parameter_type: List[ParameterType],
    # ) -> QuantumModelParameterSet:
    #     ...

    # @overload
    # def generateParameterSets(
    #     self,
    #     excluded_parameter_type: List[ParameterType],
    # ) -> QuantumModelParameterSet:
    #     ...

    # TODO: in future implement this function (for multiple ng and flux case)
    # @staticmethod
    # def _map1D(x: float, coeffs, biases) -> Tuple[QuantumModelParameter, ...]:
    #     """
    #     The actual swept parameters (flux, ng, ...) are linearly related to the value of
    #     the x axis of the transition plot. This funcition serves as a map between the two.
    #     """
    #     return

    def _generateXcoordinateListForMarkedPoints(
        self, extracted_data: AllExtractedData
    ) -> np.ndarray:
        """
        Generate a list of parameter values for parameter sweeps from the extracted data;
        the extracted data contains the x coordinate of the two-tone spectroscopy plot.

        Parameters
        ----------
        extracted_data: AllExtractedData
            The extracted data from the two-tone spectroscopy experiment.

        Returns
        -------
        np.ndarray
        """
        # obtain the x-axis coordinate of the extracted data; since the x-coordinates of the
        # sample points are fixed by the first set of the data, we extract the x-coordinates
        # from the first set of the data
        x_coordinates = extracted_data.distinctSortedXValues()
        return x_coordinates

    def _generateXcoordinateListForPrefit(
        self, extracted_data: AllExtractedData
    ) -> np.ndarray:
        """
        Generate a list of x coordinates for the prefit. The x coordinates are
        currently made of (1) a uniformly distributed list of x coordinates in
        between the min and max of the x-coordinates of the extracted data, and
        (2) the x-coordinates of the extracted data.
        """
        # obtain the x-axis coordinate of the extracted data; since the x-coordinates of the
        # sample points are fixed by the first set of the data, we extract the x-coordinates
        # from the first set of the data
        x_coordinates_from_data = extracted_data.distinctSortedXValues()
        # generate a list of x coordinates for the prefit
        try:
            points_add = np.round(float(self.pointsAddCallback())).astype(int)
        except ValueError:
            raise ValueError("Expect an integer for the number of points to add.")

        x_coordinates_uniform = np.linspace(
            min(x_coordinates_from_data), max(x_coordinates_from_data), points_add
        )[1:-1]
        x_coordinates_all = np.concatenate(
            [x_coordinates_from_data, x_coordinates_uniform]
        )

        return np.sort(x_coordinates_all)

    @staticmethod
    def _setCalibrationFunction(
        parameter: ParamBase, calibration_data: CalibrationData
    ) -> None:
        """
        Set the calibration function for a parameter. By now, the calibration function is
        obtained from the calibrateDataset function in the CalibrationData object. Only one
        ng or flux is assumed in the model.

        Parameters
        ----------
        parameter: QuantumModelParameter
            The parameter to be calibrated.
        calibration_func: Callable
            The calibration function.
        """
        # TODO generalize this function to multiple ng and flux case in future
        # notice that the `calibrateDataset` function below takes
        parameter.calibration_func = lambda x: calibration_data.calibrateDataPoint(
            [x, 0], calibration_axis="x"
        )[0]

    def _generateParameterSweep(
        self,
        x_coordinate_list: ndarray,
        sweep_parameter_set: ParamSet,
    ) -> ParameterSweep:
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
        # set paramvals_by_name
        paramvals_by_name = {"x-coordinate": x_coordinate_list}
        # set subsys_update_info
        subsys_update_info = {"x-coordinate": list(sweep_parameter_set.keys())}
        # set update_hilbertspace
        update_hilbertspace = self._update_hilbertspace_for_ParameterSweep(
            sweep_parameter_set
        )

        try:
            evals_count = np.round(float(self.evalCountCallback())).astype(int)
        except ValueError:
            raise ValueError("Expect an integer for the number of energy levels.")
        # TODO: When evals_count is greater than the total dim, raise an error message

        param_sweep = ParameterSweep(
            hilbertspace=self.hilbertspace,
            paramvals_by_name=paramvals_by_name,
            update_hilbertspace=update_hilbertspace,
            evals_count=evals_count,  # change this later to connect to the number from the view
            subsys_update_info=subsys_update_info,
            autorun=False,
            num_cpus=1,  # change this later to connect to the number from the view
        )
        return param_sweep

    def _updateQuantumModelParameter(
        self, parameter: Union[QMSweepParam, QMSliderParam]
    ) -> None:
        """
        Update HilbertSpace object with a parameter.

        Parameters
        ----------
        parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
        """
        parameter.setParameterForParent()
        # TODO: for future, phi grid min/max would need special care here

    def _updateQuantumModelFromParameterSet(
        self, parameter_set: ParamSet
    ) -> None:
        """
        Update HilbertSpace object with a set of parameters in QuantumModelParameterSet.

        Parameters
        ----------
        parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
        """
        for parameters in parameter_set.values():
            for parameter in parameters.values():
                self._updateQuantumModelParameter(parameter)

    def newSweep(
        self,
        slider_or_fit_parameter_set: ParamSet,
        sweep_parameter_set: ParamSet,
        calibration_data: CalibrationData,
        extracted_data: AllExtractedData,
        prefit_result: StatusModel,
    ) -> None:
        """
        Create a new ParameterSweep object.

        Parameters
        ----------
        slider_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are controlled by sliders.
        sweep_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are subject to changes in the parameter sweep.
        calibration_data: CalibrationData
            The CalibrationData object that stores the calibration data.
        extracted_data: AllExtractedData
            The extracted data from the two-tone spectroscopy experiment.
        """
        # set calibration function for the parameters in the sweep parameter set
        # TODO consider moving this part (update calibration function) to somewhere else
        for parameters in sweep_parameter_set.values():
            for parameter in parameters.values():
                self._setCalibrationFunction(parameter, calibration_data)

        # update the HilbertSpace object and generate parameter sweep
        try:
            self._updateQuantumModelFromParameterSet(slider_or_fit_parameter_set)
            self.sweep = self._generateParameterSweep(
                x_coordinate_list=self._generateXcoordinateListForPrefit(
                    extracted_data
                ),
                sweep_parameter_set=sweep_parameter_set,
            )
        except Exception as e:
            prefit_result.status_type = "ERROR"
            if str(e).startswith("min()"):
                prefit_result.statusStrForView = (
                    f"Please extract data before running the prefit."
                )
            else:
                prefit_result.statusStrForView = (
                    f"Fail to initialize the parameter sweep with "
                    f"{type(e).__name__}: {e}."
                )
            return

        prefit_result.status_type = "SUCCESS"
        prefit_result.statusStrForView = f""

    @Slot()
    def sweep2SpecNMSE(
        self,
        slider_or_fit_parameter_set: ParamSet,
        sweep_parameter_set: ParamSet,
        # spectrum_data: CalculatedSpecData,
        calibration_data: CalibrationData,
        extracted_data: AllExtractedData,
        result: StatusModel,
    ):
        """
        It is connected to the signal emitted by the UI when the user clicks the plot button
        for the prefit stage. It make use of the existing sweep object to
        get a spectrum data and MSE.

        It's not allowed to use when the sweep is not generated.
        """
        # run sweep (generate a new sweep if not exist)
        try:
            self.sweep
        except AttributeError:
            self.newSweep(
                slider_or_fit_parameter_set=slider_or_fit_parameter_set,
                sweep_parameter_set=sweep_parameter_set,
                calibration_data=calibration_data,
                extracted_data=extracted_data,
                prefit_result=result,
            )

        result.status_type = "COMPUTING"
        self.sweep.run()

        # generate specdata --------------------------------------------
        # for highlighting
        specdata_for_highlighting = self.sweep.transitions(
            subsystems=self.subsystems_to_plot(),
            initial=self.initial_state(),
            # sidebands=sidebands,
            photon_number=self.photons(),
            make_positive=False,
            as_specdata=True,
        )

        # overall data
        overall_specdata = copy.deepcopy(self.sweep[(slice(None),)].dressed_specdata)
        overall_specdata.energy_table -= specdata_for_highlighting.subtract

        # scale the spectrum data accordingly, based on the calibration
        self._scaleYByInverseCalibration(calibration_data, overall_specdata)
        self._scaleYByInverseCalibration(calibration_data, specdata_for_highlighting)

        # emit the spectrum data to the plot view
        spectrum_element = SpectrumElement(
            "spectrum",
            overall_specdata,
            specdata_for_highlighting,
        )
        self.readyToPlot.emit(spectrum_element)

        # --------------------------------------------------------------

        # mse calculation
        mse, status_type, status_text = self.calculateMSE(extracted_data=extracted_data)

        # pass MSE and status messages to the model
        result.oldMseForComputingDelta = result.newMseForComputingDelta
        result.newMseForComputingDelta = mse
        result.status_type = status_type
        result.statusStrForView = status_text

    @Slot()
    def updateCalculation(
        self,
        slider_or_fit_parameter_set: ParamSet,
        sweep_parameter_set: ParamSet,
        # spectrum_data: CalculatedSpecData,
        calibration_data: CalibrationData,
        extracted_data: AllExtractedData,
        prefit_result: StatusModel,
    ) -> None:
        """
        It is connected to the signal emitted by the UI when the user changes the slider
        of a parameter. It receives a QuantumModelParameterSet object and updates the
        the HilbertSpace object. If auto run is on, it will also compute the spectrum
        and MSE.

        Parameters
        ----------
        slider_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are controlled by sliders.
        sweep_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are subject to changes in the parameter sweep.
        spectrum_data: CalculatedSpecData
            The CalculatedSpecData object that stores the spectrum data.
        calibration_data: CalibrationData
            The CalibrationData object that stores the calibration data.
        extracted_data: AllExtractedData
            The extracted data from the two-tone spectroscopy experiment.
        """
        self.newSweep(
            slider_or_fit_parameter_set=slider_or_fit_parameter_set,
            sweep_parameter_set=sweep_parameter_set,
            calibration_data=calibration_data,
            extracted_data=extracted_data,
            prefit_result=prefit_result,
        )

        # if autorun, perform the rest of the steps (compute spectrum, plot, calculate MSE)
        if self.autorun_callback():
            self.sweep2SpecNMSE(
                slider_or_fit_parameter_set=slider_or_fit_parameter_set,
                sweep_parameter_set=sweep_parameter_set,
                # spectrum_data=spectrum_data,
                extracted_data=extracted_data,
                calibration_data=calibration_data,
                result=prefit_result,
            )

    def _scaleYByInverseCalibration(
        self,
        calibration_data: CalibrationData,
        specdata: SpectrumData,
    ):
        """
        scale the spectrum data accordingly, based on the calibration
        this step is carried out based on the inverse calibration function
        in the calibration data
        """
        for param_idx in range(len(specdata.energy_table)):
            for energy_idx in range(len(specdata.energy_table[param_idx])):
                specdata.energy_table[param_idx][
                    energy_idx
                ] = calibration_data.inverseCalibrateDataPoint(
                    [0, specdata.energy_table[param_idx][energy_idx]],
                    inverse_calibration_axis="y",
                )[
                    1
                ]

    def _update_hilbertspace_for_ParameterSweep(
        self,
        sweptParameterSet: ParamSet,
    ) -> None:
        """
        Update the HilbertSpace object with the values of parameters and coupling coefficients
        received from the UI when the sweep is running. This method returns a callable for
        `update_hilbertspace` that is passed to the ParameterSweep object.
        """

        # update parameters according to the x-coordinate
        # TODO consider adding hilbertspace regeneration here
        def update_hilbertspace(x) -> None:
            for parameters in sweptParameterSet.values():
                for parameter in parameters.values():
                    parameter.value = parameter.calibration_func(x)
                    parameter.setParameterForParent()

        return update_hilbertspace

    def calculateMSE(
        self, extracted_data: AllExtractedData
    ) -> Tuple[Union[float, None], str, str]:
        """
        Calculate the mean square error between the extracted data and the simulated data
        from the parameter sweep. Currently, the MSE is calculated from the transition
        spectrum of the self.sweep attribute (i.e. the ParameterSweep object is stored in
        the controller). This method is supposed to be called after running the parameter
        sweep.

        Parameters
        ----------
        extracted_data: AllExtractedData
            The extracted data from the two-tone spectroscopy experiment.

        Returns
        -------
        mse: Union[float, None]
            The mean square error between the extracted data and the simulated data from
            the parameter sweep.
        status_type: str
            The status type of the result.
        status_text: str
            The status text of the result.
        """
        # Steps:
        # 1. obtain tags from the extracted data for each data point
        # 2. according to the tags, fetch the corresponding frequency from the transition data
        # 3. if no transition can be found with the tag, find out the closest transition from the
        #    transition calculation
        # 4. calculate the MSE

        mse = 0
        status_type = ""
        status_text = ""
        # dataNames_without_tag = []
        dataNames_with_unidentifiable_tag = []
        # calibrate the data in the following way: keep the x-coordinate unchanged, but calibrate
        # the y-coordinate
        extracted_data_y_calibrated = extracted_data.allDataSorted(
            applyCalibration=True, calibration_axis="y"
        )
        # for all the extracted data, identify any NO_TAG or CROSSING tagged sets
        # for dataName, tag in zip(extracted_data.dataNames, extracted_data.assocTagList):
        #     if tag.tagType is NO_TAG or tag.tagType is CROSSING:
        #         dataNames_without_tag.append(dataName)
        # # if there is any NO_TAG or CROSSING tagged sets, add a warning message and set status type to WARNING
        # if dataNames_without_tag != []:
        #     status_text += (
        #         f"Data sets {dataNames_without_tag} are not tagged."
        #         "Selected transition frequencies are matched to the closest ones in the model, "
        #         "starting from the ground state.\n"
        #     )
        #     status_type = "WARNING"
        # loop over extracted data sets and the corresponding tags
        for dataName, extracted_data_set, tag in zip(
            extracted_data.dataNames,
            extracted_data_y_calibrated,
            extracted_data.assocTagList,
        ):
            for data_point in extracted_data_set:
                # obtain the transition frequency from the transition data
                (
                    transition_freq,
                    get_transition_freq_status,
                ) = self._getTransitionFrequencyFromParamSweep(
                    x_coord=data_point[0],
                    sweep=self.sweep,
                    tag=tag,
                    data_freq=data_point[1],
                )
                # if the transition_freq is None, return directly with a mse of None
                if transition_freq is None:
                    mse = None
                    status_type = "ERROR"
                    status_text = (
                        f"The {tag.tagType} tag {tag.initial}->{tag.final} includes"
                        " state label(s) that exceed evals count."
                    )
                    return mse, status_type, status_text
                # if the return status is not SUCCESS, add a warning message and set status type to WARNING
                if get_transition_freq_status != "SUCCESS":
                    status_type = "WARNING"
                    # append the dataName to the list of dataNames_with_unidentifiable_tag
                    # only if the name is not already in the list
                    if dataName not in dataNames_with_unidentifiable_tag:
                        dataNames_with_unidentifiable_tag.append(dataName)

                if tag.photons is None:
                    photons = 1  # NO_TAG
                else:
                    photons = tag.photons
                transition_freq /= photons

                # add to the MSE
                mse += (data_point[1] - transition_freq) ** 2
        # normalize the MSE
        mse /= sum(
            [
                len(extracted_data_set)
                for extracted_data_set in extracted_data_y_calibrated
            ]
        )
        # add to the status text if there is any unidentifiable tag
        if dataNames_with_unidentifiable_tag != []:
            status_text += (
                f"Data sets {dataNames_with_unidentifiable_tag} have unidentifiable state "
                "labels or are untagged. "
                "Selected transition frequencies are matched to the closest ones in the model, "
                "starting from the ground state.\n"
            )
        if status_type == "":
            status_type = "SUCCESS"
        return mse, status_type, status_text

    def _getTransitionFrequencyFromParamSweep(
        self,
        x_coord: float,
        sweep: ParameterSweep,
        tag: Tag,
        data_freq: Union[float, None] = None,
    ) -> Tuple[
        Union[float, None],
        Literal[
            "SUCCESS",
            "DRESSED_OUT_OF_RANGE",
            "NO_MATCHED_BARE_INITIAL",
            "NO_MATCHED_BARE_FINAL",
            "NO_MATCHED_BARE_INITIAL_AND_FINAL",
        ],
    ]:
        """
        Obtain the cooresponding transition frequency provided by the tag from a ParameterSweep
        instance. If the tag is not provided or can not identify states,
        the closest transition frequency is returned.

        Parameters
        ----------
        x_coord: float
            The x coordinate of the transition plot.
        sweep: ParameterSweep
            The ParameterSweep instance. The sweep must be performed and is swept over the x coordinate.
        """
        # raise error if no tag is provided
        # TODO need to think about what happens if NO_TAG is provided, by now NO_TAG is treated as if we
        # specify CROSSING
        simulation_freq = None
        status = None

        # if provided dressed label
        if (
            tag.tagType
            == "DISPERSIVE_DRESSED"
            # or tag.tagType is CROSSING_DRESSED
        ):
            # if the state is above evals_count, terminate the computation and return error status
            if sweep.dressed_evals_count() < max(tag.initial, tag.final):
                status = "ERROR"
                return simulation_freq, status
            else:
                initial_energy = sweep["evals"]["x-coordinate":x_coord][tag.initial]
                final_energy = sweep["evals"]["x-coordinate":x_coord][tag.final]
                simulation_freq = final_energy - initial_energy
                status = "SUCCESS"
                return simulation_freq, status

        # if provided bare label
        elif tag.tagType == "DISPERSIVE_BARE":
            initial_energy = sweep["x-coordinate":x_coord].energy_by_bare_index(
                tag.initial
            )
            final_energy = sweep["x-coordinate":x_coord].energy_by_bare_index(tag.final)
            # if either initial or final state cannot be identified, change the status and find out
            # the closest transition
            if initial_energy is not np.nan and final_energy is not np.nan:
                simulation_freq = final_energy - initial_energy
                status = "SUCCESS"
                return simulation_freq, status
            elif initial_energy is np.nan and final_energy is not np.nan:
                status = "NO_MATCHED_BARE_INITIAL"
                eigenenergies = sweep["evals"]["x-coordinate":x_coord]
                # find out the position of the final state energy
                final_energy_dressed_label = sweep[
                    "x-coordinate":x_coord
                ].dressed_index(tag.final)
                possible_transitions = np.array(
                    [
                        eigenenergies[final_energy_dressed_label] - eigenenergy
                        for eigenenergy in eigenenergies[:final_energy_dressed_label]
                    ]
                )
                # find the closest transition
                closest_traansition_index = (
                    np.abs(possible_transitions - data_freq)
                ).argmin()
                simulation_freq = possible_transitions[closest_traansition_index]
                return simulation_freq, status

            elif final_energy is np.nan and initial_energy is not np.nan:
                status = "NO_MATCHED_BARE_FINAL"
                eigenenergies = sweep["evals"]["x-coordinate":x_coord]
                # find out the position of the final state energy
                initial_energy_dressed_label = sweep[
                    "x-coordinate":x_coord
                ].dressed_index(tag.initial)
                possible_transitions = np.array(
                    [
                        eigenenergy - eigenenergies[initial_energy_dressed_label]
                        for eigenenergy in eigenenergies[initial_energy_dressed_label:]
                    ]
                )
                # find the closest transition
                closest_traansition_index = (
                    np.abs(possible_transitions - data_freq)
                ).argmin()
                simulation_freq = possible_transitions[closest_traansition_index]
                return simulation_freq, status
            # if both initial and final states cannot be identified, change the status and pass the
            # case to the CROSSING or NO_TAG case
            else:
                status = "NO_MATCHED_BARE_INITIAL_AND_FINAL"

        # if provided no label, or the label is not recognized, or the label is CROSSING
        # calculate all the possible (positive) transitions and find the closest one
        eigenenergies = sweep["evals"]["x-coordinate":x_coord]
        # currently only consider the case where the initial state is the ground state
        # TODO: generalize this to the case where the initial state is not the ground state
        possible_transitions = np.array(
            [eigenenergy - eigenenergies[0] for eigenenergy in eigenenergies[1:]]
        )
        # find the closest transition
        closest_traansition_index = (np.abs(possible_transitions - data_freq)).argmin()
        simulation_freq = possible_transitions[closest_traansition_index]
        return simulation_freq, status

    def MSEByParameters(
        self,
        parameterSet: ParamSet,
        sweep_parameter_set: ParamSet,
        calibration_data: CalibrationData,
        extracted_data: AllExtractedData,
    ):
        """
        For parameter fitting purpose, calculate the MSE with just the
        parameters
        """
        # set calibration functions for the parameters in the sweep parameter set
        for parameters in sweep_parameter_set.values():
            for parameter in parameters.values():
                self._setCalibrationFunction(parameter, calibration_data)
        # update the HilbertSpace object and generate parameter sweep
        # this step is after the setup of calibration functions because the update_hilbertspace in ParameterSweep need the calibration information
        self._updateQuantumModelFromParameterSet(parameterSet)
        # generate parameter sweep
        self.sweep = self._generateParameterSweep(
            x_coordinate_list=self._generateXcoordinateListForMarkedPoints(
                extracted_data
            ),
            sweep_parameter_set=sweep_parameter_set,
        )
        # run sweep
        self.sweep.run()
        return self.calculateMSE(extracted_data)[0]
