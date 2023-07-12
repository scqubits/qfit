# quantum_system_model.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from typing import List, Optional, Tuple, Union, Dict

import numpy as np

import qfit.io_utils.file_io_serializers as serializers

from scqubits import HilbertSpace, ParameterSweep


class QuantumSystemModel(serializers.Serializable):
    def __init__(
        self,
        hilbertspace: HilbertSpace,
    ):
        """
        Class for handling the HilbertSpace object, including: (1) identifying parameters in each subsystem of the Hamiltonian
        and coupling coefficients of the interaction terms, (2) receiving updated values of parameters and coupling coefficients
        from the UI and reflect changes in the HilbertSpace object, (3) generating a ParameterSweep object, (4) compute the relevant
        transition spectrum.

        Parameters
        ----------
        hilbertspace: HilbertSpace
        """
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
