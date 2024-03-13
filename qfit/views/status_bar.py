from PySide6.QtCore import (
    QObject,
    Slot,
    Qt,
)
from PySide6.QtWidgets import QStatusBar, QLabel, QSizePolicy


class StatusBarView(QObject):
    """
    A view for the status bar.

    Parameters
    ----------
    parent : QObject
        The parent object.
    statusBar : QStatusBar
        The status bar.
    """
    def __init__(
        self,
        parent: QObject,
        statusBar: QStatusBar,
    ):
        """
        All widgets related to tagging.
        """
        super().__init__(parent)

        self.statusBar = statusBar
        self.statusBarLabel = QLabel()
        # self.statusBarLabel.setFixedWidth(900)
        self.statusBarLabel.setMinimumWidth(1000)
        self.statusBarLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.statusBarLabel.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        self.statusBarLabel.setStyleSheet(
            "padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px;"
        )
        self.statusBarLabel.setWordWrap(True)

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
