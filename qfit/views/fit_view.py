from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from qfit.widgets.grouped_sliders import (
    LabeledSlider,
    GroupedWidgetSet,
    SPACING_BETWEEN_GROUPS,
)
from qfit.widgets.foldable_table import (
    FoldableTable,
    MinMaxItems,
    FittingParameterItems,
)
from qfit.widgets.foldable_widget import FoldableWidget
from qfit.models.data_structures import ParamAttr
from qfit.utils.helpers import clearChildren

from typing import Dict, List


class FitParamView(QObject):
    dataEditingFinished = Signal(ParamAttr)

    def __init__(
        self,
        fitScrollAreaWidget: QWidget,
    ):
        super().__init__()

        self.fitScrollWidget = fitScrollAreaWidget
        self._configureLayout()

    def _configureLayout(self):
        fitScrollArea = self.fitScrollWidget.parent()
        fitScrollArea.setStyleSheet(f"background-color: rgb(33, 33, 33);")
        self.fitScrollWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def fitTableInserts(
        self,
        paramNameDict: Dict[str, List[str]],
        removeExisting: bool = True
    ):
        """
        Insert a set of tables for the fitting parameters
        """

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

    # Signal processing ================================================
    def _signalProcessing(self):
        for groupName, group in self.fitTableSet.items():
            for name, item in group.items():
                item: FittingParameterItems
                item.minValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName: self.dataEditingFinished.emit(
                        ParamAttr(groupName, name, "min", item.minValue.text())
                    )
                )
                item.maxValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName: self.dataEditingFinished.emit(
                        ParamAttr(groupName, name, "max", item.maxValue.text())
                    )
                )
                item.fixCheckbox.toggled.connect(
                    lambda value, name=name, groupName=groupName: self.dataEditingFinished.emit(
                        ParamAttr(groupName, name, "isFixed", value)
                    )
                )
                item.initialValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName: self.dataEditingFinished.emit(
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