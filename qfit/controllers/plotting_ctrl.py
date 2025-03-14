from PySide6.QtCore import Slot, QObject, Signal

from qfit.widgets.mpl_canvas import MplFigureCanvas

import numpy as np
import copy
import matplotlib as mpl
from qfit.utils.helpers import ySnap, OrderedDictMod
from qfit.models.measurement_data import (
    MeasDataType,
)
from qfit.models.data_structures import FilterConfig
from qfit.settings import MARKER_SIZE
from qfit.utils.helpers import makeUnique

from typing import TYPE_CHECKING, Union, Dict, Any, Tuple, Literal, List, Callable
import warnings

if TYPE_CHECKING:
    from qfit.models.calibration import CaliParamModel

    from qfit.models.parameter_set import SweepParamSet
    from qfit.models.measurement_data import MeasDataSet
    from qfit.models.extracted_data import AllExtractedData, ActiveExtractedData
    from qfit.models.numerical_model import QuantumModel
    from qfit.views.paging_view import PageView


mpl.rcParams["toolbar"] = "None"
try:
    mpl.use("qtagg")
except ImportError as e: 
    warnings.warn(f"Recieving error {e} while importing matplotlib, indicating "
                  "that the code is running in a headless environment for "
                  "testing. Using Agg backend instead.")
    mpl.use("Agg")
    


class StandaloneCanvasAndConfigs:
    """
    It is a data structure that manages the dynamical view - standalone 
    mplFigureCanvas and its configs.
    """
    def __init__(
        self,
        name: str,
        rawX: Dict[str, np.ndarray],
        rawY: Dict[str, np.ndarray],
        figNames: List[str],
        canvas: MplFigureCanvas,
    ):
        self.name = name
        self.rawX = rawX
        self.rawY = rawY
        self.figNames = figNames
        self.canvas = canvas


