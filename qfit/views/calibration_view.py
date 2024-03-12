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

from qfit.models.parameter_set import ParamSet
from qfit.models.data_structures import QMSweepParam, ParamAttr


class CalibrationView(QObject):
    """
    The view for the calibration table, manipulating the raw vector and 
    the mapped vector. It receives the data from the user typing and the
    clicking on the canvas, and communicates with the corresponding model.

    Parameters
    ----------
    rawLineEdits : Dict[str, "CalibrationLineEdit"]
        The line edits for the raw vectors.
    mapLineEdits : Dict[str, "CalibrationLineEdit"]
        The line edits for the mapped vectors.
    calibrationButtons : Dict[str, QPushButton]
        The buttons for the calibration status.
    """
    caliStatusChangedByButtonClicked = Signal(object)
    dataEditingFinished = Signal(ParamAttr)
    caliViewRawVecUpdatedForSwapXY = Signal()
    _virtualButton: QPushButton

    sweepParamSet: ParamSet[QMSweepParam]
    caliTableXRowNr: int
    sweepParamParentName: str
    sweepParamName: str
    rawXVecNameList: List[str]
    rawYName: str
    caliTableSet: Dict[str, Dict[str, "CalibrationLineEdit"]]
    rowIdxToButtonGroupId: Dict[str, int]
    buttonGroupIdToRowIdx: Dict[int, str]

    def __init__(
        self,
        parent: QObject,
        rawLineEdits: Dict[str, "CalibrationLineEdit"],
        mapLineEdits: Dict[str, "CalibrationLineEdit"],
        calibrationButtons: Dict[str, QPushButton],
    ):
        """
        Note: In the future, all the line edits and buttons should be generated
        dynamically based on the number of calibration rows.
        """
        super().__init__(parent)

        self.rawLineEdits = rawLineEdits
        self.mapLineEdits = mapLineEdits
        self.calibrationButtons = calibrationButtons
        self.caliTableSet = {}
        self._previousCheckedButtonIdx = None

    def dynamicalInit(
        self,
        rawXVecNameList: List[str],
        rawYName: str,
        caliTableXRowNr: int,
        sweepParamSet: ParamSet[QMSweepParam],
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the calibration view will reinitialized by this method.

        Parameters
        ----------
        rawXVecNameList : List[str]
            The names of the raw vector components, from the measurement datas'
            x axis.
        rawYName : str
            The name of the raw vector component, from the measurement datas'
            y axis.
        caliTableXRowNr : int
            The number of rows in the calibration table. It is determined in
            the calibration model based on the number of raw vector components,
            number of figures and the number of sweep parameters.
        sweepParamSet : ParamSet[QMSweepParam]
            The sweep parameters for the calibration. 
        """
        self.sweepParamSet = sweepParamSet
        self.caliTableXRowNr = caliTableXRowNr
        self.sweepParamParentName = list(self.sweepParamSet.keys())[0]
        self.sweepParamName = list(
            self.sweepParamSet[self.sweepParamParentName].keys()
        )[0]
        self.rawXVecNameList = rawXVecNameList
        self.rawYName = rawYName

        self.caliButtonGroup = QButtonGroup()
        self._generateRowIdxToButtonGroupIdDict()
        for Idx, button in self.calibrationButtons.items():
            self.caliButtonGroup.addButton(button, self.rowIdxToButtonGroupId[Idx])
        self.caliButtonGroup.setExclusive(False)

        # generate the calibration table set
        self._generateCaliTableSet()

        # need to be removed in the future
        self.caliTableSet["X1"][self.rawXVecNameList[0]].setSibling(
            self.caliTableSet["X2"][self.rawXVecNameList[0]]
        )
        self.caliTableSet["Y1"][self.rawYName].setSibling(
            self.caliTableSet["Y2"][self.rawYName]
        )

        # connects
        self._setupEditingFinishedSignalEmit()
        self.caliButtonGroup.idClicked.connect(self.onCaliButtonClicked)

    def _generateCaliTableSet(self):
        """
        Generate the calibration table set, which is a dictionary of dictionaries.

        In the future, the line edits and buttons should be generated dynamically
        based on the number of raw and mapped vector components.
        """
        if self.caliTableSet != {}:
            self.caliTableSet.clear()
        self.caliTableSet: Dict[str, Dict[str, "CalibrationLineEdit"]] = {
            "X1": {
                self.rawXVecNameList[0]: self.rawLineEdits["X1"],
                f"{self.sweepParamParentName}.{self.sweepParamName}": self.mapLineEdits[
                    "X1"
                ],
            },
            "X2": {
                self.rawXVecNameList[0]: self.rawLineEdits["X2"],
                f"{self.sweepParamParentName}.{self.sweepParamName}": self.mapLineEdits[
                    "X2"
                ],
            },
            "Y1": {
                self.rawYName: self.rawLineEdits["Y1"],
                "mappedY": self.mapLineEdits["Y1"],
            },
            "Y2": {
                self.rawYName: self.rawLineEdits["Y2"],
                "mappedY": self.mapLineEdits["Y2"],
            },
        }

    def _generateRowIdxToButtonGroupIdDict(self):
        """
        Maintain a dictionary to translate the row index to the button group id.

        Note: we should generalize to functions in the future.
        """
        self.rowIdxToButtonGroupId: Dict[str, int] = {}
        for rowIdx in range(self.caliTableXRowNr):
            self.rowIdxToButtonGroupId[f"X{rowIdx+1}"] = rowIdx
        self.rowIdxToButtonGroupId["Y1"] = self.caliTableXRowNr
        self.rowIdxToButtonGroupId["Y2"] = self.caliTableXRowNr + 1

        self.buttonGroupIdToRowIdx: Dict[int, str] = {
            v: k for k, v in self.rowIdxToButtonGroupId.items()
        }

    def _setupEditingFinishedSignalEmit(self):
        """
        Equivalent to _signalProcessing() in other views.
        Signal emitting when the data in the line edits are changed.
        """
        for rowIdx in self.caliTableSet:
            for compName, lineEdit in self.caliTableSet[rowIdx].items():
                # disconnect first if there is any connection
                try:
                    lineEdit.editingFinished.disconnect()
                except RuntimeError:
                    # if the line edit is not connected to any signal, then it will raise
                    # a RuntimeError, and we can just pass it.
                    pass
                # note: inclusion of lineEdit in the lambda function is necessary, otherwise
                # the last lineEdit will be used for all the lambda functions
                # The lambda function in the code doesn't capture the value of rowIdx and
                # compName at the time it's defined, but rather when it's called.
                lineEdit.editingFinished.connect(
                    lambda rowIdx=rowIdx, compName=compName, lineEdit=lineEdit: self.dataEditingFinished.emit(
                        ParamAttr(rowIdx, compName, "value", lineEdit.text())
                    )
                )

    @Slot(ParamAttr)
    def setBoxValue(self, paramAttr: ParamAttr):
        """
        Update the view when the model emits the signal to update the view.
        """
        # if pointPairSource, no such view available currently
        if paramAttr.name == "pointPairSource":
            return
        rowIdx = paramAttr.parentName
        colName = paramAttr.name
        widget: QObject = self.caliTableSet[rowIdx][colName]
        widget.setText(paramAttr.value)

    @Slot(int)
    def onCaliButtonClicked(self, buttonGroupIdx: int):
        """
        Internally determine the current calibration status, update the view and
        emit the signal for which calibration button is clicked to the controller.
        """
        # if the pressed button is the one that is already checked, then temporarily
        # set the exclusive mode off and uncheck the button, then turn on the exclusive
        # mode again
        buttonIdx = self.buttonGroupIdToRowIdx[buttonGroupIdx]
        if buttonIdx is self._previousCheckedButtonIdx:
            self.calibrationButtons[buttonIdx].setChecked(False)
            self._previousCheckedButtonIdx = None
            self.caliStatusChangedByButtonClicked.emit(False)
            return
        else:
            for button in self.calibrationButtons.values():
                button.setChecked(False)
            self.calibrationButtons[buttonIdx].setChecked(True)
            self._previousCheckedButtonIdx = buttonIdx
            self.caliStatusChangedByButtonClicked.emit(buttonIdx)

    @Slot()
    def uncheckAllCaliButtons(self):
        for button in self.calibrationButtons.values():
            button.setChecked(False)
        self._previousCheckedButtonIdx = None

    def calibrationStatus(self):
        for calibrationLabel, button in self.calibrationButtons.items():
            if button.isChecked():
                return calibrationLabel
        return False

    @Slot(str, dict)
    def postCaliPointSelectedOnCanvas(self, rowIdx: str, data: Dict[str, float]):
        """
        After the user clicking on the canvas, and model processing the data,
        update the view:
            - Uncheck the calibration buttons
            - Automatically focus on the line edit for the user to type in 
            the mapped value 
        
        Note that the view data is updated through setBoxValue signal. 
        """
        # if x axis is calibrated, update the raw line edits by the value of the clicked point
        if rowIdx[0] == "X":
            for rawXVecCompName in self.rawXVecNameList:
                self.caliTableSet[rowIdx][rawXVecCompName].home(False)
            colName = f"{self.sweepParamParentName}.{self.sweepParamName}"
        # if y axis is calibrated, update the raw line edits by the value of the clicked point
        elif rowIdx[0] == "Y":
            self.caliTableSet[rowIdx][self.rawYName].home(False)
            colName = "mappedY"

        # focus on the line edit so that the user can type in the value
        self.caliTableSet[rowIdx][colName].selectAll()
        self.caliTableSet[rowIdx][colName].setFocus()
        self.uncheckAllCaliButtons()

    @Slot()
    def swapXYAfterModelChanges(self):
        """
        To be phased out in the future; not the best code design
        """
        self.rawXVecNameList, self.rawYName = [self.rawYName], self.rawXVecNameList[0]
        # regenerate calibration table set
        self._generateCaliTableSet()
        # re setup the signal emitting
        self._setupEditingFinishedSignalEmit()
        self.caliViewRawVecUpdatedForSwapXY.emit()

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


class CalibrationLineEdit(FloatLineEdit):
    """
    A line edit that accepts a float as input, providing validation and
    warning on invalid input.
    """
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
