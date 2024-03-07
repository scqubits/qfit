from PySide6.QtCore import QObject
from PySide6.QtWidgets import QPushButton

from qfit.widgets.settings import SettingsWidget
from typing import TYPE_CHECKING, Union, Dict, Any, Optional, List

class SettingsCtrl(QObject):
    """
    This controller handles the settings widget. Specifically its connections and
    logics for the settings widget.
    """

    def __init__(
        self,
        parent: QObject,
        settingsWidget: SettingsWidget,
        settingsButton: QPushButton,
    ):
        super().__init__(parent)
        
        self.settingsWidget = settingsWidget
        self.settingsButton = settingsButton
        self.uiSettingsConnects()

    def uiSettingsConnects(self):
        self.settingsButton.clicked.connect(self.settingsWidget.toggle)
        self.settingsWidget.ui.settingsCloseButton.clicked.connect(
            self.settingsWidget.hide
        )
