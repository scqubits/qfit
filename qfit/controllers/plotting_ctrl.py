from PySide6.QtCore import Slot, QObject, Signal

from qfit.widgets.mpl_canvas import MplFigureCanvas

import numpy as np
import matplotlib as mpl
import scqubits as scq
from qfit.utils.helpers import y_snap, OrderedDictMod
from qfit.models.measurement_data import (
    NumericalMeasurementData,
    ImageMeasurementData,
    MeasurementDataType,
)

from qfit.models.data_structures import QMSweepParam

from typing import TYPE_CHECKING, Union, Dict, Any, Tuple, Literal, List, Callable

if TYPE_CHECKING:
    from qfit.models.calibration import CaliParamModel

    from qfit.models.parameter_set import SweepParamSet
    # from qfit.models.calibration_data import CalibrationData
    from qfit.models.measurement_data import MeasDataSet
    from qfit.models.extracted_data import AllExtractedData, ActiveExtractedData
    from qfit.models.numerical_model import QuantumModel
    from qfit.views.paging_view import PageView


mpl.rcParams["toolbar"] = "None"
mpl.use("qtagg")


class PlottingCtrl(QObject):
    """
    Establishes the connection among the mpl canvas, the mpl toolbar, and the
    other user interfaces.
    """

    disconnectCanvas: bool
    xSnapTool: bool
    trans0Focused: bool
    axisSnap: Literal["X", "Y", "OFF"]
    clickResponse: Literal[
        "ZOOM",
        "PAN",
        "EXTRACT",
    ]
    dataDestination: Literal["CALI_X", "CALI_Y", "EXTRACT", "NONE"]

    # other annotations
    pageView: "PageView"
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
            # "ParamSet",
        ],
        views: Tuple[Any, ...],
        # calibrationStates: Dict[str, Literal['CALIBRATE_X1', 'CALIBRATE_X2', 'CALIBRATE_Y1', 'CALIBRATE_Y2']],
    ):
        super().__init__(parent)
        (
            self.measurementData,
            self.calibrationModel,
            self.allDatasets,
            self.activeDataset,
            self.quantumModel,
            # self.sweepParameterSet,
        ) = models
        (
            self.measComboBoxes,
            self.measPlotSettings,
            self.swapXYButton,
            self.canvasTools,
            self.calibrationButtons,
            self.calibratedCheckBox,
            self.pageView,
        ) = views
        self.mplCanvas = mplCanvas
        self.axes = mplCanvas.axes
        self._staticInit()

    def _staticInit(self):
        self.disconnectCanvas = False  # used to temporarily switch off canvas updates
        self.xSnapTool = True  # whether the horizontal snap is on
        self.trans0Focused = True  # whether the first transition is focused
        self.axisSnap = "OFF"  # the axis snap mode, override xSnap when not "OFF"
        self.clickResponse = "EXTRACT"  # the response to a mouse click
        self.dataDestination = "NONE"  # the destination of the data after a click
        self.calibrateAxes = False  # whether the ticklabels are calibrated

        self.canvasToolConnects()
        self.staticPlotElementsConnects()
        self.mouseClickConnects()
        self.plottingModeConnects()
        self.caliConnects()

        # Although measurement data is updated when reloaded,
        # but swapXY only involves the "pointer" of measurement data,
        # so it only need to be connected once.
        self.swapXYButton.clicked.connect(self.swapXY)

        # previously in dynamicalInit
        self.measPlotSettingConnects()
        # self.uiXYZComboBoxesConnects()
        self.dynamicalPlotElementsConnects()

    def dynamicalInit(
        self,
        measurementData: List["MeasurementDataType"],
    ):
        self.measurementData.dynamicalInit(measurementData)
        self.measDataComboBoxesInit()

        # plot everything available
        self.measurementData.emitReadyToPlot()
        self.measurementData.emitRelimCanvas()
        self.measurementData.emitRawXMap()
        self.activeDataset.emitReadyToPlot()
        self.allDatasets.emitReadyToPlot()
        self.allDatasets.emitFocusChanged()  # update the snapX
        self.setXYAxes()
        self.updateCursor()

    # measurement ======================================================
    def measDataComboBoxesInit(self):
        """
        Load the available data into the combo boxes for the x, y, and z axes.
        """
        zDataNames = list(self.measurementData.currentMeasData._zCandidates.keys())
        self.measComboBoxes["z"].clear()
        self.measComboBoxes["z"].addItems(zDataNames)
        self.measComboBoxes["z"].setCurrentText(
            self.measurementData.currentMeasData.currentZ.name
        )
        # self.setupXYDataBoxes()

    def measPlotSettingConnects(self):
        """Connect the UI elements related to display of data"""
        self.measPlotSettings["topHat"].toggled.connect(
            self.measurementData.toggleTopHatFilter
        )
        self.measPlotSettings["wavelet"].toggled.connect(
            self.measurementData.toggleWaveletFilter
        )
        self.measPlotSettings["edge"].toggled.connect(
            self.measurementData.toggleEdgeFilter
        )
        self.measPlotSettings["bgndX"].toggled.connect(
            self.measurementData.toggleBgndSubtractX
        )
        self.measPlotSettings["bgndY"].toggled.connect(
            self.measurementData.toggleBgndSubtractY
        )
        self.measPlotSettings["log"].toggled.connect(
            self.measurementData.toggleLogColoring
        )
        self.measPlotSettings["min"].valueChanged.connect(self.measurementData.setZMin)
        self.measPlotSettings["max"].valueChanged.connect(self.measurementData.setZMax)

        self.measPlotSettings["color"].currentTextChanged.connect(
            self.mplCanvas.updateColorMap
        )

    def uiXYZComboBoxesConnects(self):
        self.measComboBoxes["z"].activated.connect(self.zDataUpdate)
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
        self.measurementData.setCurrentZ(itemIndex)
        # self.setupXYDataBoxes()

    # @Slot(int)
    # def xAxisUpdate(self, itemIndex: int):
    #     self.measurementData.setCurrentX(itemIndex)

    # @Slot(int)
    # def yAxisUpdate(self, itemIndex: int):
    #     self.measurementData.setCurrentY(itemIndex)

    @Slot()
    def swapXY(self):
        """
        Swap the x and y axes of the measurement data. It should be called
        at the end when the swapXY button is clicked as it updates the
        plot.
        """
        self.mplCanvas.plottingDisabled = True

        # maybe: self.calibrationData.swapXY()

        self.measurementData.swapXY()
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
        self.calibratedCheckBox.toggled.connect(self.toggleCalibrateAxes)
        self.calibrationModel.xCaliUpdated.connect(self.onXCaliFuncUpdated)
        self.calibrationModel.yCaliUpdated.connect(self.onYCaliFuncUpdated)

    @Slot(bool)
    def toggleCalibrateAxes(self, checked: bool):
        """If calibration check box is changed, toggle the calibration status of the
        calibrationData. Also induce change at the level of the displayed data of
        selected points."""

        self.calibrateAxes = checked
        self.setXYAxes()

    def setXYAxes(self):
        """
        Toggle the labels on the canvas.
        TODO: more bugs to fix on zooming, swapping xy, etc.
        """

        if self.measurementData.rowCount() == 0:
            # not yet initialized
            return

        rawX = self.measurementData.currentMeasData.rawX
        rawY = self.measurementData.currentMeasData.rawY
        rawXLim = {key: (val[0], val[-1]) for key, val in rawX.items()}
        rawYLim = rawY.itemByIndex(0)   # only have one key
        
        if not self.calibrateAxes:
            self.mplCanvas.updateXAxes(rawXLim)
            self.mplCanvas.updateYAxes(rawYLim.name, (rawYLim.data[0], rawYLim.data[-1]))

            return

        # when need to show the calibrated data
        # x calibration
        currentSweepParam = self.XCaliFuncDict[self.measurementData.currentMeasData.name]

        currentSweepParam.setByRawX(
            {key: rng[0] for key, rng in rawXLim.items()}
        )
        mappedXLeft = currentSweepParam.getFlattenedAttrDict("value")
        currentSweepParam.setByRawX(
            {key: rng[1] for key, rng in rawXLim.items()}
        )
        mappedXRight = currentSweepParam.getFlattenedAttrDict("value")
        mappedXLim = {
            key: (mappedXLeft[key], mappedXRight[key]) 
            for key in mappedXLeft.keys()
        }

        # y calibration
        mappedYName = f"Energy [GHz]"
        # ylabel = f"Energy [{scq.get_units()}]" # when we implement the units
        mappedYLim = (
            self.YCaliFunc(rawYLim.data[0]), 
            self.YCaliFunc(rawYLim.data[-1])
        )

        self.mplCanvas.updateXAxes(mappedXLim)
        self.mplCanvas.updateYAxes(mappedYName, mappedYLim)

    # plotting =========================================================
    def staticPlotElementsConnects(self):
        """
        Should be done at the end and will emit all readyToPlot signal
        """
        self.activeDataset.readyToPlot.connect(self.mplCanvas.updateElement)
        self.allDatasets.readyToPlot.connect(self.mplCanvas.updateElement)
        self.allDatasets.readyToPlotX.connect(self.mplCanvas.updateElement)

        self.allDatasets.distinctXUpdated.connect(
            self.mplCanvas.updateCursorXSnapValues
        )

    def dynamicalPlotElementsConnects(self):
        """
        Should be done at the end and will emit all readyToPlot signal
        """
        self.measurementData.readyToPlot.connect(self.mplCanvas.updateElement)
        self.measurementData.relimCanvas.connect(self.mplCanvas.relim)
        self.quantumModel.readyToPlot.connect(self.mplCanvas.updateElement)
        return

    def mouseClickConnects(self):
        """Set up the matplotlib canvas and start monitoring for mouse click events in the canvas area."""
        self.cidCanvas = self.mplCanvas.canvas.mpl_connect(
            "button_press_event", self.canvasClickMonitoring
        )

        self.cidMove = self.mplCanvas.canvas.mpl_connect(
            "motion_notify_event", self.canvasMouseMonitoring
        )

    def canvasToolConnects(self):
        """Connect the UI buttons for reset, zoom, and pan functions of the matplotlib canvas."""
        self.canvasTools["reset"].clicked.connect(self.mplCanvas.resetView)
        self.canvasTools["zoom"].clicked.connect(self.toggleZoom)
        self.canvasTools["pan"].clicked.connect(self.togglePan)
        self.canvasTools["select"].clicked.connect(self.toggleSelect)

    def plottingModeConnects(self):
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
        self.xSnapTool = checked
        self.updateCursor()

    @property
    def xSnap(self):
        """
        Only in the extract mode, focusing on a transition other than 
        the first one, x snap can be turned on.
        """
        return (
            self.xSnapTool 
            and not self.trans0Focused
            and self.dataDestination == "EXTRACT"
        )

    def setTrans0Focused(self, checked: bool):
        self.trans0Focused = checked
        self.updateCursor()

    def setClickResponse(self, response: Literal["ZOOM", "PAN", "EXTRACT"]):
        self.clickResponse = response
        self.updateCursor()

    @Slot()
    def setDataDestAxisSnap(
        self,
        destination: Literal["CALI_X", "CALI_Y", "EXTRACT", "NONE"],
    ):
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
        self.setClickResponse("EXTRACT")
        self.mplCanvas.selectOn()

    @Slot()
    def toggleZoom(self):
        self.setClickResponse("ZOOM")
        self.mplCanvas.zoomView()

    @Slot()
    def togglePan(self):
        self.setClickResponse("PAN")
        self.mplCanvas.panView()

    def updateCursor(self):
        """
        Callback for updating the matching mode and the cursor.

        When will this method be called?
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
        """Main loop for acting on mouse events occurring in the canvas area."""

        if self.dataDestination == "NONE":
            return
        if self.clickResponse != "EXTRACT":
            return
        if event.xdata is None or event.ydata is None:
            return

        # process the data
        xName = self.measurementData.currentMeasData.currentX.name
        yName = self.measurementData.currentMeasData.currentY.name
        xyDict = OrderedDictMod(
            {
                xName: event.xdata,
                yName: event.ydata,
            }
        )  # needed by extracted data
        rawX = self.measurementData.currentMeasData.rawXByCurrentX(event.xdata)
        rawXYDict = rawX | xyDict  # needed by calibration data

        # calibration mode
        if self.dataDestination in ["CALI_X", "CALI_Y"]:
            # model: update the calibration data
            self.calibrationModel.processSelectedPtFromPlot(
                data=rawXYDict, figName=self.measurementData.currentMeasData.name
            )
            # the above will then trigger the update the view:
            # turn off highlighting, set value, etc

            # controller: update the status
            self.dataDestination = "NONE"
            return

        # select mode
        if self.dataDestination == "EXTRACT":
            current_data = self.activeDataset.allPoints()

            # x snap
            snappedX = self.mplCanvas.specialCursor.snapToProperX(event.xdata)
            xyDict[xName] = snappedX
            rawX = self.measurementData.currentMeasData.rawXByCurrentX(snappedX)
            if not self.xSnapTool:
                # turn on the horizontal snap automatically, if the user turned it off
                self.canvasTools["snapX"].setChecked(True)

            # remove the point if it is close to another point
            for index, x2y2 in enumerate(current_data.transpose()):
                if self.isRelativelyClose(np.array(xyDict.valList), x2y2):
                    self.activeDataset.remove(index)
                    return

            # y snap
            if self.canvasTools["snapY"].isChecked():
                x_list = self.measurementData.currentMeasData.currentX.data
                y_list = self.measurementData.currentMeasData.currentY.data
                z_data = self.measurementData.currentMeasData.currentZ.data

                # calculate half index range as 5x linewidth
                linewidth = 0.02  # GHz
                half_y_range = linewidth * 5
                try:
                    snapped_y1 = y_snap(
                        x_list=x_list,
                        y_list=y_list,
                        z_data=z_data,
                        user_selected_xy=xyDict.valList,
                        half_y_range=half_y_range,
                        mode="lorentzian",
                    )
                    xyDict[yName] = snapped_y1

                except RuntimeError:
                    pass

            self.activeDataset.append(xyDict, rawX)

    @Slot()
    def canvasMouseMonitoring(self, event):
        self.axes.figure.canvas.flush_events()
        if not self.xSnapTool:
            return

        if event.xdata is None or event.ydata is None:
            return

    def onXCaliFuncUpdated(self, XCaliFuncDict: Dict[str, "SweepParamSet"]):
        """Update the X calibration function and the labels on the canvas."""
        self.XCaliFuncDict = XCaliFuncDict
        self.setXYAxes()

    def onYCaliFuncUpdated(self, YCaliFunc: Callable, invYCaliFunc: Callable):
        """Update the Y calibration function and the labels on the canvas."""
        self.YCaliFunc = YCaliFunc
        self.invYCaliFunc = invYCaliFunc
        self.setXYAxes()

    def isRelativelyClose(self, x1y1: np.ndarray, x2y2: np.ndarray):
        """Check whether the point x1y1 is relatively close to x2y2, given the current
        field of view on the canvas."""
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        xmin, xmax = xlim
        ymin, ymax = ylim
        xrange = xmax - xmin
        yrange = ymax - ymin
        x1y1 = x1y1 / [xrange, yrange]
        x2y2 = x2y2 / [xrange, yrange]

        distance = np.linalg.norm(x1y1 - x2y2)
        if distance < 0.025:
            return True

        return False
