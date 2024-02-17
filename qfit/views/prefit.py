from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QLineEdit, QComboBox, QCheckBox, QSpinBox
from qfit.widgets.validated_line_edits import IntTupleLineEdit, IntLineEdit, StateLineEdit

from typing import List, Dict, Any, Literal
class PrefitView(QObject):

    optionUpdated = Signal(str, Any)

    def __init__(
        self,
        options: Dict[str, Any],
        subsysNames: List[str],
        hilbertDim: int,
    ):
        super().__init__()

        self.options = options
        self.evalsCount: IntLineEdit = self.options["evalsCount"]
        self.subsysToPlot: QComboBox = self.options["subsysToPlot"]
        self.initialState: StateLineEdit = self.options["initialState"]
        self.photons: QSpinBox = self.options["photons"]
        self.pointsAdded: IntLineEdit = self.options["pointsAdded"]
        self.autoRun: QCheckBox = self.options["autoRun"]

        self.initializeOptions(subsysNames, hilbertDim)

    def blockAllSignals(self, b: bool):
        super().blockSignals(b)

        for option in self.options.values():
            option.blockSignals(b)

    def initializeOptions(self, subsysNames: List[str], hilbertDim: int):
        """
        Should be re-iniitalized when hilbert space changes
        """
        self.blockAllSignals(True)

        # evals count
        if hilbertDim > 20:
            dim = 20
        else:
            dim = hilbertDim
        self.evalsCount.setText(str(dim))

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
    def optionsConnects(self):
        self.subsysToPlot.currentIndexChanged.connect(
            lambda: self.optionUpdated.emit("subsysToPlot", self.subsysToPlot.currentText())
        )
        self.initialState.editingFinished.connect(
            lambda: self.optionUpdated.emit("initialState", self.initialState.text())
        )
        self.photons.valueChanged.connect(
            lambda: self.optionUpdated.emit("photons", self.photons.value())
        )
        self.pointsAdded.editingFinished.connect(
            lambda: self.optionUpdated.emit("pointsAdded", self.pointsAdded.text())
        )
        self.autoRun.stateChanged.connect(
            lambda: self.optionUpdated.emit("autoRun", self.autoRun.isChecked())
        )