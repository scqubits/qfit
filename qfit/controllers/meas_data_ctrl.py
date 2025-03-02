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
    from qfit.widgets.menu import MenuWidget


class MeasDataCtrl(QObject):
    def __init__(
        self,
        parent: QObject | None,
        models: Tuple["MeasDataSet"],
        views: Tuple["ImporterView", "PageView", "MeasDataView", "MenuWidget"],
        fullReplaceMeasData: Callable[[List["MeasDataType"]], None],
        fullDynamicalInit: Callable[[], None],
    ) -> None:
        super().__init__(parent)
        (self.measDataSet,) = models
        (self.importerView, self.pageView, self.measDataView, self.menu) = views
        self.fullReplaceMeasData = fullReplaceMeasData
        self.fullDynamicalInit = fullDynamicalInit

        self.switchFigConnects()
        self.importFigConnects()
        self.metaInfoConnects()
        self.configConnects()
        self.transposeConnects()
        self.continueConnects()
        self.dataLoadConnects()
        
    def switchToFig(self, figIdx: int) -> None:
        self.measDataView.switchToFig(figIdx)

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

    @Slot()
    def continueToPostImportStages(self) -> None:
        """
        Continue to the calibration page.
        """
        self.measDataSet.importFinished = True

        self.fullReplaceMeasData(self.measDataSet.fullData)
        self.fullDynamicalInit()
        self.switchToFig(0)

        self.importerView.enableFigImport(False)

        self.pageView.switchToPage("calibrate")
        self.pageView.setEnabled(False, "setup")
        self.pageView.setEnabled(True, "calibrate")
        self.pageView.setEnabled(True, "extract")
        self.pageView.setEnabled(True, "prefit")
        self.pageView.setEnabled(True, "fit")

        self.menu.ui.menuSaveButton.setEnabled(True)
        self.menu.ui.menuSaveAsButton.setEnabled(True)

    def continueConnects(self) -> None:
        """
        Connect the continue button between model and view.
        """
        self.importerView.continueClicked.connect(self.continueToPostImportStages)

    def dataLoadConnects(self) -> None:
        """
        Establish connections for reading .qfit file.
        """
        self.measDataSet.dataLoaded.connect(lambda _: self.continueToPostImportStages())
        self.measDataSet.dataLoaded.connect(self.measDataView.reloadFig)
