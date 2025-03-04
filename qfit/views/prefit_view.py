from PySide6.QtCore import QObject, Signal, Slot, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QCheckBox,
    QSpinBox,
    QPushButton,
    QWidget,
    QFrame,
)
from qfit.widgets.validated_line_edits import IntLineEdit, MultiStatesLineEdit

from qfit.widgets.grouped_sliders import (
    LabeledSlider,
    GroupedWidgetSet,
    SPACING_BETWEEN_GROUPS,
)
from qfit.widgets.custom_table import (
    FoldableTable,
    MinMaxItems,
)
from qfit.widgets.foldable_widget import FoldableWidget
from qfit.models.data_structures import ParamAttr
from qfit.utils.helpers import clearChildren

from typing import Dict, List, Any


class PrefitParamView(QObject):
    """
    A view for the prefit parameters. This view is a widget that contains
    a set of sliders and a min max table for the prefit parameters.
    It is responsible for displaying the parameters and their values, and
    also for emitting signals when the parameters are changed.

    Parameters
    ----------
    parent : QObject
        The parent object.
    prefitScrollAreaWidget : QWidget
        The widget that contains the prefit parameters.
    prefitMinmaxScrollAreaWidget : QWidget
        The widget that contains the prefit min max table.
    prefitMinMaxFrame : QFrame
        The frame that contains the prefit min max table, which can be
        folded.
    """

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
        parent: QObject,
        prefitScrollAreaWidget: QWidget,
        prefitMinmaxScrollAreaWidget: QWidget,
        prefitMinMaxFrame: QFrame,
    ):
        super().__init__(parent)

        self.prefitScrollAreaWidget = prefitScrollAreaWidget
        self.prefitMinmaxScrollAreaWidget = prefitMinmaxScrollAreaWidget
        self.prefitMinMaxFrame = prefitMinMaxFrame

        # setting for prefit minmax scroll area
        # self.prefitMinmaxScrollAreaWidget.setWidgetResizable(True)

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
        self, paramNameDict: Dict[str, List[str]], removeExisting: bool = True
    ):
        """
        Initialize the prefit sliders by a dictionary of parameter names.

        Parameters
        ----------
        paramNameDict : Dict[str, List[str]]
            The names of the prefit parameters. The keys are the group names,
            and the values are the parameter names in each group.
        removeExisting : bool, optional
            Whether to remove the existing widgets, by default True. For now,
            it is not implemented to set to False.
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
        self, paramNameDict: Dict[str, List[str]], removeExisting: bool = True
    ):
        """
        Initialize the minmax table by a dictionary of parameter names.

        Parameters
        ----------
        paramNameDict : Dict[str, List[str]]
            The names of the prefit parameters. The keys are the group names,
            and the values are the parameter names in each group.
        removeExisting : bool, optional
            Whether to remove the existing widgets, by default True. For now,
            it is not implemented to set to False.
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
        self.foldable_widget = FoldableWidget("RANGES OF SLIDERS", self.minMaxTable)
        prefitMinmaxScrollLayout.addWidget(self.foldable_widget)

        # temporary fix for the height of the row - after addWidget the
        # row height were reset to 30 - don't know why
        self.minMaxTable.setHeightOfRow()

        # default to fold the table
        self.foldable_widget.toggle()

    # def _removeMinMax(self, groupName: str):
    #     pass

    def insertSliderMinMax(
        self,
        HSParamNames: Dict[str, List[str]],
        caliParamNames: Dict[str, List[str]],
        removeExisting: bool = True,
    ):
        """
        Given the dictionaries of parameter names, it will initialize
        the sliders and minmax table for the prefit parameters. Note that
        we distinguish and keep track of the HilbertSpace parameters and
        the calibration model parameters. It's important as we need to
        emit different signals for the two types of parameters.

        Parameters
        ----------
        HSParamNames : Dict[str, List[str]]
            The names of the prefit parameters for the HilbertSpace.
        caliParamNames : Dict[str, List[str]]
            The names of the prefit parameters for the calibration model.
        removeExisting : bool, optional
            Whether to remove the existing widgets, by default True. For now,
            it is not implemented to set to False.
        """
        self.HSNames = list(HSParamNames.keys())

        paramNameDict = HSParamNames | caliParamNames
        self._insertSliders(paramNameDict, removeExisting)
        self._insertMinMax(paramNameDict, removeExisting)
        # don't know yet the exact reason, but only when _insertMinMax is called
        # I can set width of the columns successfully for the minmax table
        # in Windows. TODO: find out the reason.
        self.minMaxTable.setWidthOfColumn()
        self._connectMinmaxTableFolding()
        self._signalProcessing()

    # signal processing ================================================
    def _signalProcessing(self):
        """
        Collect the signals from the sliders and minmax table, and emit
        in one connection. It should be called whenver the sliders and minmax
        table are re-initialized.

        Note that different signals are emitted for the HilbertSpace parameters
        and the calibration model parameters.
        """
        for groupName, group in self.sliderSet.items():
            for name, slider in group.items():
                slider: LabeledSlider

                if groupName in self.HSNames:
                    signalSet = self.HSSignals
                else:
                    signalSet = self.caliSignals

                slider.sliderValueChangedConnect(
                    lambda value, name=name, groupName=groupName, signalSet=signalSet: signalSet[
                        "sliderChanged"
                    ].emit(
                        ParamAttr(groupName, name, "value", value)
                    )
                )
                slider.textValueChangedConnect(
                    lambda text, name=name, groupName=groupName, signalSet=signalSet: signalSet[
                        "textChanged"
                    ].emit(
                        ParamAttr(groupName, name, "value", text)
                    )
                )
                slider.editingFinishedConnect(
                    lambda name=name, groupName=groupName, signalSet=signalSet: signalSet[
                        "editingFinished"
                    ].emit(
                        groupName, name
                    )
                )

        for groupName, group in self.minMaxTable.items():
            for name, item in group.items():
                item: MinMaxItems

                if groupName in self.HSNames:
                    signalSet = self.HSSignals
                else:
                    signalSet = self.caliSignals

                item.minValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signalSet=signalSet: signalSet[
                        "rangeEditingFinished"
                    ].emit(
                        ParamAttr(groupName, name, "min", item.minValue.text())
                    )
                )
                item.maxValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signalSet=signalSet: signalSet[
                        "rangeEditingFinished"
                    ].emit(
                        ParamAttr(groupName, name, "max", item.maxValue.text())
                    )
                )

    def _connectMinmaxTableFolding(self):
        self.foldable_widget.expandWidgetToggled.connect(self.toggleMinMaxTableFrame)

    # slots ==========================================================
    @Slot(ParamAttr)
    def setByParamAttr(self, paramAttr: ParamAttr, toSlider: bool = True):
        """
        Set the value of the parameter from the model using ParamAttr.
        """
        if paramAttr.attr == "value":
            labeledSlider: LabeledSlider = self.sliderSet[paramAttr.parentName][
                paramAttr.name
            ]
            labeledSlider.setValue(paramAttr.value, toSlider=toSlider)
        elif paramAttr.attr == "min":
            assert toSlider is False
            item: MinMaxItems = self.minMaxTable[paramAttr.parentName][paramAttr.name]
            item.minValue.setText(paramAttr.value)
        elif paramAttr.attr == "max":
            assert toSlider is False
            item: MinMaxItems = self.minMaxTable[paramAttr.parentName][paramAttr.name]
            item.maxValue.setText(paramAttr.value)
        else:
            raise ValueError(f"Invalid attribute {paramAttr.attr}")

    @Slot(bool)
    def toggleMinMaxTableFrame(self, b: bool):
        """
        Toggle the visibility of the minmax table frame.
        """
        if b:
            self.prefitMinMaxFrame.setMaximumHeight(400)
        else:
            self.prefitMinMaxFrame.setMaximumHeight(0)


