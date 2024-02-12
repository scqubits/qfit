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
from qfit.models.data_structures import QMSliderParam, ParamAttr
from qfit.models.quantum_model_parameters import ParamSet
from qfit.utils.helpers import clearChildren

from typing import Dict, List, Optional, Union, overload, Literal


class PrefitParamView(QObject):
    sliderValueChanged = Signal(ParamAttr)
    textValueChanged = Signal(ParamAttr)
    valueEditingFihished = Signal(str, str)
    rangeEditingFinished = Signal(ParamAttr)

    # Initialization ===================================================

    def __init__(
        self, 
        prefitScrollAreaWidget: QWidget,
        prefitMinmaxScrollAreaWidget: QWidget,
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.prefitScrollAreaWidget = prefitScrollAreaWidget
        self.prefitMinmaxScrollAreaWidget = prefitMinmaxScrollAreaWidget    

    def _insertSliders(
        self,
        paramNameDict: Dict[str, List[str]],
        removeExisting: bool = True
    ):
        """
        View init: pre-fit sliders

        Insert a set of sliders for the prefit parameters according to the parameter set
        """
        # remove the existing widgets, if we somehow want to rebuild the sliders
        if removeExisting:
            clearChildren(self.prefitScrollAreaWidget)
        else:
            raise NotImplementedError("Not implemented yet")

        # create a QWidget for the scrollArea and set a layout for it
        prefitScrollLayout = self.prefitScrollAreaWidget.layout()

        # set the alignment of the entire prefit scroll layout
        prefitScrollLayout.setAlignment(Qt.AlignTop)

        # generate the slider set
        self.sliderSet = GroupedWidgetSet(
            widgetClass=LabeledSlider,
            initKwargs={"label_value_position": "left_right"},
            columns=1,
            parent=self.prefitScrollAreaWidget,
        )

        for key, para_list in paramNameDict.items():
            self.sliderSet.addGroupedWidgets(
                key,
                para_list,
            )

        prefitScrollLayout.addWidget(self.sliderSet)

        # add a spacing between the sliders and the min max table
        prefitScrollLayout.addSpacing(SPACING_BETWEEN_GROUPS)

    # def _removeSliderGroup(self, groupName: str):
    #     pass

    def _insertMinMax(
        self,
        paramNameDict: Dict[str, List[str]],
        removeExisting: bool = True
    ):
        """
        View init: pre-fit min max table
        """
        # remove the existing widgets, if we somehow want to rebuild the sliders
        if removeExisting:
            clearChildren(self.prefitMinmaxScrollAreaWidget)
        else:
            raise NotImplementedError("Not implemented yet")

        # create a QWidget for the minmax scroll area and set a layout for it
        prefitMinmaxScrollLayout = self.prefitMinmaxScrollAreaWidget.layout()

        # set the alignment of the entire prefit minmax scroll layout
        prefitMinmaxScrollLayout.setAlignment(Qt.AlignTop)

        self.minMaxTable = FoldableTable(
            MinMaxItems,
            paramNumPerRow=1,
            groupNames=list(paramNameDict.keys()),
        )
        self.minMaxTable.setCheckable(False)
        self.minMaxTable.setChecked(False)

        # insert parameters
        for key, para_list in paramNameDict.items():
            for para_name in para_list:
                self.minMaxTable.insertParams(key, para_name)

        # add the minmax table to the scroll area
        foldable_widget = FoldableWidget("RANGES OF SLIDERS", self.minMaxTable)
        prefitMinmaxScrollLayout.addWidget(foldable_widget)

        # default to fold the table
        foldable_widget.toggle()

    # def _removeMinMax(self, groupName: str):
    #     pass
        
    def insertSliderMinMax(
        self,
        paramNameDict: Dict[str, List[str]],
        removeExisting: bool = True
    ):
        self._insertSliders(paramNameDict, removeExisting)
        self._insertMinMax(paramNameDict, removeExisting)
        self._signalProcessing()

    # signal processing ================================================
    def _signalProcessing(self):
        """
        Collect the signals from the sliders and minmax table, and emit
        in one connection. It should be called whenver the sliders and minmax 
        table are re-initialized.
        """
        for groupName, group in self.sliderSet.items():
            for name, slider in group.items():
                slider: LabeledSlider
                slider.sliderValueChangedConnect(
                    lambda value, name=name, groupName=groupName: self.sliderValueChanged.emit(
                        ParamAttr(groupName, name, "value", value)
                    )
                )
                slider.textValueChangedConnect(
                    lambda text, name=name, groupName=groupName: self.textValueChanged.emit(
                        ParamAttr(groupName, name, "value", text)
                    )
                )
                slider.editingFinishedConnect(
                    lambda name=name, groupName=groupName: self.valueEditingFihished.emit(groupName, name)
                )
        
        for groupName, group in self.minMaxTable.items():
            for name, item in group.items():
                item: MinMaxItems
                item.minValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName: self.rangeEditingFinished.emit(
                        ParamAttr(groupName, name, "min", item.minValue.text())
                    )
                )
                item.maxValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName: self.rangeEditingFinished.emit(
                        ParamAttr(groupName, name, "max", item.maxValue.text())
                    )
                )

    # setters ==========================================================
    @Slot(ParamAttr)
    def setByParamAttr(self, paramAttr: ParamAttr, toSlider: bool = True):
        if paramAttr.attr == "value":
            labeledSlider: LabeledSlider = self.sliderSet[paramAttr.parantName][paramAttr.name]
            labeledSlider.setValue(paramAttr.value, toSlider=toSlider)
        elif paramAttr.attr == "min":
            assert toSlider == False
            item: MinMaxItems = self.minMaxTable[paramAttr.parantName][paramAttr.name]
            item.minValue.setText(paramAttr.value)
        elif paramAttr.attr == "max":
            assert toSlider == False
            item: MinMaxItems = self.minMaxTable[paramAttr.parantName][paramAttr.name]
            item.maxValue.setText(paramAttr.value)
        else:
            raise ValueError(f"Invalid attribute {paramAttr.attr}")


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
        item: FittingParameterItems = self.fitTableSet[paramAttr.parantName][paramAttr.name]
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
        