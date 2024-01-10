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
    - DISPERSIVE_BARE: transition between two states tagged by
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
    
    def __repr__(self):
        return self.__str__()


class TaggingCtrl(QObject):
    def __init__(
        self,
        subsysCount: int,
        dataSets: Tuple["AllExtractedData", "ActiveExtractedData"],
        ui: "Ui_MainWindow",
        ui_groups: Tuple[Dict[str, Any], ...],
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

        self.ui = ui
        self.groupBox, self.radioButtons, self.bareLabels, self.dressedLabels = ui_groups
        self.allDatasets, self.activeDataset = dataSets

        self.subsysCount = subsysCount

        self._initializeUI()

        self._modeSwitchConnects()
        self._viewUpdatedConnects()
        self._modelUpdatedConnects()

    # Initialization ===================================================
    def _initializeUI(self):
        """
        Set up the UI for the tagging panel:
        - In NO_TAG mode, switch off (hide) the bare and dressed tagging panels
        - Set the number of subsystems
        """
        self.groupBox["bare"].setVisible(False)
        self.groupBox["dressed"].setVisible(False)

        # the number of subsystems are used by the initial and final state line edits
        # to check the validity of the input
        self.bareLabels["initial"].setTupleLength(self.subsysCount)
        self.bareLabels["final"].setTupleLength(self.subsysCount)

    # Connections ======================================================
    def _modeSwitchConnects(self):
        """
        respond to the user switching between the three modes (no tag, bare tag, dressed tag)
        """
        # connect the radio buttons to the corresponding tagging panels
        # one for each mode
        self.radioButtons["bare"].toggled.connect(
            lambda: self._onBareRadioButtonToggled()
        )
        self.radioButtons["dressed"].toggled.connect(
            lambda: self._onDressedRadioButtonToggled()
        )
        self.radioButtons["no tag"].toggled.connect(
            lambda: self._onNoTagRadioButtonToggled()
        )

    def _viewUpdatedConnects(self):
        """
        Connect the signals for user changes through UI in the tagging section to the corresponding
        slots that update the model accordingly.
        """
        # Once the user has finished editing the tag, update the AllExtractedData data
        # each view (LineEdit and SpinBox) has its own signal and a common slot _tagViewToModel to
        # update the model
        self.bareLabels["initial"].editingFinished.connect(self._tagViewToModel)
        self.bareLabels["final"].editingFinished.connect(self._tagViewToModel)
        self.bareLabels["photons"].valueChanged.connect(lambda: self._tagViewToModel())
        self.dressedLabels["initial"].valueChanged.connect(lambda: self._tagViewToModel())
        self.dressedLabels["final"].valueChanged.connect(lambda: self._tagViewToModel())
        self.dressedLabels["photons"].valueChanged.connect(
            lambda: self._tagViewToModel()
        )

    def _modelUpdatedConnects(self):
        """
        Once the dataset selection and title selection is changed, change the tag panel
        correspondingly
        """
        self.activeDataset.dataSwitchSignal.signal.connect(self._tagModelToView)

    # Processing =======================================================
    def _clear(self):
        """
        Clear all previous tag inputs in the UI.
        """
        self.bareLabels["initial"].clear()
        self.bareLabels["final"].clear()
        self.bareLabels["photons"].setValue(1)
        self.dressedLabels["initial"].setValue(0)
        self.dressedLabels["final"].setValue(1)
        self.dressedLabels["photons"].setValue(1)

    def _isValidInitialBare(self):
        """
        Check if the input initial state is valid for bare-states tagging.
        """
        if not self.groupBox["bare"].isVisible():
            return True  # only bare-states tags require validation
        if not self.bareLabels["initial"].isValid():
            return False
        return True

    def _isValidFinalBare(self):
        """
        Check if the input final state is valid for bare-states tagging.
        """
        if not self.groupBox["bare"].isVisible():
            return True  # only bare-states tags require validation
        if not self.bareLabels["final"].isValid():
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
        self.groupBox["bare"].setVisible(False)
        self.groupBox["dressed"].setVisible(False)

    def _setNoTagInView(self, tag: Tag):
        """
        Set the UI to display no tag (do nothing, but should be in the no-tag page first)).
        """
        return  # do nothing

    def _toBareTagPage(self):
        """
        Switch the UI to the bare-states tag page.
        """
        self.groupBox["bare"].setVisible(True)
        self.groupBox["dressed"].setVisible(False)

    def _setBareTagInView(self, tag: Tag):
        """
        Set the UI to display a bare-states tag (should be in the bare tag page first).
        """
        self.bareLabels["initial"].setFromTuple(tag.initial)
        self.bareLabels["final"].setFromTuple(tag.final)
        self.bareLabels["photons"].setValue(tag.photons)

    def _toDressedTagPage(self):
        """
        Switch the UI to the dressed-states tag page.
        """
        self.groupBox["bare"].setVisible(False)
        self.groupBox["dressed"].setVisible(True)

    def _setDressedTagInView(self, tag: Tag):
        """
        Set the UI to display a dressed-states tag (should be in the dressed tag page first).
        """
        self.dressedLabels["initial"].setValue(tag.initial)
        self.dressedLabels["final"].setValue(tag.final)
        self.dressedLabels["photons"].setValue(tag.photons)

    def blockAllSignals(self, block: bool):
        """
        Block all signals in the contrller, model and view.
        """
        self.blockSignals(block)

        # View: Tag panel
        for values in self.radioButtons.values():
            values.blockSignals(block)
        for values in self.bareLabels.values():
            values.blockSignals(block)
        for values in self.dressedLabels.values():
            values.blockSignals(block)
            
        # Model: transitions
        self.allDatasets.blockSignals(block)
        self.activeDataset.blockSignals(block)

    def getTagFromView(self) -> Tag:
        """
        Provide an external interface (outside of this class) to generate the tag from the view.
        It returns a tag based on the current view

        Returns
        -------
        tag: Tag
            tag data from the view
        """
        tag = Tag()
        # if no tag radio button selected, or the input for other tag types are invalid,
        # set the tag type to NO_TAG
        if self.radioButtons["no tag"].isChecked() or not self._isValid():
            tag.tagType = NO_TAG
        elif self.radioButtons["bare"].isChecked():
            tag.tagType = DISPERSIVE_BARE
            tag.initial = self.bareLabels["initial"].getTuple()
            tag.final = self.bareLabels["final"].getTuple()
            tag.photons = self.bareLabels["photons"].value()
            # tag.subsysList = self.ui.subsysNamesLineEdit.getSubsysNameList()
        elif self.radioButtons["dressed"].isChecked():
            tag.tagType = DISPERSIVE_DRESSED
            tag.initial = self.dressedLabels["initial"].value()
            tag.final = self.dressedLabels["final"].value()
            tag.photons = self.dressedLabels["photons"].value()
        return tag

    def setTagInView(self, tag):
        """
        Provide an external interface (outside of this class) to set the tag in the view.
        It sets the tag view based on the tag data.

        Parameters
        ----------
        tag: Tag
            tag data to be set in the view
        """
        # we have to block all signals to avoid multiple calls
        self.blockAllSignals(True)

        self._clear()
        if tag.tagType == NO_TAG:
            self.radioButtons["no tag"].toggle()
            self._toNoTagPage()
            self._setNoTagInView(tag)
        elif tag.tagType == DISPERSIVE_BARE:
            self.radioButtons["bare"].toggle()
            self._toBareTagPage()
            self._setBareTagInView(tag)
        elif tag.tagType == DISPERSIVE_DRESSED:
            self.radioButtons["dressed"].toggle()
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
        if not self.radioButtons["bare"].isChecked():
            return
        self._toBareTagPage()  # switch to bare tag page
        self._tagViewToModel()  # update the model's tag as user indended to switch to bare tag

    @Slot()
    def _onDressedRadioButtonToggled(self):
        """
        Slot for dressed button being toggled. If the dressed button is checked, switch the
        UI to the dressed tag page. Else, do nothing.
        """
        if not self.radioButtons["dressed"].isChecked():
            return
        self._toDressedTagPage()
        self._tagViewToModel()

    @Slot()
    def _onNoTagRadioButtonToggled(self):
        """
        Slot for no tag button being toggled. If the no tag button is checked, switch the
        UI to the no tag page. Else, do nothing.
        """
        if not self.radioButtons["no tag"].isChecked():
            return
        self._toNoTagPage()
        self._tagViewToModel()

    # @Slot()
    # def _setTagTitle(self):
    #     """
    #     Set the title for the tag panel based on the current dataset.
    #     """
    #     self.ui.transitionLabel.setText(
    #         f"LABEL for {self.allDatasets.currentDataName()}"
    #     )

    @Slot()
    def _tagModelToView(self):
        """
        Whenever the active dataset is switched, update the tag panel to match the current dataset.
        """
        # self._setTagTitle()

        tag = self.allDatasets.currentTagItem()
        # print("M2V:", tag.tagType)
        self.setTagInView(tag)

    @Slot()
    def _tagViewToModel(self):
        """
        Whenever the user finishes editing the tag, update the tag data in the model.
        """
        # obtain the tag from the view
        tag = self.getTagFromView()
        # print("V2M:", tag.tagType)
        self.allDatasets.updateCurrentTag(tag)
