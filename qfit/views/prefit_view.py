from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtWidgets import QComboBox, QCheckBox, QSpinBox, QPushButton, QWidget
from qfit.widgets.validated_line_edits import IntLineEdit, StateLineEdit

from qfit.widgets.grouped_sliders import (
    LabeledSlider,
    GroupedWidgetSet,
    SPACING_BETWEEN_GROUPS,
)
from qfit.widgets.foldable_table import (
    FoldableTable,
    MinMaxItems,
)
from qfit.widgets.foldable_widget import FoldableWidget
from qfit.models.data_structures import ParamAttr
from qfit.utils.helpers import clearChildren

from typing import Dict, List, Any


class PrefitParamView(QObject):
    HSSliderChanged = Signal(ParamAttr)
    HSTextChanged = Signal(ParamAttr)
    HSEditingFinished = Signal(str, str)
    HSRangeEditingFinished = Signal(ParamAttr)
    
    caliSliderChanged = Signal(ParamAttr)
    caliTextChanged = Signal(ParamAttr)
    caliEditingFinished = Signal(str, str)
    caliRangeEditingFinished = Signal(ParamAttr)

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

        # A list to tell whether the parameter belongs to a hilbertspace
        # or a calibration model.
        self.HSNames: List[str] = []  
        # Group the signals for easier connection (avoid code repetition)
        self.HSSignals = {
            "sliderChanged": self.HSSliderChanged,
            "textChanged": self.HSTextChanged,
            "editingFinished": self.HSEditingFinished,
            "rangeEditingFinished": self.HSRangeEditingFinished,
        }
        self.caliSignals = {
            "sliderChanged": self.caliSliderChanged,
            "textChanged": self.caliTextChanged,
            "editingFinished": self.caliEditingFinished,
            "rangeEditingFinished": self.caliRangeEditingFinished,
        }


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
        HSParamNames: Dict[str, List[str]],
        caliParamNames: Dict[str, List[str]],
        removeExisting: bool = True
    ):
        self.HSNames = list(HSParamNames.keys())
        
        paramNameDict = HSParamNames | caliParamNames 
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

                if groupName in self.HSNames:
                    signalSet = self.HSSignals
                else:
                    signalSet = self.caliSignals

                slider.sliderValueChangedConnect(
                    lambda value, name=name, groupName=groupName, signalSet=signalSet: 
                    signalSet["sliderChanged"].emit(
                        ParamAttr(groupName, name, "value", value)
                    )
                )
                slider.textValueChangedConnect(
                    lambda text, name=name, groupName=groupName, signalSet=signalSet: 
                    signalSet["textChanged"].emit(
                        ParamAttr(groupName, name, "value", text)
                    )
                )
                slider.editingFinishedConnect(
                    lambda name=name, groupName=groupName, signalSet=signalSet: 
                    signalSet["editingFinished"].emit(groupName, name)
                )
        
        for groupName, group in self.minMaxTable.items():
            for name, item in group.items():
                item: MinMaxItems
                item.minValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signalSet=signalSet: 
                    signalSet["rangeEditingFinished"].emit(
                        ParamAttr(groupName, name, "min", item.minValue.text())
                    )
                )
                item.maxValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signalSet=signalSet: 
                    signalSet["rangeEditingFinished"].emit(
                        ParamAttr(groupName, name, "max", item.maxValue.text())
                    )
                )

    # setters ==========================================================
    @Slot(ParamAttr)
    def setByParamAttr(self, paramAttr: ParamAttr, toSlider: bool = True):
        if paramAttr.attr == "value":
            labeledSlider: LabeledSlider = self.sliderSet[paramAttr.parentName][paramAttr.name]
            labeledSlider.setValue(paramAttr.value, toSlider=toSlider)
        elif paramAttr.attr == "min":
            assert toSlider == False
            item: MinMaxItems = self.minMaxTable[paramAttr.parentName][paramAttr.name]
            item.minValue.setText(paramAttr.value)
        elif paramAttr.attr == "max":
            assert toSlider == False
            item: MinMaxItems = self.minMaxTable[paramAttr.parentName][paramAttr.name]
            item.maxValue.setText(paramAttr.value)
        else:
            raise ValueError(f"Invalid attribute {paramAttr.attr}")


class PrefitView(QObject):

    optionUpdated = Signal(str, Any)

    def __init__(
        self,
        runSweep: QPushButton,
        options: Dict[str, Any],
    ):
        super().__init__()

        self.runSweep = runSweep

        self.options = options
        self.evalsCount: IntLineEdit = self.options["evalsCount"]
        self.subsysToPlot: QComboBox = self.options["subsysToPlot"]
        self.initialState: StateLineEdit = self.options["initialState"]
        self.photons: QSpinBox = self.options["photons"]
        self.pointsAdded: IntLineEdit = self.options["pointsAdded"]
        self.autoRun: QCheckBox = self.options["autoRun"]

        self.optionsConnects()

    def dynamicalInit(
        self,
        subsysNames: List[str],
    ):
        self.initializeOptions(subsysNames)

    def initializeOptions(self, subsysNames: List[str]):
        """
        Should be re-iniitalized when hilbert space changes
        """
        self.blockAllSignals(True)

        self.evalsCount.setText("1")

        # load subsystems
        self.subsysToPlot.clear()
        for subsys_name in subsysNames:
            self.subsysToPlot.insertItem(0, subsys_name)

        # initial state
        self.initialState.setTupleLength(len(subsysNames))

        # photons
        self.photons.setValue(1)

        # points added
        self.pointsAdded.setText("10")

        # auto run
        self.autoRun.setChecked(True)

        self.blockAllSignals(False)

    # Signal processing ======================================================
    def blockAllSignals(self, b: bool):
        super().blockSignals(b)

        for option in self.options.values():
            option.blockSignals(b)

    def setOptions(self, option: str, value: Any):
        self.blockAllSignals(True)
        if option == "subsysToPlot":
            self.subsysToPlot.setCurrentText(value)
        elif option == "evalsCount":
            self.evalsCount.setText(value)
        elif option == "initialState":
            self.initialState.setText(value)
        elif option == "photons":
            self.photons.setValue(value)
        elif option == "pointsAdded":
            self.pointsAdded.setText(value)
        elif option == "autoRun":
            self.autoRun.setChecked(value)
        self.blockAllSignals(False)

    def emitOption(self, option: str):
        if option == "subsysToPlot":
            self.optionUpdated.emit(option, self.subsysToPlot.currentText())
        elif option == "initialState":
            self.optionUpdated.emit(option, self.initialState.text())
        elif option == "photons":
            self.optionUpdated.emit(option, self.photons.value())
        elif option == "pointsAdded":
            self.optionUpdated.emit(option, self.pointsAdded.text())
        elif option == "autoRun":
            self.optionUpdated.emit(option, self.autoRun.isChecked())

    # def emitAllOptions(self):
    #     self.emitOption("subsysToPlot")
    #     self.emitOption("initialState")
    #     self.emitOption("photons")
    #     self.emitOption("pointsAdded")
    #     self.emitOption("autoRun")

    def optionsConnects(self):
        self.subsysToPlot.currentIndexChanged.connect(
            lambda: self.emitOption("subsysToPlot")
        )
        self.initialState.editingFinished.connect(
            lambda: self.emitOption("initialState")
        )
        self.photons.valueChanged.connect(
            lambda: self.emitOption("photons")
        )
        self.pointsAdded.editingFinished.connect(
            lambda: self.emitOption("pointsAdded")
        )
        self.autoRun.stateChanged.connect(
            lambda: self.emitOption("autoRun")
        )