class PlottingCtrl(QObject):
    """
    The controller for the plotting canvas. It is responsible for handling the
    mouse click events and the UI elements for the canvas and connecting them
    to the backend models.

    Relevant UI elements:
    - mplCanvas: the matplotlib canvas
    - measComboBoxes: the combo boxes for the x, y, and z axes
    - measPlotSettings: the check boxes and spin boxes for the plot settings
    - swapXYButton: the button for swapping the x and y axes
    - canvasTools: the buttons for reset, zoom, and pan functions of the canvas
    - calibrationButtons: the buttons for calibrating the axes
    - calibratedCheckBox: the check box for toggling the calibration status
    - pageView: the view for switching between different pages

    Relevant models:
    - measurementData
    - calibrationModel
    - allDatasets: the model for all the extracted data
    - activeDataset: the model for the currently selected data

    Parameters
    ----------
    parent: QObject
        The parent object
    mplCanvas: MplFigureCanvas
        The matplotlib canvas
    models: Tuple[MeasDataSet, CaliParamModel, AllExtractedData,
        ActiveExtractedData, QuantumModel]
    views: Tuple[Any, ...]
        measComboBoxes, measPlotSettings, swapXYButton, canvasTools,
        calibrationButtons, calibratedCheckBox, pageView
    """

    # state of the controller, determining the how things are plotted
    disconnectCanvas: bool  # switch off canvas updates
    xSnapTool: bool  # whether x snap tool is selected
    trans0Focused: bool  # whether the first extracted transition is focused
    axisSnap: Literal["X", "Y", "OFF"]  # whether to snap to one of the axes
    clickResponse: Literal[  # the response to a mouse click
        "ZOOM",
        "PAN",
        "EXTRACT",
    ]
    dataDestination: Literal["CALI_X", "CALI_Y", "EXTRACT", "NONE"]
    # after a click, to where we send the click position

    # calibration functions
    XCaliFuncDict: Dict[str, "SweepParamSet"]
    YCaliFunc: Callable

    def __init__(
        self,
        parent: QObject,
        mplCanvas: "MplFigureCanvas",
        models: Tuple[
            "MeasDataSet",
            "CaliParamModel",
            "AllExtractedData",
            "ActiveExtractedData",
            "QuantumModel",
        ],
        views: Tuple[Any, ...],
    ):
        super().__init__(parent)
        (
            self.measDataSet,
            self.calibrationModel,
            self.allDatasets,
            self.activeDataset,
            self.quantumModel,
            # self.sweepParameterSet,
        ) = models
        (
            self.measComboBoxes,
            self.measPlotSettings,
            # self.swapXYButton,
            self.canvasTools,
            # self.calibrationButtons,
            self.calibratedCheckBox,
            self.pageView,
        ) = views
        self.mplCanvas = mplCanvas
        self.axes = mplCanvas.axes

        # initialize the state of the controller
        self.disconnectCanvas = False  # used to temporarily switch off canvas updates
        self.xSnapTool = True  # whether the horizontal snap is on
        self.trans0Focused = True  # whether the first transition is focused
        self.axisSnap = "OFF"  # the axis snap mode, override xSnap when not "OFF"
        self.clickResponse = "EXTRACT"  # the response to a mouse click
        self.dataDestination = "NONE"  # the destination of the data after a click
        self.calibrateAxes = False  # whether the ticklabels are calibrated
        self.standaloneCanvases: Dict[str, StandaloneCanvasAndConfigs] = {}

        # connects
        self.dataSwitchConnects()
        self.canvasToolConnects()
        self.plotElementsConnects()
        self.mouseClickConnects()
        self.plottingModeConnects()
        self.caliConnects()

        # Although measurement data is updated when reloaded,
        # but swapXY only involves the "pointer" of measurement data,
        # so it only need to be connected once.
        # self.swapXYButton.clicked.connect(self.swapXY)

        # previously in dynamicalInit
        self.measPlotSettingConnects()
        # self.uiXYZComboBoxesConnects()

    def dynamicalInit(self):
        """
        When the app is reloaded (new measurement data and hilbert space),
        reinitialize the all relevant models and views.
        """
        self.zComboBoxReload()

        # plot everything available
        self.setXYAxesForAll()
        self.measDataSet.emitReadyToPlot()
        self.measDataSet.emitRelimCanvas()
        self.measDataSet.emitRawXMap()
        self.activeDataset.emitReadyToPlot()
        self.allDatasets.emitReadyToPlot()
        self.allDatasets.emitFocusChanged()  # update the snapX
        self.updateCursor()

    # measurement ======================================================
    def zComboBoxReload(self):
        """
        Load the available data into the combo boxes for the x, y, and z axes.
        """
        zDataNames = self.measDataSet.currentMeasData.zCandidates.keyList
        self.measComboBoxes["z"].clear()
        self.measComboBoxes["z"].addItems(zDataNames)
        self.measComboBoxes["z"].setCurrentText(
            self.measDataSet.currentMeasData.principalZ.name
        )
        # self.setupXYDataBoxes()

    def _modelStoreFilter(self):
        """
        Update the filter for the measurement data.

        Note: part of it should be a view method, but it is too much hassle
        to implement it now.
        """
        fiter = FilterConfig(
            topHat=self.measPlotSettings["topHat"].isChecked(),
            wavelet=self.measPlotSettings["wavelet"].isChecked(),
            edge=self.measPlotSettings["edge"].isChecked(),
            bgndX=self.measPlotSettings["bgndX"].isChecked(),
            bgndY=self.measPlotSettings["bgndY"].isChecked(),
            log=self.measPlotSettings["log"].isChecked(),
            min=self.measPlotSettings["min"].value(),
            max=self.measPlotSettings["max"].value(),
            color=self.measPlotSettings["color"].currentText(),
        )
        self.measDataSet.storeFilter(fiter)

    def _viewStoreFilter(self, filterConfig: FilterConfig):
        """
        Update the filter for the measurement data.

        Note: part of it should be a view method, but it is too much hassle
        to implement it now.
        """
        self.measPlotSettings["topHat"].setChecked(filterConfig.topHat)
        self.measPlotSettings["wavelet"].setChecked(filterConfig.wavelet)
        self.measPlotSettings["edge"].setChecked(filterConfig.edge)
        self.measPlotSettings["bgndX"].setChecked(filterConfig.bgndX)
        self.measPlotSettings["bgndY"].setChecked(filterConfig.bgndY)
        self.measPlotSettings["log"].setChecked(filterConfig.log)
        self.measPlotSettings["min"].setValue(filterConfig.min)
        self.measPlotSettings["max"].setValue(filterConfig.max)
        self.measPlotSettings["color"].setCurrentText(filterConfig.color)

    def measPlotSettingConnects(self):
        """Connect the options related to display of measurement data"""
        self.measPlotSettings["topHat"].toggled.connect(self._modelStoreFilter)
        self.measPlotSettings["wavelet"].toggled.connect(self._modelStoreFilter)
        self.measPlotSettings["edge"].toggled.connect(self._modelStoreFilter)
        self.measPlotSettings["bgndX"].toggled.connect(self._modelStoreFilter)
        self.measPlotSettings["bgndY"].toggled.connect(self._modelStoreFilter)
        self.measPlotSettings["log"].toggled.connect(self._modelStoreFilter)
        self.measPlotSettings["min"].valueChanged.connect(self._modelStoreFilter)
        self.measPlotSettings["max"].valueChanged.connect(self._modelStoreFilter)
        self.measPlotSettings["color"].currentTextChanged.connect(self._modelStoreFilter)
        self.measPlotSettings["color"].currentTextChanged.connect(
            lambda: self.mplCanvas.updateColorMap(self.measPlotSettings["color"].currentText())
        )
        
    def dataSwitchConnects(self):
        """
        Connect the combo boxes for the x, y, and z axes to the measurement data.
        """
        self.measComboBoxes["z"].activated.connect(self.zDataUpdate)

        self.measDataSet.figSwitched.connect(self.switchFig)

        # self.measComboBoxes["x"].activated.connect(self.xAxisUpdate)
        # self.measComboBoxes["y"].activated.connect(self.yAxisUpdate)

    # def setupXYDataBoxes(self):
    #     if isinstance(self.measurementData._currentMeasData, ImageMeasurementData):
    #         return

    #     self.measComboBoxes["x"].clear()
    #     xDataNames = list(self.measurementData._currentMeasData._currentXCompatibles.keys())
    #     self.measComboBoxes["x"].addItems(xDataNames)
    #     self.measComboBoxes["x"].setCurrentText(self.measurementData._currentMeasData.currentX.name)

    #     self.measComboBoxes["y"].clear()
    #     yDataNames = list(self.measurementData._currentMeasData._currentYCompatibles.keys())
    #     self.measComboBoxes["y"].addItems(yDataNames)
    #     self.measComboBoxes["y"].setCurrentText(self.measurementData._currentMeasData.currentY.name)

    @Slot(int)
    def zDataUpdate(self, itemIndex: int):
        """
        Update the z axis of the measurement data.
        """
        self.measDataSet.storePrincipalZ(itemIndex)
        # self.setupXYDataBoxes()

    # @Slot(int)
    # def xAxisUpdate(self, itemIndex: int):
    #     self.measurementData.setCurrentX(itemIndex)

    # @Slot(int)
    # def yAxisUpdate(self, itemIndex: int):
    #     self.measurementData.setCurrentY(itemIndex)

    @Slot(np.ndarray, np.ndarray)
    def relimCanvas(self, xData: np.ndarray, yData: np.ndarray):
        """
        Update the axes limits of the canvas based on the x and y data.
        """
        self.mplCanvas.relimPrincipalAxes(xData, yData)
        if self.measDataSet.rowCount() > 0:
            self._setXYAxesByCurrentMeasData()

    @Slot(str)
    def switchFig(self, figName: str):
        """
        Switch the measurement data to the one with the given figure name. It will
        update the combo boxes for the x, y, and z axes and plot the new data.

        Note: The most of slots like this are connected in the MeasDataCtrl, not
        in models' corresponding controllers. Plotting related slots should be
        the only exception.
        """
        self.zComboBoxReload()
        self._viewStoreFilter(self.measDataSet.exportFilter())
        # self.setXYAxesByCurrentMeasData() # will be called when relimCanvas

    @Slot()
    def swapXY(self):
        """
        Swap the x and y axes of the measurement data. It should be called
        at the end when the swapXY button is clicked as it updates the
        plot.
        """
        self.mplCanvas.plottingDisabled = True

        # maybe: self.calibrationData.swapXY()

        self.measDataSet.swapXY()
        # self.setupXYDataBoxes()

        self.allDatasets.swapXY()

        self.calibrationModel.updateCaliModelRawVecNameListForSwapXY()

        xBgndSub = self.measPlotSettings["bgndX"].checkState()
        yBgndSub = self.measPlotSettings["bgndY"].checkState()

        self.measPlotSettings["bgndX"].setCheckState(yBgndSub)
        self.measPlotSettings["bgndY"].setCheckState(xBgndSub)

        self.mplCanvas.plottingDisabled = False
        self.mplCanvas.plotAllElements(resetXYLim=True)

    # calibration ======================================================
    def caliConnects(self):
        """
        Connect the "view calibrated axes" check box.
        Connect the calibration model to the canvas.
        """
        self.calibratedCheckBox.toggled.connect(self.toggleCalibrateAxes)
        self.calibrationModel.xCaliUpdated.connect(self.onXCaliFuncUpdated)
        self.calibrationModel.yCaliUpdated.connect(self.onYCaliFuncUpdated)

    @Slot(bool)
    def toggleCalibrateAxes(self, checked: bool):
        """
        If calibration check box is changed, toggle the calibration status of the
        calibrationData. Also induce change at the level of the displayed data of
        selected points.
        """

        self.calibrateAxes = checked
        self.setXYAxesForAll()

    def _setXYAxes(
        self, 
        rawX: Dict[str, np.ndarray],
        rawY: Dict[str, np.ndarray],
        calibFuncName: str,
        canvas: MplFigureCanvas | None = None
    ):
        """
        Update the x and y axes of the canvas based on
        - a given rawX and rawY axes to be shown / calibrated
        - a calibration function (each figure gets its own calibration function,
        so we need to put in the name of the figure)
        
        This function can be also used for standalone mplCanvas.
        """
        if canvas is None:
            canvas = self.mplCanvas

        if self.measDataSet.rowCount() == 0:
            # not yet initialized
            return

        rawXLim = {key: (val[0], val[-1]) for key, val in rawX.items()}
        rawYLim = rawY.itemByIndex(0)  # only have one key

        if not self.calibrateAxes:
            canvas.updateXAxes(rawXLim)
            canvas.updateYAxes(
                rawYLim.name, (rawYLim.data[0], rawYLim.data[-1])
            )
            return

        # when need to show the calibrated data
        # x calibration
        currentSweepParam = self.XCaliFuncDict[calibFuncName]

        currentSweepParam.setByRawX({key: rng[0] for key, rng in rawXLim.items()})
        mappedXLeft = currentSweepParam.getFlattenedAttrDict("value")
        currentSweepParam.setByRawX({key: rng[1] for key, rng in rawXLim.items()})
        mappedXRight = currentSweepParam.getFlattenedAttrDict("value")
        mappedXLim = {
            key: (mappedXLeft[key], mappedXRight[key]) for key in mappedXLeft.keys()
        }

        # y calibration
        mappedYName = f"Energy [GHz]"
        # ylabel = f"Energy [{scq.get_units()}]" # when we implement the units
        mappedYLim = (self.YCaliFunc(rawYLim.data[0]), self.YCaliFunc(rawYLim.data[-1]))

        canvas.updateXAxes(mappedXLim)
        canvas.updateYAxes(mappedYName, mappedYLim)
        
    def _setXYAxesByCurrentMeasData(self):
        measData = self.measDataSet.currentMeasData
        self._setXYAxes(
            rawX=measData.rawX,
            rawY=measData.rawY,
            calibFuncName=measData.name,
            canvas=self.mplCanvas
        )
        
    def _setXYAxesForStandaloneCanvas(self, canvasName: str):
        canvasAndConfigs = self.standaloneCanvases[canvasName]
        self._setXYAxes(
            rawX=canvasAndConfigs.rawX,
            rawY=canvasAndConfigs.rawY,
            calibFuncName=canvasAndConfigs.figNames[0],
            canvas=canvasAndConfigs.canvas
        )
        
    def setXYAxesForAll(self):
        self._setXYAxesByCurrentMeasData()
        for canvasName in self.standaloneCanvases.keys():
            self._setXYAxesForStandaloneCanvas(canvasName)

    def onXCaliFuncUpdated(self, XCaliFuncDict: Dict[str, "SweepParamSet"]):
        """Update the X calibration function and the labels on the canvas."""
        self.XCaliFuncDict = XCaliFuncDict
        self.setXYAxesForAll()

    def onYCaliFuncUpdated(self, YCaliFunc: Callable, invYCaliFunc: Callable):
        """Update the Y calibration function and the labels on the canvas."""
        self.YCaliFunc = YCaliFunc
        self.invYCaliFunc = invYCaliFunc
        self.setXYAxesForAll()

    def storeCalibrationPoint(self, xName, yName, xData, yData):
        """
        Store the calibration point to the calibration model. Perform the following:
        - snap the x value
        - update the calibration data

        """
        rawX = self.measDataSet.currentMeasData.rawXByPrincipalX(xData)
        rawXYDict = rawX | {yName: yData}

        # model: update the calibration data
        self.calibrationModel.processSelectedPtFromPlot(
                data=rawXYDict, figName=self.measDataSet.currentMeasData.name
            )
        # the above will then trigger the update the view:
        # turn off highlighting, set value, etc

        # controller: update the status
        self.dataDestination = "NONE"

    # extracted data ==================================================
    def storeExtractedPoint(self, xName: str, yName: str, xData: float, yData: float):
        """
        Store the extracted point to the active dataset. Perform the following:
        - snap the x value
        - remove the point if it is close to another point
        - snap the y value

        Parameters
        ----------
        xName: str
            The name of the x axis
        yName: str
            The name of the y axis
        xData: float
            The x value of the extracted point
        yData: float
            The y value of the extracted point
        """
        allPoints = self.activeDataset.allPoints()

        # x snap
        xData = self.mplCanvas.specialCursor.snapToProperX(xData)
        rawX = self.measDataSet.currentMeasData.rawXByPrincipalX(xData)
        if not self.xSnapTool:
            # turn on the horizontal snap automatically, if the user turned it off
            self.canvasTools["snapX"].setChecked(True)

        # remove the point if it is close to another point
        for index, x2y2 in enumerate(allPoints.transpose()):
            if self.isRelativelyClose(np.array([xData, yData]), x2y2):
                self.activeDataset.remove(index)
                return

        # y snap
        if self.canvasTools["snapY"].isChecked():
            x_list = self.measDataSet.currentMeasData.principalX.data
            y_list = self.measDataSet.currentMeasData.principalY.data
            z_data = self.measDataSet.currentMeasData.principalZ.data

            # calculate half index range as 5x linewidth
            linewidth = 0.01  # GHz
            half_y_range = self.invYCaliFunc(linewidth * 5) - self.invYCaliFunc(0)

            # snap the y value
            yData = ySnap(
                x_list=x_list,
                y_list=y_list,
                z_data=z_data,
                user_selected_xy=(xData, yData),
                half_y_range=half_y_range,
                mode="lorentzian",
            )

        self.activeDataset.append(
            OrderedDictMod({xName: xData, yName: yData}),
            rawX,
        )

    def isRelativelyClose(self, x1y1: np.ndarray, x2y2: np.ndarray):
        distance = self.mplCanvas._distanceInPts(x1y1, x2y2)
        return distance < np.sqrt(MARKER_SIZE)

    # plotting =========================================================
    def plotElementsConnects(self):
        """
        Connect the all of the models's readyToPlot signals to the canvas
        for plotting the data.
        """
        self.activeDataset.readyToPlot.connect(self.mplCanvas.updateElement)
        self.allDatasets.readyToPlot.connect(self.mplCanvas.updateElement)
        self.allDatasets.readyToPlotX.connect(self.mplCanvas.updateElement)

        self.allDatasets.distinctXUpdated.connect(
            self.mplCanvas.updateCursorXSnapValues
        )

        self.measDataSet.readyToPlot.connect(self.mplCanvas.updateElement)
        self.measDataSet.relimCanvas.connect(self.relimCanvas)
        self.quantumModel.readyToPlotMainCanvas.connect(self.mplCanvas.updateElement)

    def mouseClickConnects(self):
        """
        Set up the matplotlib canvas and start monitoring for mouse click
        events in the canvas area.
        """
        self.mplCanvas.canvas.mpl_connect(
            "button_press_event", self.canvasClickMonitoring
        )

        # self.mplCanvas.canvas.mpl_connect(
        #     "motion_notify_event", self.canvasMouseMonitoring
        # )

    def canvasToolConnects(self):
        """
        Connect the UI buttons for reset, zoom, and pan functions of the
        matplotlib canvas.
        """
        self.canvasTools["reset"].clicked.connect(self.toggleReset)
        self.canvasTools["zoom"].clicked.connect(self.toggleZoom)
        self.canvasTools["pan"].clicked.connect(self.togglePan)
        self.canvasTools["select"].clicked.connect(self.toggleSelect)

    def plottingModeConnects(self):
        """
        The state of the controller is updated by calibrating, switching pages,
        and turning on the x snap tool.
        """

        # calibration --> data destination
        self.calibrationModel.plotCaliPtExtractStart.connect(self.setDataDestAxisSnap)
        self.calibrationModel.plotCaliPtExtractFinished.connect(
            lambda: self.setDataDestAxisSnap("NONE")
        )

        # page switch --> data destination
        self.pageView.pageChanged.connect(
            lambda curr: self.setDataDestAxisSnap(
                "EXTRACT" if curr == "extract" else "NONE"
            )
        )

        # page switch --> plotting element property change (visibility)
        self.pageView.pageChanged.connect(self.mplCanvas.updateElemPropertyByPage)

        # x snap
        self.canvasTools["snapX"].toggled.connect(self.setXSnapTool)
        self.allDatasets.focusChanged.connect(
            lambda: self.setTrans0Focused(self.allDatasets.currentRow == 0)
        )

    @Slot()
    def setXSnapTool(self, checked: bool):
        """
        Update the x snap tool state when toggling the UI button.
        """
        self.xSnapTool = checked
        self.updateCursor()

    @property
    def xSnap(self) -> Literal["MeasData", "ExtrX", "OFF"]:
        """
        X snap helps to align the x value of the selected point to the x value of
        the data points / measurement data grid.

        Combining the information of the x snap tool and the data destination,
        we determine the x snap mode.
        """
        if self.dataDestination == "EXTRACT":
            if self.xSnapTool and not self.trans0Focused:
                # In extracted mode, snap to the x values if tool is on
                return "ExtrX"
            else:
                # In extracted mode, snap to the measData if tool is off
                return "MeasData"
        else:
            return "OFF"

    def setTrans0Focused(self, checked: bool):
        """
        Update the trans0Focused when the user changes the focus of the extracted
        data.
        """
        self.trans0Focused = checked
        self.updateCursor()

    def setClickResponse(self, response: Literal["ZOOM", "PAN", "EXTRACT"]):
        """
        Set the response to a mouse click. The response can be one of the following:
        - ZOOM: zoom in the canvas
        - PAN: pan the canvas
        - EXTRACT: select a point from the canvas
        """
        self.clickResponse = response
        self.updateCursor()

    @Slot()
    def setDataDestAxisSnap(
        self,
        destination: Literal["CALI_X", "CALI_Y", "EXTRACT", "NONE"],
    ):
        """
        Set the data (click's position) destination after a mouse click.
        The destination can be one of the following:
        - CALI_X: calibration model, update x raw data
        - CALI_Y: calibration model, update y raw data
        - EXTRACT: extracted data, add a point
        - NONE: do nothing

        It also update the axis snap mode and the cursor.
        """
        self.dataDestination = destination

        if destination == "CALI_X":
            self.axisSnap = "X"
        elif destination == "CALI_Y":
            self.axisSnap = "Y"
        else:
            self.axisSnap = "OFF"

        self.updateCursor()

    @Slot()
    def toggleSelect(self):
        """
        Toggle the selection mode. When the selection mode is on, the user can
        select a point from the canvas for calibration or extraction.
        """
        self.setClickResponse("EXTRACT")
        self.mplCanvas.selectOn()

    @Slot()
    def toggleZoom(self):
        """
        Toggle the zoom mode. When the zoom mode is on, the user can zoom in
        the canvas.
        """
        self.setClickResponse("ZOOM")
        self.mplCanvas.zoomView()

    @Slot()
    def togglePan(self):
        """
        Toggle the pan mode. When the pan mode is on, the user can pan the
        canvas.
        """
        self.setClickResponse("PAN")
        self.mplCanvas.panView()
        
    @Slot()
    def toggleReset(self):
        """
        Reset the zoom and pan of the canvas.
        """
        self.mplCanvas.resetView()
        self._setXYAxesByCurrentMeasData()

    def updateCursor(self):
        """
        Callback for updating the matching mode and crosshair for the cursor.

        Update cursor will be called when:
        1. Page switch --> Calibration & Selecting page have different crosshair
        2. Calibration mode on / off --> Crosshair is partially on for axis snap
        3. X Snap on / off --> Crosshair updated
        """
        # crosshair
        horizOn, vertOn = False, False  # destination: NONE
        if self.dataDestination == "EXTRACT":
            # selection in selection page --> full xy crosshair
            horizOn, vertOn = True, True
        elif self.dataDestination == "CALI_X":
            # calibrate X --> only vertical crosshair
            horizOn, vertOn = False, True
        elif self.dataDestination == "CALI_Y":
            # calibrate Y --> only horizontal crosshair
            horizOn, vertOn = True, False

        self.mplCanvas.updateCursor(
            axisSnapMode=self.axisSnap,
            xSnapMode=self.xSnap,
            horizOn=horizOn,
            vertOn=vertOn,
        )

    @Slot()
    def canvasClickMonitoring(self, event):
        """
        Main loop for acting on mouse events occurring in the canvas area.

        Based on the dataDestination and clickResponse, the controller will
        process the data and send it to the appropriate model.

        dataDestination == "EXTRACT" & clickResponse == "EXTRACT":
            - add a point to the active dataset
        dataDestination == "CALI_X" & clickResponse == "EXTRACT":
            - update the x calibration data
        dataDestination == "CALI_Y" & clickResponse == "EXTRACT":
            - update the y calibration data

        """

        if self.dataDestination == "NONE":
            return
        if self.clickResponse != "EXTRACT":
            return
        if event.xdata is None or event.ydata is None:
            return

        # position of the click
        xdata, ydata = self.axes.transData.inverted().transform((event.x, event.y))
        xName = self.measDataSet.currentMeasData.principalX.name
        yName = self.measDataSet.currentMeasData.principalY.name

        # select mode
        if self.dataDestination == "EXTRACT":
            return self.storeExtractedPoint(xName, yName, xdata, ydata)

        # calibration mode
        if self.dataDestination in ["CALI_X", "CALI_Y"]:
            return self.storeCalibrationPoint(xName, yName, xdata, ydata)

    def createStandaloneCanvas(
        self, 
        selectedDataNames: List[str | int] | None = None,
        numericalPoints: int = 10, 
        xLim: Tuple[float, float] | None = None, 
        yLim: Tuple[float, float] | None = None,
    ):
        """
        Create a standalone canvas with multiple measurement data.
        
        Parameters
        ----------
        selectedDataNames: List[str | int]
            The names (or indices) of the measurement data to be displayed.
        numericalPoints: int
            To plot the numerical calculation, the number of points to be 
            swept over.
        xLim: Tuple[float, float] | None
            The x limits of the canvas. Currently not supported.
        yLim: Tuple[float, float] | None
            The y limits of the canvas. Currently not supported.
        """
        if xLim is not None or yLim is not None:
            raise NotImplementedError("Setting a custom x or y limit is not implemented")
        
        # create a unique name for the canvas: e.g. "Collection (1)"
        existingNames = list(self.standaloneCanvases.keys())
        canvasName = makeUnique(existingNames + ["Collection"])[-1]
        canvas = MplFigureCanvas(standalone=True)

        # step 1: add the selected measurement data to the canvas -------------
        fullData = self.measDataSet.fullData
        selectedData = []
        figNames = []
        if selectedDataNames is None:
            selectedDataNames = range(len(fullData))
        for idx, data in enumerate(fullData):
            if idx in selectedDataNames or data.name in selectedDataNames:
                selectedData.append(data)
                figNames.append(data.name)

        # all of the data must be collinear with each other
        for data in selectedData[1:]:
            if not selectedData[0].isCollinearWith(data):
                raise ValueError(f"Data {data.name} are not collinear with {selectedData[0].name}")
            
        for data in selectedData:
            elem = copy.deepcopy(data.generatePlotElement())
            canvas._plottingElements[elem.fileName] = elem
        canvas.plotAllElements()
            
        # step 2: relim the canvas --------------------------------------------
        # collect all the rawX and rawY axes
        allRawX = OrderedDictMod()
        allRawY = OrderedDictMod()
        for data in selectedData:
            for key, val in data.rawX.items():
                if key not in allRawX:
                    allRawX[key] = val
                else:
                    allRawX[key] = np.concatenate([allRawX[key], val])
            for key, val in data.rawY.items():
                if key not in allRawY:
                    allRawY[key] = val
                else:
                    allRawY[key] = np.concatenate([allRawY[key], val])
                
        # extract the min and max of each axis that enclose all the data
        rawX = OrderedDictMod()
        rawY = OrderedDictMod()
        for key, val in allRawX.items():
            rawX[key] = np.array([np.min(val), np.max(val)])
        for key, val in allRawY.items():
            rawY[key] = np.array([np.min(val), np.max(val)])
            
        # set the boundary of the measurement data
        prcpXName = selectedData[0].principalX.name
        prcpYName = selectedData[0].principalY.name
        canvas.relimPrincipalAxes(
            x=rawX[prcpXName],
            y=rawY[prcpYName]
        )
        
        # store the standalone canvas (used in setXYAxesForStandaloneCanvas)
        self.standaloneCanvases[canvasName] = StandaloneCanvasAndConfigs(
            name=canvasName,
            rawX=rawX,
            rawY=rawY,
            canvas=canvas,
            figNames=figNames,
        )
        
        # set the axes
        self._setXYAxesForStandaloneCanvas(canvasName)
        
        # step 3: add the numerical calculation -------------------------------
        allPrcpX = np.array([])

        for data in selectedData:
            assert data.principalX.name == prcpXName, "principalX names are not the same"
            
            allPrcpX = np.concatenate([allPrcpX, data.principalX.data])
            
        self.quantumModel._newStandaloneCanvas(
            name=canvasName,
            pointsAdded=numericalPoints,
            xLim=(np.min(allPrcpX), np.max(allPrcpX)),
            caliByFigName=selectedData[0].name,
        )
        
        # step 4: connect the signals -----------------------------------------
        self.quantumModel._sweepConfigsForStandaloneCanvas[
            canvasName
        ].readyToPlot.connect(canvas.updateElement)
        
        canvas.canvasClosed.connect(
            lambda canvasName=canvasName: self.removeStandaloneCanvas(canvasName)
        )
        
        # step 5: show the canvas ---------------------------------------------
        canvas.canvas.draw()
        canvas.show()

    def removeStandaloneCanvas(self, canvasName: str):
        """
        Remove a standalone canvas.
        """
        self.quantumModel._removeSweepForStandaloneCanvas(canvasName)
        self.standaloneCanvases.pop(canvasName)
        
        