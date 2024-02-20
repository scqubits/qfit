# calibration.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide6.QtWidgets import QMessageBox, QPushButton, QButtonGroup

from qfit.widgets.validated_line_edits import FloatLineEdit


from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from typing import Tuple, Dict, Any, List, Union, Literal

from qfit.models.quantum_model_parameters import HSParamSet
from qfit.models.data_structures import QMSweepParam, ParamAttr


class CalibrationView(QObject):
    caliStatusChangedByButtonClicked = Signal(object)
    dataEditingFinished = Signal(ParamAttr)

    def __init__(
        self,
        rawXVecCompNameList: List[str],
        rawYName: str,
        caliTableXRowNr: int,
        sweepParamSet: HSParamSet[QMSweepParam],
        rawLineEdits: Dict[Union[int, str], "CalibrationLineEdit"],
        mapLineEdits: Dict[Union[int, str], "CalibrationLineEdit"],
        calibrationButtons: Dict[Union[int, str], QPushButton],
    ):
        super().__init__()

        self.sweepParamSet = sweepParamSet
        self.caliTableXRowNr = caliTableXRowNr
        self.sweepParamParentName = list(self.sweepParamSet.keys())[0]
        self.sweepParamName = list(
            self.sweepParamSet[self.sweepParamParentName].keys()
        )[0]
        self.rawXVecCompNameList = rawXVecCompNameList
        self.rawYName = rawYName
        self.caliTableSet: Dict[str, Dict[str, "CalibrationLineEdit"]] = {
            "X0": {
                self.rawXVecCompNameList[0]: rawLineEdits[0],
                f"{self.sweepParamParentName}.{self.sweepParamName}": mapLineEdits[0],
            },
            "X1": {
                self.rawXVecCompNameList[0]: rawLineEdits[1],
                f"{self.sweepParamParentName}.{self.sweepParamName}": mapLineEdits[1],
            },
            "Y0": {
                self.rawYName: rawLineEdits["Y0"],
                "mappedY": mapLineEdits["Y0"],
            },
            "Y1": {
                self.rawYName: rawLineEdits["Y1"],
                "mappedY": mapLineEdits["Y1"],
            },
        }

        self.calibrationButtons = calibrationButtons
        self.caliButtonGroup = QButtonGroup()
        self.caliButtonGroup.setExclusive(True)

        # generalize to functions in the future
        self.rowIdxToButtonGroupId: Dict[Union[str, int], int] = (
            self._generateRowIdxToButtonGroupIdDict()
        )
        # generate the inverse dictionary
        self.buttonGroupIdToRowIdx: Dict[int, Union[str, int]] = {
            v: k for k, v in self.rowIdxToButtonGroupId.items()
        }
        self._addButtonsToGroup()

        # need to be removed in the future
        self.caliTableSet["X0"][self.rawXVecCompNameList[0]].setSibling(
            self.caliTableSet["X1"][self.rawXVecCompNameList[0]]
        )
        self.caliTableSet["Y0"][self.rawYName].setSibling(
            self.caliTableSet["Y1"][self.rawYName]
        )

    def _generateRowIdxToButtonGroupIdDict(self):
        """
        Generate the dictionary to translate the row index to the button group id.
        """
        translation_dict = {}
        for rowIdx in range(self.caliTableXRowNr):
            translation_dict[rowIdx] = rowIdx
        translation_dict["Y0"] = self.caliTableXRowNr
        translation_dict["Y1"] = self.caliTableXRowNr + 1
        return translation_dict

    def _addButtonsToGroup(self):
        for rowIdx, button in self.calibrationButtons.items():
            self.caliButtonGroup.addButton(
                button, id=self.rowIdxToButtonGroupId[rowIdx]
            )

    # def _highlightCaliButton(self, button: QPushButton, reset: bool = False):
    #     """Highlight the button by changing its stylesheet."""
    #     if reset:
    #         button.setStyleSheet("")
    #     else:
    #         button.setStyleSheet("QPushButton {background-color: #BE82FA}")

    # def _resetHighlightButtons(self):
    #     """Reset the highlighting of all calibration buttons."""
    #     for label in self.calibrationButtons:
    #         self._highlightCaliButton(self.calibrationButtons[label], reset=True)

    def setupEditingFinishedSignalEmit(self):
        """
        Equivalent to _signalProcessing()
        Signal emitting when the data in the line edits are changed.
        """
        for rowIdx in self.caliTableSet:
            for compName, lineEdit in self.caliTableSet[rowIdx].items():
                lineEdit.editingFinished.connect(
                    lambda rowIdx=rowIdx, compName=compName: self.dataEditingFinished.emit(
                        ParamAttr(rowIdx, compName, "value", lineEdit.text())
                    )
                )

    @Slot(ParamAttr)
    def setBoxValue(self, paramAttr: ParamAttr):
        rowIdx = paramAttr.parantName
        colName = paramAttr.name
        lineEdit: "CalibrationLineEdit" = self.caliTableSet[rowIdx][colName]
        lineEdit.setText(paramAttr.value)

    @Slot()
    def onCaliButtonClicked(self):
        """
        Internally determine the current calibration status, update the view and
        emit the signal for which calibration button is clicked to the controller.
        """
        buttonGroupCheckedId = self.caliButtonGroup.checkedId()
        # if no button is checked, then emit the signal to turn off the calibration
        if buttonGroupCheckedId == -1:
            self.caliStatusChangedByButtonClicked.emit(False)
            return
        # otherwise, emit the signal for the button clicked
        self.caliStatusChangedByButtonClicked.emit(
            self.buttonGroupIdToRowIdx[buttonGroupCheckedId]
        )

    @Slot()
    def uncheckAllCaliButtons(self):
        for button in self.caliButtonGroup.buttons():
            button.setChecked(False)

    def calibrationStatus(self):
        for calibrationLabel, button in self.calibrationButtons.items():
            if button.isChecked():
                return calibrationLabel
        return False

    @Slot(str, dict)
    def postCaliPointSelectedOnCanvas(self, rowIdx: str, data: Dict[str, float]):
        """
        CALIBRATION VIEW
        """
        # update the raw line edits by the value of the clicked point
        for rawXVecCompName in self.rawXVecCompNameList:
            self.caliTableSet[rowIdx][rawXVecCompName].setText(
                str(data[rawXVecCompName])
            )
            self.caliTableSet[rowIdx][rawXVecCompName].home(False)
        # highlight the map line edit
        self.caliTableSet[rowIdx][
            f"{self.sweepParamParentName}.{self.sweepParamName}"
        ].selectAll()
        self.caliTableSet[rowIdx][
            f"{self.sweepParamName}.{self.sweepParamName}"
        ].setFocus()
        self.uncheckAllCaliButtons()

    #     self.msg = None

    # def calibrationErrorMsg(self):
    #     if self.msg is None:
    #         self.msg = QMessageBox()
    #         self.msg.setIcon(QMessageBox.Warning)
    #         self.msg.setText("Calibration Error")
    #         self.msg.setInformativeText(
    #             "The two coordinate components used for calibration must not be identical."
    #         )
    #         self.msg.setWindowTitle("Error")
    #         self.msg.exec_()
    #         self.msg = None

    # obsolete
    # def calibrationPoints(self):
    #     rVec1 = (
    #         self.rawLineEdits["CALI_X1"].value(),
    #         self.rawLineEdits["CALI_Y1"].value(),
    #     )
    #     rVec2 = (
    #         self.rawLineEdits["CALI_X2"].value(),
    #         self.rawLineEdits["CALI_Y2"].value(),
    #     )
    #     mVec1 = (
    #         self.mapLineEdits["CALI_X1"].value(),
    #         self.mapLineEdits["CALI_Y1"].value(),
    #     )
    #     mVec2 = (
    #         self.mapLineEdits["CALI_X2"].value(),
    #         self.mapLineEdits["CALI_Y2"].value(),
    #     )
    #     return rVec1, rVec2, mVec1, mVec2

    # obsolete
    # def setView(self, rawVec1, rawVec2, mapVec1, mapVec2):
    #     self.rawLineEdits["CALI_X1"].setText(str(rawVec1[0]))
    #     self.rawLineEdits["CALI_X2"].setText(str(rawVec2[0]))
    #     self.rawLineEdits["CALI_Y1"].setText(str(rawVec1[1]))
    #     self.rawLineEdits["CALI_Y2"].setText(str(rawVec2[1]))
    #     self.mapLineEdits["CALI_X1"].setText(str(mapVec1[0]))
    #     self.mapLineEdits["CALI_X2"].setText(str(mapVec2[0]))
    #     self.mapLineEdits["CALI_Y1"].setText(str(mapVec1[1]))
    #     self.mapLineEdits["CALI_Y2"].setText(str(mapVec2[1]))


class CalibrationLineEdit(FloatLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.editingFinished.connect(self.processUpdate)
        self.previousStr = None
        self.siblingLineEdit = None

    def setSibling(self, siblingLineEdit):
        self.siblingLineEdit = siblingLineEdit

    def siblingValueDifferent(self):
        if not self.siblingLineEdit:
            return True
        return self.value() != self.siblingLineEdit.value()

    def focusOutEvent(self, arg):
        result = super().focusOutEvent(arg)
        # self.processUpdate()
        return result

    def setText(self, arg):
        if self.previousStr is None:
            self.previousStr = arg
        try:
            _ = float(arg)
        except ValueError:
            arg = self.previousStr
        else:
            self.previousStr = arg
        super().setText(arg)

    def value(self):
        return float(self.text())

    # def processUpdate(self):
    #     if self.hasAcceptableInput() and self.siblingValueDifferent():
    #         self.previousStr = self.text()
    #     else:
    #         self.setText(self.previousStr)

    ###########################################################################
