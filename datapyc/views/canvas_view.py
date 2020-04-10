# canvas_view.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from PySide2 import QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QFrame, QVBoxLayout
from matplotlib.backend_bases import cursors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor

import datapyc.core.app_state as appstate
from datapyc.core.app_state import State


class NavigationHidden(NavigationToolbar2QT):
    # only connect to external buttons
    toolitems = [t for t in NavigationToolbar2QT.toolitems if t[0] in ('Home', 'Pan', 'Zoom')]

    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates=False)
        self.set_cursor(cursors.SELECT_REGION)

    def _init_toolbar(self):
        pass

    def _update_buttons_checked(self):
        pass

    def setPanMode(self, on=True):
        if on:
            self._active = 'PAN'
        else:
            self._active = None

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ''
        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ''

        if on:
            self._idPress = self.canvas.mpl_connect('button_press_event', self.press_pan)
            self._idRelease = self.canvas.mpl_connect('button_release_event', self.release_pan)
            self.mode = 'pan/zoom'
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)

    def setZoomMode(self, on=True):
        if on:
            self._active = 'ZOOM'
        else:
            self._active = None

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ''
        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ''

        if on:
            self._idPress = self.canvas.mpl_connect('button_press_event', self.press_zoom)
            self._idRelease = self.canvas.mpl_connect('button_release_event', self.release_zoom)
            self.mode = 'zoom rect'
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)
        self.set_message(self.mode)

    def set_cursor(self, cursor):
        self.canvas.setCursor(QtCore.Qt.CrossCursor)


class FigureCanvas(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.canvas = FigureCanvasQTAgg(Figure())
        self.toolbar = NavigationHidden(self.canvas, self)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        self._crosshair = None

    def axes(self):
        return self.canvas.figure.axes[0]

    def select_crosshair(self, horizOn=True, vertOn=True):
        self._crosshair = Cursor(self.axes(), useblit=True, horizOn=horizOn, vertOn=vertOn, color='black', linewidth=1)
        self.canvas.draw()

    def zoomOn(self):
        self.toolbar.setZoomMode(on=True)  # toggle zoom at the level of the NavigationToolbar2QT, enabling actual
                                          # zoom functionality
        appstate.state = State.ZOOM
        self.select_crosshair()

    def panOn(self):
        self.toolbar.setPanMode(on=True)  # toggle pan at the level of the NavigationToolbar2QT, enabling actual
                                          # pan functionality
        appstate.state = State.PAN
        self.select_crosshair()

    def selectOn(self):
        self.toolbar.setZoomMode(on=False)
        self.toolbar.setPanMode(on=False)
        appstate.state = State.SELECT
        self.select_crosshair()

    def calibrateOn(self, strXY):
        self.toolbar.setZoomMode(on=False)
        self.toolbar.setPanMode(on=False)
        if strXY == 'X':
            horizOn = False
            vertOn = True
        else:
            horizOn = True
            vertOn = False
        self.select_crosshair(horizOn=horizOn, vertOn=vertOn)

    @Slot()
    def resetView(self):
        self.toolbar.home()

    @Slot()
    def zoomView(self):
        self.zoomOn()

    @Slot()
    def panView(self):
        self.panOn()
