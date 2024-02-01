from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING, Tuple, Dict, Any

if TYPE_CHECKING:
    from qfit.ui_designer.ui_window import Ui_MainWindow
    from qfit.core.mainwindow import MainWindow
    from qfit.models.extracted_data import AllExtractedData, ActiveExtractedData
    from qfit.views.status_bar import StatusBarView
    from qfit.models.status import StatusModel


class StatusCtrl(QObject):
    def __init__(
        self,
        models: Tuple["AllExtractedData", "ActiveExtractedData"],
        statusModel: "StatusModel",
        statusBarView: "StatusBarView",
        *args,
        **kwargs,
    ):
        """
        Controller for the status bar. This controller serves as a transmittor between the status bar
        (view) and models that may produce signals that inform user about state of the app (such as
        completion of calculation, MSE report, etc.). The status bar will be updated accordingly.

        Relevant UI elements:
        - status bar

        Relevant model:
        - fit
        - prefit
        - status model

        Parameters
        ----------
        statusBarView: StatusBarView
        """
        super().__init__(*args, **kwargs)

        self.statusModel = statusModel
        self.statusBarView = statusBarView
        self.models = models

        self._messageUpdatedConnects()

    # Connections ======================================================
    def _messageUpdatedConnects(self):
        """
        Connect the signals for updating messages in the status bar.
        """
        self.statusModel.normalStatusChanged.connect(
            self.statusBarView.updateNormalMessage
        )
        # self.statusModel.tempStatusChanged.connect(self.statusBarView.updateTempMessage)
