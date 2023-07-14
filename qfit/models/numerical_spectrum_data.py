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

import qfit.io_utils.file_io_serializers as serializers

class SpectrumData(serializers.Serializable):
    """
    Class for storing and manipulating the spectrum data calculated from the scqbits
    backends. 
    """
    def __init__(self, transitions, labels) -> None:
        pass

    def canvasPlot(self, axes: Axes, **kwargs):
        pass

    

