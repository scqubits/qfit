from PySide6.QtWidgets import (
    QPushButton,
)

from qfit.widgets.settings import SettingsWidget
from typing import TYPE_CHECKING, Union, Dict, Any, Optional, List

class SettingsCtrl:
    """
    This controller handles the settings widget. Specifically its connections and
    logics for the settings widget.
    """

    def __init__(
        self,
        settingsWidget: SettingsWidget,
        settingsButton: QPushButton,
    ):
        self.settingsWidget = settingsWidget
        self.settingsButton = settingsButton
        self.uiSettingsConnects()

    def uiSettingsConnects(self):
        self.settingsButton.clicked.connect(self.settingsWidget.toggle)
        self.settingsWidget.ui.settingsCloseButton.clicked.connect(
            self.settingsWidget.hide
        )
