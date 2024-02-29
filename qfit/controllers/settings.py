import sys
import os
import numpy as np
import copy

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QPushButton,
)

from scqubits.core.hilbert_space import HilbertSpace

from qfit.models.registry import Registry
from qfit.widgets.settings import SettingsWidgetSet
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

    def __init__(
        self,
        settingsWidgetSet: SettingsWidgetSet,
        settingsButtonSet: Dict[str, QPushButton],
    ):
        self.settingsWidgetSet = settingsWidgetSet
        self.settingsButtonSet = settingsButtonSet
        self.uiSettingsConnects()

    def uiSettingsConnects(self):
        # toggle on the settings widgets
        self.settingsButtonSet["visual"].clicked.connect(
            self.settingsWidgetSet.visual.toggle
        )
        self.settingsButtonSet["fit"].clicked.connect(self.settingsWidgetSet.fit.toggle)
        self.settingsButtonSet["numericalSpectrum"].clicked.connect(
            self.settingsWidgetSet.numericalSpectrum.toggle
        )
        # close buttons
        self.settingsWidgetSet.visual.ui.visualSettingsCloseButton.clicked.connect(
            self.settingsWidgetSet.visual.hide
        )
        self.settingsWidgetSet.fit.ui.fitSettingsCloseButton.clicked.connect(
            self.settingsWidgetSet.fit.hide
        )
        self.settingsWidgetSet.numericalSpectrum.ui.numSpecSettingsCloseButton.clicked.connect(
            self.settingsWidgetSet.numericalSpectrum.hide
        )
