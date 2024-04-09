from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy,
    QPushButton,
    QLineEdit,
    QComboBox,
)
from PySide6.QtGui import QIcon

from qfit.widgets.custom_table import (
    FoldableTable,
    FittingParameterItems,
)
from qfit.widgets.validated_line_edits import FloatLineEdit
from qfit.models.data_structures import ParamAttr
from qfit.utils.helpers import clearChildren

from typing import Dict, List, Any


class FitParamView(QObject):
    """
    A view for the fitting parameters. This view is a widget that contains
    a set of tables for the fitting parameters. It is responsible for
    displaying the parameters and their values, and also for emitting
    signals when the parameters are changed.

    Parameters
    ----------
    parent : QObject
        The parent object.
    fitScrollAreaWidget : QWidget
        The widget that contains the fitting parameters.
    """

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
        """
        Configure the layout of the widget.
        """
        fitScrollArea = self.fitScrollWidget.parent()
        fitScrollArea.setStyleSheet(f"background-color: rgb(33, 33, 33);")
        self.fitScrollWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def fitTableInserts(
        self,
        HSParamNames: Dict[str, List[str]],
        caliParamNames: Dict[str, List[str]],
        removeExisting: bool = True,
    ):
        """
        Insert parameters to the table and each of the parameter
        is corresponding to a FittingParameterItems.

        Parameters
        ----------
        HSParamNames : Dict[str, List[str]]
            The names of the fitting parameters for the HilbertSpace.
        caliParamNames : Dict[str, List[str]]
            The names of the fitting parameters for the calibration model.
        removeExisting : bool, optional
            Whether to remove the existing widgets, by default True.
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

        # temporary fix for the height of the row - after addWidget the
        # row height were reset to 30 - don't know why
        self.fitTableSet.setHeightOfRow()

        self._signalProcessing()

    # Signal processing ================================================
    def _signalProcessing(self):
        """
        Emit signals when the parameters are changed.
        """
        for groupName, group in self.fitTableSet.items():
            for name, item in group.items():
                item: FittingParameterItems

                if groupName in self.HSNames:
                    signal = self.HSEditingFinished
                else:
                    signal = self.CaliEditingFinished

                item.minValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signal=signal: signal.emit(
                        ParamAttr(groupName, name, "min", item.minValue.text())
                    )
                )
                item.maxValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signal=signal: signal.emit(
                        ParamAttr(groupName, name, "max", item.maxValue.text())
                    )
                )
                item.fixCheckbox.toggled.connect(
                    lambda value, name=name, groupName=groupName, signal=signal: signal.emit(
                        ParamAttr(groupName, name, "isFixed", value)
                    )
                )
                item.initialValue.editingFinished.connect(
                    lambda item=item, name=name, groupName=groupName, signal=signal: signal.emit(
                        ParamAttr(
                            groupName, name, "initValue", item.initialValue.text()
                        )
                    )
                )

    # Setters ==========================================================
    @Slot(ParamAttr)
    def setBoxValue(self, paramAttr: ParamAttr):
        """
        Set the value of the parameter from the model using ParamAttr.
        """
        item: FittingParameterItems = self.fitTableSet[paramAttr.parentName][
            paramAttr.name
        ]
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
    """
    A view for the fit settings.
    """

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
        self.fitButtonMode: str = "run"

    def setEnabled(self, enabled: bool):
        for button in self.dataTransferButtons.values():
            button.setEnabled(enabled)
        self.tolLineEdit.setEnabled(enabled)
        self.optimizerComboBox.setEnabled(enabled)

    def setFitButtonEnabled(self, enabled: bool):
        self.runFit.setEnabled(enabled)

    def setFitButtonMode(self, mode: str):
        if mode == "run":
            self.fitButtonMode = "run"
            self.runFit.setText("   Run Fit")
            self.runFit.setIcon(QIcon(":/icons/svg/play.svg"))
        elif mode == "stop":
            self.fitButtonMode = "stop"
            self.runFit.setText("   Stop Fit")
            self.runFit.setIcon(QIcon(":/icons/svg/stop.svg"))