class SweepSettingsView(QObject):
    """
    A view for the sweep settings. This view is a widget that contains
    settings for the prefit, such as the number of eigenvalues to calculate,
    the initial state, the number of photons, etc. It also contains run
    sweep button and auto run checkbox.

    Parameters
    ----------
    parent : QObject
        The parent object.
    runSweep : QPushButton
        The button to run the sweep.
    options : Dict[str, Any]
        The options for the prefit settings. The keys should be "evalsCount",
        "subsysToPlot", "initialStates", "photons", "pointsAdded" and "autoRun".
        And the corresponding values should be the widgets for the options.
    """

    optionUpdated = Signal(str, object)

    def __init__(
        self,
        parent: QObject,
        runSweep: QPushButton,
        options: Dict[str, Any],
    ):
        super().__init__(parent)

        self.runSweep = runSweep

        self.options = options
        self.evalsCount: IntLineEdit = self.options["evalsCount"]
        self.subsysToPlot: QComboBox = self.options["subsysToPlot"]
        self.initialStates: MultiStatesLineEdit = self.options["initialStates"]
        self.photons: QSpinBox = self.options["photons"]
        self.pointsAdded: IntLineEdit = self.options["pointsAdded"]
        self.numCPUs: IntLineEdit = self.options["numCPUs"]
        self.autoRun: QCheckBox = self.options["autoRun"]

        self.optionsConnects()

    def replaceHS(self, subsysNames: List[str]):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the view will reinitialized by this method.

        Parameters
        ----------
        subsysNames : List[str]
            The names of the subsystems in the Hilbert space.
        """
        self.blockAllSignals(True)

        # load subsystems
        self.subsysToPlot.clear()
        for subsys_name in subsysNames:
            self.subsysToPlot.insertItem(0, subsys_name)
        self.subsysToPlot.insertItem(0, "None Selected")

        self.blockAllSignals(False)

    def setEnabled(self, value: bool):
        self.evalsCount.setEnabled(value)
        self.subsysToPlot.setEnabled(value)
        self.initialStates.setEnabled(value)
        self.photons.setEnabled(value)
        self.pointsAdded.setEnabled(value)
        self.autoRun.setEnabled(value)
        self.runSweep.setEnabled(value)
        self.numCPUs.setEnabled(value)

    # Signal processing ======================================================
    def blockAllSignals(self, b: bool):
        super().blockSignals(b)

        for option in self.options.values():
            option.blockSignals(b)

    def setOptions(self, option: str, value: Any):
        """
        Set the value of the option.

        Parameters
        ----------
        option : str
            The name of the option to set.
        value : Any
            The value to set.
        """
        self.blockAllSignals(True)
        if option == "subsysToPlot":
            self.subsysToPlot.setCurrentText(value)
        elif option == "evalsCount":
            self.evalsCount.setText(value)
        elif option == "initialStates":
            self.initialStates.setText(value)
        elif option == "photons":
            self.photons.setValue(value)
        elif option == "pointsAdded":
            self.pointsAdded.setText(value)
        elif option == "numCPUs":
            self.numCPUs.setText(value)
        elif option == "autoRun":
            self.autoRun.setChecked(value)
        self.blockAllSignals(False)

    def optionsConnects(self):
        """
        Collect the signals from the options, and emit as a optionUpdated
        signal which contains the name of the option and the value.
        """
        self.subsysToPlot.currentIndexChanged.connect(
            lambda: self.optionUpdated.emit(
                "subsysToPlot", self.subsysToPlot.currentText()
            )
        )
        self.initialStates.editingFinished.connect(
            lambda: self.optionUpdated.emit("initialStates", self.initialStates.text())
        )
        self.photons.valueChanged.connect(
            lambda: self.optionUpdated.emit("photons", self.photons.value())
        )
        self.evalsCount.editingFinished.connect(
            lambda: self.optionUpdated.emit("evalsCount", self.evalsCount.text())
        )
        self.pointsAdded.editingFinished.connect(
            lambda: self.optionUpdated.emit("pointsAdded", self.pointsAdded.text())
        )
        self.numCPUs.editingFinished.connect(
            lambda: self.optionUpdated.emit("numCPUs", self.numCPUs.text())
        )
        self.autoRun.stateChanged.connect(
            lambda: self.optionUpdated.emit("autoRun", self.autoRun.isChecked())
        )
