from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING, Tuple, Dict, Any

if TYPE_CHECKING:
    from qfit.views.status_bar import StatusBarView
    from qfit.models.calibration import CaliParamModel
    from qfit.models.measurement_data import MeasDataSet
    from qfit.models.status import StatusModel
    from qfit.models.numerical_model import QuantumModel
    from qfit.models.fit import FitModel, FitHSParams, FitCaliParams


class StatusCtrl(QObject):
    """
    Controller for the status bar. This controller serves as a transmittor between the status bar
    (view) and models that may produce signals that inform user about state of the app (such as
    completion of calculation, MSE report, etc.). The status bar will be updated accordingly.

    Relevant UI elements:
    - status bar

    Relevant model:
    - quantum model
    - fit param model
    - status model

    Parameters
    ----------
    parent : QObject
        The parent object
    models : Tuple[QuantumModel, FitModel, FitHSParams, FitCaliParams]
        The relevant models
    statusModel : StatusModel
        The status model
    statusBarView : StatusBarView
        The status bar view
    """
    def __init__(
        self,
        parent: QObject,
        models: Tuple[
            "CaliParamModel", 
            "QuantumModel", 
            "FitModel", "FitHSParams", "FitCaliParams",
            "MeasDataSet"
        ],
        statusModel: "StatusModel",
        statusBarView: "StatusBarView",
    ):
        super().__init__(parent)

        self.statusModel = statusModel
        self.models = models
        self.statusBarView = statusBarView
        # (
        #     self.quantumModel, self.fitModel, 
        #     self.fitParamModel, self.fitCaliModel
        # ) = models

        self._messageUpdatedConnects()

    # Connections ======================================================
    def _messageUpdatedConnects(self):
        """
        Connect the signals for updating messages in the status bar.
        """
        # status model (signal) --> status bar view (slot)
        self.statusModel.normalStatusChanged.connect(
            self.statusBarView.updateNormalMessage
        )
        # quantum model (signal) --> status model (slot)
        for model in self.models:
            model.updateStatus.connect(self.statusModel.updateNormalStatus)