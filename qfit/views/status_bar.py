from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import QStatusBar, QLabel
from typing import Tuple, Dict, Any, Union, List
import time


class StatusBarView(QObject):
    def __init__(
        self,
        statusBar: QStatusBar,
    ):
        """
        All widgets related to tagging.
        """
        super().__init__()

        self.statusBar = statusBar
        self.statusBarLabel = QLabel()

        self._initializeUI()

    # Initialization ===================================================
    def _initializeUI(self):
        """
        Initialize the status bar message.
        """
        self.statusBar.addWidget(self.statusBarLabel)
        self.statusBarLabel.setText("No computation carried out yet.")
        # set style sheet (here in the future)

    @Slot(str)
    def updateNormalMessage(self, message: str):
        """
        Update the status bar message, based on the message type

        Parameters
        ----------
        message : str
            The message to be displayed, including any formatting (subscripts, superscripts, etc.)
        """
        self.statusBarLabel.setText(message)

    @Slot(str, float)
    def updateTempMessage(self, message: str, messageDuration: float):
        self.statusBar.showMessage(message, messageDuration * 1000)
        # when the message is done, reset the status bar message
        # wait for messageDuration*1000 ms manually
        # time.sleep(messageDuration)
        # self.statusBar.clearMessage()
