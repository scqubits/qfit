from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING, Tuple, Dict, Any, List, Callable

if TYPE_CHECKING:
    from qfit.models.measurement_data import MeasDataSet, MeasDataType
    from qfit.views.importer_view import ImporterView
    from qfit.views.paging_view import PageView
    from qfit.views.meas_data_view import MeasDataView


class MeasDataCtrl(QObject):
    def __init__(
        self,
        parent: QObject | None,
        models: Tuple["MeasDataSet"],
        views: Tuple["ImporterView", "PageView", "MeasDataView"],
        fullReplaceMeasData: Callable[[List["MeasDataType"]], None],
        fullDynamicalInit: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        (self.measDataSet,) = models
        (self.importerView, self.pageView, self.measDataView) = views
        self.fullReplaceMeasData = fullReplaceMeasData
        self.fullDynamicalInit = fullDynamicalInit

        self.switchFigConnects()
        self.importFigConnects()
        self.metaInfoConnects()
        self.configConnects()
        self.transposeConnects()
        self.continueConnects()

    # connections ======================================================
    def importFigConnects(self) -> None:
        """
        Import the figure from the importer page.
        """
        self.importerView.addFigClicked.connect(self.measDataSet.insertRow)
        self.measDataSet.newFigAdded.connect(self.measDataView.addFig)
        self.importerView.deleteFigClicked.connect(self.measDataView.deleteFig)
        self.measDataView.figDeletedFromTab.connect(self.measDataSet.removeRow)

    def switchFigConnects(self) -> None:
        """
        Switch the figure
        """
        self.measDataView.figChanged.connect(self.measDataSet.switchFig)

    def metaInfoConnects(self) -> None:
        """
        Show the meta info for the current measurement data.
        """
        self.measDataSet.metaInfoChanged.connect(self.importerView.setMetaInfo)

    def configConnects(self) -> None:
        """
        Connect the configuration panel between model and view.
        """
        self.importerView.configChanged.connect(self.measDataSet.storeRawXYConfig)
        self.measDataSet.rawXYConfigChanged.connect(self.importerView.setConfig)

    def transposeConnects(self) -> None:
        """
        Connect the transpose button between model and view.
        """
        self.importerView.transposeZClicked.connect(self.measDataSet.transposeZ)

    def continueConnects(self) -> None:
        """
        Connect the continue button between model and view.
        """
        self.importerView.continueClicked.connect(
            lambda: self.fullReplaceMeasData(self.measDataSet.fullData)
        )
        self.importerView.continueClicked.connect(self.fullDynamicalInit)
        self.importerView.continueClicked.connect(
            lambda: self.pageView.switchToPage("calibrate")
        )
