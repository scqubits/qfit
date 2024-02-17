from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QPushButton

from typing import TYPE_CHECKING, Tuple, Dict, Any

if TYPE_CHECKING:
    from qfit.models.quantum_model_parameters import CaliParamModel
    from qfit.views.calibration import CalibrationView


class CalibrationCtrl(QObject):
    def __init__(
        self,
        caliParamModel: CaliParamModel,
        calibrationView: CalibrationView,
        pageButtons: Dict[str, QPushButton],
        *args,
        **kwargs,
    ):
        """
        Controller for calibration. This controller serves as a transmittor between the calibration
        data (model) and the calibration panel (view). User interact with the calibration panel
        (edit values in line edits, calibration extraction status changed, etc.) will trigger the
        model to update. Changes in the model (e.g. a calibration point is extracted from the figure)
        will be reflected in the calibration panel.

        Notice that the connections that transport selected calibration points from the canvas to the
        calibration panel are done in the plotting controller instead of here:
        View -(Model)-> Model: plotting view -(measurement dataset)-> calibration model
        Model --> View: calibration parameter model --> plotting view

        Relevant UI elements:
        - calibration view (a table of raw vector components, mapped vector components, and source of
        the point pair, and associated buttons for calibration extraction)
        - page buttons (buttons for switching between different pages of the main window)

        Relevant model:
        - calibration model
        """
        super().__init__(*args, **kwargs)

        self.caliParamModel = caliParamModel
        self.calibrationView = calibrationView
        self.pageButtons = pageButtons
        self.uiCalibrationConnects()

    def uiCalibrationConnects(self):
        """
        Connect UI elements for data calibration.
        """
        # user interact with calibration panel, updating calibration status stored
        # in the model
        # calibration view --> calibration parameter model
        self.calibrationView.caliStatusChangedByButtonClicked.connect(
            self.caliParamModel.updateStatusFromCaliView
        )

        # when menu switches to other pages, inform calibration model to turn off
        # the calibration
        # menu button clicks --> calibration parameter model
        for pageStr in ["extract", "fit", "prefit"]:
            self.pageButtons[pageStr].clicked.connect(self.caliParamModel.interruptCali)

        # text edit for table entries --> calibration parameter model
        # emit dataEditingFinished signal when editing is finished
        self.calibrationView.setupEditingFinishedSignalEmit()
        self.calibrationView.dataEditingFinished.connect(
            self.caliParamModel.storeParamAttr
        )

        # calibration model --> calibration view (updatebox signal)
        self.caliParamModel.updateBox.connect(self.calibrationView.setBoxValue)

        # calibration model informs the calibration view to turn off the calibration
        # button and update the value in the view
        # calibration parameter model --> calibration view
        self.caliParamModel.plotCaliPtExtractFinished.connect(
            self.calibrationView.postCaliPointSelectedOnCanvas
        )
        self.caliParamModel.plotCaliPtExtractInterrupted.connect(
            self.calibrationView.uncheckAllCaliButtons
        )

        # self.ui.swapXYButton.clicked.connect(self.swapXY)

        # self.calibrationData.caliClicked.connect(self.postCaliPointSelectedOnCanvas)
