from PySide6.QtCore import (
    QObject,
    Signal,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qfit.ui_designer.ui_window import Ui_MainWindow

# tagging types (to facilitate file io: do not use Enum)
NO_TAG = "NO_TAG"
DISPERSIVE_DRESSED = "DISPERSIVE_DRESSED"
DISPERSIVE_BARE = "DISPERSIVE_BARE"

class Tag(QObject):
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


class TagCtrl(QObject):
    changedTagType = Signal()
    changedTagData = Signal()

    def __init__(
        self, 
        ui_TagData: "Ui_MainWindow",
        subsysCount: int, 
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.ui = ui_TagData

        self.subsysCount = subsysCount

        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(False)
        self.defaultStyleLineEdit = self.ui.initialStateLineEdit.styleSheet()

        self.ui.initialStateLineEdit.setTupleLength(self.subsysCount)
        self.ui.finalStateLineEdit.setTupleLength(self.subsysCount)

        self.establishConnections()

    def establishConnections(self):
        self.ui.tagDispersiveBareRadioButton.toggled.connect(self.setDispersiveBareMode)
        self.ui.tagDispersiveDressedRadioButton.toggled.connect(
            self.setDispersiveDressedMode
        )
        self.ui.noTagRadioButton.toggled.connect(self.setNoTagMode)
        # self.ui.tagCrossingRadioButton.toggled.connect(self.setCrossingMode)
        # self.ui.tagCrossingDressedRadioButton.toggled.connect(
        #     self.setCrossingDressedMode
        # )

        # self.ui.tagDispersiveBareRadioButton.toggled.connect(self.setLineEditColor)
        # self.ui.tagDispersiveDressedRadioButton.toggled.connect(self.setLineEditColor)
        # self.ui.noTagRadioButton.toggled.connect(self.setLineEditColor)
        # self.ui.tagCrossingRadioButton.toggled.connect(self.setLineEditColor)
        # self.ui.tagCrossingDressedRadioButton.toggled.connect(self.setLineEditColor)

        # self.ui.subsysNamesLineEdit.textChanged.connect(
        #     lambda x: self.setLineEditColor()
        # )
        # self.ui.initialStateLineEdit.textChanged.connect(
        #     lambda x: self.setLineEditColor()
        # )
        # self.ui.finalStateLineEdit.textChanged.connect(
        #     lambda x: self.setLineEditColor()
        # )

        # self.ui.subsysNamesLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.initialStateLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.finalStateLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.phNumberBareSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())
        self.ui.initialStateSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())
        self.ui.finalStateSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())
        self.ui.phNumberDressedSpinBox.valueChanged.connect(lambda: self.changedTagData.emit())

    def setNoTagMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(False)
        self.changedTagType.emit()

    def setDispersiveBareMode(self):
        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(True)
        self.changedTagType.emit()
        # self.ui.subsysNamesLineEdit.editingFinished.emit()
        self.ui.initialStateLineEdit.editingFinished.emit()
        self.ui.finalStateLineEdit.editingFinished.emit()

    def setDispersiveDressedMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(True)
        self.changedTagType.emit()

    # def setCrossingMode(self):
    #     self.ui.tagBareGroupBox.setVisible(False)
    #     self.ui.tagDressedGroupBox.setVisible(False)
    #     self.changedTagType.emit()

    # def setCrossingDressedMode(self):
    #     self.ui.tagBareGroupBox.setVisible(False)
    #     self.ui.tagDressedGroupBox.setVisible(True)
    #     self.changedTagType.emit()

    def clear(self):
        """
        Clear all previous tag inputs in the UI.
        """
        self.ui.initialStateLineEdit.clear()
        self.ui.finalStateLineEdit.clear()
        self.ui.phNumberBareSpinBox.setValue(1)
        self.ui.initialStateSpinBox.setValue(0)
        self.ui.finalStateSpinBox.setValue(1)
        self.ui.phNumberDressedSpinBox.setValue(1)

    def isValidInitialBare(self):
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.initialStateLineEdit.isValid():
            return False
        return True

    def isValidFinalBare(self):
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.finalStateLineEdit.isValid():
            return False
        return True

    def isValid(self):
        return self.isValidInitialBare() and self.isValidFinalBare()

    def getTagFromUI(self):
        tag = Tag()
        if self.ui.noTagRadioButton.isChecked() or not self.isValid():
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
        # elif self.ui.tagCrossingRadioButton.isChecked():
        #     tag.tagType = CROSSING
        # elif self.ui.tagCrossingDressedRadioButton.isChecked():
        #     tag.tagType = CROSSING_DRESSED
        #     tag.initial = self.ui.initialStateSpinBox.value()
        #     tag.final = self.ui.finalStateSpinBox.value()
        #     tag.photons = self.ui.phNumberDressedSpinBox.value()
        return tag

    def setTag(self, tag):
        self.blockSignals(True)
        if tag.tagType == NO_TAG:
            self.ui.noTagRadioButton.toggle()
            self.setNoTagMode()
            self.clear()
        elif tag.tagType == DISPERSIVE_BARE:
            self.ui.tagDispersiveBareRadioButton.toggle()
            self.setDispersiveBareMode()
            # self.ui.subsysNamesLineEdit.setFromSubsysNameList(tag.subsysList)
            self.ui.initialStateLineEdit.setFromTuple(tag.initial)
            self.ui.finalStateLineEdit.setFromTuple(tag.final)
            self.ui.phNumberBareSpinBox.setValue(tag.photons)
        elif tag.tagType == DISPERSIVE_DRESSED:
            self.setDispersiveDressedMode()
            self.ui.tagDispersiveDressedRadioButton.toggle()
            self.ui.initialStateSpinBox.setValue(tag.initial)
            self.ui.finalStateSpinBox.setValue(tag.final)
            self.ui.phNumberDressedSpinBox.setValue(tag.photons)
        # elif tag.tagType == CROSSING:
        #     self.ui.tagCrossingRadioButton.toggle()
        #     self.setCrossingMode()
        # elif tag.tagType == CROSSING_DRESSED:
        #     self.ui.tagCrossingDressedRadioButton.toggle()
        #     self.setCrossingDressedMode()
        #     self.ui.initialStateSpinBox.setValue(tag.initial)
        #     self.ui.finalStateSpinBox.setValue(tag.final)
        #     self.ui.phNumberDressedSpinBox.setValue(tag.photons)
        self.blockSignals(False)

    # def setLineEditColor(self, *args, **kwargs):
    #     # if (
    #     #     not self.ui.tagBareGroupBox.isVisible()
    #     #     or self.ui.subsysNamesLineEdit.isValid()
    #     # ):
    #     #     self.ui.subsysNamesLineEdit.setStyleSheet(self.defaultStyleLineEdit)
    #     # else:
    #     #     self.ui.subsysNamesLineEdit.setStyleSheet("border: 3px solid red;")

    #     if not self.ui.tagBareGroupBox.isVisible() or self.isValidInitialBare():
    #         self.ui.initialStateLineEdit.setStyleSheet(self.defaultStyleLineEdit)
    #     else:
    #         self.ui.initialStateLineEdit.setStyleSheet("border: 3px solid red;")

    #     if not self.ui.tagBareGroupBox.isVisible() or self.isValidFinalBare():
    #         self.ui.finalStateLineEdit.setStyleSheet(self.defaultStyleLineEdit)
    #     else:
    #         self.ui.finalStateLineEdit.setStyleSheet("border: 3px solid red;")
