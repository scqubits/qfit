from PySide6.QtCore import (
    QObject,
    Slot,
)
from PySide6.QtWidgets import QPushButton


from typing import Dict

from qfit.widgets.gif_tooltip import DialogWindowWithMedia


class HelpButtonCtrl(QObject):
    def __init__(
        self,
        helpButtons: Dict[str, "QPushButton"],
        *args,
        **kwargs,
    ):
        """
        Controller for the helper push buttons. Once clicked, a window will pop up to show
        the corresponding help message. The help message is hard coded in the controller
        here.

        Relevant UI elements:
        - help buttons

        Relevant model:
        - None

        ARGUMENTS
        ---------
        helpbuttons: Dict[str, QPushButton]
            dictionary of help buttons
        additional arguments are passed to QObject.__init__()
        """
        super().__init__(*args, **kwargs)

        self.helpButtons = helpButtons

        for button_name, help_button in self.helpButtons.items():
            # fetch the method
            help_method = getattr(self, button_name + "Help")
            help_button.clicked.connect(help_method)

    @Slot()
    def calibrationHelp(self):
        tutorial_dialog = DialogWindowWithMedia(
            "test",
            [
                (":/gifs/calibration_gif.gif", 600),
                (":/images/calibration_x1x2y1y2.png", 400),
            ],
        )
        tutorial_dialog.exec()

    @Slot()
    def fitHelp(self):
        tutorial_dialog = DialogWindowWithMedia(
            "test",
            [
                (":/gifs/calibration_gif.gif", 600),
                (":/images/calibration_x1x2y1y2.png", 400),
            ],
        )
        tutorial_dialog.exec()

    @Slot()
    def prefitResultHelp(self):
        tutorial_dialog = DialogWindowWithMedia(
            "test",
            [
                (":/gifs/calibration_gif.gif", 600),
                (":/images/calibration_x1x2y1y2.png", 400),
            ],
        )
        tutorial_dialog.exec()

    @Slot()
    def fitResultHelp(self):
        tutorial_dialog = DialogWindowWithMedia(
            "test",
            [
                (":/gifs/calibration_gif.gif", 600),
                (":/images/calibration_x1x2y1y2.png", 400),
            ],
        )
        tutorial_dialog.exec()

    @Slot()
    def numericalSpectrumSettingsHelp(self):
        tutorial_dialog = DialogWindowWithMedia(
            "test",
            [
                (":/gifs/calibration_gif.gif", 600),
                (":/images/calibration_x1x2y1y2.png", 400),
            ],
        )
        tutorial_dialog.exec()
