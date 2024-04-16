from PySide6.QtCore import Slot, QObject, Signal

from qfit.widgets.mpl_canvas import MplFigureCanvas

import numpy as np
import matplotlib as mpl
from qfit.utils.helpers import ySnap, OrderedDictMod
from qfit.models.measurement_data import (
    MeasDataType,
)
from qfit.models.data_structures import FilterConfig
from qfit.settings import MARKER_SIZE

from typing import TYPE_CHECKING, Union, Dict, Any, Tuple, Literal, List, Callable

if TYPE_CHECKING:
    from qfit.models.calibration import CaliParamModel

    from qfit.models.parameter_set import SweepParamSet
    from qfit.models.measurement_data import MeasDataSet
    from qfit.models.extracted_data import AllExtractedData, ActiveExtractedData
    from qfit.models.numerical_model import QuantumModel
    from qfit.views.paging_view import PageView


mpl.rcParams["toolbar"] = "None"
mpl.use("qtagg")


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
        self.setXYAxes(self.measDataSet.currentMeasData)
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
            self.setXYAxes(self.measDataSet.currentMeasData)

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
        # self.setXYAxes(self.measData.currentMeasData)  # will be called when relimCanvas  

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
        self.setXYAxes(self.measDataSet.currentMeasData)

    def setXYAxes(self, measData: MeasDataType):
        """
        Update the x and y axes of the canvas based on the current measurement data
        and the calibration functions.
        """

        if self.measDataSet.rowCount() == 0:
            # not yet initialized
            return

        rawX = measData.rawX
        rawY = measData.rawY
        rawXLim = {key: (val[0], val[-1]) for key, val in rawX.items()}
        rawYLim = rawY.itemByIndex(0)  # only have one key

        if not self.calibrateAxes:
            self.mplCanvas.updateXAxes(rawXLim)
            self.mplCanvas.updateYAxes(
                rawYLim.name, (rawYLim.data[0], rawYLim.data[-1])
            )
            return

        # when need to show the calibrated data
        # x calibration
        currentSweepParam = self.XCaliFuncDict[
            self.measDataSet.currentMeasData.name
        ]

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

        self.mplCanvas.updateXAxes(mappedXLim)
        self.mplCanvas.updateYAxes(mappedYName, mappedYLim)

    def onXCaliFuncUpdated(self, XCaliFuncDict: Dict[str, "SweepParamSet"]):
        """Update the X calibration function and the labels on the canvas."""
        self.XCaliFuncDict = XCaliFuncDict
        self.setXYAxes(self.measDataSet.currentMeasData)

    def onYCaliFuncUpdated(self, YCaliFunc: Callable, invYCaliFunc: Callable):
        """Update the Y calibration function and the labels on the canvas."""
        self.YCaliFunc = YCaliFunc
        self.invYCaliFunc = invYCaliFunc
        self.setXYAxes(self.measDataSet.currentMeasData)

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
        self.quantumModel.readyToPlot.connect(self.mplCanvas.updateElement)

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
        self.canvasTools["reset"].clicked.connect(self.mplCanvas.resetView)
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
