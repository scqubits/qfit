# menu.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFocusEvent
from PySide6.QtCore import Qt

from qfit.ui_designer.ui_menu import Ui_MenuWidget


class MenuWidget(QWidget):
    """
    A floating menu widget that is shown when the user clicks the menu button.
    """
    def __init__(self, parent):
        super(MenuWidget, self).__init__(parent)
        self.ui = Ui_MenuWidget()
        self.ui.setupUi(self)

        self.move(0, 60)
        self.hide()

    def toggle(self):
        if self.isHidden():
            self.setFocus(Qt.OtherFocusReason)
            self.show()
        else:
            self.hide()

    def focusOutEvent(self, event: QFocusEvent) -> None:
        """
        Overriding the QFocusEvent handler to hide the widget when it loses focus.
        """
        if event.lostFocus():
            self.hide()
