# extracted_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from typing import Callable, Optional, Union, Tuple, List

import numpy as np
from matplotlib.axes import Axes
from scqubits.core.param_sweep import ParameterSweep

import qfit.io_utils.file_io_serializers as serializers

# for test only
# ------------------------------------------------------------------------------
import scqubits as scq
def test_param_sweep(hilbertspace, xlim: Tuple[float, float], bias = 0.0) -> ParameterSweep:

    # bias serves as a calibration parameter
    def update_hilbertspace(x):
        hilbertspace["fluxonium"].flux = (x - xlim[0]) / (xlim[1] - xlim[0]) + bias

    sweep = ParameterSweep(
        hilbertspace = hilbertspace,
        paramvals_by_name = {"x": np.linspace(*xlim, 20)},
        update_hilbertspace = update_hilbertspace,
    )
    return sweep
# ------------------------------------------------------------------------------

class SpectrumData(serializers.Serializable):
    """
    Class for storing and manipulating the spectrum data calculated from the scqbits
    backends. 
    """
    subsystem_names: List[str]
    initial_state_str: str
    final_state_str: str

    def __init__(self) -> None:
        self.parameter_sweep: Optional[ParameterSweep] = None
        pass

    def setupUICallbacks(
        self,
    ):
        """
        Plot options from the UI
        """
        
        # for test only
        # ------------------------------------------------------------------------------
        self.subsystem_names = ["fluxonium"]
        self.initial_state_str = "0"
        self.final_state_str = ""
        # ------------------------------------------------------------------------------

        pass

    def update(self, parameter_sweep: ParameterSweep) -> None:
        self.parameter_sweep = parameter_sweep

    # for test only
    # ------------------------------------------------------------------------------
    def test_update(self, hilbertspace, ):
        self.hilbertspace = hilbertspace
    # ------------------------------------------------------------------------------

    def subsystems(self):
        return [self.parameter_sweep.subsys_by_id_str(name) for name in self.subsystem_names]
    
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
        return self._state_str_2_label(self.initial_state_str)
    
    def final_state(self):
        return self._state_str_2_label(self.final_state_str)

    def canvasPlot(self, axes: Axes, **kwargs):

        # for test only
        # ------------------------------------------------------------------------------
        try:
            self.parameter_sweep = test_param_sweep(
                self.hilbertspace, 
                axes.get_xlim(),
                bias = 0.5
            )
        except AttributeError:
            return 
        # ------------------------------------------------------------------------------

        # the actual function begins here
        # ##############################################################################
        try: 
            self.parameter_sweep
        except AttributeError:
            # no data to plot
            return
        
        fig = axes.get_figure()

        # there is a scaling issue. Should make use of the calibration data
        # self.parameter_sweep.plot_transitions(
        #     subsystems = self.subsystems(),
        #     initial = self.initial_state(),
        #     final = self.final_state(),
        #     fig_ax = (fig, axes),
        # )

        # just a naive scaling:
        plot_x = self.parameter_sweep.parameters.paramvals_by_name["x"]
        plot_y = self.parameter_sweep["evals"]
        plot_y = plot_y - plot_y[:, 0:1]
        axes.plot(
            plot_x, plot_y, **kwargs            
        )






