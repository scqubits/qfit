# mainwindow.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import copy
import sys
from functools import partial
from typing import TYPE_CHECKING, Dict, Tuple, Union

import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np

from scqubits.core.hilbert_space import HilbertSpace

from PySide6.QtCore import QPoint, QRect, QSize, Qt, Slot
from PySide6.QtGui import QColor, QMouseEvent, Qt
from PySide6.QtWidgets import (
    QLabel, 
    QWidget,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
    QMessageBox,
    QPushButton,
    QStyle,
)

import qfit.core.app_state as appstate
from qfit.models.calibration_data import CalibrationData
from qfit.widgets.calibration import CalibrationView
from qfit.core.app_state import State
from qfit.core.helpers import transposeEach
from qfit.models.extracted_data import ActiveExtractedData, AllExtractedData
from qfit.widgets.data_tagging import TagDataView
from qfit.io_utils.import_data import importFile
from qfit.io_utils.save_data import saveFile
from qfit.settings import color_dict
from qfit.ui_views.resizable_window import ResizableFramelessWindow
from qfit.ui_designer.ui_window import Ui_MainWindow
from qfit.widgets.menu import MenuWidget

from qfit.models.quantum_model_parameters import (
    QuantumModelSliderParameter, QuantumModelParameterSet)
from qfit.models.numerical_spectrum_data import SpectrumData
from qfit.controllers.numerical_model import QuantumModel
from qfit.widgets.grouped_sliders import GroupedSliders, GroupedSliderSet

if TYPE_CHECKING:
    from qfit.widgets.calibration import CalibrationLineEdit
    from qfit.models.qfit_data import QfitData

MeasurementDataType = Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]

mpl.rcParams["toolbar"] = "None"


