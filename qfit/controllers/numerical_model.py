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

    def setupUICallbacks(self):
        """
        Obtain information from UI including:
        * plot options
        * ...
        """

        # for test only
        # ------------------------------------------------------------------------------
        self.plot_subsystem_names = lambda *args: ["fluxonium"]
        self.initial_state_str = lambda *args: "0"
        self.final_state_str = lambda *args: ""
        # ------------------------------------------------------------------------------

        pass

    def subsystems(self):
        return [
            self.hilbertspace.subsys_by_id_str(name)
            for name in self.plot_subsystem_names()
        ]

    @staticmethod
    def _state_str_2_label(state_str: str):
        # convert string to state label

        # empty string means None
        if state_str == "":
            return None

        # comma separated string means tuple
        if "," in state_str:
            return tuple(int(x) for x in state_str.split(","))

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
        parameter_type: Literal["slider", "sweep"],
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
        parameter_type: Literal["slider", "sweep"]
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
                    if parameter_type == "slider":
                        parameter_set.addParameter(
                            name=parameter_name,
                            parent_system=subsystem,
                            param_type=parameter_type,
                            **DEFAULT_PARAM_MINMAX[parameter_type],
                        )
                    elif parameter_type == "sweep":
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
            return parameter_set
        else:
            interactions = self.hilbertspace.interaction_list
            for interaction_term_index in range(len(interactions)):
                if parameter_type == "slider":
                    parameter_set.addParameter(
                        name=f"g{interaction_term_index+1}",
                        parent_system=self.hilbertspace,
                        param_type="interaction_strength",
                        **DEFAULT_PARAM_MINMAX["interaction_strength"],
                    )
                elif parameter_type == "sweep":
                    parameter_set.addParameter(
                        name=f"g{interaction_term_index+1}",
                        parent_system=self.hilbertspace,
                        param_type="interaction_strength",
                        value=0,
                    )
            return parameter_set

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
        )[1:-1].tolist()
        x_coordinates_all = x_coordinates_from_data + x_coordinates_uniform
        x_coordinates_all.sort()
        return np.array(x_coordinates_all)

    @classmethod
    def setCalibrationFunction(
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
        parameter.calibration_func = calibration_data.calibrateDataset

    def generateParameterSweep(
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
        update_hilbertspace = self._update_hilbertspace_for_ParameterSweep()
        param_sweep = ParameterSweep(
            hilbertspace=self.hilbertspace,
            paramvals_by_name=paramvals_by_name,
            update_hilbertspace=update_hilbertspace,
            evals_count=20,  # change this later to connect to the number from the view
            subsys_update_info=subsys_update_info,
            autorun=False,
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
        # update the HilbertSpace object with the slider parameter
        self._updateQuantumModelFromParameterSet(slider_parameter_set)

        # set calibration function for the parameters in the sweep parameter set
        for parameters in sweep_parameter_set.values():
            for parameter in parameters.values():
                self.setCalibrationFunction(parameter, calibration_data)

        # generate parameter sweep
        self.sweep = self.generateParameterSweep(
            self._generateXcoordinateListForPrefit(extracted_data), sweep_parameter_set
        )

        # # for test only
        # # ------------------------------------------------------------------------------
        # self.sweep = test_param_sweep(self.hilbertspace, bias=0.0, scale=0.01)

        specdata_for_highlighting = self.sweep.transitions(
            subsystems=self.plot_subsystem_names(),
            initial=self.initial_state(),
            final=self.final_state(),
            # sidebands=sidebands,
            # photon_number=photon_number,
            make_positive=True,
            as_specdata=True,
        )

        spectrum_data.update(
            copy.deepcopy(self.sweep.dressed_specdata),
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
        x: float,
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
