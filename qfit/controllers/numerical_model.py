import numpy as np

from typing import overload

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.param_sweep import ParameterSweep
from scqubits.core.qubit_base import QuantumSystem

from typing import Dict, List, Tuple, Union
from qfit.models.parameter_settings import ParameterType

from qfit.models.quantum_model_parameters import (
    QuantumModelParameter,
    QuantumModelSliderParameter,
    QuantumModelParameterSet,
)
from qfit.models.numerical_spectrum_data import SpectrumData

from qfit.models.parameter_settings import QSYS_PARAM_NAMES, DEFAULT_PARAM_MINMAX


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
        super().__init__()
        self.hilbertspace: HilbertSpace = hilbertspace
        self.parameter_set: QuantumModelParameterSet = self.generateParameterSets(
            self.hilbertspace
        )
        self.sweep = self._generateParameterSweep()

    @overload
    def generateParameterSets(
        hilbertspace: HilbertSpace,
        included_parameter_type: List[ParameterType],
    ) -> QuantumModelParameterSet:
        ...

    @overload
    def generateParameterSets(
        hilbertspace: HilbertSpace,
        excluded_parameter_type: List[ParameterType],
    ) -> QuantumModelParameterSet:
        ...

    @staticmethod
    def generateParameterSets(
        hilbertspace: HilbertSpace,
        included_parameter_type: Union[List[ParameterType], None] = None,
        excluded_parameter_type: Union[List[ParameterType], None] = None,
    ) -> QuantumModelParameterSet:
        """
        Get the names of all parameters (excluding offset charges and external fluxes) in the HilbertSpace object.
        The returned dictionary has subsystem id strings as keys and dictionaries of different types of parameters
        as values. For example, if the HilbertSpace object contains two capacitively coupled transmon qubits,
        the returned QuantumModelParameterSet object will have a parameter object (a dictionary):

        {tmon1: {"EJ": ["EJ"], "EC": ["EC"], "cutoffs": ["ncut"], "truncated_dim": ["truncated_dim"]},
        tmon2: {"EJ": ["EJ"], "EC": ["EC"], "cutoffs": ["ncut"], "truncated_dim": ["truncated_dim"]},
        hilbertspace: {"interaction_strength": ["g1"]}
        }

        Returns
        -------
            A QuantumModelParameterSet object that stores all the parameters in the HilbertSpace object.
        """
        # only one of the included_parameter_type or excluded_parameter_type can be specified
        if included_parameter_type is not None and excluded_parameter_type is not None:
            raise ValueError(
                "Only one of included_parameter_type or excluded_parameter_type can be specified."
            )
        # first, obtain all the parameters in the subsystems of the HilbertSpace object
        parameter_set = QuantumModelParameterSet()
        subsystems = hilbertspace.subsystem_list
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
                    parameter_set.add_parameter(
                        parameter_name,
                        subsystem,
                        DEFAULT_PARAM_MINMAX[parameter_type],
                        parameter_type,
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
            interactions = hilbertspace.interaction_list
            for interaction_term_index in range(len(interactions)):
                parameter_set.add_parameter(
                    f"g{interaction_term_index+1}",
                    hilbertspace,
                    DEFAULT_PARAM_MINMAX["interaction_strength"],
                    "interaction_strength",
                )
            return parameter_set

    @staticmethod
    def _map1D(x: float, coeffs, biases) -> Tuple[QuantumModelParameter, ...]:
        """
        The actual swept parameters (flux, ng, ...) are linearly related to the value of
        the x axis of the transition plot. This funcition serves as a map between the two.
        """
        return

    def setSweptParameter(
        self,
        parameters: Union[str, List[str]],
        parents: Union[QuantumSystem, List[QuantumSystem]],
    ) -> None:
        """
        Some parameter in self.parameter_set should not be controlled by the slider, but
        instead be swept over as the x axis of the transition plot. This function sets the
        """
        pass

    def _generateParameterSweep(self) -> ParameterSweep:
        """
        Generate a ParameterSweep object from the HilbertSpace object.

        Returns
        -------
        ParameterSweep
        """

        # auto run = False !!!!!!!!!!!!

        pass

    def _updateQuantumModelParameter(self, parameter: QuantumModelParameter) -> None:
        """
        Update HilbertSpace object with the value of a parameter received from the UI.

        Parameters
        ----------
        parameter: QuantumModelParameter
        """

        pass

    def _updateQuantumModelBySlider(
        self, parameter_set: QuantumModelParameterSet
    ) -> None:
        """
        Update the HilbertSpace object with the values of parameters and coupling coefficients
        received from the UI.

        Parameters
        ----------
        parameter_set: QuantumModelParameterSet
        """

        pass

    def _update_hilbertspace_for_ParameterSweep(self, x) -> None:
        """
        Update the HilbertSpace object with the values of parameters and coupling coefficients
        received from the UI when the sweep is running. This method is the callable `update_hilbertspace`
        that is passed to the ParameterSweep object.
        """

        # use _map1D to get the values of parameters and coupling coefficients from x

        pass

    def _updateParameterSweepBySlider(self) -> None:
        """
        Update/regenerate the ParameterSweep object with the values of parameters and coupling coefficients
        received from the UI.
        """

        pass

    def _computeSpectrum(self) -> None:
        """
        Compute the transition spectrum from the ParameterSweep object and send data to
        the spectrum model.
        """

        pass
