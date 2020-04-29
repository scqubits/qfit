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
from PySide2.QtCore import QRegExp, QObject, Signal
from PySide2.QtGui import QRegExpValidator, QValidator, QPalette
from PySide2.QtWidgets import QLineEdit

from datapyc.models.tagdata_model import Tag, NO_TAG, DISPERSIVE_BARE, DISPERSIVE_DRESSED, CROSSING, CROSSING_DRESSED


class TagDataView(QObject):
    dispersiveBareActivated = Signal()
    
    def __init__(self, ui_TagData, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = ui_TagData
        self.defaultStyleLineEdit = self.ui.subsysNamesLineEdit.styleSheet()
        self.currentTag = Tag()

        # establish connects
        self.ui.tagDispersiveBareRadioButton.pressed.connect(self.setDispersiveBareMode)
        self.ui.tagDispersiveDressedRadioButton.pressed.connect(self.setDispersiveDressedMode)
        self.ui.noTagRadioButton.pressed.connect(self.setNoTagMode)
        self.ui.tagCrossingRadioButton.pressed.connect(self.setCrossingMode)
        self.ui.tagCrossingDressedRadioButton.pressed.connect(self.setCrossingDressedMode)

        self.ui.tagDispersiveBareRadioButton.pressed.connect(self.setLineEditColor)
        self.ui.tagDispersiveDressedRadioButton.pressed.connect(self.setLineEditColor)
        self.ui.noTagRadioButton.pressed.connect(self.setLineEditColor)
        self.ui.tagCrossingRadioButton.pressed.connect(self.setLineEditColor)
        self.ui.tagCrossingDressedRadioButton.pressed.connect(self.setLineEditColor)

        self.ui.subsysNamesLineEdit.textChanged.connect(lambda x: self.setLineEditColor())
        self.ui.initialStateLineEdit.textChanged.connect(lambda x: self.setLineEditColor())
        self.ui.finalStateLineEdit.textChanged.connect(lambda x: self.setLineEditColor())

    def setNoTagMode(self):
        self.ui.tagBareGroupBox.setEnabled(False)
        self.ui.tagDressedGroupBox.setEnabled(False)

    def setDispersiveBareMode(self):
        self.ui.tagBareGroupBox.setEnabled(True)
        self.ui.tagDressedGroupBox.setEnabled(False)
        self.ui.subsysNamesLineEdit.editingFinished.emit()
        self.ui.initialStateLineEdit.editingFinished.emit()
        self.ui.finalStateLineEdit.editingFinished.emit()

    def setDispersiveDressedMode(self):
        self.ui.tagDressedGroupBox.setEnabled(True)
        self.ui.tagBareGroupBox.setEnabled(False)

    def setCrossingMode(self):
        self.ui.tagBareGroupBox.setEnabled(False)
        self.ui.tagDressedGroupBox.setEnabled(False)

    def setCrossingDressedMode(self):
        self.ui.tagBareGroupBox.setEnabled(False)
        self.ui.tagDressedGroupBox.setEnabled(True)

    def isValidInitialBare(self):
        if not self.ui.tagBareGroupBox.isEnabled():
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
        if not self.ui.tagBareGroupBox.isEnabled():
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
        if not self.isValid():
            return None

        tag = Tag()
        if self.ui.noTagRadioButton.isChecked():
            tag.tagType = NO_TAG
        elif self.ui.tagDispersiveBareRadioButton.isChecked():
            tag.tagType = DISPERSIVE_BARE
        elif self.ui.tagDispersiveDressedRadioButton.isChecked():
            tag.tagType = DISPERSIVE_DRESSED
        elif self.ui.tagCrossingRadioButton.isChecked():
            tag.tagType = CROSSING
        elif self.ui.tagCrossingDressedRadioButton.isChecked():
            tag.tagType = CROSSING_DRESSED

    def setLineEditColor(self, *args, **kwargs):
        if not self.ui.tagBareGroupBox.isEnabled() or self.ui.subsysNamesLineEdit.isValid():
            self.ui.subsysNamesLineEdit.setStyleSheet(self.defaultStyleLineEdit)
        else:
            self.ui.subsysNamesLineEdit.setStyleSheet("border: 3px solid red;")

        if not self.ui.tagBareGroupBox.isEnabled() or self.isValidInitialBare():
            self.ui.initialStateLineEdit.setStyleSheet(self.defaultStyleLineEdit)
        else:
            self.ui.initialStateLineEdit.setStyleSheet("border: 3px solid red;")

        if not self.ui.tagBareGroupBox.isEnabled() or self.isValidFinalBare():
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

    def setText(self, arg):
        self.previousStr = arg
        if not self.isValid():
            arg = self.previousStr
        super().setText(arg)

    def value(self):
        return self.text()

    def getSubsysNameList(self):
        if self.isValid():
            return [name.strip() for name in self.value().split(',')]
        return []

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
        regEx = QRegExp("^[0-9]+(, ?[0-9]+)*$")
        validator = QRegExpValidator(regEx)
        self.setValidator(validator)
        self.editingFinished.connect(self.processUpdate)
        self.previousStr = ""

    def setText(self, arg):
        if self.previousStr == "":
            self.previousStr = arg
        try:
            _ = float(arg)
        except ValueError:
            arg = self.previousStr
        else:
            self.previousStr = arg
        super().setText(arg)

    def value(self):
        return self.text()

    def getTuple(self):
        return eval(self.value() + ',')

    def processUpdate(self):
        if self.hasAcceptableInput():
            self.previousStr = self.text()
        else:
            self.setText(self.previousStr)

    def isValid(self):
        return self.hasAcceptableInput()
