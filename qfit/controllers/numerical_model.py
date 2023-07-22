import numpy as np

from numpy import ndarray

from typing import overload
import copy

import scqubits as scq
from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.param_sweep import ParameterSweep
from scqubits.core.qubit_base import QuantumSystem

from typing import Dict, List, Tuple, Union, Callable
from typing_extensions import Literal

from qfit.models.parameter_settings import ParameterType

from qfit.models.quantum_model_parameters import (
    QuantumModelParameter,
    QuantumModelSliderParameter,
    QuantumModelParameterSet,
)
from qfit.models.numerical_spectrum_data import SpectrumData
from qfit.models.calibration_data import CalibrationData
from qfit.models.extracted_data import AllExtractedData

from qfit.models.parameter_settings import QSYS_PARAM_NAMES, DEFAULT_PARAM_MINMAX


# for test only
# ------------------------------------------------------------------------------
def test_hilbert_space():
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


def test_param_sweep(hilbertspace, bias=0.0, scale=1.0) -> ParameterSweep:
    # bias serves as a calibration parameter
    def update_hilbertspace(x):
        hilbertspace["fluxonium"].flux = x * scale + bias

    sweep = ParameterSweep(
        hilbertspace=hilbertspace,
        paramvals_by_name={"x": np.linspace(-bias / scale, (1 - bias) / scale, 21)},
        update_hilbertspace=update_hilbertspace,
    )
    return sweep


# ------------------------------------------------------------------------------


