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
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QToolButton, QSizePolicy
)

from matplotlib.backend_bases import cursors
from matplotlib.backends.backend_qtagg import (
    # FigureCanvasQTAgg,
    FigureCanvas as FigureCanvasQTAgg,
    NavigationToolbar2QT,
)

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib.cm as cm

from qfit.utils.helpers import ySnap

from qfit.models.data_structures import PlotElement
from qfit.settings import color_dict, MARKER_SIZE


class MplNavButtons(QFrame):
    pass


class NavigationHidden(NavigationToolbar2QT):
    """
    This class extends the NavigationToolbar2QT class from Matplotlib to 
    create a custom navigation toolbar for a Matplotlib figure.

    The toolbar is designed to be hidden, with only the "Home", "Pan", 
    and "Zoom" buttons connected to external buttons. 

    The class overrides several methods from the parent class to customize 
    the behavior of the toolbar. It provides methods to set the pan and 
    zoom modes, set the cursor, and handle the release of the zoom and 
    pan buttons, as well as the home button.

    Parameters
    ----------
    canvas : FigureCanvasQTAgg
        The canvas on which the figure is drawn.
    parent : MplFigureCanvas
        The parent widget.
    """

    def __init__(
        self,
        canvas: FigureCanvasQTAgg,
        parent: "MplFigureCanvas",
        parentIsStandalone: bool = False,
    ):
        super().__init__(canvas, parent, coordinates=False)

        # Hide all buttons.
        if not parentIsStandalone:
            for child in self.findChildren(QToolButton):
                child.setVisible(False)
            self.update()
        
        # only connect to external buttons
        self.toolitems = [
            t for t in NavigationToolbar2QT.toolitems if t[0] in ("Home", "Pan", "Zoom")
        ]

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

