from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QLineEdit, QComboBox, QCheckBox, QSpinBox, QPushButton
from qfit.widgets.validated_line_edits import IntTupleLineEdit, IntLineEdit, StateLineEdit

from typing import List, Dict, Any, Literal
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