import numpy as np

from typing import overload

import scqubits as scq
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


def test_hilert_space():
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

    def generateSliderParameterSets(
        self,
        parameter_set: QuantumModelParameterSet,
        included_parameter_type: Union[List[ParameterType], None] = None,
        excluded_parameter_type: Union[List[ParameterType], None] = None,
    ) -> None:
        """
        Get the names of parameters in the HilbertSpace object. User may optionally specify
        parameter types that are excluded/included. The returned dictionary has subsystem
        id strings as keys and dictionaries of different types of parameters as values. 
        For example, if the HilbertSpace object contains two capacitively coupled transmon 
        qubits, the parameter_set (a QuantumModelParameterSet object) will have a parameter object 
        (a dictionary):

        {tmon1: {"EJ": ["EJ"], "EC": ["EC"], "cutoffs": ["ncut"], "truncated_dim": ["truncated_dim"]},
        tmon2: {"EJ": ["EJ"], "EC": ["EC"], "cutoffs": ["ncut"], "truncated_dim": ["truncated_dim"]},
        hilbertspace: {"interaction_strength": ["g1"]}
        }

        Parameters:
        -----------
        parameter_set: QuantumModelParameterSet
            A QuantumModelParameterSet object that stores the parameters in the HilbertSpace object.
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
                    parameter_set.add_parameter(
                        name = parameter_name,
                        parent_system = subsystem,
                        param_type = parameter_type,
                        **DEFAULT_PARAM_MINMAX[parameter_type]
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
                parameter_set.add_parameter(
                    name = f"g{interaction_term_index+1}",
                    parent_system = self.hilbertspace,
                    param_type = "interaction_strength",
                    **DEFAULT_PARAM_MINMAX["interaction_strength"]
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

    def _updateQuantumModelParameter(
        self, parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
    ) -> None:
        """
        Update HilbertSpace object with a parameter.

        Parameters
        ----------
        parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
        """
        if parameter.parent.__class__ == HilbertSpace:
            # the parameter in this case is always an interaction strength
            # add the if condition here in case if we want to adjust other parameters in the future
            if parameter.param_type == "interaction_strength":
                interaction_index = int(parameter.name[1:]) - 1
                interaction = parameter.parent.interaction_list[interaction_index]
                interaction.g_strength = parameter.value
        # otherwise, the parameters are class parameters of the subsystems
        else:
            setattr(parameter.parent, parameter.name, parameter.value)
            # TODO: for future, phi grid min/max would need special care here

    def _updateQuantumModelParameterSet(
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

    def onParameterChange(
        self, 
        parameter_set: QuantumModelParameterSet,
        spectrum_data: SpectrumData,
    ) -> None:
        """
        It is connected to the signal emitted by the UI when the user changes the slider
        of a parameter. It receives a QuantumModelParameterSet object and updates the
        the HilbertSpace object. If auto run is on, it will also compute the spectrum.

        Parameters
        ----------
        parameter: Union[QuantumModelParameter, QuantumModelSliderParameter]
        """
        self._updateQuantumModelParameterSet(parameter_set)
        # self._computeSpectrum()

        # mse calculation

        # update spectrum_data
        # do not need call spectrum_data.canvasPlot(). It is done in the mainwindow with 
        # another connection

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
