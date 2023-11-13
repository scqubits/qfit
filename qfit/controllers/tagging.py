from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from qfit.ui_designer.ui_window import Ui_MainWindow
    from qfit.core.mainwindow import MainWindow
    from qfit.models.extracted_data import AllExtractedData, ActiveExtractedData

# tagging types (to facilitate file io: do not use Enum)
NO_TAG = "NO_TAG"
DISPERSIVE_DRESSED = "DISPERSIVE_DRESSED"
DISPERSIVE_BARE = "DISPERSIVE_BARE"


class Tag:
    """
    Store a single dataset tag. The tag can be of different types:
    - NO_TAG: user did not tag data
    - DISPERSIVE_DRESSED: transition between two states tagged by
    dressed-states indices
    - DISPERSIVE_BARE: : transition between two states tagged by
    bare-states indices

    Parameters
    ----------
    tagType: str
        one of the tag types listed above
    initial, final: int, or tuple of int, or None
        - For NO_TAG, no initial and final state are specified.
        - For DISPERSIVE_DRESSED, initial and final state are specified
        by an int dressed index.
        - FOR DISPERSIVE_BARE, initial and final state are specified by
        a tuple of ints (exc. levels of each subsys)
    photons: int or None
        - For NO_TAG, no photon number is specified.
        - For all other tag types, this int specifies the photon number rank of the transition.
    """

    def __init__(
        self, tagType=NO_TAG, initial=None, final=None, photons=None, subsysList=None
    ):
        self.tagType = tagType
        self.initial = initial
        self.final = final
        self.photons = photons
        self.subsysList = subsysList

    def __str__(self):
        return "Tag: {0} {1} {2} {3} {4}".format(
            self.tagType,
            str(self.initial),
            str(self.final),
            str(self.photons),
            str(self.subsysList),
        )


