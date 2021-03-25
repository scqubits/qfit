# tagdata_view.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide2.QtCore import QObject, Signal
from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import QRegularExpression as QRegExp
from PySide2.QtGui import QRegularExpressionValidator as QRegExpValidator
from PySide2.QtGui import QValidator


from datapyc.io_utils import file_io_serializers as serializers

# tagging types (to facilitate file io: do not use Enum)
NO_TAG = "NO_TAG"
DISPERSIVE_DRESSED = "DISPERSIVE_DRESSED"
DISPERSIVE_BARE = "DISPERSIVE_BARE"
CROSSING = "CROSSING"
CROSSING_DRESSED = "CROSSING_DRESSED"


class Tag(serializers.Serializable):
    """
    Store a single dataset tag. The tag can be of different types:
    - NO_TAG: user did not tag data
    - DISPERSIVE_DRESSED: transition between two states in the dispersive regime, tagged by dressed-states indices
    - DISPERSIVE_BARE: : transition between two states in the dispersive regime, tagged by bare-states indices
    - CROSSING: avoided crossing, left untagged (fitting should use closest-energy states)
    - CROSSING_DRESSED: avoided crossing, tagged by dressed-states indices

    Parameters
    ----------
    tagType: str
        one of the tag types listed above
    initial, final: int, or tuple of int, or None
        - For NO_TAG and CROSSING, no initial and final state are specified.
        - For DISPERSIVE_DRESSED and CROSSING_DRESSED, initial and final state are specified by an int dressed index.
        - FOR DISPERSIVE_BARE, initial and final state are specified by a tuple of ints (exc. levels of each subsys)
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


class TagDataView(QObject):
    changedTagType = Signal()
    changedTagData = Signal()

    def __init__(self, ui_TagData, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = ui_TagData

        self.ui.tagDressedGroupBox.setVisible(False)
        self.ui.tagBareGroupBox.setVisible(False)
        self.defaultStyleLineEdit = self.ui.subsysNamesLineEdit.styleSheet()

        # establish connects
        self.ui.tagDispersiveBareRadioButton.toggled.connect(self.setDispersiveBareMode)
        self.ui.tagDispersiveDressedRadioButton.toggled.connect(
            self.setDispersiveDressedMode
        )
        self.ui.noTagRadioButton.toggled.connect(self.setNoTagMode)
        self.ui.tagCrossingRadioButton.toggled.connect(self.setCrossingMode)
        self.ui.tagCrossingDressedRadioButton.toggled.connect(
            self.setCrossingDressedMode
        )

        self.ui.tagDispersiveBareRadioButton.toggled.connect(self.setLineEditColor)
        self.ui.tagDispersiveDressedRadioButton.toggled.connect(self.setLineEditColor)
        self.ui.noTagRadioButton.toggled.connect(self.setLineEditColor)
        self.ui.tagCrossingRadioButton.toggled.connect(self.setLineEditColor)
        self.ui.tagCrossingDressedRadioButton.toggled.connect(self.setLineEditColor)

        self.ui.subsysNamesLineEdit.textChanged.connect(
            lambda x: self.setLineEditColor()
        )
        self.ui.initialStateLineEdit.textChanged.connect(
            lambda x: self.setLineEditColor()
        )
        self.ui.finalStateLineEdit.textChanged.connect(
            lambda x: self.setLineEditColor()
        )

        self.ui.subsysNamesLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.initialStateLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.finalStateLineEdit.editingFinished.connect(self.changedTagData.emit)
        self.ui.phNumberBareSpinBox.valueChanged.connect(
            lambda x: self.changedTagData.emit
        )

        self.ui.initialStateSpinBox.valueChanged.connect(
            lambda x: self.changedTagData.emit
        )
        self.ui.finalStateSpinBox.valueChanged.connect(
            lambda x: self.changedTagData.emit
        )
        self.ui.phNumberDressedSpinBox.valueChanged.connect(
            lambda x: self.changedTagData.emit
        )

    def setNoTagMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(False)
        self.changedTagType.emit()

    def setDispersiveBareMode(self):
        self.ui.tagBareGroupBox.setVisible(True)
        self.ui.tagDressedGroupBox.setVisible(False)
        self.changedTagType.emit()
        # self.ui.subsysNamesLineEdit.editingFinished.emit()
        # self.ui.initialStateLineEdit.editingFinished.emit()
        # self.ui.finalStateLineEdit.editingFinished.emit()

    def setDispersiveDressedMode(self):
        self.ui.tagDressedGroupBox.setVisible(True)
        self.ui.tagBareGroupBox.setVisible(False)
        self.changedTagType.emit()

    def setCrossingMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(False)
        self.changedTagType.emit()

    def setCrossingDressedMode(self):
        self.ui.tagBareGroupBox.setVisible(False)
        self.ui.tagDressedGroupBox.setVisible(True)
        self.changedTagType.emit()

    def isValidInitialBare(self):
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.subsysNamesLineEdit.isValid():
            return False
        subsysCount = self.ui.subsysNamesLineEdit.subsysCount()

        if not self.ui.initialStateLineEdit.isValid():
            return False
        if len(self.ui.initialStateLineEdit.getTuple()) != subsysCount:
            return False
        return True

    def isValidFinalBare(self):
        if not self.ui.tagBareGroupBox.isVisible():
            return True  # only bare-states tags require validation
        if not self.ui.subsysNamesLineEdit.isValid():
            return False
        subsysCount = self.ui.subsysNamesLineEdit.subsysCount()

        if not self.ui.finalStateLineEdit.isValid():
            return False
        if len(self.ui.finalStateLineEdit.getTuple()) != subsysCount:
            return False
        return True

    def isValid(self):
        return self.isValidInitialBare() and self.isValidFinalBare()

    def getTag(self):
        tag = Tag()
        if self.ui.noTagRadioButton.isChecked() or not self.isValid():
            tag.tagType = NO_TAG
        elif self.ui.tagDispersiveBareRadioButton.isChecked():
            tag.tagType = DISPERSIVE_BARE
            tag.initial = self.ui.initialStateLineEdit.getTuple()
            tag.final = self.ui.finalStateLineEdit.getTuple()
            tag.photons = self.ui.phNumberBareSpinBox.value()
            tag.subsysList = self.ui.subsysNamesLineEdit.getSubsysNameList()
        elif self.ui.tagDispersiveDressedRadioButton.isChecked():
            tag.tagType = DISPERSIVE_DRESSED
            tag.initial = self.ui.initialStateSpinBox.value()
            tag.final = self.ui.finalStateSpinBox.value()
            tag.photons = self.ui.phNumberDressedSpinBox.value()
        elif self.ui.tagCrossingRadioButton.isChecked():
            tag.tagType = CROSSING
        elif self.ui.tagCrossingDressedRadioButton.isChecked():
            tag.tagType = CROSSING_DRESSED
            tag.initial = self.ui.initialStateSpinBox.value()
            tag.final = self.ui.finalStateSpinBox.value()
            tag.photons = self.ui.phNumberDressedSpinBox.value()
        return tag

    def setTag(self, tag):
        self.blockSignals(True)
        if tag.tagType == NO_TAG:
            self.ui.noTagRadioButton.toggle()
            self.setNoTagMode()
        elif tag.tagType == DISPERSIVE_BARE:
            self.ui.tagDispersiveBareRadioButton.toggle()
            self.setDispersiveBareMode()
            self.ui.subsysNamesLineEdit.setFromSubsysNameList(tag.subsysList)
            self.ui.initialStateLineEdit.setFromTuple(tag.initial)
            self.ui.finalStateLineEdit.setFromTuple(tag.final)
            self.ui.phNumberBareSpinBox.setValue(tag.photons)
        elif tag.tagType == DISPERSIVE_DRESSED:
            self.setCrossingDressedMode()
            self.ui.tagDispersiveDressedRadioButton.toggle()
            self.ui.initialStateSpinBox.setValue(tag.initial)
            self.ui.finalStateSpinBox.setValue(tag.final)
            self.ui.phNumberDressedSpinBox.setValue(tag.photons)
        elif tag.tagType == CROSSING:
            self.ui.tagCrossingRadioButton.toggle()
            self.setCrossingMode()
        elif tag.tagType == CROSSING_DRESSED:
            self.ui.tagCrossingDressedRadioButton.toggle()
            self.setCrossingDressedMode()
            self.ui.initialStateSpinBox.setValue(tag.initial)
            self.ui.finalStateSpinBox.setValue(tag.final)
            self.ui.phNumberDressedSpinBox.setValue(tag.photons)
        self.blockSignals(False)

    def setLineEditColor(self, *args, **kwargs):
        if (
            not self.ui.tagBareGroupBox.isVisible()
            or self.ui.subsysNamesLineEdit.isValid()
        ):
            self.ui.subsysNamesLineEdit.setStyleSheet(self.defaultStyleLineEdit)
        else:
            self.ui.subsysNamesLineEdit.setStyleSheet("border: 3px solid red;")

        if not self.ui.tagBareGroupBox.isVisible() or self.isValidInitialBare():
            self.ui.initialStateLineEdit.setStyleSheet(self.defaultStyleLineEdit)
        else:
            self.ui.initialStateLineEdit.setStyleSheet("border: 3px solid red;")

        if not self.ui.tagBareGroupBox.isVisible() or self.isValidFinalBare():
            self.ui.finalStateLineEdit.setStyleSheet(self.defaultStyleLineEdit)
        else:
            self.ui.finalStateLineEdit.setStyleSheet("border: 3px solid red;")


class StrTupleLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        regEx = QRegExp("(^[a-zA-Z][a-zA-Z0-9]*)+(, ?([a-zA-Z][a-zA-Z0-9]*)+)*$")
        validator = QRegExpValidator(regEx)
        self.setValidator(validator)

        self.editingFinished.connect(self.processUpdate)
        self.previousStr = ""

    def setText(self, nameListStr):
        if self.validator().validate(nameListStr, 0)[0] is QValidator.State.Acceptable:
            self.previousStr = nameListStr
        super().setText(nameListStr)

    def value(self):
        return self.text()

    def getSubsysNameList(self):
        if self.isValid():
            return [name.strip() for name in self.value().split(",")]
        return []

    def setFromSubsysNameList(self, subsysNameList):
        subsysStr = ", ".join(subsysNameList)
        self.setText(subsysStr)

    def subsysCount(self):
        return len(self.getSubsysNameList())

    def processUpdate(self):
        if self.hasAcceptableInput():
            self.previousStr = self.text()
        else:
            self.setText(self.previousStr)

    def isValid(self):
        return self.hasAcceptableInput()


class IntTupleLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        regEx = QRegExp("^([1-9]\d*|0)(, ?([1-9]\d*|0))*$")
        validator = QRegExpValidator(regEx)
        self.setValidator(validator)
        self.editingFinished.connect(self.processUpdate)
        self.previousStr = ""

    def setText(self, tupleStr):
        if self.validator().validate(tupleStr, 0)[0] is QValidator.State.Acceptable:
            self.previousStr = tupleStr
        super().setText(tupleStr)

    def value(self):
        return self.text()

    def getTuple(self):
        if self.isValid():
            return eval(self.value() + ",")
        return None

    def setFromTuple(self, newTuple):
        self.setText(str(newTuple)[1:-1])

    def processUpdate(self):
        if self.hasAcceptableInput():
            self.previousStr = self.text()
        else:
            self.setText(self.previousStr)

    def isValid(self):
        return self.hasAcceptableInput()
