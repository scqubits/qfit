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


from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QButtonGroup,
    QWidget,
    QFrame,
    QLabel,
    QSizePolicy,
)

from qfit.widgets.validated_line_edits import FloatLineEdit


from PySide6.QtCore import QObject, Signal, Slot, Qt, QMetaMethod

from typing import Tuple, Dict, Any, List, Union, Literal, Type

from qfit.models.parameter_set import ParamSet, SweepParamSet
from qfit.models.data_structures import QMSweepParam, ParamAttr

from qfit.widgets.custom_table import FoldableTable, CollectionType, WidgetCollection
from qfit.utils.helpers import modifyStyleSheet


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
    clearDataSource = Signal(ParamAttr)
    caliViewRawVecUpdatedForSwapXY = Signal()
    _virtualButton: QPushButton

    sweepParamSet: ParamSet[QMSweepParam]
    caliTableXRowNr: int
    sweepParamParentNames: List[str]
    sweepParamNames: List[str]
    rawXVecNameList: List[str]
    rawYName: str
    lineEditSet: Dict[str, Dict[str, "CalibrationLineEdit"]]
    XDataSourceSet: Dict[str, Dict[str, QLabel]]
    rowIdxToButtonGroupId: Dict[str, int]
    buttonGroupIdToRowIdx: Dict[int, str]

    rawYLineEdits: Dict[str, "CalibrationLineEdit"]
    mapYLineEdits: Dict[str, "CalibrationLineEdit"]
    caliYButtons: Dict[str, QPushButton]

    rawXLineEdits: Dict[str, "CalibrationLineEdit"]
    mapXLineEdits: Dict[str, "CalibrationLineEdit"]
    caliXButtons: Dict[str, QPushButton]

    def __init__(
        self,
        parent: QObject,
        caliXScrollAreaWidget: QWidget,
        caliXFrame: QFrame,
        rawYLineEdits: Dict[str, "CalibrationLineEdit"],
        mapYLineEdits: Dict[str, "CalibrationLineEdit"],
        caliYButtons: Dict[str, QPushButton],
    ):
        """
        Note: In the future, all the line edits and buttons should be generated
        dynamically based on the number of calibration rows.
        """
        super().__init__(parent)

        self.rawYLineEdits = rawYLineEdits
        self.mapYLineEdits = mapYLineEdits
        self.caliYButtons = caliYButtons
        self.lineEditSet = {}
        self.XDataSourceSet = {}
        self._previousCheckedButtonIdx = None
        self.caliXScrollAreaWidget = caliXScrollAreaWidget
        self.caliXFrame = caliXFrame
        self.caliXScrollLayout = self.caliXScrollAreaWidget.layout()
        self.caliXScrollLayout.setAlignment(Qt.AlignTop)

    def replaceHS(self, sweepParamSet: SweepParamSet):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It updates the
        HilbertSpace object.

        Parameters
        ----------
        sweepParamSet: SweepParamSet
            The sweep parameter set for the HilbertSpace.
        """
        self.sweepParamSet = sweepParamSet
        self.sweepParamParentNames: List[str] = []
        self.sweepParamNames: List[str] = []
        self.sweepParamCombinedNames: List[str] = []
        # create a list for all sweep parameters and their parent names
        for parentName, sweepParamDict in self.sweepParamSet.items():
            for sweepParamName, sweepParam in sweepParamDict.items():
                self.sweepParamParentNames.append(parentName)
                self.sweepParamNames.append(sweepParamName)
                self.sweepParamCombinedNames.append(
                    f"{sweepParamName}<br>({parentName})"
                )

    def replaceMeasData(
        self,
        rawXVecNameList: List[str],
        rawYName: str,
        caliTableXRowNr: int,
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It replaces the figure
        names, determine the calibration mode, and reinitialize
        the calibration table entries.

        Note: For the moment, when the measurement data is updated, all of the
        properties will be re-initialized. We also assume that this method is
        called after the dynamicalInit method, so the sweep parameters are already
        initialized.

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
        """
        self.caliTableXRowNr = caliTableXRowNr
        self.rawXVecNameList = rawXVecNameList
        self.rawYName = rawYName

    def dynamicalInit(
        self,
    ):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method.
        """
        # generate the X calibration table
        self.XParamItems = self._generateXParamItems()
        self.caliXTable = FoldableTable(
            self.XParamItems,
            paramNumPerRow=1,
            groupNames=["X"],
        )
        self.caliXTable.setCheckable(False)
        self.caliXTable.setChecked(False)

        # insert parameters
        for rowIdx in range(self.caliTableXRowNr):
            self.caliXTable.insertParams("X", f"X{rowIdx+1}")
        # sizepolicy = self.caliXTable.sizePolicy()
        # sizepolicy.setVerticalPolicy(QSizePolicy.Fixed)
        # self.caliXTable.setSizePolicy(sizepolicy)

        # add the table to the scroll area
        self.caliXScrollLayout.addWidget(self.caliXTable)

        # temporary fix for the height of the row - after addWidget the
        # row height were reset to 30 - don't know why
        self.caliXTable.setHeightOfRow()
        # hide the group line
        self.caliXTable.hideGroupLine()
        # adjust size of the scroll area to the content
        self.caliXScrollAreaWidget.setMinimumHeight(self.caliXTable.sizeHint().height())

        # set calibration button group
        self.caliButtonGroup = QButtonGroup()
        self._generateRowIdxToButtonGroupIdDict()
        # identify the buttons in the x calibration table
        for _, caliXGroup in self.caliXTable.items():
            for XRowIdx, XParamItems in caliXGroup.items():
                self.caliButtonGroup.addButton(
                    XParamItems.extractRawPushButton,
                    self.rowIdxToButtonGroupId[XRowIdx],
                )
                # set stylesheet for each button
                XParamItems.extractRawPushButton.setStyleSheet(
                    """
                    QPushButton {
                    background-color: #4B4B4B;
                    border-radius: 5px;	
                    icon: url(:/icons/svg/target.svg);
                    icon-size: 16px;
                    }\n
                    QPushButton:pressed {
                    background-color: #363636;
                    icon: url(:/icons/svg/target-pressed.svg)
                    }\n
                    QPushButton:checked {
                    background-color: #5C3F83;
                    }"""
                )
                # set push button size
                XParamItems.extractRawPushButton.setMinimumSize(28, 28)
                XParamItems.extractRawPushButton.setMaximumSize(28, 28)
                # set size policy to fixed
                sizePolicy = XParamItems.extractRawPushButton.sizePolicy()
                sizePolicy.setHorizontalPolicy(QSizePolicy.Fixed)
                sizePolicy.setVerticalPolicy(QSizePolicy.Fixed)
                # set checkable and checked
                XParamItems.extractRawPushButton.setCheckable(True)
                XParamItems.extractRawPushButton.setChecked(False)
        for YRowIdx, button in self.caliYButtons.items():
            self.caliButtonGroup.addButton(button, self.rowIdxToButtonGroupId[YRowIdx])
        self.caliButtonGroup.setExclusive(False)

        # generate a set for all line edits
        self._generateLineEditSet()
        self._generateXDataSourceSet()

        # connects
        self._setupEditingFinishedSignalEmit()
        self.caliButtonGroup.idClicked.connect(self.onCaliButtonClicked)

    def _generateXParamItems(self) -> Type[WidgetCollection]:
        """
        Generate the X parameter type for the calibration table, used for the Foldable table.
        """

        # subclass WidgetCollection
        class XParamItems(WidgetCollection):
            rawXVecNameList = self.rawXVecNameList
            sweepParamCombinedNames = self.sweepParamCombinedNames
            columns = ["EXTRACT<br>RAW"]
            for rawXVecName in rawXVecNameList:
                columns.append(rawXVecName)
            for sweepParamName in sweepParamCombinedNames:
                columns.append(sweepParamName)
            columns.append("DATA<br>SOURCE")
            # column background colors
            columnBackgroundColors: Dict[str, None | str] = {
                "EXTRACT<br>RAW": None,
            }

            for idx, rawXVecName in enumerate(
                rawXVecNameList + sweepParamCombinedNames
            ):
                columnBackgroundColors[rawXVecName] = (
                    "#292929" if idx % 2 == 0 else "#363636"
                )
            columnBackgroundColors["DATA<br>SOURCE"] = None
            # column widths
            columnWidths = {
                "EXTRACT<br>RAW": 100,
                "DATA<br>SOURCE": 100,
            }
            for rawXVecName in rawXVecNameList:
                columnWidths[rawXVecName] = 100
            for sweepParamName in sweepParamCombinedNames:
                columnWidths[sweepParamName] = 100
            columnCount = len(columns)

            def __init__(self, parent, name: str):
                super().__init__(parent, name)
                self.extractRawPushButton = QPushButton()
                # set style sheet
                self.extractRawPushButton.setStyleSheet(
                    """
                    QPushButton {
                    background-color: #4B4B4B;
                    border-radius: 5px;	
                    icon: url(:/icons/svg/target.svg)
                    }\n
                    QPushButton:pressed {
                    background-color: #363636;
                    icon: url(:/icons/svg/target-pressed.svg)
                    }\n
                    QPushButton:checked {
                    background-color: #5C3F83;
                    }"""
                )

                self.dataSourceLabel = QLabel()
                self.entriesDict = {
                    "EXTRACT<br>RAW": self.extractRawPushButton,
                    "DATA<br>SOURCE": self.dataSourceLabel,
                }
                for rawXVecName in self.rawXVecNameList:
                    self.entriesDict[rawXVecName] = CalibrationLineEdit()
                for sweepParamName in self.sweepParamCombinedNames:
                    self.entriesDict[sweepParamName] = CalibrationLineEdit()

                # loop over the dict to set the style sheet
                for key, value in self.entriesDict.items():
                    modifyStyleSheet(value, "color", "white")
                    # change the border color of the line edit
                    if isinstance(value, FloatLineEdit):
                        modifyStyleSheet(value, "border", "1px solid #5F5F5F")
                    value.setMinimumSize(45, 20)
                    if self.columnBackgroundColors[key] is not None:
                        modifyStyleSheet(
                            value, "background-color", self.columnBackgroundColors[key]
                        )
                    self.addWidget(key, value)

        return XParamItems

    def _generateLineEditSet(self):
        if self.lineEditSet != {}:
            for rowIdx in self.lineEditSet:
                for compName, lineEdit in self.lineEditSet[rowIdx].items():
                    lineEdit.editingFinished.disconnect()
                    lineEdit.deleteLater()

            self.lineEditSet.clear()

        # for each X row, create a dict for raw and mapped vectors to line edits
        for XRowIdx in range(self.caliTableXRowNr):
            self.lineEditSet[f"X{XRowIdx+1}"] = {}
            for rawXVecName in self.rawXVecNameList:
                self.lineEditSet[f"X{XRowIdx+1}"][rawXVecName] = self.caliXTable["X"][
                    f"X{XRowIdx+1}"
                ].entriesDict[rawXVecName]
            for sweepParamCombinedName in self.sweepParamCombinedNames:
                self.lineEditSet[f"X{XRowIdx+1}"][sweepParamCombinedName] = (
                    self.caliXTable["X"][f"X{XRowIdx+1}"].entriesDict[
                        sweepParamCombinedName
                    ]
                )
        self.lineEditSet["Y1"] = {
            self.rawYName: self.rawYLineEdits["Y1"],
            "mappedY": self.mapYLineEdits["Y1"],
        }
        self.lineEditSet["Y2"] = {
            self.rawYName: self.rawYLineEdits["Y2"],
            "mappedY": self.mapYLineEdits["Y2"],
        }

    def _generateXDataSourceSet(self):
        if self.XDataSourceSet != {}:
            for XRowIdx in range(self.caliTableXRowNr):
                self.XDataSourceSet[f"X{XRowIdx+1}"]["DATA<br>SOURCE"].setText("")
            self.XDataSourceSet.clear()
        for XRowIdx in range(self.caliTableXRowNr):
            self.XDataSourceSet[f"X{XRowIdx+1}"] = {}
            self.XDataSourceSet[f"X{XRowIdx+1}"]["DATA<br>SOURCE"] = self.caliXTable[
                "X"
            ][f"X{XRowIdx+1}"].entriesDict["DATA<br>SOURCE"]

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
        for rowIdx in self.lineEditSet:
            for compName, lineEdit in self.lineEditSet[rowIdx].items():
                # disconnect first if there is any connection
                editingFinishedSignal = QMetaMethod.fromSignal(lineEdit.editingFinished)
                if lineEdit.isSignalConnected(editingFinishedSignal):
                    lineEdit.editingFinished.disconnect()
                
                # note: inclusion of lineEdit in the lambda function is necessary, otherwise
                # the last lineEdit will be used for all the lambda functions
                # The lambda function in the code doesn't capture the value of rowIdx and
                # compName at the time it's defined, but rather when it's called.
                lineEdit.editingFinished.connect(
                    lambda rowIdx=rowIdx, compName=compName, lineEdit=lineEdit: self.dataEditingFinished.emit(
                        ParamAttr(rowIdx, compName, "value", lineEdit.text())
                    )
                )
            # in addition, if the raw X is modified by the user, then the data source
            # should be cleared
            if rowIdx[0] == "X":
                for compName in self.rawXVecNameList:
                    lineEdit = self.lineEditSet[rowIdx][compName]
                    self.XDataSourceSet[rowIdx]["DATA<br>SOURCE"].setText("")
                    lineEdit.editingFinished.connect(
                        lambda rowIdx=rowIdx: self.clearDataSource.emit(
                            ParamAttr(rowIdx, "DATA<br>SOURCE", "value", "")
                        )
                    )

    @Slot(ParamAttr)
    def setBoxValue(self, paramAttr: ParamAttr):
        """
        Update the view when the model emits the signal to update the view.
        """

        rowIdx = paramAttr.parentName
        colName = paramAttr.name
        # if dataSource, the widget is the label in x-table
        if paramAttr.name == "DATA<br>SOURCE":
            if rowIdx[0] == "X":
                widget: QObject = self.XDataSourceSet[rowIdx][colName]
            else:
                return
        else:
            widget: QObject = self.lineEditSet[rowIdx][colName]
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
            self.caliButtonGroup.button(buttonGroupIdx).setChecked(False)
            self._previousCheckedButtonIdx = None
            self.caliStatusChangedByButtonClicked.emit(False)
            return
        else:
            for allButtonIdx in self.buttonGroupIdToRowIdx.keys():
                self.caliButtonGroup.button(allButtonIdx).setChecked(False)
            self.caliButtonGroup.button(buttonGroupIdx).setChecked(True)
            self._previousCheckedButtonIdx = buttonIdx
            self.caliStatusChangedByButtonClicked.emit(buttonIdx)

    @Slot()
    def uncheckAllCaliButtons(self):
        for button in self.caliButtonGroup.buttons():
            button.setChecked(False)
        self._previousCheckedButtonIdx = None

    def calibrationStatus(self):
        for calibrationLabel, button in self.caliYButtons.items():
            if button.isChecked():
                return calibrationLabel
        for calibrationLabel, button in self.caliXButtons.items():
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
                self.lineEditSet[rowIdx][rawXVecCompName].home(False)
            colName = f"{self.sweepParamNames[0]}<br>({self.sweepParamParentNames[0]})"
        # if y axis is calibrated, update the raw line edits by the value of the clicked point
        elif rowIdx[0] == "Y":
            self.lineEditSet[rowIdx][self.rawYName].home(False)
            colName = "mappedY"

        # focus on the line edit so that the user can type in the value
        self.lineEditSet[rowIdx][colName].selectAll()
        self.lineEditSet[rowIdx][colName].setFocus()
        self.uncheckAllCaliButtons()

    @Slot()
    def swapXYAfterModelChanges(self):
        """
        To be phased out in the future; not the best code design
        """
        self.rawXVecNameList, self.rawYName = [self.rawYName], self.rawXVecNameList[0]
        # regenerate calibration table set
        self._generateLineEditSet()
        self._generateXDataSourceSet()
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
