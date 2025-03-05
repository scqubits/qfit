from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QWidget, QLabel, QRadioButton, QSpinBox, QGroupBox, QPushButton
from typing import Tuple, Dict, Any, List

from qfit.models.data_structures import Tag
from qfit.widgets.data_extracting import ListView
from qfit.widgets.validated_line_edits import (
    MultiIntsLineEdit, MultiIntTuplesLineEdit
)

class LabelingView(QObject):
    """
    View for the labeling panels.

    Parameters
    ----------
    parent: QObject
        parent object
    uiGroups: Tuple[  
        Dict[str, QGroupBox], Dict[str, QRadioButton],  
        Dict[str, IntTupleLineEdit], Dict[str, QSpinBox],  
        Dict[str, QPushButton], ListView,  
        QLabel  
        ]
        All widgets related to the labeling panel, including the group boxes, 
        label mode radio buttons, bare and dressed label line edits, 
        extraction controls (new, delete, clear), and the list view for
        transitions, and the label for the bare label order.
    """
    tagChanged = Signal(Tag)
    subsysNames: List[str]

    def __init__(
        self,
        parent: QObject,
        uiGroups: Tuple[
            Dict[str, QGroupBox], Dict[str, QRadioButton],
            Dict[str, MultiIntTuplesLineEdit | QSpinBox], Dict[str, MultiIntsLineEdit| QSpinBox],
            Dict[str, QPushButton], ListView,
            QLabel
        ],
    ):
        super().__init__(parent)

        (
            self.groupBox, self.radioButtons, 
            self.bareLabels, self.dressedLabels,
            self.extractionCtrls, 
            self.extractionList,
            self.bareLabelOrder,
        ) = uiGroups
    
        self._modeSwitchSignalsConnects()
        self._tagChangedSignalConnects()

    # Initialization ===================================================
    def updateHS(self, subsysNames: List[str]):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the model will reinitialized by this method. It updates the 
        HilbertSpace object.

        Parameters  
        ----------
        subsysNames: List[str]
            names of the subsystems in the HilbertSpace object
        """
        self.subsysNames = subsysNames

    def dynamicalInit(self):
        """
        When the app is reloaded (new measurement data and hilbert space),
        the view will reinitialized by this method.
        """
        try: 
            self.subsysNames
        except AttributeError:
            raise AttributeError("subsysNames not set. Call updateHS before "
                                 "dynamicalInit.")
        self._initializeUI()

    def _initializeUI(self):
        """
        Set up the UI for the tagging panel:
        - In NO_TAG mode, switch off (hide) the bare and dressed tagging panels
        - Set the number and names of subsystems
        """
        self.groupBox["bare"].setVisible(False)
        self.groupBox["dressed"].setVisible(False)

        # the number of subsystems are used by the initial and final state line edits
        # to check the validity of the input
        self.bareLabels["initial"].setTupleLength(self.subsysCount)
        self.bareLabels["final"].setTupleLength(self.subsysCount)

        self.bareLabelOrder.setText(
            "* Indices ordered by: <br>"  # Three space to align with the label title
            + ", ".join(self.subsysNames)
        )

    # properties =======================================================
    @property
    def subsysCount(self) -> int:
        return len(self.subsysNames)

    # signal processing ================================================
    @Slot()
    def _emitTagChangedSignal(self):
        self.tagChanged.emit(self._currentTag())

    def _modeSwitchSignalsConnects(self):
        """
        Respond to the user switching between the three modes (no tag, bare tag, dressed tag)
        """
        # connect the radio buttons to the corresponding tagging panels
        # one for each mode
        self.radioButtons["bare"].toggled.connect(self._onBareRadioButtonToggled)
        self.radioButtons["dressed"].toggled.connect(self._onDressedRadioButtonToggled)
        self.radioButtons["no tag"].toggled.connect(self._onNoTagRadioButtonToggled)

    @Slot()
    def _onBareRadioButtonToggled(self):
        """
        Slot for bare button being toggled. If the bare button is checked, switch the
        UI to the bare tag page. Else, do nothing.
        """
        if self.radioButtons["bare"].isChecked():
            self.groupBox["bare"].setVisible(True)
            self.groupBox["dressed"].setVisible(False)
            self._emitTagChangedSignal()

    @Slot()
    def _onDressedRadioButtonToggled(self):
        """
        Slot for dressed button being toggled. If the dressed button is checked, switch the
        UI to the dressed tag page. Else, do nothing.
        """
        if self.radioButtons["dressed"].isChecked():
            self.groupBox["bare"].setVisible(False)
            self.groupBox["dressed"].setVisible(True)
            self._emitTagChangedSignal()

    @Slot()
    def _onNoTagRadioButtonToggled(self):
        """
        Slot for no tag button being toggled. If the no tag button is checked, switch the
        UI to the no tag page. Else, do nothing.
        """
        if self.radioButtons["no tag"].isChecked():
            self.groupBox["bare"].setVisible(False)
            self.groupBox["dressed"].setVisible(False)
            self._emitTagChangedSignal()

    # ------------------------------------------------------------------
    def _tagChangedSignalConnects(self):
        """
        Connect the signals for the bare and dressed tagging panels to the tagChanged signal.
        """
        self.bareLabels["initial"].editingFinished.connect(self._emitTagChangedSignal)
        self.bareLabels["final"].editingFinished.connect(self._emitTagChangedSignal)
        self.bareLabels["photons"].valueChanged.connect(lambda: self._emitTagChangedSignal())
        self.dressedLabels["initial"].editingFinished.connect(lambda: self._emitTagChangedSignal())
        self.dressedLabels["final"].editingFinished.connect(lambda: self._emitTagChangedSignal())
        self.dressedLabels["photons"].valueChanged.connect(
            self._emitTagChangedSignal
        )

    # settings =========================================================
    def blockAllSignals(self, block: bool):
        """
        For all widgets in the view, block or unblock the signals.
        """
        super().blockSignals(block)

        for values in self.radioButtons.values():
            values.blockSignals(block)
        for values in self.bareLabels.values():
            values.blockSignals(block)
        for values in self.dressedLabels.values():
            values.blockSignals(block)

    # data getters =====================================================
    def _isValidInitialBare(self):
        """
        Check if the input initial state is valid for bare-states tagging.
        """
        if not self.groupBox["bare"].isVisible():
            return True  # not visible, so no validation required
        if not self.bareLabels["initial"].isValid():
            return False
        return True

    def _isValidFinalBare(self):
        """
        Check if the input final state is valid for bare-states tagging.
        """
        if not self.groupBox["bare"].isVisible():
            return True  # not visible, so no validation required
        if not self.bareLabels["final"].isValid():
            return False
        return True
    
    def _isValidInitialDressed(self):
        """
        Check if the input initial state is valid for dressed-states tagging.
        """
        if not self.groupBox["dressed"].isVisible():
            return True  # not visible, so no validation required
        if not self.dressedLabels["initial"].isValid():
            return False
        return True

    def _isValidFinalDressed(self):
        """
        Check if the input final state is valid for dressed-states tagging.
        """
        if not self.groupBox["dressed"].isVisible():
            return True  # not visible, so no validation required
        if not self.dressedLabels["final"].isValid():
            return False
        return True

    def _isValid(self):
        """
        Check if the input tag is valid.
        """
        return (
            self._isValidInitialBare() 
            and self._isValidFinalBare()
            and self._isValidInitialDressed()
            and self._isValidFinalDressed()
        )
    
    def _currentTag(self) -> Tag:
        """
        Provide an external interface (outside of this class) to generate the tag from the view.
        It returns a tag based on the current view

        Returns
        -------
        tag: Tag
            tag data from the view
        """
        tag = Tag()
        # if no tag radio button selected, or the input for other tag types are invalid,
        # set the tag type to NO_TAG
        if self.radioButtons["no tag"].isChecked() or not self._isValid():
            tag.tagType = "NO_TAG"
        elif self.radioButtons["bare"].isChecked():
            tag.tagType = "DISPERSIVE_BARE"
            tag.initial = self.bareLabels["initial"].getTuples()
            tag.final = self.bareLabels["final"].getTuples()
            tag.photons = self.bareLabels["photons"].value()
        elif self.radioButtons["dressed"].isChecked():
            tag.tagType = "DISPERSIVE_DRESSED"
            tag.initial = self.dressedLabels["initial"].getInts()
            tag.final = self.dressedLabels["final"].getInts()
            tag.photons = self.dressedLabels["photons"].value()
        return tag
    
    # data setters =====================================================
    def _clear(self):
        """
        Clear all previous tag inputs in the UI.
        """
        self.bareLabels["initial"].clear()
        self.bareLabels["final"].clear()
        self.bareLabels["photons"].setValue(1)
        self.dressedLabels["initial"].clear()
        self.dressedLabels["final"].clear()
        self.dressedLabels["photons"].setValue(1)        

    @Slot(Tag)
    def replaceTag(self, tag: Tag):
        """
        Provide an external interface (outside of this class) to set the tag in the view.
        It sets the tag view based on the tag data.

        Parameters
        ----------
        tag: Tag
            tag data to be set in the view
        """
        # we have to block the modeSwitched/TagChanged signal to avoid multiple calls
        # but we still want to emit the signal from the radio buttons
        self.blockSignals(True)

        # clear the previous tag
        self._clear()

        # switch to the correct mode and set the tag
        if tag.tagType == "NO_TAG":
            self.radioButtons["no tag"].toggle()
        elif tag.tagType == "DISPERSIVE_BARE":
            self.radioButtons["bare"].toggle()
            self.bareLabels["initial"].setFromTuples(tag.initial)
            self.bareLabels["final"].setFromTuples(tag.final)
            self.bareLabels["photons"].setValue(tag.photons)
        elif tag.tagType == "DISPERSIVE_DRESSED":
            self.radioButtons["dressed"].toggle()
            self.dressedLabels["initial"].setFromInts(tag.initial)
            self.dressedLabels["final"].setFromInts(tag.final)
            self.dressedLabels["photons"].setValue(tag.photons)

        self.blockAllSignals(False)
