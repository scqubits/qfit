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
    from qfit.views.tagging import TaggingView
    from qfit.models.data_structures import Tag


class TaggingCtrl(QObject):
    def __init__(
        self,
        dataSets: Tuple["AllExtractedData", "ActiveExtractedData"],
        taggingView: "TaggingView",
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
        self.taggingView = taggingView

        self._viewUpdatedConnects()
        self._modelUpdatedConnects()

    # Connections ======================================================
    def _viewUpdatedConnects(self):
        """
        Connect the signals for user changes through UI in the tagging section to the corresponding
        slots that update the model accordingly.
        """
        # Once the user has finished editing the tag, update the AllExtractedData data
        # each view (LineEdit and SpinBox) has its own signal and a common slot _tagViewToModel to
        # update the model
        self.taggingView.tagChanged.connect(self.allDatasets.updateCurrentTag)

    def _modelUpdatedConnects(self):
        """
        Once the dataset selection and title selection is changed, change the tag panel
        correspondingly
        """
        self.activeDataset.dataSwitchSignal.signal.connect(self._tagModelToView)

    # Slots ============================================================
    @Slot()
    def _tagModelToView(self):
        """
        Whenever the active dataset is switched, update the tag panel to match the current dataset.
        """
        # self._setTagTitle()

        tag = self.allDatasets.currentTagItem()
        self.taggingView.setTag(tag)
