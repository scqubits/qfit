import sys
import os
import numpy as np
import copy

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
)

from scqubits.core.hilbert_space import HilbertSpace

from qfit.models.registry import Registry
from qfit.widgets.settings import VisualSettingsWidget, FitSettingsWidget, NumericalSpectrumSettingsWidget
from qfit.utils.helpers import StopExecution
from qfit.io_utils.measurement_file_readers import readMeasurementFile

# This import is necessary for the registry (in method openProjectWithRegistryDict)
from qfit.models.measurement_data import (
    ImageMeasurementData,
    NumericalMeasurementData,
)

from typing import TYPE_CHECKING, Union, Dict, Any, Optional, List

if TYPE_CHECKING:
    from qfit.core.mainwindow import MainWindow
    from qfit.models.measurement_data import (
        MeasurementDataType,
    )

class SettingsCtrl:
    """ 
    This controller handles the settings widget. Specifically its connections and 
    logics for the settings widget.
    """
    def __init__(self, settingsWidget: SettingsWidget, settingsButton: Dict[str, ] ):
        pass