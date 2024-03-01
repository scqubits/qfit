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
import copy
import warnings
from typing import Union, Literal, Tuple, Dict, Any, List

from PySide6 import QtCore
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame, QVBoxLayout

from matplotlib.backend_bases import cursors
from matplotlib.backends.backend_qtagg import (
    FigureCanvas as FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib.cm as cm

from qfit.utils.helpers import y_snap

from qfit.models.data_structures import PlotElement
from qfit.settings import color_dict



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

    def __init__(
        self, 
        canvas: FigureCanvasQTAgg, 
        parent: "MplFigureCanvas", 
    ):
        super().__init__(canvas, parent, coordinates=False)
        self.set_cursor(cursors.SELECT_REGION)
        self._idPress = None
        self._idRelease = None

    def _init_toolbar(self):
        pass

    def _update_buttons_checked(self):
        pass

    # override the default mpl keypress callback
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

    def release_zoom(self, event):
        """
        The x and y limits of the axes can only be changed by zoom, pan, or
        home buttons. To do this, we need to record the x and y limits of the
        axes after each zoom/pan/home action. The recorded x and y limits 
        will be used when the plot element is updated.
        """
        super().release_zoom(event)
        self.parent()._recordXYLim()

    def release_pan(self, event):
        """
        See release_zoom
        """
        super().release_pan(event)
        self.parent()._recordXYLim()

    def home(self):
        """
        See release_zoom
        """
        super().home()
        self.parent()._recordXYLim()


class SpecialCursor(Cursor):
    def __init__(
        self,
        axes: List[Axes],
        xSnapMode: bool,
        xSnapValues: np.ndarray,
        xyMin: Tuple[float, float],
        axisSnapMode: Literal["X", "Y", "OFF"] = "OFF",
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
        xSnapMode: bool
            Whether to snap the cursor to the closest x value in the list of all x values
        xSnapValues: np.ndarray
            The list of all x values
        axisSnapMode: Literal["X", "Y", "OFF"]
            Whether to snap the cursor to the minimum x or y value (edge of the plot).
            It overrides xSnapMode.
        xyMin: Tuple[float, float]
            The minimum x and y values
        horizOn: bool
            Whether to show the horizontal line
        vertOn: bool
            Whether to show the vertical line
        useblit: bool
            Whether to use blitting for faster drawing
        """
        super().__init__(
            axes[0], horizOn=horizOn, vertOn=vertOn, useblit=useblit, **lineprops
        )
        self.allAxes = axes
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
        
        if event.inaxes not in self.allAxes:
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
        if self.axis_snap_mode == "Y":
            point_x_coordinate = self.xyMin[0]
        elif self.xSnapMode == True:
            point_x_coordinate = self.closest_line(event.xdata)
        else:
            point_x_coordinate = event.xdata
        
        # Calculate the y-coordinate of the point based on the axis snap mode
        if self.axis_snap_mode == "X":
            point_y_coordinate = self.xyMin[1]
        else:
            point_y_coordinate = event.ydata

        # remove the old cursor
        if hasattr(self, 'cross'):
            self.cross.remove()
        
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
        if self.xSnapValues is None or len(self.xSnapValues) == 0:
            return xdat
        
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

    def remove(self):
        self.linev.remove()
        self.lineh.remove()
        if hasattr(self, 'cross'):
            self.cross.remove()


class MplFigureCanvas(QFrame):

    specialCursor: SpecialCursor

    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        # View elements
        self.cursorXSnapValues = np.array([])
        self.canvas = FigureCanvasQTAgg(Figure())
        self.toolbar = NavigationHidden(self.canvas, self)

        # initialize the layout
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        # initialize the properties
        
        self.initializeProperties()

    def initializeProperties(self):
        self.canvas.figure.subplots()
        self.axes.autoscale(enable=False)

        # remove the default x- and y-axis
        self.axes.spines['bottom'].set_visible(False)
        self.axes.xaxis.set_ticks([])
        self.axes.set_xticklabels([])
        self.axes.spines['left'].set_visible(False)
        self.axes.yaxis.set_ticks([])
        self.axes.set_yticklabels([])

        # the axes for displaying the x & y values
        self.xAxes: List[Axes] = []
        self.yAxes: List[Axes] = []
        self._plottingElements: Dict[str, PlotElement] = {}

        self.plottingDisabled: bool = False

        self.xSnapMode: bool = False
        self.crosshairHorizOn: bool = False
        self.crosshairVertOn: bool = False
        self.axisSnapMode: Literal["X", "Y", "OFF"] = "OFF"

        self.colorMapStr: str = "PuOr"
        self._updateElementColors()

        self.xLim: Tuple[float, float] = (0, 1)
        self.yLim: Tuple[float, float] = (0, 1)
        self.measXLim: Tuple[float, float] = (0, 1)
        self.measYLim: Tuple[float, float] = (0, 1)

        # should be call at the end - it will make use of other properties like 
        # coloring

    # Properties =======================================================
    @property
    def axes(self) -> Axes:
        return self.canvas.figure.axes[0]
    
    @Slot()
    def updateColorMap(self, colorMap: str):
        self.colorMapStr = colorMap
        self._updateElementColors()
        self.plotAllElements()

    def _updateElementColors(self):
        """
        According to the color map, update the colors of the elements. 
        It won't redraw the elements, but wait for the next updateAllElements() call.
        """
        self.crossColor = color_dict[self.colorMapStr]["Cross"]
        self.lineColor = color_dict[self.colorMapStr]["line"]
        self.scatterColor = color_dict[self.colorMapStr]["Scatter"]
        self.cmap = copy.copy(getattr(cm, self.colorMapStr))

    # View Manipulation: Axes ==========================================
    def _setMeasXYLim(self, xLim: Tuple[float, float], yLim: Tuple[float, float]):
        """
        When click the reset button, we want to reset to the previous x 
        and y limits determined by the measurement data. This method records
        the x and y limits of the axes when the measurement data is loaded.
        """
        self.measXLim = xLim
        self.measYLim = yLim

    def _recordXYLim(self):
        """
        When update the other plotting elements, we want to keep the 
        previous x and y limits of the axes unchanged. This method records
        the x and y limits of the axes.

        It will be called when:
        1. the view is initializes/reset internally, for example, 
            when the measurement data is loaded / transposed
        2. the view's x and y limits are zoomed/panned/reset externally
        """
        self.xLim = self.axes.get_xlim()
        self.yLim = self.axes.get_ylim()

    def _restoreXYLim(self, byMeasData: bool = False):
        """
        Keep the x and y limits of the axes unchanged.
        It will be called when the plot elements are updated and the x and y limits
        are automatically changed by matplotlib.
        """
        if byMeasData:
            self.axes.set_xlim(*self.measXLim)
            self.axes.set_ylim(*self.measYLim)
        else:
            self.axes.set_xlim(*self.xLim)
            self.axes.set_ylim(*self.yLim)

    @Slot()
    def relim(self, xLim: Tuple[float, float], yLim: Tuple[float, float]):
        """
        Set the x and y limits of the axes to fit the measurement data
        """        
        self._setMeasXYLim(xLim, yLim)
        self._restoreXYLim(byMeasData=True)
        self._recordXYLim()

    def updateXAxes(self, xAxes: Dict[str, Tuple[float, float]]):
        """
        Update the x-axes value. 
        """
        for ax in self.xAxes:
            self.canvas.figure.delaxes(ax)

        # Create a new axes for each x-values in the dictionary
        new_axes = []
        for i, (xName, xRange) in enumerate(xAxes.items()):
            ax = self.axes.twiny()
            ax.set_xlim(*xRange)
            ax.set_xlabel(xName)
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_label_position('bottom')
            ax.spines['bottom'].set_position(('outward', 40 * i))
            # ax.xaxis.set_label_coords(1.05, -0.08 * (i))  # set label position
            new_axes.append(ax)
        self.xAxes = new_axes

        # self.canvas.figure.tight_layout()
        self.updateCursor()
        self.canvas.draw()

    def updateYAxes(self, yName: str, yRange: Tuple[float, float]):
        """
        Update the y-axes. (there is only one y-axis)
        """
        for ax in self.yAxes:
            self.canvas.figure.delaxes(ax)

        # Create a new axes for each x-values in the dictionary
        ax = self.axes.twinx()
        ax.set_ylim(*yRange)
        ax.set_ylabel(yName)
        ax.yaxis.set_ticks_position('left')
        ax.yaxis.set_label_position('left')
        ax.spines['left'].set_position(('outward', 40 * 0))
        # ax.yaxis.set_label_coords(1.05, -0.08 * (i))  # set label position
        self.yAxes = [ax]

        # self.canvas.figure.tight_layout()
        self.updateCursor()
        self.canvas.draw()

    # View Manipulation: Cursor ========================================
    def updateCursor(
        self,
        xSnapMode: Union[bool, None] = None,
        axisSnapMode: Literal["X", "Y", "OFF"] = "OFF",
        horizOn: Union[bool, None] = None,
        vertOn: Union[bool, None] = None,
    ):
        """
        set up the crosshair cursor. This class memorizes the state of the crosshair
        cursor when no arguments are passed.

        Parameters:
        -----------
        x_snap_mode: Union[bool, None]
            Whether to snap the cursor to the closest x value in the list of all x values
        axis_snap_mode: Union[None, Literal["X", "Y"]]
            Whether to snap the cursor to the minimum x or y value (edge of the plot),
            it overrides x_snap_mode
        horizOn: Union[bool, None]
            whether to show the horizontal line
        vertOn: Union[bool, None]
            whether to show the vertical line
        """
        # memorize the state of the crosshair cursor
        if xSnapMode is not None:
            self.xSnapMode = xSnapMode
        if horizOn is not None:
            self.crosshairHorizOn = horizOn
        if vertOn is not None:
            self.crosshairVertOn = vertOn
        self.axisSnapMode = axisSnapMode

        # remove the old cursor
        if hasattr(self, "specialCursor"):
            self.specialCursor.remove()

        self.specialCursor = SpecialCursor(
            [self.axes] + self.xAxes + self.yAxes,
            xSnapMode = self.xSnapMode,
            xSnapValues = self.cursorXSnapValues,
            xyMin = (self.axes.get_xlim()[0], self.axes.get_ylim()[0]),
            axisSnapMode = self.axisSnapMode,
            useblit = True,
            horizOn = self.crosshairHorizOn,
            vertOn = self.crosshairVertOn,
            color = self.crossColor,
            alpha = 0.5,
        )
        self.canvas.draw()
        self.specialCursor.line_blit_on()

    def zoomOn(self):
        self.toolbar.setZoomMode(
            on=True
        )  # toggle zoom at the level of the NavigationToolbar2QT, enabling actual
        # zoom functionality
        self.updateCursor(horizOn=False, vertOn=False)

    def panOn(self):
        self.toolbar.setPanMode(
            on=True
        )  # toggle pan at the level of the NavigationToolbar2QT, enabling actual
        # pan functionality
        self.updateCursor(horizOn=False, vertOn=False)

    def selectOn(self):
        self.toolbar.setZoomMode(on=False)
        self.toolbar.setPanMode(on=False)

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
        self.updateCursor()        

    # View Manipulation: Plotting ======================================
    # toolbox
    def _checkElementName(self, name: str):
        """
        Check whether the element name is valid
        """
        if name not in [
            "measurement", 
            "active_extractions",
            "all_extractions",
            "extraction_vlines",
            "spectrum"
        ]:
            raise ValueError(
                f"Invalid element name: {name}. "
            )    
        
    def _hasElement(self, elementName: str) -> bool:
        """
        Check whether the element is in the plotting elements dictionary
        """
        self._checkElementName(elementName)
        return elementName in self._plottingElements.keys()
        
    def _coloringKwargs(self, elementName: str) -> Dict[str, Any]:
        """
        For different elements, they accept different coloring kwargs.
        """
        self._checkElementName(elementName)

        if elementName == "measurement":
            return {"cmap": self.cmap}
        elif elementName == "active_extractions":
            return {"color": self.scatterColor}
        elif elementName == "all_extractions":
            return {"color": self.scatterColor}
        elif elementName == "extraction_vlines":
            return {"color": self.lineColor}
        else:
            return {} 
        
    def _setVisible(self, elementName: str, visible: bool):
        """
        Set the visibility of the element. If the element does not exist, 
        create a dummy element and set its visibility. It will be updated
        when the actual element is created, and the visibility will be
        inherited.
        """
        if self._hasElement(elementName):
            self._plottingElements[elementName].set_visible(visible)
        else:
            # create a dummy element
            dummy_element = PlotElement(elementName)
            dummy_element.set_visible(visible)
            self.updateElement(dummy_element)

    # @Slot()
    # def relimByMeasData(self):
    #     """
    #     Set the x and y limits of the axes to fit the measurement data
    #     """
    #     if not self._hasElement("measurement"):
    #         # measurement data not loaded
    #         return 
        
    #     self.axes.set_xlim(self._plottingElements["measurement"].xLim)
    #     self.axes.set_ylim(self._plottingElements["measurement"].yLim)
    #     self._recordXYLim()

    # manipulate plotting elements        
    @Slot()
    def updateElemPropertyByPage(
        self, 
        page: Literal["calibrate", "extract", "prefit", "fit"]
    ):
        """
        Switch to the mode and update the plotting elements
        """
        if page == "calibrate":
            self._setVisible("measurement", True)
            self._setVisible("extraction_vlines", False)
            self._setVisible("active_extractions", False)
            self._setVisible("all_extractions", False)
            self._setVisible("spectrum", False)
        elif page == "extract":
            self._setVisible("measurement", True)
            self._setVisible("extraction_vlines", True)
            self._setVisible("active_extractions", True)
            self._setVisible("all_extractions", True)
            self._setVisible("spectrum", False)
        elif page == "fit" or page == "prefit":
            self._setVisible("measurement", True)
            self._setVisible("extraction_vlines", False)
            self._setVisible("active_extractions", True)
            self._setVisible("all_extractions", True)
            self._setVisible("spectrum", True)

        self.canvas.draw()
        
    def _plotElement(
        self, 
        element: Union[PlotElement, str], 
        draw: bool = True,
        **kwargs
    ):
        """
        Plot the element by name
        """
        if self.plottingDisabled:
            return
        
        if isinstance(element, str):
            element = self._plottingElements[element]

        element.canvasPlot(
            self.axes, 
            **self._coloringKwargs(element.name),
            **kwargs
        )
        self._restoreXYLim()

        if draw:
            self.canvas.draw()

    @Slot()
    def updateElement(self, element: PlotElement, **kwargs):
        """
        Update the element in the plotting elements dictionary and 
        redraw the element on the canvas. Note that the visibility of the
        element will be inherited from the previous element with the same
        name.
        """
        name = element.name
        self._checkElementName(name)

        # remove the old element and inherit its properties
        if name in self._plottingElements.keys():
            old_element = self._plottingElements[name]
            element.inheritProperties(old_element)
            old_element.remove()
        
        # draw the new element
        self._plottingElements[name] = element
        self._plotElement(name, draw=True, **kwargs)

    @Slot()
    def updateMultiElements(self, *elements: PlotElement, **kwargs):
        """
        Update multiple elements in the plotting elements dictionary and 
        redraw the elements on the canvas
        """
        for element in elements:
            self.updateElement(element, **kwargs)

    def plotAllElements(self, resetXYLim: bool = False):
        """
        Plot all elements stored in the plotting elements dictionary.

        Parameters:
        -----------
        resetXYLim: bool
            Whether to reset the x and y limits of the axes to fit all elements.
            If not, the x and y limits will be the same as before.
        """
        print(f"plot all")
        for element in self._plottingElements.values():
            self._plotElement(element, draw=False)

        if resetXYLim:
            self._restoreXYLim(byMeasData=True)

        self.canvas.draw()
        
    # Signal Processing ================================================
    