class TaggingCtrl(QObject):
    def __init__(
        self,
        subsysCount: int,
        dataSets: Tuple["AllExtractedData", "ActiveExtractedData"],
        ui: "Ui_MainWindow",
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

        ARGUMENTS
        ---------
        subsysCount: int
            number of subsystems in the system
        dataSets: Tuple[AllExtractedData, ActiveExtractedData]
            all extracted datasets and the currently active dataset
            we need the active dataset to update the tag panel when the dataset is changed
        ui: Ui_MainWindow
            the main window UI
        additional arguments are passed to QObject.__init__()
        """
        super().__init__(*args, **kwargs)

        self.ui = ui
        self.allDatasets, self.activeDataset = dataSets

        self.subsysCount = subsysCount

        self._initializeUI()

        self._viewUpdatedConnects()
        self._modelUpdatedConnects()

    # Initialization ===================================================
    def _initializeUI(self):
        """
        Set up the UI for the tagging panel:
        - In NO_TAG mode, switch off (hide) the bare and dressed tagging panels
        - Set the number of subsystems
        """
        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(False)

        # the number of subsystems are used by the initial and final state line edits
        # to check the validity of the input
        self.ui.initialStateLineEdit.setTupleLength(self.subsysCount)
        self.ui.finalStateLineEdit.setTupleLength(self.subsysCount)

    # Connections ======================================================
    def _viewUpdatedConnects(self):
        """
        Connect the signals for user changes through UI in the tagging section to the corresponding
        slots that update the model accordingly.
        """
        # connect the radio buttons to the corresponding tagging panels
        # one for each mode
        self.ui.tagDispersiveBareRadioButton.toggled.connect(
            lambda: self._onBareRadioButtonToggled()
        )
        self.ui.tagDispersiveBareRadioButton.toggled.connect(
            lambda: print("Mode clicked: bare")
        )
        self.ui.tagDispersiveDressedRadioButton.toggled.connect(
            lambda: self._onDressedRadioButtonToggled()
        )
        self.ui.tagDispersiveDressedRadioButton.toggled.connect(
            lambda: print("Mode clicked: dressed")
        )
        self.ui.noTagRadioButton.toggled.connect(
            lambda: self._onNoTagRadioButtonToggled()
        )
        self.ui.noTagRadioButton.toggled.connect(lambda: print("Mode clicked: no tag"))

        # Once the user has finished editing the tag, update the AllExtractedData data
        # each view (LineEdit and SpinBox) has its own signal and a common slot _tagViewToModel to
        # update the model
        self.ui.initialStateLineEdit.editingFinished.connect(self._tagViewToModel)
        self.ui.initialStateLineEdit.editingFinished.connect(lambda: print("initial"))
        self.ui.finalStateLineEdit.editingFinished.connect(self._tagViewToModel)
        self.ui.finalStateLineEdit.editingFinished.connect(lambda: print("final"))
        self.ui.phNumberBareSpinBox.valueChanged.connect(lambda: self._tagViewToModel())
        self.ui.phNumberBareSpinBox.valueChanged.connect(lambda: print("ph spin bare"))
        self.ui.initialStateSpinBox.valueChanged.connect(lambda: self._tagViewToModel())
        self.ui.initialStateSpinBox.valueChanged.connect(lambda: print("init spin"))
        self.ui.finalStateSpinBox.valueChanged.connect(lambda: self._tagViewToModel())
        self.ui.finalStateSpinBox.valueChanged.connect(lambda: print("final spin"))
        self.ui.phNumberDressedSpinBox.valueChanged.connect(
            lambda: self._tagViewToModel()
        )
        self.ui.phNumberDressedSpinBox.valueChanged.connect(
            lambda: print("ph spin bare")
        )

    def _modelUpdatedConnects(self):
        """
        Once the dataset selection and title selection is changed, change the tag panel
        correspondingly
        """
        # # Whenever a new dataset is activated in the AllExtractedData, update the TagDataView
        # self.ui.datasetListView.clicked.connect(self._setTagViewWithDataset)
        # self.ui.datasetListView.clicked.connect(lambda: print("dataset list"))

        # Whenever a dataset is renamed, update the title for tags
        self.allDatasets.dataChanged.connect(self._setTagTitle)
        # self.allDatasets.dataChanged.connect(lambda: print("data changed"))

        # Whenever the activae dataset is switched, reflect the change on the tag so that it
        # matches the current data set
        self.activeDataset.dataSwitchSignal.signal.connect(self._tagModelToView)
        self.activeDataset.dataSwitchSignal.signal.connect(lambda: print("data switch"))

    # Processing =======================================================
    def _clear(self):
        """
        Clear all previous tag inputs in the UI.
        """
        self.ui.initialStateLineEdit.clear()
        self.ui.finalStateLineEdit.clear()
        self.ui.phNumberBareSpinBox.setValue(1)
        self.ui.initialStateSpinBox.setValue(0)
        self.ui.finalStateSpinBox.setValue(1)
        self.ui.phNumberDressedSpinBox.setValue(1)

    def _isValidInitialBare(self):
        """ 
        Check if the input initial state is valid for bare-states tagging.
        """
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.initialStateLineEdit.isValid():
            return False
        return True

    def _isValidFinalBare(self):
        """ 
        Check if the input final state is valid for bare-states tagging.
        """
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.finalStateLineEdit.isValid():
            return False
        return True

    def _isValid(self):
        """ 
        Check if the input tag is valid.
        """
        return self._isValidInitialBare() and self._isValidFinalBare()

    def _toNoTagPage(self):
        """
        Switch the UI to the no tag page
        """
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(False)

    def _setNoTagInView(self, tag: Tag):
        """
        Set the UI to display no tag (do nothing, but should be in the no-tag page first)).
        """
        return  # do nothing

    def _toBareTagPage(self):
        """
        Switch the UI to the bare-states tag page.
        """
        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(True)

    def _setBareTagInView(self, tag: Tag):
        """
        Set the UI to display a bare-states tag (should be in the bare tag page first).
        """
        self.ui.initialStateLineEdit.setFromTuple(tag.initial)
        self.ui.finalStateLineEdit.setFromTuple(tag.final)
        self.ui.phNumberBareSpinBox.setValue(tag.photons)

    def _toDressedTagPage(self):
        """
        Switch the UI to the dressed-states tag page.
        """
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(True)

    def _setDressedTagInView(self, tag: Tag):
        """
        Set the UI to display a dressed-states tag (should be in the dressed tag page first).
        """
        self.ui.initialStateSpinBox.setValue(tag.initial)
        self.ui.finalStateSpinBox.setValue(tag.final)
        self.ui.phNumberDressedSpinBox.setValue(tag.photons)

    def blockAllSignals(self, block: bool):
        """
        Block all signals in the contrller, model and view.
        """
        self.blockSignals(block)

        # View: Tag panel
        self.ui.initialStateLineEdit.blockSignals(block)
        self.ui.finalStateLineEdit.blockSignals(block)
        self.ui.phNumberBareSpinBox.blockSignals(block)
        self.ui.initialStateSpinBox.blockSignals(block)
        self.ui.finalStateSpinBox.blockSignals(block)
        self.ui.phNumberDressedSpinBox.blockSignals(block)

        self.ui.noTagRadioButton.blockSignals(block)
        self.ui.tagDispersiveBareRadioButton.blockSignals(block)
        self.ui.tagDispersiveDressedRadioButton.blockSignals(block)

        # Model: transitions
        self.allDatasets.blockSignals(block)
        self.activeDataset.blockSignals(block)

    def getTagFromView(self) -> Tag:
        """
        Provide an external interface (outside of this class) to generate the tag from the view.
        It returns a tag based on the current view

        RETURNS
        -------
        tag: Tag
            tag data from the view
        """
        tag = Tag()
        # if no tag radio button selected, or the input for other tag types are invalid,
        # set the tag type to NO_TAG
        if self.ui.noTagRadioButton.isChecked() or not self._isValid():
            tag.tagType = NO_TAG
        elif self.ui.tagDispersiveBareRadioButton.isChecked():
            tag.tagType = DISPERSIVE_BARE
            tag.initial = self.ui.initialStateLineEdit.getTuple()
            tag.final = self.ui.finalStateLineEdit.getTuple()
            tag.photons = self.ui.phNumberBareSpinBox.value()
            # tag.subsysList = self.ui.subsysNamesLineEdit.getSubsysNameList()
        elif self.ui.tagDispersiveDressedRadioButton.isChecked():
            tag.tagType = DISPERSIVE_DRESSED
            tag.initial = self.ui.initialStateSpinBox.value()
            tag.final = self.ui.finalStateSpinBox.value()
            tag.photons = self.ui.phNumberDressedSpinBox.value()
        return tag

    def setTagInView(self, tag):
        """
        Provide an external interface (outside of this class) to set the tag in the view.
        It sets the tag view based on the tag data.

        ARGUMENTS
        ---------
        tag: Tag
            tag data to be set in the view
        """
        # we have to block all signals to avoid multiple calls
        self.blockAllSignals(True)

        self._clear()
        if tag.tagType == NO_TAG:
            self.ui.noTagRadioButton.toggle()
            self._toNoTagPage()
            self._setNoTagInView(tag)
        elif tag.tagType == DISPERSIVE_BARE:
            self.ui.tagDispersiveBareRadioButton.toggle()
            self._toBareTagPage()
            self._setBareTagInView(tag)
        elif tag.tagType == DISPERSIVE_DRESSED:
            self.ui.tagDispersiveDressedRadioButton.toggle()
            self._toDressedTagPage()
            self._setDressedTagInView(tag)

        self.blockAllSignals(False)

    # Slots ============================================================
    @Slot()
    def _onBareRadioButtonToggled(self):
        """
        Slot for bare button being toggled. If the bare button is checked, switch the 
        UI to the bare tag page. Else, do nothing.
        """
        if not self.ui.tagDispersiveBareRadioButton.isChecked():
            return
        self._toBareTagPage()  # switch to bare tag page
        self._tagViewToModel()  # update the model's tag as user indended to switch to bare tag

    @Slot()
    def _onDressedRadioButtonToggled(self):
        """
        Slot for dressed button being toggled. If the dressed button is checked, switch the 
        UI to the dressed tag page. Else, do nothing.
        """
        if not self.ui.tagDispersiveDressedRadioButton.isChecked():
            return
        self._toDressedTagPage()
        self._tagViewToModel()

    @Slot()
    def _onNoTagRadioButtonToggled(self):
        """
        Slot for no tag button being toggled. If the no tag button is checked, switch the 
        UI to the no tag page. Else, do nothing.
        """
        if not self.ui.noTagRadioButton.isChecked():
            return
        self._toNoTagPage()
        self._tagViewToModel()

    @Slot()
    def _setTagTitle(self):
        """
        Set the title for the tag panel based on the current dataset.
        """
        self.ui.transitionLabel.setText(
            f"LABEL for {self.allDatasets.currentDataName()}"
        )

    @Slot()
    def _tagModelToView(self):
        """
        Whenever the active dataset is switched, update the tag panel to match the current dataset.
        """
        self._setTagTitle()

        tag = self.allDatasets.currentTagItem()
        print("M2V:", tag.tagType)
        self.setTagInView(tag)

    @Slot()
    def _tagViewToModel(self):
        """
        Whenever the user finishes editing the tag, update the tag data in the model.
        """
        # obtain the tag from the view
        tag = self.getTagFromView()
        print("V2M:", tag.tagType)
        self.allDatasets.updateCurrentTag(tag)
