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
    _virtualButton: QPushButton

    def __init__(
        self,
        rawLineEdits: Dict[str, "CalibrationLineEdit"],
        mapLineEdits: Dict[str, "CalibrationLineEdit"],
        calibrationButtons: Dict[str, QPushButton],
    ):
        """
        In the future, all the line edits and buttons should be generated
        dynamically based on the number of calibration rows.
        """
        super().__init__()

        self.rawLineEdits = rawLineEdits
        self.mapLineEdits = mapLineEdits
        self.calibrationButtons = calibrationButtons
        self._previousCheckedButton = None

    def dynamicalInit(
        self,
        rawXVecNameList: List[str],
        rawYName: str,
        caliTableXRowNr: int,
        sweepParamSet: HSParamSet[QMSweepParam],
    ):
        print("dynamical init called for calibration view")
        self.sweepParamSet = sweepParamSet
        self.caliTableXRowNr = caliTableXRowNr
        self.sweepParamParentName = list(self.sweepParamSet.keys())[0]
        self.sweepParamName = list(
            self.sweepParamSet[self.sweepParamParentName].keys()
        )[0]
        self.rawXVecNameList = rawXVecNameList
        self.rawYName = rawYName

        # generate the calibration table set
        self._generateCaliTableSet()

        # need to be removed in the future
        self.caliTableSet["X0"][self.rawXVecNameList[0]].setSibling(
            self.caliTableSet["X1"][self.rawXVecNameList[0]]
        )
        self.caliTableSet["Y0"][self.rawYName].setSibling(
            self.caliTableSet["Y1"][self.rawYName]
        )

        # connects
        self.setupEditingFinishedSignalEmit()
        for Idx, button in self.calibrationButtons.items():
            button.clicked.connect(lambda Idx=Idx: self.onCaliButtonClicked(Idx))
            print(f"connect button {Idx} to onCaliButtonClicked")

    def _generateCaliTableSet(self):
        self.caliTableSet: Dict[str, Dict[str, "CalibrationLineEdit"]] = {
            "X0": {
                self.rawXVecNameList[0]: self.rawLineEdits["X0"],
                f"{self.sweepParamParentName}.{self.sweepParamName}": self.mapLineEdits[
                    "X0"
                ],
            },
            "X1": {
                self.rawXVecNameList[0]: self.rawLineEdits["X1"],
                f"{self.sweepParamParentName}.{self.sweepParamName}": self.mapLineEdits[
                    "X1"
                ],
            },
            "Y0": {
                self.rawYName: self.rawLineEdits["Y0"],
                "mappedY": self.mapLineEdits["Y0"],
            },
            "Y1": {
                self.rawYName: self.rawLineEdits["Y1"],
                "mappedY": self.mapLineEdits["Y1"],
            },
        }

    def _generateRowIdxToButtonGroupIdDict(self):
        """
        Maintain a dictionary to translate the row index to the button group id.

        generalize to functions in the future

        """
        self.rowIdxToButtonGroupId: Dict[str, int] = {}
        for rowIdx in range(self.caliTableXRowNr):
            self.rowIdxToButtonGroupId[f"X{rowIdx}"] = rowIdx
        self.rowIdxToButtonGroupId["Y0"] = self.caliTableXRowNr
        self.rowIdxToButtonGroupId["Y1"] = self.caliTableXRowNr + 1

        self.buttonGroupIdToRowIdx: Dict[int, Union[str, int]] = {
            v: k for k, v in self.rowIdxToButtonGroupId.items()
        }

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

    @Slot(str)
    def onCaliButtonClicked(self, buttonIdx: str):
        """
        Internally determine the current calibration status, update the view and
        emit the signal for which calibration button is clicked to the controller.
        """
        # if the pressed button is the one that is already checked, then temporarily
        # set the exclusive mode off and uncheck the button, then turn on the exclusive
        # mode again
        print("function called")
        clickedButton = self.sender()
        if clickedButton is self._previousCheckedButton:
            if clickedButton is not None:
                clickedButton.setChecked(False)
                self._previousCheckedButton = None
                self.caliStatusChangedByButtonClicked.emit(False)
                return
            else:
                return
        else:
            for button in self.calibrationButtons.values():
                button.setChecked(False)
            clickedButton.setChecked(True)
            self._previousCheckedButton = clickedButton
            print(f"{self._previousCheckedButton}")
            self.caliStatusChangedByButtonClicked.emit(buttonIdx)

    @Slot()
    def uncheckAllCaliButtons(self):
        for button in self.calibrationButtons.values():
            button.setChecked(False)
        self._previousCheckedButton = None

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
        for rawXVecCompName in self.rawXVecNameList:
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