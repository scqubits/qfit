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
        xSnapMode: bool,
        xSnapValues: np.ndarray,
        axisSnapMode: Union[None, Literal["X", "Y"]] = None,
        xyMin: Union[None, Tuple[float]] = None,
        horizOn=True,
        vertOn=True,
        useblit=False,
        **lineprops,
    ):
        """
        Parameters:
        -----------
        ax: Axes
            The Axes to attach the cursor to.
        x_snap_mode: bool
            Whether to snap the cursor to the closest x value in the list of all x values
        x_snap_values: np.ndarray
            The list of all x values
        axis_snap_mode: Union[None, Literal["X", "Y"]]
            Whether to snap the cursor to the minimum x or y value (edge of the plot)
        xy_min: Union[None, Tuple[float]]
            The minimum x and y values
        horizOn: bool
            Whether to show the horizontal line
        vertOn: bool
            Whether to show the vertical line
        useblit: bool
            Whether to use blitting for faster drawing
        """
        super().__init__(
            ax, horizOn=horizOn, vertOn=vertOn, useblit=useblit, **lineprops
        )
        self.xSnapMode = xSnapMode
        self.xSnapValues = xSnapValues

        self.axis_snap_mode = axisSnapMode
        self.xyMin = xyMin

    def onmove(self, event):
        """
        Internal event handler to draw the cursor when the mouse moves.
        
        When the mouse moves, the cursor (a scatter plot) is drawn at the
        closest x value in the list of all x values.
        """
        if self.ignore(event):
            return
        
        if not self.canvas.widgetlock.available(self):
            return
        
        if event.inaxes != self.ax:
            # Hide the vertical and horizontal lines when the mouse is outside the axes
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        
        self.needclear = True
        
        if not self.visible:
            return
        
        # Update the vertical line position based on the mouse x-coordinate
        self.linev.set_xdata((event.xdata, event.xdata))

        # Update the horizontal line position based on the mouse y-coordinate
        self.lineh.set_ydata((event.ydata, event.ydata))
        
        # Calculate the x-coordinate of the point based on the snapping mode and axis snap mode
        if self.xSnapMode == True:
            point_x_coordinate = self.closest_line(event.xdata)
        elif self.axis_snap_mode == "Y":
            point_x_coordinate = self.xyMin[0]
        else:
            point_x_coordinate = event.xdata
        
        # Calculate the y-coordinate of the point based on the axis snap mode
        if self.axis_snap_mode == "X":
            point_y_coordinate = self.xyMin[1]
        else:
            point_y_coordinate = event.ydata
        
        # Draw the cursor (a scatter plot) at the calculated coordinates
        self.cross = self.ax.scatter(
            point_x_coordinate,
            point_y_coordinate,
            c="red",
            marker=r"$\odot$",
            s=130,
            alpha=0.5,
            animated=True,
        )

        # Set the visibility of the cursor and lines
        self.cross.set_visible(self.visible)
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        # Update the canvas to reflect the changes
        self._update()

    def closest_line(self, xdat):
        """
        Find the closest x value in the list of all x values
        """
        allxdiff = {np.abs(xdat - i): i for i in self.xSnapValues}
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
    axis_snap_mode: Union[None, Literal["X", "Y"]] = None

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.cursorXSnapValues = np.array([])
        self.canvas = FigureCanvasQTAgg(Figure())
        self.toolbar = NavigationHidden(self.canvas, self)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        self._crosshair = None

    # Properties =======================================================
    def axes(self):
        return self.canvas.figure.axes[0]
    
    # View Manipulation ================================================
    def updateCrosshair(
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
        if axis_snap_mode is not None:
            self.axis_snap_mode = axis_snap_mode

        self._crosshair = SpecialCursor(
            self.axes(),
            xSnapMode = self.x_snap_mode,
            xSnapValues = self.cursorXSnapValues,
            axisSnapMode = self.axis_snap_mode,
            xyMin = (self.axes().get_xlim()[0], self.axes().get_ylim()[0]),
            useblit = True,
            horizOn = self.cross_hair_horizOn,
            vertOn = self.cross_hair_vertOn,
            color = "black",
            alpha = 0.5,
        )
        self.canvas.draw()
        self._crosshair.line_blit_on()

    def zoomOn(self):
        self.toolbar.setZoomMode(
            on=True
        )  # toggle zoom at the level of the NavigationToolbar2QT, enabling actual
        # zoom functionality
        appstate.state = State.ZOOM
        self.updateCrosshair(horizOn=False, vertOn=False)

    def panOn(self):
        self.toolbar.setPanMode(
            on=True
        )  # toggle pan at the level of the NavigationToolbar2QT, enabling actual
        # pan functionality
        appstate.state = State.PAN
        self.updateCrosshair(horizOn=False, vertOn=False)

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
            self.updateCrosshair(horizOn=True, vertOn=True)
        else:
            self.updateCrosshair(horizOn=False, vertOn=False)

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

    @Slot()
    def updateCursorXSnapValues(self, newCursorXSnapValues: np.ndarray):
        self.cursorXSnapValues = newCursorXSnapValues
        self.updateCrosshair()
    
    # Signal Processing ================================================
    