class MainWindow(ResizableFramelessWindow):
    """Class for the main window of the app."""

    ui: Ui_MainWindow
    # ui_menu: Ui_MenuWidget

    measurementData: MeasurementDataType
    extractedData: "QfitData"
    activeDataset: ActiveExtractedData
    allDatasets: AllExtractedData
    tagDataView: TagDataView

    calibrationData: CalibrationData
    calibrationView: CalibrationView
    rawLineEdits: Dict[str, "CalibrationLineEdit"]
    mapLineEdits: Dict[str, "CalibrationLineEdit"]
    calibrationButtons: Dict[str, QPushButton]
    calibrationStates: Dict[str, State]


    axes: mpl.axes.Axes
    cidCanvas: int
    offset: Union[None, QPoint]

    def __init__(self, measurementData, hilbert_space, extractedData=None):
        ResizableFramelessWindow.__init__(self)
        self.disconnectCanvas = False  # used to temporarily switch off canvas updates

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # fix visibility of collapsible panels
        self.ui.xyzDataGridFrame.setVisible(False)
        self.ui.calibrationQFrame.setVisible(False)
        self.ui.filterQFrame.setVisible(False)

        self.ui_menu = MenuWidget(parent=self)

        self.setShadows()

        self.uiPagesConnects()
        self.uiMenuConnects()

        self.setupUICalibration()
        self.calibrationData = CalibrationData()
        self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())

        self.matching_mode = False
        self.mousedat = None

        self.setupUIPlotOptions()

        self.measurementData = measurementData
        self.extractedData = extractedData
        self.dataSetupConnects()

        # prefit: controller, two models and their connection to view (sliders)
        self.sliderParameterSet = QuantumModelParameterSet()
        self.spectrumData = SpectrumData()
        self.quantumModel = QuantumModel(hilbert_space)
        self.quantumModel.generateSliderParameterSets(
            self.sliderParameterSet,
            excluded_parameter_type = [
                "ng", "flux", "cutoff", "truncated_dim"
            ]
        )
        self.dynamicalSlidersInserts()

        # setup mpl canvas
        self.uiColorScaleConnects()
        self.uiCalibrationConnects()
        self.uiCanvasControlConnects()
        self.uiMplCanvasConnects()
        self.ui.mplFigureCanvas.selectOn()

        # prefit: connect the data model to the sliders, canvas, boxes etc. Should be done after
        # the canvas is set up.
        self.dynamicalSlidersConnects()
        self.setUpSpectrumPlotConnects()
        
        self.setFocusPolicy(Qt.StrongFocus)
        self.offset = None

    def dataSetupConnects(self):
        self.measurementData.setupUICallbacks(
            self.dataCheckBoxCallbacks, self.plotRangeCallback
        )
        self.setupUIData()
        self.setupUIXYZComboBoxes()
        self.tagDataView = TagDataView(self.ui)
        self.uiDataConnects()
        self.uiDataOptionsConnects()
        self.uiDataControlConnects()
        self.uiXYZComboBoxesConnects()

        if self.extractedData is not None:
            self.allDatasets.dataNames = self.extractedData.datanames
            self.allDatasets.assocDataList = transposeEach(self.extractedData.datalist)
            self.allDatasets.assocTagList = self.extractedData.tag_data
            self.calibrationData.setCalibration(
                *self.extractedData.calibration_data.allCalibrationVecs()
            )

            self.calibrationView.setView(*self.calibrationData.allCalibrationVecs())
            self.activeDataset._data = self.allDatasets.currentAssocItem()
            self.tagDataView.setTag(self.allDatasets.currentTagItem())
            self.allDatasets.layoutChanged.emit()
            self.activeDataset.layoutChanged.emit()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.offset = None
        super().mouseReleaseEvent(event)

    def setShadows(self):
        for button in [
            self.ui.newRowButton,
            self.ui.deleteRowButton,
            self.ui.clearAllButton,
            self.ui.calibrateX1Button,
            self.ui.calibrateX2Button,
            self.ui.calibrateY1Button,
            self.ui.calibrateY2Button,
        ]:
            eff = QGraphicsDropShadowEffect(button)
            eff.setOffset(2)
            eff.setBlurRadius(18.0)
            eff.setColor(QColor(0, 0, 0, 90))
            button.setGraphicsEffect(eff)

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

    def setupUICalibration(self):
        """For the interface that enables calibration of data with respect to x and y axis, group QLineEdit elements
        and the corresponding buttons in dicts. Set up a dictionary mapping calibration labels to the corresponding
        State choices. Finally, set up an instance of CalibrationData and
        CalibrationView"""
        self.rawLineEdits = {
            "X1": self.ui.rawX1LineEdit,
            "X2": self.ui.rawX2LineEdit,
            "Y1": self.ui.rawY1LineEdit,
            "Y2": self.ui.rawY2LineEdit,
        }
        self.mapLineEdits = {
            "X1": self.ui.mapX1LineEdit,
            "X2": self.ui.mapX2LineEdit,
            "Y1": self.ui.mapY1LineEdit,
            "Y2": self.ui.mapY2LineEdit,
        }
        self.calibrationButtons = {
            "X1": self.ui.calibrateX1Button,
            "X2": self.ui.calibrateX2Button,
            "Y1": self.ui.calibrateY1Button,
            "Y2": self.ui.calibrateY2Button,
        }
        self.calibrationStates = {
            "X1": State.CALIBRATE_X1,
            "X2": State.CALIBRATE_X2,
            "Y1": State.CALIBRATE_Y1,
            "Y2": State.CALIBRATE_Y2,
        }

        self.calibrationView = CalibrationView(self.rawLineEdits, self.mapLineEdits)

    def setupUIPlotOptions(self):
        self.dataCheckBoxCallbacks = {
            "topHatFilter": self.ui.topHatCheckBox.isChecked,
            "waveletFilter": self.ui.waveletCheckBox.isChecked,
            "edgeFilter": self.ui.edgeFilterCheckBox.isChecked,
            "bgndSubtractX": self.ui.bgndSubtractXCheckBox.isChecked,
            "bgndSubtractY": self.ui.bgndSubtractYCheckBox.isChecked,
            "logColoring": self.ui.logScaleCheckBox.isChecked,
        }

    def plotRangeCallback(self):
        val1 = self.ui.rangeSliderMin.value() / 100.0
        val2 = self.ui.rangeSliderMax.value() / 100.0
        min_val = min(val1, val2)
        max_val = max(val1, val2)
        return [min_val, max_val]

    def setupUIData(self):
        """Set up the main class instances holding the data extracted from placing
        markers on the canvas. The AllExtractedData instance holds all data, whereas the
        ActiveExtractedData instance holds data of the currently selected data set."""
        self.activeDataset = ActiveExtractedData()
        self.activeDataset.setAdaptiveCalibrationFunc(
            self.calibrationData.adaptiveConversionFunc
        )
        self.ui.dataTableView.setModel(self.activeDataset)

        self.allDatasets = AllExtractedData()
        self.allDatasets.setCalibrationFunc(self.calibrationData.calibrateDataset)
        self.ui.datasetListView.setModel(self.allDatasets)

    def setupUIXYZComboBoxes(self):
        zDataNames = list(self.measurementData.zCandidates.keys())
        self.ui.zComboBox.clear()
        self.ui.zComboBox.addItems(zDataNames)
        self.ui.zComboBox.setCurrentText(self.measurementData.currentZ.name)
        self.setupXYDataBoxes()

    def uiPagesConnects(self):
        self.ui.modeSelectButton.clicked.connect(
            lambda: self.ui.pagesStackedWidget.setCurrentIndex(0)
        )
        self.ui.modeTagButton.clicked.connect(
            lambda: self.ui.pagesStackedWidget.setCurrentIndex(1)
        )
        self.ui.modePlotButton.clicked.connect(
            lambda: self.ui.pagesStackedWidget.setCurrentIndex(2)
        )
        self.ui.modeFitButton.clicked.connect(
            lambda: self.ui.pagesStackedWidget.setCurrentIndex(3)
        )

    def uiDataConnects(self):
        """Make connections for changes in data."""
        # Whenever the data layout in the ActiveExtractedData changes, update
        # the corresponding AllExtractedData data; this includes the important
        # event of adding extraction points to the ActiveExtractedData
        self.activeDataset.layoutChanged.connect(
            lambda: self.ui.datasetListView.model().updateAssocData(
                newData=self.activeDataset.all()
            )
        )

        # If data in the TableView is changed manually through editing,
        # the 'dataChanged' signal will be emitted. The following connects the signal
        # to an update in th data stored in the AllExtractedData
        self.activeDataset.dataChanged.connect(
            lambda topLeft, bottomRight: self.ui.datasetListView.model().updateAssocData(
                newData=self.activeDataset.all()
            )
        )

        # Whenever the AllExtractedData changes layout - for example, due to
        # switching from one existing data set to another one, this connection will
        # ensure that the TableView will be updated with the correct data
        self.allDatasets.layoutChanged.connect(
            lambda: self.activeDataset.setAllData(
                newData=self.allDatasets.currentAssocItem()
            )
        )

        # Whenever data sets are added or removed from the ListView, this ensures
        # that the canvas display is updated.
        self.allDatasets.layoutChanged.connect(self.updatePlot)

        # Each time the data set is changed on ListView/Model by clicking a data set,
        # the data in ActiveExtractedData is updated to reflect the new selection.
        self.ui.datasetListView.clicked.connect(
            lambda: self.activeDataset.setAllData(
                newData=self.allDatasets.currentAssocItem()
            )
        )

        # A new selection of a data set item in ListView is accompanied by an update
        # of the canvas to show the appropriate plot of selected points
        self.ui.datasetListView.clicked.connect(lambda: self.updatePlot(init=False))

        # Whenever tag type or tag data is changed, update the AllExtractedData data
        self.tagDataView.changedTagType.connect(
            lambda: self.allDatasets.updateCurrentTag(self.tagDataView.getTag())
        )
        self.tagDataView.changedTagData.connect(
            lambda: self.allDatasets.updateCurrentTag(self.tagDataView.getTag())
        )

        # Whenever a new dataset is activated in the AllExtractedData, update the TagDataView
        self.ui.datasetListView.clicked.connect(
            lambda: self.tagDataView.setTag(self.allDatasets.currentTagItem())
        )

    def uiDataOptionsConnects(self):
        """Connect the UI elements related to display of data"""
        self.ui.topHatCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.waveletCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.edgeFilterCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.bgndSubtractXCheckBox.toggled.connect(lambda x: self.updatePlot())
        self.ui.bgndSubtractYCheckBox.toggled.connect(lambda x: self.updatePlot())

    def uiColorScaleConnects(self):
        """Connect the color scale related UI elements."""
        # Toggling the loc scale check box prompts replotting.
        self.ui.logScaleCheckBox.toggled.connect(lambda x: self.updatePlot())

        # Changes in the color map dropdown menu prompt replotting.
        self.ui.colorComboBox.activated.connect(lambda x: self.updatePlot())

        # Ensure that a change in the range slider positions cause an update of the plot.
        self.ui.rangeSliderMin.valueChanged.connect(lambda x: self.updatePlot())
        self.ui.rangeSliderMax.valueChanged.connect(lambda x: self.updatePlot())

    def uiCalibrationConnects(self):
        """Connect UI elements for data calibration."""
        self.ui.calibratedCheckBox.toggled.connect(self.toggleCalibration)

        for label in self.calibrationButtons:
            self.calibrationButtons[label].clicked.connect(
                partial(self.calibrate, label)
            )

        for lineEdit in list(self.rawLineEdits.values()) + list(
            self.mapLineEdits.values()
        ):
            lineEdit.editingFinished.connect(self.updateCalibration)

    def uiCanvasControlConnects(self):
        """Connect the UI buttons for reset, zoom, and pan functions of the matplotlib canvas."""
        self.ui.resetViewButton.clicked.connect(self.ui.mplFigureCanvas.resetView)
        self.ui.zoomViewButton.clicked.connect(self.toggleZoom)
        self.ui.panViewButton.clicked.connect(self.togglePan)
        self.ui.selectViewButton.clicked.connect(self.toggleSelect)
        self.ui.swapXYButton.clicked.connect(self.swapXY)

    def uiDataControlConnects(self):
        """Connect buttons for inserting and deleting a data set, or clearing all data sets"""
        self.ui.newRowButton.clicked.connect(self.allDatasets.newRow)
        self.ui.deleteRowButton.clicked.connect(self.allDatasets.removeCurrentRow)
        self.ui.clearAllButton.clicked.connect(self.allDatasets.removeAll)

        self.ui.newRowButton.clicked.connect(
            lambda: self.tagDataView.setTag(self.allDatasets.currentTagItem())
        )
        self.ui.deleteRowButton.clicked.connect(
            lambda: self.tagDataView.setTag(self.allDatasets.currentTagItem())
        )
        self.ui.clearAllButton.clicked.connect(
            lambda: self.tagDataView.setTag(self.allDatasets.currentTagItem())
        )

    def uiXYZComboBoxesConnects(self):
        self.ui.zComboBox.activated.connect(self.zDataUpdate)
        self.ui.xComboBox.activated.connect(self.xAxisUpdate)
        self.ui.yComboBox.activated.connect(self.yAxisUpdate)

    def uiMplCanvasConnects(self):
        """Set up the matplotlib canvas and start monitoring for mouse click events in the canvas area."""
        self.axes = self.ui.mplFigureCanvas.canvas.figure.subplots()
        self.updatePlot(initialize=True)
        self.cidCanvas = self.axes.figure.canvas.mpl_connect(
            "button_press_event", self.canvasClickMonitoring
        )
        self.ui.mplFigureCanvas.set_callback(self.allDatasets)
        self.cidMove = self.axes.figure.canvas.mpl_connect(
            "motion_notify_event", self.canvasMouseMonitoring
        )

    def uiMenuConnects(self):
        self.ui.toggleMenuButton.clicked.connect(self.ui_menu.toggle)
        # self.ui_menu.menuQuitButton.clicked.connect(self.closeApp)
        # self.ui_menu.menuOpenButton.clicked.connect(self.openFile)

    def setupXYDataBoxes(self):
        self.ui.xComboBox.clear()
        xDataNames = list(self.measurementData.currentXCompatibles.keys())
        self.ui.xComboBox.addItems(xDataNames)
        self.ui.xComboBox.setCurrentText(self.measurementData.currentX.name)

        self.ui.yComboBox.clear()
        yDataNames = list(self.measurementData.currentYCompatibles.keys())
        self.ui.yComboBox.addItems(yDataNames)
        self.ui.yComboBox.setCurrentText(self.measurementData.currentY.name)

    @Slot()
    def toggleSelect(self):
        if appstate.state != State.SELECT:
            appstate.state = State.SELECT
            self.ui.mplFigureCanvas.selectOn()

    @Slot()
    def toggleZoom(self):
        if appstate.state != "ZOOM":
            appstate.state = State.ZOOM
            self.ui.mplFigureCanvas.zoomView()

    @Slot()
    def togglePan(self):
        if appstate.state != "PAN":
            appstate.state = State.PAN
            self.ui.mplFigureCanvas.panView()

    def line_select_callback(self, eclick, erelease):
        """
        Callback for line selection.

        *eclick* and *erelease* are the press and release events.
        """
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        print(f"({x1:3.2f}, {y1:3.2f}) --> ({x2:3.2f}, {y2:3.2f})")
        print(f" The buttons you used were: {eclick.button} {erelease.button}")

    @Slot()
    def canvasClickMonitoring(self, event):
        """Main loop for acting on mouse events occurring in the canvas area."""
        if event.xdata is None or event.ydata is None:
            return

        for calibrationLabel in ["X1", "X2", "Y1", "Y2"]:
            data = event.xdata if (calibrationLabel[0] == "X") else event.ydata

            if appstate.state == self.calibrationStates[calibrationLabel]:
                self.rawLineEdits[calibrationLabel].setText(str(data))
                self.rawLineEdits[calibrationLabel].home(False)
                self.mapLineEdits[calibrationLabel].selectAll()
                self.ui.selectViewButton.setChecked(True)
                self.ui.mplFigureCanvas.selectOn()
                self.rawLineEdits[calibrationLabel].editingFinished.emit()
                return

        if appstate.state == State.SELECT:
            current_data = self.activeDataset.all()
            if self.matching_mode:
                x1y1 = np.asarray([self.closest_line(event.xdata), event.ydata])
            else:
                x1y1 = np.asarray([event.xdata, event.ydata])
            for index, x2y2 in enumerate(current_data.transpose()):
                if self.isRelativelyClose(x1y1, x2y2):
                    self.activeDataset.removeColumn(index)
                    self.updatePlot()
                    return
            self.activeDataset.append(*x1y1)
            self.updatePlot()

    @Slot()
    def canvasMouseMonitoring(self, event):
        self.axes.figure.canvas.flush_events()
        self.matching_mode = False
        if (
            self.allDatasets.currentRow != 0
            and len(self.allDatasets.assocDataList[0][0]) > 0
        ):
            self.matching_mode = True
        if not self.matching_mode:
            return

        if event.xdata is None or event.ydata is None:
            return

    @Slot()
    def updatePlot(self, initialize: bool = False, **kwargs):
        """Update the current plot of measurement data and markers of selected data
        points."""
        if self.disconnectCanvas:
            return

        # If this is not the first time of plotting, store the current axes limits and
        # clear the graph.
        if not initialize:
            xlim = self.axes.get_xlim()
            ylim = self.axes.get_ylim()
        self.axes.clear()

        # Set the matplotlib colormap according to the selection in the dropdown menu.
        colorStr = self.ui.colorComboBox.currentText()
        cross_color = color_dict[colorStr]["Cross"]
        line_color = color_dict[colorStr]["line"]
        scatter_color = color_dict[colorStr]["Scatter"]
        cmap = copy.copy(getattr(cm, colorStr))
        cmap.set_bad(color="black")

        # plot the background data
        self.measurementData.canvasPlot(self.axes, cmap=cmap)

        # plot the numerically calculated spectrum
        self.spectrumData.canvasPlot(self.axes)

        # If there are any extracted data points in the currently active data set, show
        # those via a scatter plot.
        if self.activeDataset.columnCount() > 0:
            dataXY = self.activeDataset.all()
            self.axes.scatter(
                dataXY[0],
                dataXY[1],
                c=scatter_color,
                marker=r"$\odot$",
                s=130,
                alpha=0.5,
            )

        plotted_data = []
        line_data = self.allDatasets.assocDataList[0]
        for count, i in enumerate(line_data[0]):
            if i not in plotted_data:
                self.axes.axline(
                    (i, line_data[1][count]),
                    (i, line_data[1][count] - (line_data[1][count]) * 0.1),
                    c=line_color,
                    alpha=0.7,
                )
            plotted_data.append(i)

        # Make sure that new axes limits match the old ones.
        if not initialize:
            self.axes.set_xlim(xlim)
            self.axes.set_ylim(ylim)

        self.axes.figure.canvas.draw()
        self.ui.mplFigureCanvas.set_callback(self.allDatasets)

    # def toggleMenu(self):
    #     if self.menuWidget.menuFrame.isHidden():
    #         self.menuWidget.menuFrame.show()
    #     else:
    #         self.menuWidget.menuFrame.hide()

    @Slot()
    def calibrate(self, calibrationLabel: str):
        """Mouse click on one of the calibration buttons prompts switching to
        calibration mode. Mouse cursor crosshair is adjusted and canvas waits for
        click setting calibration point x or y component."""
        appstate.state = self.calibrationStates[calibrationLabel]
        self.ui.mplFigureCanvas.calibrateOn(calibrationLabel[0])

    @Slot()
    def updateCalibration(self):
        """Transfer new calibration data from CalibrationView over to calibrationData
        instance. If the model is currently applying the calibration, then emit
        signal to rewrite the table."""
        self.calibrationData.setCalibration(*self.calibrationView.calibrationPoints())
        if self.calibrationData.applyCalibration:
            self.activeDataset.layoutChanged.emit()

    @Slot()
    def toggleCalibration(self):
        """If calibration check box is changed, toggle the calibration status of the
        calibrationData. Also induce change at the level of the displayed data of
        selected points."""
        self.calibrationData.toggleCalibration()
        self.activeDataset.toggleCalibratedView()

    @Slot(int)
    def zDataUpdate(self, itemIndex: int):
        self.measurementData.setCurrentZ(itemIndex)
        self.setupXYDataBoxes()
        self.updatePlot(initialize=True)

    @Slot(int)
    def xAxisUpdate(self, itemIndex: int):
        self.measurementData.setCurrentX(itemIndex)
        self.updatePlot(initialize=True)

    @Slot(int)
    def yAxisUpdate(self, itemIndex: int):
        self.measurementData.setCurrentY(itemIndex)
        self.updatePlot(initialize=True)

    @Slot()
    def swapXY(self):
        self.disconnectCanvas = True
        self.measurementData.swapXY()
        self.setupXYDataBoxes()

        self.allDatasets.swapXY()
        self.allDatasets.layoutChanged.emit()

        xBgndSub = self.ui.bgndSubtractXCheckBox.checkState()
        yBgndSub = self.ui.bgndSubtractYCheckBox.checkState()

        self.ui.bgndSubtractXCheckBox.setCheckState(yBgndSub)
        self.ui.bgndSubtractYCheckBox.setCheckState(xBgndSub)

        rawx1 = self.rawLineEdits["X1"].value()
        rawx2 = self.rawLineEdits["X2"].value()
        rawy1 = self.rawLineEdits["Y1"].value()
        rawy2 = self.rawLineEdits["Y2"].value()
        mapx1 = self.mapLineEdits["X1"].value()
        mapx2 = self.mapLineEdits["X2"].value()
        mapy1 = self.mapLineEdits["Y1"].value()
        mapy2 = self.mapLineEdits["Y2"].value()
        self.rawLineEdits["X1"].setText(str(rawy1))
        self.rawLineEdits["Y1"].setText(str(rawx1))
        self.rawLineEdits["X2"].setText(str(rawy2))
        self.rawLineEdits["Y2"].setText(str(rawx2))
        self.mapLineEdits["X1"].setText(str(mapy1))
        self.mapLineEdits["Y1"].setText(str(mapx1))
        self.mapLineEdits["X2"].setText(str(mapy2))
        self.mapLineEdits["Y2"].setText(str(mapx2))
        self.updateCalibration()

        self.disconnectCanvas = False
        self.updatePlot(initialize=True)

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
    
    def dynamicalSlidersInserts(self):
        """
        Insert a set of sliders for the prefit parameters according to the parameter set
        """

        # create a QWidget for the scrollArea and set a layout for it
        prefitScrollWidget = QWidget()
        self.ui.prefitScrollArea.setWidget(prefitScrollWidget)
        prefitScrollLayout = QVBoxLayout()
        prefitScrollWidget.setLayout(prefitScrollLayout)

        # generate the slider set
        self.sliderSet = GroupedSliderSet(
            columns=1, label_value_position="left_right"
        )

        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.group_name_maps[key]

            self.sliderSet.addGroupedSliders(
                group_name, 
                list(para_dict.keys()),
            )

        prefitScrollLayout.addWidget(self.sliderSet)


    def dynamicalSlidersConnects(self):
        """
        Connect the sliders to the controller - update hilbertspace and spectrum
        """
        for key, para_dict in self.sliderParameterSet.items():
            group_name = self.sliderParameterSet.group_name_maps[key]

            for para_name, para in para_dict.items():
                para: QuantumModelSliderParameter
                labeled_slider = self.sliderSet[group_name][para_name]

                para.setupUICallbacks(
                    labeled_slider.slider.value,
                    labeled_slider.slider.setValue,
                    labeled_slider.value.text,
                    labeled_slider.value.setText,
                )

                # synchronize slider and box
                labeled_slider.sliderValueChangedConnect(
                    para._sliderValueToBox)
                labeled_slider.valueTextChangeConnect(
                    para._boxValueToSlider)   
                labeled_slider.value.editingFinished.connect(
                    para._onBoxEditingFinished)

                # connect to the controller to update the spectrum
                labeled_slider.editingFinishedConnect(
                    lambda *args, **kwargs: self.quantumModel.onParameterChange(
                        self.sliderParameterSet,
                        self.spectrumData,
                        self.calibrationData,
                        self.allDatasets,
                        # self.axes,
                    )
                )
                labeled_slider.editingFinishedConnect(
                    self.updatePlot
                )

                # set the initial value
                # for test only
                # ------------------------------------------------------------------------------
                # put all sliders initially to the middle
                labeled_slider.setBoxValue(f"{(para.max + para.min) / 5 + para.min:.0f}")
                # ------------------------------------------------------------------------------

    def setUpSpectrumPlotConnects(self):
        self.spectrumData.setupUICallbacks()
        self.quantumModel.setupUICallbacks()

    @Slot()
    def openFile(self, initialize: bool = False):
        if not initialize:
            self.ui_menu.toggle()
        self.measurementData, self.extractedData = importFile(parent=self)

        self.calibrationData.resetCalibration()
        self.calibrationView.setView(*self.calibrationData.allCalibrationVecs())

        self.dataSetupConnects()
        self.setupUIXYZComboBoxes()
        self.updatePlot(initialize=True)
        self.raise_()

    @Slot()
    def closeApp(self):
        """End the application"""
        if self.allDatasets.isEmpty():
            sys.exit()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("qfit")
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setInformativeText("Do you want to save changes?")
            msgBox.setText("This document has been modified.")
            msgBox.setStandardButtons(
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            msgBox.setDefaultButton(QMessageBox.Save)

            reply = msgBox.exec_()

            if reply == QMessageBox.Save:
                self.saveAndCloseApp()
            elif reply == QMessageBox.Discard:
                sys.exit()
            return

    @Slot()
    def saveAndCloseApp(self):
        """Save the extracted data and calibration information to file, then exit the
        application."""
        success = saveFile(self)
        if not success:
            return
        sys.exit()

    def resizeAndCenter(self, maxSize: QSize):
        newSize = QSize(maxSize.width() * 0.9, maxSize.height() * 0.9)
        maxRect = QRect(QPoint(0, 0), maxSize)
        self.setGeometry(
            QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, newSize, maxRect)
        )

    def closest_line(self, xdat):
        current_data = self.allDatasets.assocDataList[0]
        allxdiff = {np.abs(xdat - i): i for i in current_data[0]}
        return allxdiff[min(allxdiff.keys())]
