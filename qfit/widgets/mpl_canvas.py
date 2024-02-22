# mpl_canvas.py
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
from qfit.core.app_state import State
from qfit.utils.helpers import y_snap
from qfit.models.extracted_data import AllExtractedData

from typing import Union, Literal, Tuple


class MplNavButtons(QFrame):
    pass


class NavigationHidden(NavigationToolbar2QT):
    """
    Helper class to realize a MPL navigation toolbar without the buttons.
    """

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
        """
        Activate pan/zoom mode. on is a boolean. It first disconnects any
        prior callback set by setPanMode or setZoomMode. Then it will turn
        on the appropriate callback, and set the mode message accordingly.
        """
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
        """
        Activate zoom mode. on is a boolean. It first disconnects any
        prior callback set by setPanMode or setZoomMode. Then it will turn
        on the appropriate callback, and set the mode message accordingly.
        """
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
        self,
        ax,
        allExtractedData: AllExtractedData = None,
        x_snap_mode=None,
        axis_snap_mode: Union[None, Literal["X", "Y"]] = None,
        xy_min: Union[None, Tuple[float]] = None,
        horizOn=True,
        vertOn=True,
        useblit=False,
        **lineprops,
    ):
        super().__init__(
            ax, horizOn=horizOn, vertOn=vertOn, useblit=useblit, **lineprops
        )
        self.allExtractedData = allExtractedData
        self.x_snap_mode = x_snap_mode
        self.axis_snap_mode = axis_snap_mode
        self.xy_min = xy_min

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
        # x coordinate of the point
        if self.x_snap_mode == True:
            point_x_coordinate = self.closest_line(event.xdata)
        elif self.axis_snap_mode == "Y":
            point_x_coordinate = self.xy_min[0]
        else:
            point_x_coordinate = event.xdata
        # y coordinate of the point
        if self.axis_snap_mode == "X":
            point_y_coordinate = self.xy_min[1]
        else:
            point_y_coordinate = event.ydata
        self.cross = self.ax.scatter(
            point_x_coordinate,
            point_y_coordinate,
            c="red",
            marker=r"$\odot$",
            s=130,
            alpha=0.5,
            animated=True,
        )

        self.cross.set_visible(self.visible)
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()

    def closest_line(self, xdat):
        all_x_list = self.allExtractedData.distinctSortedXValues()
        allxdiff = {np.abs(xdat - i): i for i in all_x_list}
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


class MplFigureCanvas(QFrame):
    x_snap_mode: bool = False
    cross_hair_horizOn: bool = False
    cross_hair_vertOn: bool = False

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.allExtractedData = None
        self.canvas = FigureCanvasQTAgg(Figure())
        self.toolbar = NavigationHidden(self.canvas, self)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        self._crosshair = None

    def set_callback_for_extracted_data(self, new_extracted_data):
        self.allExtractedData = new_extracted_data
        # self.select_crosshair()

    def axes(self):
        return self.canvas.figure.axes[0]

    def select_crosshair(
        self,
        x_snap_mode: Union[bool, None] = None,
        axis_snap_mode: Union[None, Literal["X", "Y"]] = None,
        horizOn: Union[bool, None] = None,
        vertOn: Union[bool, None] = None,
    ):
        """
        set up the crosshair cursor. This class memorizes the state of the crosshair
        cursor when no arguments are passed.
        """
        if x_snap_mode is not None:
            self.x_snap_mode = x_snap_mode
        if horizOn is not None:
            self.cross_hair_horizOn = horizOn
        if vertOn is not None:
            self.cross_hair_vertOn = vertOn

        self._crosshair = SpecialCursor(
            self.axes(),
            allExtractedData=self.allExtractedData,
            x_snap_mode=self.x_snap_mode,
            axis_snap_mode=axis_snap_mode,
            xy_min=(self.axes().get_xlim()[0], self.axes().get_ylim()[0]),
            useblit=True,
            horizOn=self.cross_hair_horizOn,
            vertOn=self.cross_hair_vertOn,
            color="black",
            alpha=0.5,
        )
        self.canvas.draw()
        self._crosshair.line_blit_on()

    def zoomOn(self):
        self.toolbar.setZoomMode(
            on=True
        )  # toggle zoom at the level of the NavigationToolbar2QT, enabling actual
        # zoom functionality
        appstate.state = State.ZOOM
        self.select_crosshair(horizOn=False, vertOn=False)

    def panOn(self):
        self.toolbar.setPanMode(
            on=True
        )  # toggle pan at the level of the NavigationToolbar2QT, enabling actual
        # pan functionality
        appstate.state = State.PAN
        self.select_crosshair(horizOn=False, vertOn=False)

    def selectOn(self, showCrosshair=True):
        """
        On the view level, turning on the selection mode means showing
        the crosshair cursor.

        However, there is a situation where on a wrong
        page, clicking the selection button will not turn on the selection mode,
        so the crosshair cursor should be turned off.
        """
        self.toolbar.setZoomMode(on=False)
        self.toolbar.setPanMode(on=False)
        appstate.state = State.SELECT
        if showCrosshair:
            self.select_crosshair(horizOn=True, vertOn=True)
        else:
            self.select_crosshair(horizOn=False, vertOn=False)

    def calibrateOn(self):
        self.toolbar.setZoomMode(on=False)
        self.toolbar.setPanMode(on=False)
        # if strXY == "X":
        #     horizOn = False
        #     vertOn = True
        # else:
        #     horizOn = True
        #     vertOn = False
        # self.select_crosshair(axis_snap_mode=strXY, horizOn=horizOn, vertOn=vertOn)

    @Slot()
    def resetView(self):
        self.toolbar.home()

    @Slot()
    def zoomView(self):
        self.zoomOn()

    @Slot()
    def panView(self):
        self.panOn()
