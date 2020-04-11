# mainwindow.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from functools import partial

# from unittest.mock import MagicMock
# import sys
#
# sys.modules['IPython'] = MagicMock()
# sys.modules['ipywidgets'] = MagicMock()

import matplotlib.cm as cm
import numpy as np
from PySide2.QtCore import Slot, SLOT, QSize, QPoint, QRect
from PySide2.QtGui import Qt
from PySide2.QtQml import QQmlProperty
from PySide2.QtWidgets import QMainWindow, QStyle

import datapyc.core.app_state as appstate
from datapyc.core.app_state import State
from datapyc.models.calibration_model import CalibrationModel
from datapyc.views.calibration_view import CalibrationView
from datapyc.models.extractdata_model import ActiveExtractedDataModel, AllExtractedDataModel
from datapyc.ui.ui_window import Ui_MainWindow
from datapyc.io.save_data import saveFile
from datapyc.core.helpers import transposeEach


class MainWindow(QMainWindow):
    """Class for the main window of the app."""
    def __init__(self, measurementData, extractedData=None):
        super().__init__()
        self.measurementData = measurementData
        self.extractedData = extractedData

        self.activeDatasetModel = None
        self.allDatasetsModel = None
        self.calibrationModel = None
        self.rawLineEdits = None
        self.mapLineEdits = None
        self.calibrationButtons = None
        self.calibrationStates = None
        self.calibrationView = None
        self.minRangeSliderProperty = None
        self.maxRangeSliderProperty = None
        self.axes = None
        self.cidCanvas = None
        self.doXYSwap = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupUiCalibration()
        self.setupUiOptions()
        self.setupUiDataModel()
        self.setupUiXYZComboBoxes()

        self.uiDataConnects()
        self.uiDataOptionsConnects()
        self.uiColorScaleConnects()
        self.uiCalibrationConnects()
        self.uiCanvasControlConnects()
        self.uiDataControlConnects()
        self.uiXYZComboBoxesConnects()
        self.uiMplCanvasConnects()
        self.saveAndCloseConnects()

        self.ui.mplFigureCanvas.selectOn()

        if self.extractedData is not None:
            self.allDatasetsModel.dataNames = self.extractedData.datanames
            self.allDatasetsModel.assocDataList = transposeEach(self.extractedData.datalist)
            self.calibrationModel = self.extractedData.calibration_data
            self.activeDatasetModel._data = self.allDatasetsModel.currentAssocItem()
            self.allDatasetsModel.layoutChanged.emit()
            self.activeDatasetModel.layoutChanged.emit()


    def setupUiCalibration(self):
        """For the interface that enables calibration of data with respect to x and y axis, group QLineEdit elements
        and the corresponding buttons in dicts. Set up a dictionary mapping calibration labels to the corresponding
        State choices. Finally, set up an instance of CalibrationModel and CalibrationView"""
        self.rawLineEdits = {
            'X1': self.ui.rawX1LineEdit,
            'X2': self.ui.rawX2LineEdit,
            'Y1': self.ui.rawY1LineEdit,
            'Y2': self.ui.rawY2LineEdit
        }
        self.mapLineEdits = {
            'X1': self.ui.mapX1LineEdit,
            'X2': self.ui.mapX2LineEdit,
            'Y1': self.ui.mapY1LineEdit,
            'Y2': self.ui.mapY2LineEdit
        }
        self.calibrationButtons = {
            'X1': self.ui.calibrateX1Button,
            'X2': self.ui.calibrateX2Button,
            'Y1': self.ui.calibrateY1Button,
            'Y2': self.ui.calibrateY2Button
        }
        self.calibrationStates = {
            'X1': State.CALIBRATE_X1,
            'X2': State.CALIBRATE_X2,
            'Y1': State.CALIBRATE_Y1,
            'Y2': State.CALIBRATE_Y2
        }

        self.calibrationModel = CalibrationModel()
        self.calibrationView = CalibrationView(self.rawLineEdits, self.mapLineEdits)
        self.calibrationModel.setCalibration(*self.calibrationView.calibrationPoints())

    def setupUiOptions(self):
        dataCheckBoxCallbacks = {'savgolFilterX': self.ui.savgolFilterXCheckBox.isChecked,
                                 'savgolFilterY': self.ui.savgolFilterYCheckBox.isChecked,
                                 'gaussLaplaceFilter': self.ui.gaussLaplaceCheckBox.isChecked,
                                 'bgndSubtractX': self.ui.bgndSubtractXCheckBox.isChecked,
                                 'bgndSubtractY': self.ui.bgndSubtractYCheckBox.isChecked,
                                 'swapXY': self.ui.swapXYCheckBox.isChecked,
                                 'logColoring': self.ui.logScaleCheckBox.isChecked}

        # Left and right values of the double slider manipulating the z plot range
        self.minRangeSliderProperty = QQmlProperty(self.ui.quickWidget.rootObject(), "first.value")
        self.maxRangeSliderProperty = QQmlProperty(self.ui.quickWidget.rootObject(), "second.value")

        plotRangeCallbacks = {'left': self.minRangeSliderProperty.read, 'right': self.maxRangeSliderProperty.read}

        self.measurementData.setupUiCallbacks(dataCheckBoxCallbacks, plotRangeCallbacks)

    def setupUiDataModel(self):
        """Set up the main class instances holding the data extracted from placing markers on the canvas. The AllExtractedDataModel
         instance holds all data, whereas the ActiveExtractedDataModel instance holds data of the currently selected data set."""
        self.activeDatasetModel = ActiveExtractedDataModel()
        self.activeDatasetModel.setAdaptiveCalibrationFunc(self.calibrationModel.adaptiveConversionFunc)
        self.ui.dataTableView.setModel(self.activeDatasetModel)

        self.allDatasetsModel = AllExtractedDataModel()
        self.allDatasetsModel.setCalibrationFunc(self.calibrationModel.calibrateDataset)
        self.ui.datasetListView.setModel(self.allDatasetsModel)

    def setupUiXYZComboBoxes(self):
        zDataNames = [dataName for dataName in self.measurementData.zCandidates.keys()]
        self.ui.zComboBox.addItems(zDataNames)
        self.ui.zComboBox.setCurrentText(self.measurementData.currentZ.name)
        self.setupXYDataBoxes()

    def uiDataConnects(self):
        """Make connections for changes in data."""
        # Whenever the data layout in the ActiveExtractedDataModel changes, update the corresponding AllExtractedDataModel data; this includes the
        # important event of adding extraction points to the ActiveExtractedDataModel
        self.activeDatasetModel.layoutChanged.connect(
            lambda: self.ui.datasetListView.model().updateAssocData(newData=self.activeDatasetModel.all()))

        # If data in the TableView is changed manually through editing, the 'dataChanged' signal will be emitted. The
        # following connects the signal to an update in th data stored in the AllExtractedDataModel
        self.activeDatasetModel.dataChanged.connect(
            lambda topLeft, bottomRight: self.ui.datasetListView.model().updateAssocData(
                newData=self.activeDatasetModel.all()
            )
        )

        # Whenever the AllExtractedDataModel changes layout - for example, due to switching from one existing data set to another
        # one, this connection will ensure that the TableView will be updated with the correct data
        self.allDatasetsModel.layoutChanged.connect(
            lambda: self.activeDatasetModel.setAllData(newData=self.allDatasetsModel.currentAssocItem()))

        # Whenever data sets are added or removed from the ListView, this ensures that the canvas display is updated.
        self.allDatasetsModel.layoutChanged.connect(self.updatePlot)

        # Each time the data set is changed on ListView/Model by clicking a data set, the data in ActiveExtractedDataModel is updated
        # to reflect the new selection.
        self.ui.datasetListView.clicked.connect(
            lambda: self.activeDatasetModel.setAllData(newData=self.allDatasetsModel.currentAssocItem()))

        # A new selection of a data set item in ListView is accompanied by an update of the canvas to show the
        # appropriate plot of selected points
        self.ui.datasetListView.clicked.connect(lambda: self.updatePlot(init=False))

    def uiDataOptionsConnects(self):
        """Connect the UI elements related to display of data"""
        self.ui.savgolFilterXCheckBox.toggled.connect(self.updatePlot)
        self.ui.savgolFilterYCheckBox.toggled.connect(self.updatePlot)
        self.ui.gaussLaplaceCheckBox.toggled.connect(self.updatePlot)
        self.ui.swapXYCheckBox.toggled.connect(self.toggleSwapXY)
        self.ui.bgndSubtractXCheckBox.toggled.connect(self.updatePlot)
        self.ui.bgndSubtractYCheckBox.toggled.connect(self.updatePlot)

    def uiColorScaleConnects(self):
        """Connect the color scale related UI elements."""
        # Toggling the loc scale check box prompts replotting.
        self.ui.logScaleCheckBox.toggled.connect(self.updatePlot)

        # Changes in the color map dropdown menu prompt replotting.
        self.ui.colorComboBox.activated.connect(self.updatePlot)

        # Ensure that a change in the range slider positions cause an update of the plot.
        self.minRangeSliderProperty.connectNotifySignal(self, SLOT("updatePlot()"))
        self.maxRangeSliderProperty.connectNotifySignal(self, SLOT("updatePlot()"))

    def uiCalibrationConnects(self):
        """Connect UI elements for data calibration."""
        self.ui.calibratedCheckBox.toggled.connect(self.toggleCalibration)

        for label in self.calibrationButtons.keys():
            self.calibrationButtons[label].clicked.connect(partial(self.calibrate, label))

        for lineEdit in (list(self.rawLineEdits.values()) + list(self.mapLineEdits.values())):
            lineEdit.editingFinished.connect(self.updateCalibration)

    def uiCanvasControlConnects(self):
        """Connect the UI buttons for reset, zoom, and pan functions of the matplotlib canvas."""
        self.ui.resetViewButton.clicked.connect(self.ui.mplFigureCanvas.resetView)
        self.ui.zoomViewButton.clicked.connect(self.toggleZoom)
        self.ui.panViewButton.clicked.connect(self.togglePan)
        self.ui.selectViewButton.clicked.connect(self.toggleSelect)

    def uiDataControlConnects(self):
        """Connect buttons for inserting and deleting a data set, or clearing all data sets"""
        self.ui.newRowButton.clicked.connect(self.allDatasetsModel.newRow)
        self.ui.deleteRowButton.clicked.connect(self.allDatasetsModel.removeCurrentRow)
        self.ui.clearAllButton.clicked.connect(self.allDatasetsModel.removeAll)

    def uiXYZComboBoxesConnects(self):
        self.ui.zComboBox.activated.connect(self.zDataUpdate)
        self.ui.xComboBox.activated.connect(self.xAxisUpdate)
        self.ui.yComboBox.activated.connect(self.yAxisUpdate)

    def uiMplCanvasConnects(self):
        """Set up the matplotlib canvas and start monitoring for mouse click events in the canvas area."""
        self.axes = self.ui.mplFigureCanvas.canvas.figure.subplots()
        self.updatePlot(initialize=True)
        self.cidCanvas = self.axes.figure.canvas.mpl_connect('button_press_event', self.canvasClickMonitoring)

    def saveAndCloseConnects(self):
        self.ui.buttonBox.accepted.connect(self.saveAndCloseApp)
        self.ui.buttonBox.rejected.connect(self.closeApp)

    def setupXYDataBoxes(self):
        self.ui.xComboBox.clear()
        xDataNames = [dataName for dataName in self.measurementData.currentXCompatibles.keys()]
        self.ui.xComboBox.addItems(xDataNames)
        self.ui.xComboBox.setCurrentText(self.measurementData.currentX.name)

        self.ui.yComboBox.clear()
        yDataNames = [dataName for dataName in self.measurementData.currentYCompatibles.keys()]
        self.ui.yComboBox.addItems(yDataNames)
        self.ui.yComboBox.setCurrentText(self.measurementData.currentY.name)

    @Slot()
    def toggleSelect(self):
        if appstate.state != State.SELECT:
            appstate.state = State.SELECT
            self.ui.mplFigureCanvas.selectOn()

    @Slot()
    def toggleZoom(self):
        if appstate.state != 'ZOOM':
            appstate.state = State.ZOOM
            self.ui.mplFigureCanvas.zoomView()

    @Slot()
    def togglePan(self):
        if appstate.state != 'PAN':
            appstate.state = State.PAN
            self.ui.mplFigureCanvas.panView()

    @Slot()
    def canvasClickMonitoring(self, event):
        """Main loop for acting on mouse events occurring in the canvas area."""
        if event.xdata is None or event.ydata is None:
            return None

        for calibrationLabel in ['X1', 'X2', 'Y1', 'Y2']:
            data = event.xdata if (calibrationLabel[0] == 'X') else event.ydata

            if appstate.state == self.calibrationStates[calibrationLabel]:
                self.rawLineEdits[calibrationLabel].setText(str(data))
                self.rawLineEdits[calibrationLabel].home(False)
                self.mapLineEdits[calibrationLabel].selectAll()
                self.ui.mplFigureCanvas.selectOn()
                self.rawLineEdits[calibrationLabel].editingFinished.emit()
                return None

        if appstate.state == State.SELECT:
            current_data = self.activeDatasetModel.all()
            x1y1 = np.asarray([event.xdata, event.ydata])
            if self.doXYSwap:
                x1y1 = np.flip(x1y1)
            for index, x2y2 in enumerate(current_data.transpose()):
                if self.isRelativelyClose(x1y1, x2y2):
                    self.activeDatasetModel.removeColumn(index)
                    self.updatePlot()
                    return None
            self.activeDatasetModel.append(*x1y1)
            self.updatePlot()

    @Slot()
    def updatePlot(self, slotdummy=None, initialize=False, toggleXY=False, **kwargs):
        """Update the current plot of measurement data and markers of selected data points."""
        # If this is not the first time of plotting, store the current axes limits and clear the graph.
        if (not initialize) and (not toggleXY):
            xlim = self.axes.get_xlim()
            ylim = self.axes.get_ylim()
        self.axes.clear()

        # Set the matplotlib colormap according to the selection in the dropdown menu.
        colorStr = self.ui.colorComboBox.currentText()
        cmap = getattr(cm, colorStr)
        cmap.set_bad(color='black')

        self.measurementData.canvasPlot(self.axes, cmap=cmap)

        # If there are any extracted data points in the currently active data set, show those via a scatter plot.
        if self.activeDatasetModel.columnCount() > 0:
            transform = self.transformXY()
            dataXY = transform(self.activeDatasetModel.all())
            self.axes.scatter(dataXY[0], dataXY[1], c='orange', marker='x')

        # Make sure that new axes limits match the old ones.
        if not initialize and not toggleXY:
            self.axes.set_xlim(xlim)
            self.axes.set_ylim(ylim)

        self.axes.figure.canvas.draw()

    @Slot()
    def calibrate(self, calibrationLabel):
        """Mouse click on one of the calibration buttons prompts switching to calibration mode. Mouse cursor crosshair
        is adjusted and canvas waits for click setting calibration point x or y component."""
        appstate.state = self.calibrationStates[calibrationLabel]
        self.ui.mplFigureCanvas.calibrateOn(calibrationLabel[0])

    @Slot()
    def updateCalibration(self):
        """Transfer new calibration data from CalibrationView over to CalibrationModel instance. If the model is
        currently applying the calibration, then emit signal to rewrite the table."""
        self.calibrationModel.setCalibration(*self.calibrationView.calibrationPoints())
        if self.calibrationModel.applyCalibration:
            self.activeDatasetModel.layoutChanged.emit()

    @Slot()
    def toggleCalibration(self):
        """If calibration check box is changed, toggle the calibration status of the CalibrationModel. Also induce
        change at the level of the displayed data of selected points."""
        self.calibrationModel.toggleCalibration()
        self.activeDatasetModel.toggleCalibratedView()

    @Slot(int)
    def zDataUpdate(self, itemIndex):
        self.measurementData.setCurrentZ(itemIndex)
        self.setupXYDataBoxes()
        self.updatePlot(initialize=True)

    @Slot(int)
    def xAxisUpdate(self, itemIndex):
        self.measurementData.setCurrentX(itemIndex)
        self.updatePlot(initialize=True)

    @Slot(int)
    def yAxisUpdate(self, itemIndex):
        self.measurementData.setCurrentY(itemIndex)
        self.updatePlot(initialize=True)

    @Slot()
    def toggleSwapXY(self):
        self.doXYSwap = not self.doXYSwap
        self.updatePlot(toggleXY=True)

    def transformXY(self):
        if self.doXYSwap:
            return lambda array: np.flip(array, axis=0)
        else:
            return lambda array: array

    def isRelativelyClose(self, x1y1, x2y2):
        """Check whether the point x1y1 is relatively close to x2y2, given the current field of view on the canvas."""
        xlim = self.axes.get_xlim() if not self.doXYSwap else self.axes.get_ylim()
        ylim = self.axes.get_ylim() if not self.doXYSwap else self.axes.get_xlim()
        xmin, xmax = xlim
        ymin, ymax = ylim
        xrange = xmax - xmin
        yrange = ymax - ymin
        x1y1 = x1y1 / [xrange, yrange]
        x2y2 = x2y2 / [xrange, yrange]
        distance = np.linalg.norm(x1y1-x2y2)
        if distance < 0.025:
            return True
        return False

    @Slot()
    def closeApp(self):
        """End the application"""
        exit()

    @Slot()
    def saveAndCloseApp(self):
        """Save the extracted data and calibration information to file, then exit the application."""
        saveFile(self)
        exit()

    def resizeAndCenter(self, maxSize):
        newSize = QSize(maxSize.width() * 0.9, maxSize.height() * 0.9)
        maxRect = QRect(QPoint(0, 0), maxSize)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, newSize, maxRect))