class QuantumModel:
    """
    Class for handling the HilbertSpace object, including: (1) identifying parameters in each subsystem of the Hamiltonian
    and coupling coefficients of the interaction terms, (2) receiving updated values of parameters and coupling coefficients
    from the UI and reflect changes in the HilbertSpace object, (3) generating a ParameterSweep object, (4) compute the relevant
    transition spectrum.

    Parameters
    ----------
    hilbertspace: HilbertSpace
    """

    def __init__(
        self,
        hilbertspace: HilbertSpace,
    ):
        self.hilbertspace: HilbertSpace = hilbertspace

    def setupPlotUICallbacks(self):
        """
        Obtain information from plot option UI including:
        * plot options
        * ...
        """

        # for test only
        # ------------------------------------------------------------------------------
        self.subsystem_names_to_plot = lambda *args: "fluxonium"
        self.initial_state_str = lambda *args: "0,0"
        self.final_state_str = lambda *args: ""

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

        elif isinstance(subsys_names, list):
            return [self.hilbertspace.subsys_by_id_str(name) for name in subsys_names]

        else:
            raise TypeError(
                f"subsystem_names_to_plot() should give a string or a list of strings, not {type(subsys_names)}."
            )

    @staticmethod
    def _state_str_2_label(state_str: str):
        # convert string to state label

        # empty string means None
        if state_str == "":
            return None

        # comma separated string means tuple
        if "," in state_str:
            label_str = state_str.split(",")
            return tuple(int(x) for x in label_str if x != "")  # delete '' in the tuple

        # otherwise, try to interpret it as an integer
        try:
            return int(state_str)
        except ValueError:
            return None

    def initial_state(self):
        return self._state_str_2_label(self.initial_state_str())

    def final_state(self):
        return self._state_str_2_label(self.final_state_str())

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

    def addParametersToParameterSet(
        self,
        parameter_set: QuantumModelParameterSet,
        parameter_usage: Literal["slider", "sweep", "fit"],
        included_parameter_type: Union[List[ParameterType], None] = None,
        excluded_parameter_type: Union[List[ParameterType], None] = None,
    ) -> None:
        """
        Add parameters to a QuantumModelParameterSet object for the HilbertSpace object
        for parameters that are supposed to be adjusted by using sliders or by using parameter sweeps.
        User may optionally specify parameter types that are excluded/included.

        Parameters:
        -----------
        parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object.
        parameter_type: Literal["slider", "sweep", "fit"]
            The type of the parameter.
        included_parameter_type: List[ParameterType]
            A list of parameter types that are included in the returned parameter set.
        excluded_parameter_type: List[ParameterType]
            A list of parameter types that are excluded in the returned parameter set.
        """
        # only one of the included_parameter_type or excluded_parameter_type can be specified
        if included_parameter_type is not None and excluded_parameter_type is not None:
            raise ValueError(
                "Only one of included_parameter_type or excluded_parameter_type can be specified."
            )
        # first, obtain all the parameters in the subsystems of the HilbertSpace object
        subsystems = self.hilbertspace.subsystem_list
        for subsystem in subsystems:
            # obtain the parameter names in the subsystem
            # first identify the type of the subsystem
            subsystem_type = subsystem.__class__
            # then get the parameters in the subsystem
            parameters = QSYS_PARAM_NAMES[subsystem_type]
            # add the parameter names to the parameter set
            # parameters is a dictionary with parameter types as keys and lists of parameter names as values
            for parameter_type, parameter_names in parameters.items():
                # check if the parameter type is included or excluded
                if (
                    (included_parameter_type is not None)
                    and (parameter_type not in included_parameter_type)
                ) or (
                    (excluded_parameter_type is not None)
                    and (parameter_type in excluded_parameter_type)
                ):
                    continue
                for parameter_name in parameter_names:
                    if parameter_usage == "slider":
                        parameter_set.addParameter(
                            name=parameter_name,
                            parent_system=subsystem,
                            param_type=parameter_type,
                            **DEFAULT_PARAM_MINMAX[parameter_type],
                        )
                    elif (parameter_usage == "sweep") or (parameter_usage == "fit"):
                        parameter_set.addParameter(
                            name=parameter_name,
                            parent_system=subsystem,
                            param_type=parameter_type,
                            value=0,  # TODO: change this value later
                        )
        # then add interaction strengths to the parameter set
        if (
            (included_parameter_type is not None)
            and ("interaction_strength" not in included_parameter_type)
        ) or (
            (excluded_parameter_type is not None)
            and ("interaction_strength" in excluded_parameter_type)
        ):
            pass
        else:
            interactions = self.hilbertspace.interaction_list
            for interaction_term_index in range(len(interactions)):
                if parameter_usage == "slider":
                    parameter_set.addParameter(
                        name=f"g{interaction_term_index+1}",
                        parent_system=self.hilbertspace,
                        param_type="interaction_strength",
                        **DEFAULT_PARAM_MINMAX["interaction_strength"],
                    )
                elif (parameter_usage == "sweep") or (parameter_usage == "fit"):
                    parameter_set.addParameter(
                        name=f"g{interaction_term_index+1}",
                        parent_system=self.hilbertspace,
                        param_type="interaction_strength",
                        value=0,
                    )

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
        x_coordinates = extracted_data.allDataSorted(applyCalibration=False)[0][:, 0]
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
        x_coordinates_from_data = extracted_data.allDataSorted(applyCalibration=False)[
            0
        ][:, 0]
        # generate a list of x coordinates for the prefit
        x_coordinates_uniform = np.linspace(
            min(x_coordinates_from_data), max(x_coordinates_from_data), 20
        )[1:-1]
        x_coordinates_all = np.concatenate(
            [x_coordinates_from_data, x_coordinates_uniform]
        )

        return np.sort(x_coordinates_all)

    @staticmethod
    def _setCalibrationFunction(
        parameter: QuantumModelParameter, calibration_data: CalibrationData
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
            [x, 0]
        )[0]

    def _generateParameterSweep(
        self,
        x_coordinate_list: ndarray,
        sweep_parameter_set: QuantumModelParameterSet,
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
        param_sweep = ParameterSweep(
            hilbertspace=self.hilbertspace,
            paramvals_by_name=paramvals_by_name,
            update_hilbertspace=update_hilbertspace,
            evals_count=20,  # change this later to connect to the number from the view
            subsys_update_info=subsys_update_info,
            autorun=False,  # TODO set to false by default later
            num_cpus=1,  # change this later to connect to the number from the view
        )
        return param_sweep

    def _updateQuantumModelParameter(
        self, parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
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
        self, parameter_set: QuantumModelParameterSet
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

    def onSliderParameterChange(
        self,
        slider_parameter_set: QuantumModelParameterSet,
        sweep_parameter_set: QuantumModelParameterSet,
        spectrum_data: SpectrumData,
        calibration_data: CalibrationData,
        extracted_data: AllExtractedData,
    ) -> None:
        """
        It is connected to the signal emitted by the UI when the user changes the slider
        of a parameter. It receives a QuantumModelParameterSet object and updates the
        the HilbertSpace object. If auto run is on, it will also compute the spectrum.

        Parameters
        ----------
        slider_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are controlled by sliders.
        sweep_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are subject to changes in the parameter sweep.
        spectrum_data: SpectrumData
            The SpectrumData object that stores the spectrum data.
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
        self.onParameterChange(
            update_parameter_set=slider_parameter_set,
            sweep_parameter_set=sweep_parameter_set,
            x_coordinate_list=self._generateXcoordinateListForPrefit(extracted_data),
        )

        # if autorun, perform the rest of the steps (compute spectrum, plot, calculate MSE)
        if self.autorun_callback():
            self.onButtonRunClicked(spectrum_data)

    def onParameterChange(
        self,
        update_parameter_set: QuantumModelParameterSet,
        sweep_parameter_set: QuantumModelParameterSet,
        x_coordinate_list: ndarray,
    ) -> None:
        """
        Perform parameter change from a parameter set and generate `self.sweep` attribute.

        Parameters
        ----------
        update_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are updated (but not swept).
        sweep_parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object,
            which are subject to changes in the parameter sweep. Parameters in this set must have
            the updated calibration_func attribute.
        x_coordinate_list: ndarray
            The x coordinates of the sweep.
        """
        # update the HilbertSpace object with the slider parameter
        self._updateQuantumModelFromParameterSet(update_parameter_set)
        # generate parameter sweep
        self.sweep = self._generateParameterSweep(
            x_coordinate_list=x_coordinate_list, sweep_parameter_set=sweep_parameter_set
        )

    def onButtonRunClicked(self, spectrum_data: SpectrumData):
        """
        It is connected to the signal emitted by the UI when the user clicks the run button
        for the prefit stage. It runs the parameter sweep and then generate the plots.
        """
        self.sweep.run()

        try:
            subsys = self.subsystems_to_plot()
        except ValueError:
            return

        specdata_for_highlighting = self.sweep.transitions(
            subsystems=subsys,
            initial=self.initial_state(),
            final=self.final_state(),
            # sidebands=sidebands,
            # photon_number=photon_number,
            make_positive=True,
            as_specdata=True,
        )

        # TODO: scale with calibration data

        # substract the ground state energy
        overall_specdata = copy.deepcopy(self.sweep[(slice(None),)].dressed_specdata)
        overall_specdata.energy_table -= specdata_for_highlighting.subtract

        spectrum_data.update(
            overall_specdata,
            specdata_for_highlighting,
        )
        # ------------------------------------------------------------------------------

        # mse calculation

        # update spectrum_data
        # do not need call spectrum_data.canvasPlot(). It is done in the mainwindow with
        # another connection
        # print(self._generateXcoordinateList(extracted_data=extracted_data))

    def _update_hilbertspace_for_ParameterSweep(
        self,
        sweptParameterSet: QuantumModelParameterSet,
    ) -> None:
        """
        Update the HilbertSpace object with the values of parameters and coupling coefficients
        received from the UI when the sweep is running. This method returns a callable for
        `update_hilbertspace` that is passed to the ParameterSweep object.
        """

        # update parameters according to the x-coordinate
        def update_hilbertspace(x) -> None:
            for parameters in sweptParameterSet.values():
                for parameter in parameters.values():
                    parameter.value = parameter.calibration_func(x)
                    parameter.setParameterForParent()

        return update_hilbertspace

    def _computeSpectrum(self) -> None:
        """
        Compute the transition spectrum from the ParameterSweep object and send data to
        the spectrum model.
        """

        pass

    def calculateMSE(self, extracted_data: AllExtractedData) -> float:
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
        float
            The mean square error.
        """
        # Steps:
        # 1. obtain tags from the extracted data for each data point
        # 2. according to the tags, fetch the corresponding frequency from the transition data
        # 3. if no transition can be found with the tag, find out the closest transition from the
        #    transition calculation
        # 4. calculate the MSE
        pass
