import numpy as np

import scqubits as scq

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.param_sweep import ParameterSweep
from scqubits.core.qubit_base import QuantumSystem

from typing import Dict, List, Tuple, Union

from qfit.models.quantum_model_parameters import (
    QuantumModelParameter,
    QuantumModelParameterSet,
)
from qfit.models.numerical_spectrum_data import SpectrumData


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
        self.parameter_set: QuantumModelParameterSet = self.getParamNames(
            self.hilbertspace
        )
        self.sweep = self._generateParameterSweep()

    @staticmethod
    def getParamNames(hilbertspace: HilbertSpace) -> QuantumModelParameterSet:
        """
        Get the names of all parameters (excluding offset charges and external fluxes) in the HilbertSpace object.
        The returned dictionary has subsystem id strings as keys and dictionaries of different types of parameters
        as values. For example, if the HilbertSpace object contains two capacitively coupled transmon qubits,
        the returned dictionary will look like:

        {"tmon1": {"circuit elements": ["EJ", "EC"], "cutoffs": ["ncut"], "truncated dimensions": ["truncated_dim"]},
        "tmon2": {"circuit elements": ["EJ", "EC"], "cutoffs": ["ncut"], "truncated dimensions": ["truncated_dim"]},
        "coupling": {"coupling coefficients": ["g1"]}
        }

        Returns
        -------
            Names of parameters in the HilbertSpace object
        """

        return

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
        parameter: QuantumSystemParameter
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
        parameter_set: QuantumSystemParameterSet
        """

        pass

    def _generate_update_hilbertspace(self, x) -> None:
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
