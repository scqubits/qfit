import numpy as np

import scqubits as scq

from scqubits.core.hilbert_space import HilbertSpace
from scqubits.core.param_sweep import ParameterSweep

from typing import Dict, List, Tuple, Union

from qfit.models.numerical_spectrum_data import SpectrumData


class NumericalModel():
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
        self.param_names: Dict[str, Dict[str, List[str]]] = self.get_param_names(
            self.hilbertspace
        )

    @staticmethod
    def get_param_names(hilbertspace: HilbertSpace) -> Dict[str, Dict[str, List[str]]]:
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
