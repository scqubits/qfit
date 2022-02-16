# canvas_view.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import numpy as np

from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame, QVBoxLayout

from matplotlib.backend_bases import cursors
from matplotlib.backends.backend_qtagg import (
    FigureCanvas as FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor


import qfit.core.app_state as appstate
from qfit.data.extracted_data import AllExtractedData

from qfit.core.app_state import State


class NavigationHidden(NavigationToolbar2QT):
    # only connect to external buttons
    toolitems = [
        t for t in NavigationToolbar2QT.toolitems if t[0] in ("Home", "Pan", "Zoom")
    ]

    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates=False)
        self.set_cursor(cursors.SELECT_REGION)
        self._idPress = None
        self._idRelease = None

    def _init_toolbar(self):
        pass

    def _update_buttons_checked(self):
        pass

    def setPanMode(self, on=True):
        if on:
            self._active = "PAN"
        else:
            self._active = None

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ""
        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ""

        if on:
            self._idPress = self.canvas.mpl_connect(
                "button_press_event", self.press_pan
            )
            self._idRelease = self.canvas.mpl_connect(
                "button_release_event", self.release_pan
            )
            self.mode = "pan/zoom"
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)

        self.set_message(self.mode)

    def setZoomMode(self, on=True):
        if on:
            self._active = "ZOOM"
        else:
            self._active = None

        if self._idPress is not None:
            self._idPress = self.canvas.mpl_disconnect(self._idPress)
            self.mode = ""
        if self._idRelease is not None:
            self._idRelease = self.canvas.mpl_disconnect(self._idRelease)
            self.mode = ""

        if on:
            self._idPress = self.canvas.mpl_connect(
                "button_press_event", self.press_zoom
            )
            self._idRelease = self.canvas.mpl_connect(
                "button_release_event", self.release_zoom
            )
            self.mode = "zoom rect"
            self.canvas.widgetlock(self)
        else:
            self.canvas.widgetlock.release(self)

        for a in self.canvas.figure.get_axes():
            a.set_navigate_mode(self._active)
        self.set_message(self.mode)

    def set_cursor(self, cursor):
        self.canvas.setCursor(QtCore.Qt.CrossCursor)


class SpecialCursor(Cursor):
    def __init__(
        self, ax, callback=None, horizOn=True, vertOn=True, useblit=False, **lineprops
    ):
        super().__init__(
            ax, horizOn=horizOn, vertOn=vertOn, useblit=useblit, **lineprops
        )
        self.callback = callback
        self.matching_mode = False

    def onmove(self, event):
        """Internal event handler to draw the cursor when the mouse moves."""
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible:
            return
        self.linev.set_xdata((event.xdata, event.xdata))

        self.lineh.set_ydata((event.ydata, event.ydata))
        if (
            self.callback
            and self.callback.currentRow != 0
            and len(self.callback.assocDataList[0][0]) > 0
        ):
            self.matching_mode = True
        if self.matching_mode == True:
            self.cross = self.ax.scatter(
                self.closest_line(event.xdata),
                event.ydata,
                c="red",
                marker="x",
                s=150,
                animated=True,
            )
        else:
            self.cross = self.ax.scatter(
                event.xdata, event.ydata, c="red", marker="x", s=150, animated=True
            )

        self.cross.set_visible(self.visible)
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()

    def closest_line(self, xdat):
        current_data = self.callback.assocDataList[0]
        allxdiff = {np.abs(xdat - i): i for i in current_data[0]}
        if allxdiff:
            return allxdiff[min(allxdiff.keys())]
        else:
            return xdat

    def _update(self):
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.linev)
            self.ax.draw_artist(self.lineh)
            self.ax.draw_artist(self.cross)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()
        return False

    def line_blit_on(self):
        self.line_blit = True

    def line_blit_off(self):
        self.line_blit = False


class FigureCanvas(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.callback = None
        self.canvas = FigureCanvasQTAgg(Figure())
        self.toolbar = NavigationHidden(self.canvas, self)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        self._crosshair = None

    def set_callback(self, new_callback):
        self.callback = new_callback
        self.select_crosshair()

    def axes(self):
        return self.canvas.figure.axes[0]

    def select_crosshair(self, horizOn=True, vertOn=True):
        self._crosshair = SpecialCursor(
            self.axes(),
            callback=self.callback,
            useblit=True,
            horizOn=horizOn,
            vertOn=vertOn,
            color="black",
            linewidth=1,
        )
        self.canvas.draw()
        self._crosshair.line_blit_on()

    def zoomOn(self):
        self.toolbar.setZoomMode(
            on=True
        )  # toggle zoom at the level of the NavigationToolbar2QT, enabling actual
        # zoom functionality
        appstate.state = State.ZOOM
        self.select_crosshair()

    def panOn(self):
        self.toolbar.setPanMode(
            on=True
        )  # toggle pan at the level of the NavigationToolbar2QT, enabling actual
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
        if strXY == "X":
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
