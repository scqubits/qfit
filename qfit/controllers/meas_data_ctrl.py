from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING, Tuple, Dict, Any, List

if TYPE_CHECKING:
    from scqubits.core.hilbert_space import HilbertSpace
    from qfit.models.measurement_data import MeasDataSet
    from qfit.models.meas_data_importer import MeasDataImporter
    from qfit.models.extracted_data import AllExtractedData
    from qfit.models.numerical_model import QuantumModel

class MeasDataCtrl(QObject):
    def __init__(
        self, 
        parent: QObject | None,
        models: Tuple[
            "MeasDataImporter", "MeasDataSet"
        ],
    ) -> None:
        super().__init__(parent)
        (
            self.measImporter, self.measDataSet
        ) = models

        self.switchFigConnects()

    # connections ======================================================
    def switchFigConnects(self) -> None:
        # from view to model, depending on which page the user is in,
        # switch the figure in the model
        # if the user is in the importer page:
        #     self.some_view_not_implemented_yet.switchFigSignal.connect(self.measImporter.switchFig)
        # elif the user is in other page:
        #     self.some_view_not_implemented_yet.switchFigSignal.connect(self.measDataSet.switchFig)
        pass