class SpecialCursor(Cursor):
    """
    This class extends the Cursor class from Matplotlib:
        - It draws a cursor (a scatter plot) with x/y/axis snapping and
        visibility control.
        - It draws a vertical and horizontal line (crosshair) with visibility
        control.
        - It uses blitting for faster drawing.

    Parameters
    ----------
    ax: Axes
        A list of Axes that the cursor is attached to, these axes share 
        the same x-axis or y-axis.
    xSnapMode: Literal["MeasData", "ExtrX", "OFF"]
        Whether to snap the cursor to the closest x value in a list.
        - "MeasData": snap to the closest x value in the x values of the 
        measurement data
        - "ExtrX": snap to the closest x value in the extracted data points
        - "OFF": do not snap to any x value
    distinctExtrX: np.ndarray
        The list of all x values in the extracted data points
    measX: np.ndarray
        The list of all x values in the measurement data
    axisSnapMode: Literal["X", "Y", "OFF"]
        Whether to snap the cursor to the minimum x or y value (edge of the plot).
        It overrides xSnapMode.
    horizOn: bool
        Whether to show the horizontal line
    vertOn: bool
        Whether to show the vertical line
    useblit: bool
        Whether to use blitting for faster drawing
    **lineprops: Any
        Additional properties for the lines and the cursor
    """
    def __init__(
        self,
        axes: List[Axes],
        xSnapMode: Literal["MeasData", "ExtrX", "OFF"],
        distinctExtrX: np.ndarray,
        measX: np.ndarray,
        xyMin: Tuple[float, float],
        axisSnapMode: Literal["X", "Y", "OFF"] = "OFF",
        horizOn=True,
        vertOn=True,
        useblit=False,
        **lineprops,
    ):
        super().__init__(
            axes[0], horizOn=horizOn, vertOn=vertOn, useblit=useblit, **lineprops
        )
        self.allAxes = axes
        self.xSnapMode = xSnapMode
        self.distinctExtrX = distinctExtrX
        self.measX = measX

        self.axis_snap_mode = axisSnapMode
        self.xyMin = xyMin

    def onmove(self, event):
        """
        Internal event handler to draw the cursor when the mouse moves.

        When the mouse moves, the cursor (a scatter plot) is drawn at the
        calculated coordinates. The vertical and horizontal lines (crosshair)
        are also drawn at the calculated coordinates. 
        """
        # Do nothing if the event is ignored or the widget is locked 
        # or the cursor is not visible
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if not self.visible:
            return
        
        # Hide the vertical and horizontal lines when the mouse is outside the axes
        if event.inaxes not in self.allAxes:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)
            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True

        # convert the mouse x and y coordinates to the data coordinates
        xdata, ydata = self.allAxes[0].transData.inverted().transform((event.x, event.y))

        # Calculate the x-coordinate of the point based on the snapping mode and axis snap mode
        if self.axis_snap_mode == "Y":
            point_x_coordinate = self.xyMin[0]
        else:
            point_x_coordinate = self.snapToProperX(xdata)

        # Calculate the y-coordinate of the point based on the axis snap mode
        if self.axis_snap_mode == "X":
            point_y_coordinate = self.xyMin[1]
        else:
            point_y_coordinate = ydata

        # Update the vertical line position based on the mouse x-coordinate
        self.linev.set_xdata((point_x_coordinate, point_x_coordinate))
        # Update the horizontal line position based on the mouse y-coordinate
        self.lineh.set_ydata((point_y_coordinate, point_y_coordinate))

        # remove the old cursor
        if hasattr(self, "cross"):
            try:
                self.cross.remove()
            except ValueError:
                pass

        # Draw the cursor (a scatter plot) at the calculated coordinates
        self.cross = self.ax.scatter(
            point_x_coordinate,
            point_y_coordinate,
            c="red",
            marker=r"$\odot$",
            s=MARKER_SIZE,
            alpha=0.5,
            animated=True,
        )

        # Set the visibility of the cursor and lines
        self.cross.set_visible(self.visible)
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        # Update the canvas to reflect the changes
        self._update()

    def _closestX(self, xdat: float, xArray: np.ndarray):
        """
        Find the closest x value in the list of all x values
        """
        allxdiff = {np.abs(xdat - i): i for i in xArray}
        if allxdiff:
            return allxdiff[min(allxdiff.keys())]
        else:
            return xdat

    def _snapToMeasDataGrid(self, xdat):
        """
        Find the closest x value in the list of all x values in the measurement data
        """
        if self.measX is None or len(self.measX) == 0:
            return xdat

        return self._closestX(xdat, self.measX)

    def _snapToExtrX(self, xdat):
        """
        Find the closest x value in the list of all x values in the extracted data points
        """
        if self.distinctExtrX is None or len(self.distinctExtrX) == 0:
            return xdat

        return self._closestX(xdat, self.distinctExtrX)
    
    def snapToProperX(self, xdat):
        """
        Snap the cursor to the closest x value if the xSnapMode is not "OFF".
        """
        if self.xSnapMode == "ExtrX":
            return self._snapToExtrX(xdat)
        elif self.xSnapMode == "MeasData":
            return self._snapToMeasDataGrid(xdat)
        else:
            return xdat

    def _update(self):
        """
        Update the canvas to reflect the changes
        """
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
        if hasattr(self, "cross"):
            self.cross.remove()


