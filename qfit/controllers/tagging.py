from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qfit.ui_designer.ui_window import Ui_MainWindow
    from qfit.core.mainwindow import MainWindow

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
    changedTagType = Signal()
    changedTagData = Signal()

    def __init__(
        self, 
        subsysCount: int, 
        mainWindow: "MainWindow",
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.mainWindow = mainWindow
        self.ui = self.mainWindow.ui

        self.subsysCount = subsysCount

        self._initializeUI()

        self._taggingConnects()
        self._datasetConnects()

    def _initializeUI(self):
        """
        Set up the UI for the tagging panel:
        - In NO_TAG mode, switch off the bare and dressed tagging panels
        - Set the number of subsystems
        """
        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(False)

        self.ui.initialStateLineEdit.setTupleLength(self.subsysCount)
        self.ui.finalStateLineEdit.setTupleLength(self.subsysCount)

    def _taggingConnects(self):
        # connect the radio buttons to the corresponding tagging panels
        self.ui.tagDispersiveBareRadioButton.toggled.connect(self._setBareMode)
        self.ui.tagDispersiveDressedRadioButton.toggled.connect(
            self._setDressedMode
        )
        self.ui.noTagRadioButton.toggled.connect(self._setNoTagMode)

        # Once the user has finished editing the tag, emit the changedTagData signal
        self.ui.initialStateLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.finalStateLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.phNumberBareSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())
        self.ui.initialStateSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())
        self.ui.finalStateSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())
        self.ui.phNumberDressedSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())

    def _datasetConnects(self):
        """
        Once the dataset selection is changed, change the tag panel 
        correspondingly
        """
        # Whenever tag type or tag data is changed, update the AllExtractedData data
        self.changedTagType.connect(
            lambda: self.mainWindow.allDatasets.updateCurrentTag(self.getTagFromUI())
        )
        self.changedTagData.connect(
            lambda: self.mainWindow.allDatasets.updateCurrentTag(self.getTagFromUI())
        )

        # Whenever a new dataset is activated in the AllExtractedData, update the TagDataView
        self.ui.datasetListView.clicked.connect(self._syncTagWithDataset)

        # Whenever a dataset is renamed, update the title for tags
        self.mainWindow.allDatasets.dataChanged.connect(self._syncTagTitle)

        # switch the tag so that it matches the current data set
        self.mainWindow.activeDataset.dataSwitchSignal.signal.connect(self._syncTagWithDataset)

    @Slot()
    def _syncTagTitle(self):
        self.ui.transitionLabel.setText(
            f"LABEL for {self.mainWindow.allDatasets.currentDataName()}"
        )

    @Slot()
    def _syncTagWithDataset(self):
        self._syncTagTitle()
        self.setTag(self.mainWindow.allDatasets.currentTagItem())

    @Slot()
    def _setNoTagMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(False)
        self.changedTagType.emit()

    @Slot()
    def _setBareMode(self):
        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(True)
        self.changedTagType.emit()
        self.ui.initialStateLineEdit.editingFinished.emit()
        self.ui.finalStateLineEdit.editingFinished.emit()

    @Slot()
    def _setDressedMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(True)
        self.changedTagType.emit()

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
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.initialStateLineEdit.isValid():
            return False
        return True

    def _isValidFinalBare(self):
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.finalStateLineEdit.isValid():
            return False
        return True

    def _isValid(self):
        return self._isValidInitialBare() and self._isValidFinalBare()

    def getTagFromUI(self):
        tag = Tag()
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

    def setTag(self, tag):
        self.blockSignals(True)
        self._clear()
        if tag.tagType == NO_TAG:
            self.ui.noTagRadioButton.toggle()
            self._setNoTagMode()
        elif tag.tagType == DISPERSIVE_BARE:
            self.ui.tagDispersiveBareRadioButton.toggle()
            self._setBareMode()
            # self.ui.subsysNamesLineEdit.setFromSubsysNameList(tag.subsysList)
            self.ui.initialStateLineEdit.setFromTuple(tag.initial)
            self.ui.finalStateLineEdit.setFromTuple(tag.final)
            self.ui.phNumberBareSpinBox.setValue(tag.photons)
        elif tag.tagType == DISPERSIVE_DRESSED:
            self._setDressedMode()
            self.ui.tagDispersiveDressedRadioButton.toggle()
            self.ui.initialStateSpinBox.setValue(tag.initial)
            self.ui.finalStateSpinBox.setValue(tag.final)
            self.ui.phNumberDressedSpinBox.setValue(tag.photons)
        self.blockSignals(False)