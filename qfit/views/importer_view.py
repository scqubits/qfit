from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QScrollArea,
    QLabel,
    QCheckBox,
    QMessageBox,
)
from PySide6.QtCore import QObject, Signal, Slot, Qt

from qfit.models.data_structures import MeasMetaInfo, MeasRawXYConfig

from typing import Tuple, Dict, Any, List, Union, Literal, Type


class ImporterView(QObject):
    """
    The view for the importer.
    """

    # signals
    configChanged = Signal(MeasRawXYConfig)
    transposeZClicked = Signal()
    continueClicked = Signal()
    addFigClicked = Signal()
    deleteFigClicked = Signal()

    def __init__(
        self,
        parent: QWidget,
        metaInfo: Dict[str, QLabel],
        importFigButtons: Dict[str, QPushButton],
        axesSelectionArea: Dict[str, QScrollArea],
        transposeButton: QPushButton,
        continueButton: QPushButton,
    ):
        super().__init__(parent)

        self.metaInfo = metaInfo
        self.importFigButtons = importFigButtons
        self.axesSelectionArea = axesSelectionArea
        self.transposeButton = transposeButton
        self.continueButton = continueButton

        self.checkBoxes: Dict[str, Dict[str, QCheckBox]] = {
            "x": {},
            "y": {},
        }

        self.signalProcessing()

    # meta info ========================================================
    @Slot()
    def setMetaInfo(self, metaInfo: MeasMetaInfo):
        """
        Given a MeasMetaInfo object, set the text of the labels in the
        view.
        """
        self.metaInfo["name"].setText(metaInfo.name)
        self.metaInfo["file"].setText(metaInfo.file)
        self.metaInfo["shape"].setText(", ".join([str(i) for i in metaInfo.shape]))
        self.metaInfo["xCandidateNames"].setText(", ".join(metaInfo.xCandidateNames))
        self.metaInfo["yCandidateNames"].setText(", ".join(metaInfo.yCandidateNames))
        self.metaInfo["zCandidateNames"].setText(", ".join(metaInfo.zCandidateNames))
        self.metaInfo["discardedKeys"].setText(", ".join(metaInfo.discardedKeys))

    # config ===========================================================
    def _insertCheckBox(self, axis: str, names: List[str]):
        """
        Given a list of names, insert a checkbox for each name into the
        scroll area.
        """
        scrollArea = self.axesSelectionArea[axis]
        layout = scrollArea.widget().layout()

        # clear layout
        for checkBox in self.checkBoxes[axis].values():
            layout.removeWidget(checkBox)
            checkBox.deleteLater()
        self.checkBoxes[axis] = {}

        # insert checkboxes
        for name in names:
            checkBox = QCheckBox(name)

            # configure the check box
            checkBox.setEnabled(True)
            checkBox.setCheckable(True)
            checkBox.setStyleSheet(
                """
QCheckBox:disabled {	
	color: rgb(85, 85, 85);
}
QCheckBox::indicator:disabled {	
	border: 1px solid rgb(85, 85, 85);
   background: transparent;
}
"""
            )

            # connect to the signal
            checkBox.clicked.connect(self.emitConfigChanged)

            # insert the check box
            layout.addWidget(checkBox)
            self.checkBoxes[axis][name] = checkBox

    def _checkCheckBox(self, axis: str, names: List[str]):
        """
        Given a list of names, check the checkboxes for each name.
        """
        for name, checkBox in self.checkBoxes[axis].items():
            if name in names:
                checkBox.setChecked(True)
            else:
                checkBox.setChecked(False)

    def _grayOutCheckBox(self, axis: str, names: List[str]):
        """
        Given a list of names, gray out the checkboxes for each name.
        """
        for name, checkBox in self.checkBoxes[axis].items():
            if name in names:
                checkBox.setEnabled(False)
            else:
                checkBox.setEnabled(True)

    @Slot()
    def setConfig(self, config: MeasRawXYConfig):
        """
        Given a MeasRawXYConfig object, set the text of the labels in the
        view.
        """
        # check buttons
        self._insertCheckBox("x", config.xCandidates)
        self._insertCheckBox("y", config.yCandidates)
        self._checkCheckBox("x", config.checkedX)
        self._checkCheckBox("y", config.checkedY)
        self._grayOutCheckBox("x", config.grayedX)
        self._grayOutCheckBox("y", config.grayedY)

        # other buttons
        self.transposeButton.setEnabled(config.allowTranspose)
        self.transposeButton.setVisible(config.allowTranspose)
        self.continueButton.setEnabled(config.allowContinue)

    def getConfig(self) -> MeasRawXYConfig:
        """
        Return the checked x and y candidates.
        """
        config = MeasRawXYConfig(
            checkedX=[
                name
                for name, checkBox in self.checkBoxes["x"].items()
                if checkBox.isChecked()
            ],
            checkedY=[
                name
                for name, checkBox in self.checkBoxes["y"].items()
                if checkBox.isChecked()
            ],
        )
        return config

    def emitConfigChanged(self):
        """
        Emit a signal to notify that the config has changed.
        """
        self.configChanged.emit(self.getConfig())

    # other buttons ====================================================
    def enableFigImport(self, enabled: bool):
        self.importFigButtons["new"].setEnabled(enabled)
        self.importFigButtons["new"].setVisible(enabled)
        self.importFigButtons["delete"].setEnabled(enabled)
        self.importFigButtons["delete"].setVisible(enabled)

    def onContinueClicked(self):
        """
        Emit a signal when the continue button is clicked.
        """
        # send a message box to confirm
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(
            "By leaving the import page, you will not be able to "
            "come back to add or remove datasets or change the axis settings. "
            "Are you sure you want to continue?"
        )
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        reply = msgBox.exec()

        if reply == QMessageBox.Yes:
            self.enableFigImport(False)
            self.continueClicked.emit()
        else:
            pass

    # signal processing ================================================
    def signalProcessing(self):
        """
        Connect signals to slots.
        """
        self.transposeButton.clicked.connect(lambda: self.transposeZClicked.emit())
        self.importFigButtons["new"].clicked.connect(lambda: self.addFigClicked.emit())
        self.importFigButtons["delete"].clicked.connect(
            lambda: self.deleteFigClicked.emit()
        )

        self.continueButton.clicked.connect(self.onContinueClicked)
