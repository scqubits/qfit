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
from scqubits.core.storage import SpectrumData

import qfit.io_utils.file_io_serializers as serializers

class SpectrumData(serializers.Serializable):
    """
    Class for storing and manipulating the spectrum data calculated from the scqbits
    backends. 
    """
    subsystem_names: List[str]
    initial_state_str: str
    final_state_str: str

    def __init__(self) -> None:
        self.overall_specdata: Optional[SpectrumData] = None
        self.highlighted_specdata: Optional[SpectrumData] = None
        self.label_list: Optional[List[str]] = None
        pass

    def setupUICallbacks(
        self,
    ):
        """
        Plot options from the UI
        """
        pass

    def update(
        self, 
        overall_specdata: SpectrumData, 
        highlighted_specdata: SpectrumData,
    ):
        """
        Update the data from the backend
        """
        self.overall_specdata = overall_specdata
        self.highlighted_specdata = highlighted_specdata

    def canvasPlot(self, axes: Axes, **kwargs):

        if self.overall_specdata is None or self.highlighted_specdata is None:
            # no data to plot
            return
        
        fig = axes.get_figure()

        self.highlighted_specdata.plot_evals_vs_paramvals(
            color = "gainsboro", 
            linewidth = 0.75,
            fig_ax = (fig, axes),
        )     

        self.highlighted_specdata.plot_evals_vs_paramvals(
            # label_list = self.highlighted_specdata.labels,
            fig_ax = (fig, axes),
        )     


