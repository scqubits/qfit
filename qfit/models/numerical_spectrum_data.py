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


from typing import Callable, Optional, Union

import numpy as np
from matplotlib.axes import Axes
from scqubits.core.param_sweep import ParameterSweep

import qfit.io_utils.file_io_serializers as serializers

class SpectrumData(serializers.Serializable):
    """
    Class for storing and manipulating the spectrum data calculated from the scqbits
    backends. 
    """
    def __init__(self) -> None:
        self.parameter_sweep: Optional[ParameterSweep] = None
        pass

    def setupUICallbacks(
        self,
    ):
        """
        Plot options from the UI
        """
        pass

    def update(self, parameter_sweep: ParameterSweep) -> None:
        self.parameter_sweep = parameter_sweep

    def canvasPlot(self, axes: Axes, **kwargs):

        xlim = axes.get_xlim()
        ylim = axes.get_ylim()

        # plot random data for now
        x = np.linspace(xlim[0], xlim[1], 100)
        y = np.random.rand(100) * (ylim[1] - ylim[0]) + ylim[0]

        axes.scatter(x, y, **kwargs)




