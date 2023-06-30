# mpl_navbuttons.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################



from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget


from qfit.ui_designer.ui_mpl_navbuttons import Ui_MplNavButtons
from qfit.widgets.mpl_canvas import MplFigureCanvas


class MplNavButtons(QWidget):
    def __init__(self, parent: MplFigureCanvas):
        super(MplNavButtons, self).__init__(parent)
        self._mplFigureCanvas = parent

        self.ui = Ui_MplNavButtons()
        self.ui.setupUi(self)

        for button in [
            self.ui.zoomViewButton,
            self.ui.resetViewButton,
            self.ui.panViewButton,
            self.ui.selectViewButton,
            self.ui.swapXYButton,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)

    def set_connections(self):
        """Connect the UI buttons for reset, zoom, and pan functions of the matplotlib canvas."""
        self.ui.resetViewButton.clicked.connect(self._mplFigureCanvas.resetView)
        self.ui.zoomViewButton.clicked.connect(self._mplFigureCanvas.toggleZoom)
        self.ui.panViewButton.clicked.connect(self._mplFigureCanvas.togglePan)
        self.ui.selectViewButton.clicked.connect(self._mplFigureCanvas.toggleSelect)
        self.ui.swapXYButton.clicked.connect(self._mplFigureCanvas.swapXY)