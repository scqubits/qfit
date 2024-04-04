from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING, Tuple, Dict, Any, List

if TYPE_CHECKING:
    from scqubits.core.hilbert_space import HilbertSpace
    from qfit.models.extracted_data import AllExtractedData, ActiveExtractedData
    from qfit.models.measurement_data import MeasDataType, MeasDataSet
    from qfit.views.labeling_view import LabelingView


class ExtractingCtrl(QObject):
    """
    Controller for the extraction of transitions. This controller serves as a
    transmittor between the extracted data (model) and the extraction & tagging panel (view).

    Notice that the connections that transport selected transitions from the
    canvas to the extraction model are done in the plotting controller instead
    of here.

    Relevant UI elements:
    - tagging section (title, radio buttons for the three modes and options for each mode)
    - extraction section (a table of extracted transitions, and associated buttons for extraction)

    Relevant model:
    - extracted data (all and active)
    - measurement data

    Parameters
    ----------
    parent : QObject
        The parent QObject.
    dataSets : Tuple[AllExtractedData, ActiveExtractedData]
        The extracted data model (all and active).
    labelingView : LabelingView
        The extraction & tagging view.
    """

    def __init__(
        self,
        parent: QObject,
        models: Tuple["AllExtractedData", "ActiveExtractedData", "MeasDataSet"],
        labelingView: "LabelingView",
    ):

        super().__init__(parent)

        self.allDatasets, self.activeDataset, self.measDataSet = models
        self.labelingView = labelingView

        self._switchFigConnects()
        self._viewUpdatedConnects()
        self._modelUpdatedConnects()
        self._uiExtractedDataConnects()
        self._uiExtractedDataControlConnects()

    # initialization ===================================================
    def replaceHS(self, hilbertspace: "HilbertSpace"):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.

        Parameters
        ----------
        hilbertspace : HilbertSpace
            The HilbertSpace object.
        """
        self.labelingView.updateHS(
            [subsys.id_str for subsys in hilbertspace.subsystem_list],
        )

    def replaceMeasData(self, measurementData: List["MeasDataType"]):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.

        Parameters
        ----------
        measurementData : List[MeasurementDataType]
            The measurement data.
        """
        self.allDatasets.replaceMeasData([data.name for data in measurementData])

    def dynamicalInit(self):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.
        """
        self.labelingView.dynamicalInit()
        self.allDatasets.dynamicalInit()

        # select the first row. setModel should be called after dynamicalInit
        # it requires the data to be loaded first
        self.labelingView.extractionList.setModel(self.allDatasets)
        self.labelingView.extractionList.selectItem(0, blockSignals=True)

        self._mainSwitchFigConnects()

    # Connections ======================================================
    def _switchFigConnects(self):
        """
        When the user switches between different measurement data figures,
        the extracted transitions displayed should be updated accordingly.

        This function connects to the slots for the import stage
        """
        self.measDataSet.figSwitched.connect(self.allDatasets.switchFig)

    def _mainSwitchFigConnects(self):
        """
        Different from the switchFigConnects, this function connects to the slots
        for the main stage. 
        """
        self.measDataSet.figSwitched.connect(
            lambda: self.labelingView.extractionList.selectItem(
                self.allDatasets.currentRow, blockSignals=True
            )
        )

    def _uiExtractedDataControlConnects(self):
        """Connect buttons for inserting and deleting a data set, or clearing all data sets"""
        # update the backend model
        self.labelingView.extractionCtrls["new"].clicked.connect(
            self.allDatasets.newRow
        )
        self.labelingView.extractionCtrls["delete"].clicked.connect(
            self.allDatasets.removeCurrentRow
        )
        self.labelingView.extractionCtrls["clear"].clicked.connect(
            self.allDatasets.removeAll
        )

    def _uiExtractedDataConnects(self):
        """Make connections for changes in extracted data."""

        # UI selection --> Model selection
        self.labelingView.extractionList.focusChanged.connect(
            self.allDatasets.setCurrentRow
        )

        # allDataset selection --> activeDataset update
        self.allDatasets.focusChanged.connect(self.activeDataset.replaceAllData)

        # If data in the TableView is changed manually through editing,
        # the 'dataChanged' signal will be emitted. The following connects the signal
        # to an update in th data stored in the AllExtractedData
        self.activeDataset.dataUpdated.connect(self.allDatasets.updateCurrentTransition)

        # whenever a row is inserted or removed, select the current row
        # in the view VISUALLY. It comlete a loop from the view to model
        # and back to view. To avoid infinite loop, block the signal
        # TODO need to implement a view update whenever model change (the currentRow)
        self.allDatasets.rowsInserted.connect(
            lambda: self.labelingView.extractionList.selectItem(
                self.allDatasets.currentRow, blockSignals=True
            )
        )
        self.allDatasets.rowsRemoved.connect(
            lambda: self.labelingView.extractionList.selectItem(
                self.allDatasets.currentRow, blockSignals=True
            )
        )

    def _viewUpdatedConnects(self):
        """
        Connect the signals for user changes through UI in the tagging section to the corresponding
        slots that update the model accordingly.
        """
        # Once the user has finished editing the tag, update the AllExtractedData data
        self.labelingView.tagChanged.connect(self.activeDataset.updateTag)

    def _modelUpdatedConnects(self):
        """
        Once the dataset selection and title selection is changed, change the tag panel
        correspondingly
        """
        self.activeDataset.dataSwitched.connect(
            lambda transition: self.labelingView.replaceTag(transition.tag)
        )
