from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSizePolicy, 
    QPushButton, QLineEdit, QComboBox,
)

from qfit.widgets.foldable_table import (
    FoldableTable,
    FittingParameterItems,
)
from qfit.widgets.validated_line_edits import FloatLineEdit
from qfit.models.data_structures import ParamAttr
from qfit.utils.helpers import clearChildren

from typing import Dict, List, Any


class FitParamView(QObject):
    HSEditingFinished = Signal(ParamAttr)
    CaliEditingFinished = Signal(ParamAttr)

    def __init__(
        self,
        parent: QObject,
        fitScrollAreaWidget: QWidget,
    ):
        super().__init__(parent)

        self.fitScrollWidget = fitScrollAreaWidget
        self._configureLayout()

        # A list to tell whether the parameter belongs to a hilbertspace
        # or a calibration model.
        self.HSNames: List[str] = []

    def _configureLayout(self):
        fitScrollArea = self.fitScrollWidget.parent()
        fitScrollArea.setStyleSheet(f"background-color: rgb(33, 33, 33);")
        self.fitScrollWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def fitTableInserts(
        self,
        HSParamNames: Dict[str, List[str]],
        caliParamNames: Dict[str, List[str]],
        removeExisting: bool = True
    ):
        """
        Insert a set of tables for the fitting parameters
        """

        self.HSNames = list(HSParamNames.keys())
        paramNameDict = HSParamNames | caliParamNames 

        # remove the existing widgets, if we somehow want to rebuild the sliders
        if removeExisting:
            clearChildren(self.fitScrollWidget)
            
        if self.fitScrollWidget.layout() is None:
            fitScrollLayout = QVBoxLayout(self.fitScrollWidget)
        else:
            fitScrollLayout = self.fitScrollWidget.layout()


        # create an empty table with just group names
        self.fitTableSet = FoldableTable(
            FittingParameterItems,
            paramNumPerRow=1,
            groupNames=list(paramNameDict.keys()),
        )

        # insert parameters
        for group_name, para_list in paramNameDict.items():
            for name in para_list:
                self.fitTableSet.insertParams(group_name, name)

        fitScrollLayout.addWidget(self.fitTableSet)

        self._signalProcessing()

    # Signal processing ================================================
    def _signalProcessing(self):
        for groupName, group in self.fitTableSet.items():
            for name, item in group.items():
                item: FittingParameterItems

                if groupName in self.HSNames:
                    signal = self.HSEditingFinished
                else:
                    signal = self.CaliEditingFinished

                item.minValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signal=signal: 
                    signal.emit(
                        ParamAttr(groupName, name, "min", item.minValue.text())
                    )
                )
                item.maxValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signal=signal: 
                    signal.emit(
                        ParamAttr(groupName, name, "max", item.maxValue.text())
                    )
                )
                item.fixCheckbox.toggled.connect(
                    lambda value, name=name, groupName=groupName, signal=signal: 
                    signal.emit(
                        ParamAttr(groupName, name, "isFixed", value)
                    )
                )
                item.initialValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signal=signal: 
                    signal.emit(
                        ParamAttr(groupName, name, "initValue", item.initialValue.text())
                    )
                )

    # Setters ==========================================================
    @Slot(ParamAttr)
    def setBoxValue(self, paramAttr: ParamAttr):
        item: FittingParameterItems = self.fitTableSet[paramAttr.parentName][paramAttr.name]
        if paramAttr.attr == "min":
            item.minValue.setText(paramAttr.value)
        elif paramAttr.attr == "max":
            item.maxValue.setText(paramAttr.value)
        elif paramAttr.attr == "initValue":
            item.initialValue.setText(paramAttr.value)
        elif paramAttr.attr == "value":
            item.resultValue.setText(paramAttr.value)
        elif paramAttr.attr == "isFixed":
            item.fixCheckbox.setChecked(paramAttr.value)
        else:
            raise ValueError(f"Invalid attribute {paramAttr.attr}")        
        

class FitView(QObject):
    def __init__(
        self,
        parent: QObject,
        runFit: QPushButton,
        dataTransferButtons: Dict[str, QPushButton],
        options: Dict[str, Any],
    ):
        super().__init__(parent)
        self.runFit = runFit
        self.dataTransferButtons = dataTransferButtons
        self.tolLineEdit: FloatLineEdit = options["tol"]
        self.optimizerComboBox: QComboBox = options["optimizer"]