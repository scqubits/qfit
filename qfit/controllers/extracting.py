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
    from qfit.views.extracting import ExtractingView
    from qfit.models.data_structures import Tag


class ExtractingCtrl(QObject):
    def __init__(
        self,
        dataSets: Tuple["AllExtractedData", "ActiveExtractedData"],
        extractingView: "ExtractingView",
        *args,
        **kwargs,
    ):
        """
        Controller for the tagging panel (not for the tag data itself). This controller serves as a
        transmittor between the tag data (model) and the tag panel (view). User interact with the
        tag panel and the model will be updated accordingly, meanwhile, changes in the model (e.g.
        a different dataset is selected) will be reflected in the tag panel.

        Relevant UI elements:
        - tagging section (title, radio buttons for the three modes and options for each mode)

        Relevant model:
        - extracted data (all and active)

        Parameters
        ----------
        subsysCount: int
            number of subsystems in the system
        dataSets: Tuple[AllExtractedData, ActiveExtractedData]
            all extracted datasets and the currently active dataset
            we need the active dataset to update the tag panel when the dataset is changed
        ui: Ui_MainWindow
            the main window UI
        ui_groups:
            A tuple of UI dictionaries: uiLabelBoxes, uiLabelRadioButtons, uiBareLabelInputs 
            and uiDressedLabelInputs
        additional arguments are passed to QObject.__init__()
        """
        super().__init__(*args, **kwargs)

        self.allDatasets, self.activeDataset = dataSets
        self.extractingView = extractingView

        self._viewUpdatedConnects()
        self._modelUpdatedConnects()
        self._uiExtractedDataConnects()
        self._uiExtractedDataControlConnects()

    # initialization ===================================================
    def dynamicalInit(self):
        self.allDatasets.blockSignals(True)
        self.allDatasets.removeAll()        # move to load from registry
        self.allDatasets.blockSignals(False)

    def _uiExtractedDataControlConnects(self):
        """Connect buttons for inserting and deleting a data set, or clearing all data sets"""
        # update the backend model
        self.extractingView.extractionCtrls["new"].clicked.connect(self.allDatasets.newRow)
        self.extractingView.extractionCtrls["delete"].clicked.connect(self.allDatasets.removeCurrentRow)
        self.extractingView.extractionCtrls["clear"].clicked.connect(self.allDatasets.removeAll)

    def _uiExtractedDataConnects(self):
        """Make connections for changes in extracted data."""
        self.extractingView.extractionList.setModel(self.allDatasets)
        self.extractingView.extractionList.selectItem(self.allDatasets.currentRow) # select the first row

        # UI selection --> Model selection
        self.extractingView.extractionList.focusChanged.connect(
            self.allDatasets.setCurrentRow
        )

        # allDataset selection --> activeDataset update
        self.allDatasets.focusChanged.connect(
            self.activeDataset.replaceAllData
        )

        # If data in the TableView is changed manually through editing,
        # the 'dataChanged' signal will be emitted. The following connects the signal
        # to an update in th data stored in the AllExtractedData
        self.activeDataset.dataUpdated.connect(
            self.allDatasets.updateAssocData
        ) 

        # whenever a row is inserted or removed, select the current row 
        # in the view VISUALLY. It comlete a loop from the view to model 
        # and back to view. To avoid infinite loop, block the signal
        self.allDatasets.rowsInserted.connect(
            lambda: self.extractingView.extractionList.selectItem(self.allDatasets.currentRow, blockSignals=True)
        )
        self.allDatasets.rowsRemoved.connect(
            lambda: self.extractingView.extractionList.selectItem(self.allDatasets.currentRow, blockSignals=True)
        )

    # Connections ======================================================
    def _viewUpdatedConnects(self):
        """
        Connect the signals for user changes through UI in the tagging section to the corresponding
        slots that update the model accordingly.
        """
        # Once the user has finished editing the tag, update the AllExtractedData data
        self.extractingView.tagChanged.connect(self.activeDataset.updateTag)

    def _modelUpdatedConnects(self):
        """
        Once the dataset selection and title selection is changed, change the tag panel
        correspondingly
        """
        self.activeDataset.dataSwitched.connect(
            lambda data, tag: self.extractingView.replaceTag(tag)
        )