class MplFigureCanvas(QFrame):
    """
    This class extends the QFrame class from PySide6 to create a custom
    widget for a Matplotlib figure.

    The widget contains a Matplotlib canvas and a custom navigation toolbar.
    It provides methods to update the x- and y-axes, the cursor, and the
    plotting elements. It also provides methods to reset the view, zoom in,
    and pan.

    Parameters
    ----------
    parent : QWidget
        The parent widget.
    """
    
    canvasClosed = Signal()

    def __init__(self, parent=None, standalone: bool = False):
        QFrame.__init__(self, parent)

        # this widget could be initialized outside of the main window
        # and shown as a standalone plotting widget
        self._standalone = standalone
        
        self.initViewElem()
        self.initPlotting()

    def initViewElem(self):
        self.canvas = FigureCanvasQTAgg(Figure())
        self.toolbar = NavigationHidden(
            self.canvas, 
            self, 
            parentIsStandalone=self._standalone,
        )

        # initialize the layout
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        # change background color
        self.canvas.figure.patch.set_facecolor("#B8B8B8")
        self.canvas.figure.subplots()
        self.axes.autoscale(enable=False)

    def initPlotting(self):
        """
        Initialize the properties of the widget, including the axes, the
        plotting elements, the cursor, and the view limits.
        """
        # remove the default x- and y-axis
        self.axes.spines['bottom'].set_visible(False)
        self.axes.xaxis.set_ticks([])
        self.axes.set_xticklabels([])
        self.axes.spines['left'].set_visible(False)
        self.axes.yaxis.set_ticks([])
        self.axes.set_yticklabels([])

        # reduce the margin of the axes
        self._adjustMargin(xAxisNum=1)

        # limits of the principal axes
        self._currentPrcplXLim: Tuple[float, float] = (0, 1)    # x, y lims after zoom/pan
        self._currentPrcplYLim: Tuple[float, float] = (0, 1)
        self._measPrcplXLim: Tuple[float, float] = (0, 1)       # x, y lims after reset
        self._measPrcplYLim: Tuple[float, float] = (0, 1)
        self._measPrcplXList = np.ndarray(self._measPrcplXLim)

        # the axes for displaying the x & y values
        self._xAxes: List[Axes] = []
        self._yAxes: List[Axes] = []
        # limits of the displayed spine, ticks, and labels
        self._currentAllXLim: List[Tuple[float, float]] = []
        self._currentAllYLim: List[Tuple[float, float]] = []
        self._allXLim: List[Tuple[float, float]] = []
        self._allYLim: List[Tuple[float, float]] = []

        # plotting elements, settings, and colors
        self._plottingElements: Dict[str, PlotElement] = {}
        self.plottingDisabled: bool = False

        self._xSnapMode: Literal["MeasData", "ExtrX", "OFF"] = "OFF"
        self._distinctExtrX = np.array([])
        self._crosshairHorizOn: bool = False
        self._crosshairVertOn: bool = False
        self._axisSnapMode: Literal["X", "Y", "OFF"] = "OFF"

        self._colorMapStr: str = "PuOr"
        self._updateElementColors()


    # Properties =======================================================
    @property
    def axes(self) -> Axes:
        return self.canvas.figure.axes[0]

    @Slot()
    def updateColorMap(self, colorMap: str):
        """
        Update the color map of the plotting elements. 
        """
        if colorMap != self._colorMapStr:
            self._colorMapStr = colorMap
            self._updateElementColors()
            self.plotAllElements()

    def _updateElementColors(self):
        """
        According to the color map, update the colors of the elements.
        It won't redraw the elements, but wait for the next updateAllElements() call.
        """
        self.crossColor = color_dict[self._colorMapStr]["Cross"]
        self.lineColor = color_dict[self._colorMapStr]["line"]
        self.scatterColor = color_dict[self._colorMapStr]["Scatter"]
        self.cmap = copy.copy(getattr(cm, self._colorMapStr))

    # View: Coordinates ================================================
    def _adjustMargin(self, xAxisNum: int):

        # Calculate the desired margins in points
        rightTopMarginInch = (0.1, 0.1)
        leftBottomMarginInch = (self._xAxesLoc(4.2), self._xAxesLoc(xAxisNum + 1.2))

        # Convert the margins to fractions of the figure size
        topRightMargin = self._inchToRatio(rightTopMarginInch)[::-1]
        bottomLeftMargin = self._inchToRatio(leftBottomMarginInch)[::-1]

        self.canvas.figure.subplots_adjust(
            top = 1 - topRightMargin[0],
            right = 1 - topRightMargin[1], 
            bottom = bottomLeftMargin[0],
            left = bottomLeftMargin[1],
        )
        self.canvas.draw() 

    def _inchToRatio(self, inch: Tuple[float, float]) -> np.ndarray:
        """
        Convert an xy vector in inches to a ratio of the figure size.
        """ 
        figSizeInch = self.canvas.figure.get_size_inches()
        inch = np.array(inch)
        return inch / figSizeInch
    
    def _inchToPts(self, inch: Tuple[float, float]) -> np.ndarray:
        """
        Convert an xy vector in inches to the points.

        Note that MPL will treat the dpi to be fixed at 100, and will 
        automacally scale the points to the actual dpi of the figure.
        """ 
        return np.array(inch) * 100
        # return np.array(inch) * self.canvas.figure.dpi    # wrong

    def _distanceInPts(self, x1y1: np.ndarray, x2y2: np.ndarray) -> float:
        """
        Calculate the distance between two points in pts.
        """
        x1y1Pts = self.axes.transData.transform(x1y1)
        x2y2Pts = self.axes.transData.transform(x2y2)

        distance = np.linalg.norm(x1y1Pts - x2y2Pts)

        # as mpl treats the dpi to be fixed at 100, we need to scale the distance
        normed_dis = distance * 100 / self.canvas.figure.dpi

        # print(x1y1Pts, x2y2Pts, x2y2Pts - x1y1Pts, distance, normed_dis)
        return normed_dis

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjustMargin(xAxisNum=len(self._xAxes))

    # View Manipulation: Axes ==========================================
    def _setMeasXList(self, xList: np.ndarray):
        """
        When the measurement data is loaded, we want to record the x values
        of the measurement data. This method records the principal x values 
        of the measurement data.
        """
        self._measPrcplXList = xList
        self.updateCursor()

    def _setMeasXYLim(self, xLim: Tuple[float, float], yLim: Tuple[float, float]):
        """
        When click the reset button, we want to reset to the previous x
        and y limits determined by the measurement data. This method records
        the x and y limits of the axes when the measurement data is loaded.
        """
        self._measPrcplXLim = xLim
        self._measPrcplYLim = yLim

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
        self._currentPrcplXLim = self.axes.get_xlim()
        self._currentPrcplYLim = self.axes.get_ylim()

        for xAx in self._xAxes:
            self._currentAllXLim.append(xAx.get_xlim())
        for yAx in self._yAxes:
            self._currentAllYLim.append(yAx.get_ylim())

    def _dispLimByPrcplLim(
        self,
        currentPrcplLim: Tuple[float, float], 
        measPrcplLim: Tuple[float, float], 
        originalLim: Tuple[float, float],
    ) -> Tuple[float, float]:
        """
        Displayed axes' limits are simutaneously scaled with the principal axes' limits.

        Parameters:
        -----------
        currentPrcplLim: Tuple[float, float]
            The current principal limits of the axes (which was just set)
        measPrcplLim: Tuple[float, float]
            The original limits of the principal axes
        originalLim: Tuple[float, float]
            The original limits of the displayed axes
        """
        # determine the linear relationship between the principal limits 
        # and the displayed limits. displayed = k * principal + b
        k = (originalLim[1] - originalLim[0]) / (measPrcplLim[1] - measPrcplLim[0])
        b = originalLim[0] - k * measPrcplLim[0]

        # calculate the displayed limits
        dispLim = (k * currentPrcplLim[0] + b, k * currentPrcplLim[1] + b)

        return self._nonSignularLim(dispLim)
    
    @staticmethod
    def _nonSignularLim(lim: Tuple[float, float]) -> Tuple[float, float]:
        """
        Process the limits of the axes, making it not to be a single point.
        """
        if lim[0] == lim[1]:
            return lim[0]*0.9 - 1, lim[0]*1.1 + 1
        else:
            return lim

    def _restoreXYLim(self, byMeasData: bool = False):
        """
        Keep the x and y limits of the axes unchanged.
        It will be called when the plot elements are updated and the x and y limits
        are automatically changed by matplotlib.
        """
        if byMeasData:
            self.axes.set_xlim(*self._measPrcplXLim)
            self.axes.set_ylim(*self._measPrcplYLim)

            for i, xAx in enumerate(self._xAxes):
                xAx.set_xlim(*self._nonSignularLim(self._allXLim[i]))
            for i, yAx in enumerate(self._yAxes):
                yAx.set_ylim(*self._nonSignularLim(self._allYLim[i]))
            
        else:
            self.axes.set_xlim(*self._nonSignularLim(self._currentPrcplXLim))
            self.axes.set_ylim(*self._nonSignularLim(self._currentPrcplYLim))

            for i, xAx in enumerate(self._xAxes):
                xAx.set_xlim(*self._dispLimByPrcplLim(
                    self._currentPrcplXLim, self._measPrcplXLim, self._allXLim[i]
                ))
            for i, yAx in enumerate(self._yAxes):
                yAx.set_ylim(*self._dispLimByPrcplLim(
                    self._currentPrcplYLim, self._measPrcplYLim, self._allYLim[i]
                ))

    @Slot(np.ndarray, np.ndarray)
    def relimPrincipalAxes(self, x: np.ndarray, y: np.ndarray):
        """
        Set the principal x and y limits of the axes to fit the measurement data.

        This Slot should be called accopmanied with updateXAxes and updateYAxes.
        """        
        xLim = (np.min(x), np.max(x))
        yLim = (np.min(y), np.max(y))
        self._setMeasXYLim(xLim, yLim)
        self._setMeasXList(x)

        self._restoreXYLim(byMeasData=True)
        self._recordXYLim()

    @staticmethod
    def _xAxesLoc(which: int | float):
        """The outwards location of the x-axes in inches."""
        return 0.2 * which

    def updateXAxes(self, xAxes: Dict[str, Tuple[float, float]]):
        """
        Update the displayed x-axes value.

        This Slot should be called accopmanied with relim and updateYAxes.
        """
        self._allXLim = list(xAxes.values())
        self._currentAllXLim = copy.deepcopy(self._allXLim)

        for ax in self._xAxes:
            self.canvas.figure.delaxes(ax)

        # Create a new axes for each x-values in the dictionary
        new_axes = []
        for i, (xName, xRange) in enumerate(xAxes.items()):
            ax = self.axes.twiny()

            # process the name
            if "<br>" in xName:
                xName = xName.replace("<br>", "\n")

            # ticks and spines
            _, spineLoc = self._inchToPts((0, self._xAxesLoc(i)))
            ax.spines['bottom'].set_position(('outward', spineLoc))
            ax.xaxis.set_ticks_position('bottom')
            if xRange[0] == xRange[1]:
                ax.set_xlim(*self._nonSignularLim(xRange))
                ax.set_xticks([xRange[0]])
                ax.set_xticklabels([f"Coordinate fixed at: {xRange[0]:.4e}"])
            else:
                ax.set_xlim(*xRange)

            # label
            labelLoc = self._inchToPts((-0.05, -self._xAxesLoc(i + 0.5)))
            ax.annotate(
                xName, xy=labelLoc, 
                xycoords='axes points', 
                ha='right', va='center'
            )

            new_axes.append(ax)

        self._xAxes = new_axes

        # layout 
        self._adjustMargin(xAxisNum=len(self._xAxes))

        # self.canvas.figure.tight_layout()
        self.updateCursor()
        self.canvas.draw()

    def updateYAxes(self, yName: str, yRange: Tuple[float, float]):
        """
        Update the y-axes. (there is only one y-axis)

        This Slot should be called accopmanied with relim and updateXAxes.
        """
        self._allYLim = [yRange]
        self._currentAllYLim = copy.deepcopy(self._allYLim)
        
        for ax in self._yAxes:
            self.canvas.figure.delaxes(ax)

        # Create a new axes for each x-values in the dictionary
        ax = self.axes.twinx()
        ax.set_ylim(*self._nonSignularLim(yRange))
        ax.set_ylabel(yName)
        ax.yaxis.set_ticks_position('left')
        ax.yaxis.set_label_position('left')
        ax.spines['left'].set_position(('outward', 40 * 0))
        # ax.yaxis.set_label_coords(1.05, -0.08 * (i))  # set label position
        self._yAxes = [ax]

        # self.canvas.figure.tight_layout()
        self.updateCursor()
        self.canvas.draw()

    # View Manipulation: Cursor ========================================
    def updateCursor(
        self,
        xSnapMode: Literal["MeasData", "ExtrX", "OFF", None] = None,
        axisSnapMode: Literal["X", "Y", "OFF"] = "OFF",
        horizOn: Union[bool, None] = None,
        vertOn: Union[bool, None] = None,
    ):
        """
        set up the crosshair cursor. This class memorizes the state of the crosshair
        cursor when no arguments are passed.

        Parameters:
        -----------
        xSnapMode: Literal["MeasData", "ExtrX", "OFF"] = None
            Whether to snap the cursor to the closest x value in a list.
            - "MeasData": snap to the closest x value in the x values of the measurement data
            - "ExtrX": snap to the closest x value in the extracted data points
            - "OFF": do not snap to any x value
            - None: keep the current state
        axisSnapMode: Literal["X", "Y", "OFF"] = "OFF"
            Whether to snap the cursor to the minimum x or y value (edge of the plot).
            It overrides xSnapMode.
        horizOn: bool = None
            Whether to show the horizontal line. If None, keep the current state.
        vertOn: bool = None
            Whether to show the vertical line. If None, keep the current state.
        """
        if self._standalone:
            return  # do nothing in standalone mode
        
        # memorize the state of the crosshair cursor
        if xSnapMode is not None:
            self._xSnapMode = xSnapMode
        if horizOn is not None:
            self._crosshairHorizOn = horizOn
        if vertOn is not None:
            self._crosshairVertOn = vertOn
        self._axisSnapMode = axisSnapMode

        # remove the old cursor
        if hasattr(self, "specialCursor"):
            self.specialCursor.remove()

        self.specialCursor = SpecialCursor(
            [self.axes] + self._xAxes + self._yAxes,
            xSnapMode = self._xSnapMode,
            distinctExtrX = self._distinctExtrX,
            measX=self._measPrcplXList,
            xyMin = (self.axes.get_xlim()[0], self.axes.get_ylim()[0]),
            axisSnapMode = self._axisSnapMode,
            useblit = True,
            horizOn = self._crosshairHorizOn,
            vertOn = self._crosshairVertOn,
            color = self.crossColor,
            alpha = 0.5,
        )
        self.canvas.draw()
        self.specialCursor.line_blit_on()

    @Slot()
    def updateCursorXSnapValues(self, newCursorXSnapValues: np.ndarray):
        self._distinctExtrX = newCursorXSnapValues
        self.updateCursor()

    # View Manipulation: Navigation ====================================

    def zoomOn(self):
        """
        Enable zoom mode and remove the cursor crosshair.
        """
        self.toolbar.setZoomMode(
            on=True
        )  # toggle zoom at the level of the NavigationToolbar2QT, enabling actual
        # zoom functionality
        self.updateCursor(horizOn=False, vertOn=False)

    def panOn(self):
        """
        Enable pan mode and remove the cursor crosshair.
        """
        self.toolbar.setPanMode(
            on=True
        )  # toggle pan at the level of the NavigationToolbar2QT, enabling actual
        # pan functionality
        self.updateCursor(horizOn=False, vertOn=False)

    def selectOn(self):
        """
        Enable select mode.
        """
        self.toolbar.setZoomMode(on=False)
        self.toolbar.setPanMode(on=False)

    @Slot()
    def resetView(self):
        self.toolbar.home()
        # set the x and y limits of the axes to fit the measurement data
        self.axes.set_xlim(*self._measPrcplXLim)
        self.axes.set_ylim(*self._measPrcplYLim)
        self.canvas.draw()
        self._recordXYLim()

        # reset the margins
        self._adjustMargin(xAxisNum=len(self._xAxes))

    @Slot()
    def zoomView(self):
        self.zoomOn()

    @Slot()
    def panView(self):
        self.panOn()

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
            "spectrum",
        ]:
            raise ValueError(f"Invalid element name: {name}. ")

    def _hasElement(self, elementName: str) -> bool:
        """
        Check whether the element is in the plotting elements dictionary
        """
        self._checkElementName(elementName)
        return elementName in self._plottingElements.keys()

    def _specialKwargs(self, elementName: str) -> Dict[str, Any]:
        """
        For different elements, they accept different special kwargs.
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
        elif elementName == "spectrum":
            return {
                "xlim": self._measPrcplXLim,
                "ylim": self._measPrcplYLim,
            }
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

    # manipulate plotting elements        
    @Slot()
    def updateElemPropertyByPage(
        self, page: Literal["calibrate", "extract", "prefit", "fit"]
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
        self, element: Union[PlotElement, str], draw: bool = True, **kwargs
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
            **self._specialKwargs(element.name), 
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
        
        # We may have multiple MplFigureCanvas instances, 
        # deepcopy the element to avoid reference issues
        element = copy.deepcopy(element)

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
        for element in self._plottingElements.values():
            self._plotElement(element, draw=False)

        if resetXYLim:
            self._restoreXYLim(byMeasData=True)

        self.canvas.draw()
        
    def closeEvent(self, event):
        self.canvasClosed.emit()
        super().closeEvent(event)