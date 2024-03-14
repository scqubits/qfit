from PySide6.QtCore import (
    QObject,
    Slot,
)
from PySide6.QtWidgets import QPushButton


from typing import Dict

from qfit.widgets.gif_tooltip import DialogWindowWithMedia


class HelpButtonCtrl(QObject):
    """
    Controller for the helper push buttons. Once clicked, a window will pop up to show
    the corresponding help message. The help message is hard coded in the controller
    here.

    Relevant UI elements:
    - help buttons

    Relevant model:
    - None

    Parameters
    ----------
    parent : QObject
        parent object
    helpButtons : Dict[str, QPushButton]
        dictionary of help buttons with the key being the name of the button
    """

    def __init__(
        self,
        parent: QObject,    
        helpButtons: Dict[str, "QPushButton"],
    ):
        super().__init__(parent)

        self.helpButtons = helpButtons

        for button_name, help_button in self.helpButtons.items():
            # fetch the method
            help_method = getattr(self, button_name + "Help")
            help_button.clicked.connect(help_method)

    @Slot()
    def calibrationHelp(self):
        """
        Show the help message for the calibration stage
        """
        help_text = "<p style='line-height: 150%'>"
        help_text += "<b>Calibrate axes in 4 steps</b><br>"
        help_text += "(1) Click the calibration point selection button for x1.<br>"
        help_text += "(2) On the canvas, click on a position where the calibrated value x1' (e.g. half-flux point) is known.<br>"
        help_text += "(3) Enter the value x1' (e.g. 0.5).<br>"
        help_text += "(4) Repeat above for x2, y1, y2."
        help_text += "</p>"
        tutorial_dialog = DialogWindowWithMedia(
            help_text,
            [
                (":/images/calibration_new.png", 800),
            ],
        )
        tutorial_dialog.exec()

    @Slot()
    def fitHelp(self):
        """
        Show the help message for the fitting stage
        """
        help_text = "<p style='line-height: 150%'>"
        help_text += "<b>Name</b>: name of the parameter. <br>"
        help_text += "<b>Fix</b>: toggle on to fix the parameter at the initial value during the fitting process. <br>"
        help_text += "<b>Initial</b>: initial value of the parameter. <br>"
        help_text += (
            "<b>Min</b>: the lower bound of the parameter for the fitting. <br>"
        )
        help_text += (
            "<b>Max</b>: the upper bound of the parameter for the fitting. <br>"
        )
        help_text += "<b>Current</b>: value of the parameter when the fitting process is finished."
        help_text += "</p>"
        tutorial_dialog = DialogWindowWithMedia(
            help_text,
        )
        tutorial_dialog.exec()


    @Slot()
    def numericalSpectrumSettingsHelp(self):
        """
        Show the help message for the numerical spectrum settings
        """
        help_text = "<p style='line-height: 150%'>"
        help_text += "<b>TRANSITIONS</b>: subsystem for which the simulated transition frequencies are to be extracted. <br>"
        help_text += "<b>INITIAL STATES</b>: the initial state to be considered for transitions. Dressed or bare labels are acceptable. <br>"
        help_text += (
            "<b>PHOTONS</b>: number of photons (N) involved in the process.<br>"
        )
        help_text += "                The simulated transition frequency = (difference in eigenenergies)/N <br>"
        help_text += "<b>EVALS COUNT</b>: number of eigenstates and eigenvalues to be computed. <br>"
        help_text += "<b>POINTS ADDED</b>: additional swept parameter sampling points displayed on the simulated transition spectrum."
        help_text += "</p>"
        tutorial_dialog = DialogWindowWithMedia(
            help_text,
        )
        tutorial_dialog.exec()
