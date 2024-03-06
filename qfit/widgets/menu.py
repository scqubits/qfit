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

from qfit.ui_designer.ui_menu import Ui_MenuWidget


class MenuWidget(QWidget):
    def __init__(self, parent):
        super(MenuWidget, self).__init__(parent)
        self.ui = Ui_MenuWidget()
        self.ui.setupUi(self)

        self.move(0, 32)
        self.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()
