# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui',
# licensing of 'ui_mainwindow.ui' applies.
#
# Created: Tue Apr 28 08:02:34 2020
#      by: pyside2-uic  running on PySide6 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(835, 717)
        MainWindow.setWindowTitle("qfit")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.dataTableView = TableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dataTableView.sizePolicy().hasHeightForWidth()
        )
        self.dataTableView.setSizePolicy(sizePolicy)
        self.dataTableView.setMinimumSize(QtCore.QSize(0, 150))
        self.dataTableView.setMaximumSize(QtCore.QSize(16777215, 150))
        self.dataTableView.setStyleSheet("")
        self.dataTableView.setObjectName("dataTableView")
        self.gridLayout.addWidget(self.dataTableView, 2, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Close | QtWidgets.QDialogButtonBox.Save
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 3, 1, 1)
        self.datasetListView = ListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.datasetListView.sizePolicy().hasHeightForWidth()
        )
        self.datasetListView.setSizePolicy(sizePolicy)
        self.datasetListView.setMinimumSize(QtCore.QSize(0, 150))
        self.datasetListView.setMaximumSize(QtCore.QSize(230, 150))
        self.datasetListView.setObjectName("datasetListView")
        self.gridLayout.addWidget(self.datasetListView, 2, 2, 1, 1)
        self.dataButtonGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.dataButtonGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.dataButtonGroupBox.setSizePolicy(sizePolicy)
        self.dataButtonGroupBox.setMinimumSize(QtCore.QSize(80, 100))
        self.dataButtonGroupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.dataButtonGroupBox.setTitle("")
        self.dataButtonGroupBox.setObjectName("dataButtonGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dataButtonGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.newRowButton = QtWidgets.QPushButton(self.dataButtonGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy)
        self.newRowButton.setToolTip("")
        self.newRowButton.setText("New dataset")
        self.newRowButton.setObjectName("newRowButton")
        self.verticalLayout.addWidget(self.newRowButton)
        self.deleteRowButton = QtWidgets.QPushButton(self.dataButtonGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.deleteRowButton.sizePolicy().hasHeightForWidth()
        )
        self.deleteRowButton.setSizePolicy(sizePolicy)
        self.deleteRowButton.setToolTip("")
        self.deleteRowButton.setText("Delete dataset")
        self.deleteRowButton.setObjectName("deleteRowButton")
        self.verticalLayout.addWidget(self.deleteRowButton)
        self.clearAllButton = QtWidgets.QPushButton(self.dataButtonGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.clearAllButton.sizePolicy().hasHeightForWidth()
        )
        self.clearAllButton.setSizePolicy(sizePolicy)
        self.clearAllButton.setToolTip("")
        self.clearAllButton.setText("Clear all")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.clearAllButton.setIcon(icon)
        self.clearAllButton.setObjectName("clearAllButton")
        self.verticalLayout.addWidget(self.clearAllButton)
        self.gridLayout.addWidget(self.dataButtonGroupBox, 2, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.selectTab = QtWidgets.QWidget()
        self.selectTab.setObjectName("selectTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.selectTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.imageOptionsVerticalGroupBox = QtWidgets.QGroupBox(self.selectTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.imageOptionsVerticalGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.imageOptionsVerticalGroupBox.setSizePolicy(sizePolicy)
        self.imageOptionsVerticalGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.imageOptionsVerticalGroupBox.setTitle("Image Options")
        self.imageOptionsVerticalGroupBox.setObjectName("imageOptionsVerticalGroupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.imageOptionsVerticalGroupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.bgndSubtractXCheckBox = QtWidgets.QCheckBox(
            self.imageOptionsVerticalGroupBox
        )
        self.bgndSubtractXCheckBox.setToolTip("Background subtraction along X")
        self.bgndSubtractXCheckBox.setText("Subtract Bgnd X")
        self.bgndSubtractXCheckBox.setChecked(False)
        self.bgndSubtractXCheckBox.setTristate(False)
        self.bgndSubtractXCheckBox.setObjectName("bgndSubtractXCheckBox")
        self.gridLayout_8.addWidget(self.bgndSubtractXCheckBox, 2, 0, 1, 1)
        self.bgndSubtractYCheckBox = QtWidgets.QCheckBox(
            self.imageOptionsVerticalGroupBox
        )
        self.bgndSubtractYCheckBox.setToolTip("Background subtraction along Y")
        self.bgndSubtractYCheckBox.setText("Subtract Bgnd Y")
        self.bgndSubtractYCheckBox.setObjectName("bgndSubtractYCheckBox")
        self.gridLayout_8.addWidget(self.bgndSubtractYCheckBox, 2, 1, 1, 1)
        self.savgolFilterYCheckBox = QtWidgets.QCheckBox(
            self.imageOptionsVerticalGroupBox
        )
        self.savgolFilterYCheckBox.setToolTip("Savitzky-Golay filter (Y cuts)")
        self.savgolFilterYCheckBox.setText("Savitzky-Golay Filter Y")
        self.savgolFilterYCheckBox.setObjectName("savgolFilterYCheckBox")
        self.gridLayout_8.addWidget(self.savgolFilterYCheckBox, 0, 1, 1, 1)
        self.savgolFilterXCheckBox = QtWidgets.QCheckBox(
            self.imageOptionsVerticalGroupBox
        )
        self.savgolFilterXCheckBox.setToolTip("Savitzky-Golay filter (X cuts)")
        self.savgolFilterXCheckBox.setText("Savitzky-Golay Filter X")
        self.savgolFilterXCheckBox.setObjectName("savgolFilterXCheckBox")
        self.gridLayout_8.addWidget(self.savgolFilterXCheckBox, 0, 0, 1, 1)
        self.gaussLaplaceCheckBox = QtWidgets.QCheckBox(
            self.imageOptionsVerticalGroupBox
        )
        self.gaussLaplaceCheckBox.setToolTip("Apply Gauss-Laplace filter")
        self.gaussLaplaceCheckBox.setText("Gauss-Laplace Filter")
        self.gaussLaplaceCheckBox.setObjectName("gaussLaplaceCheckBox")
        self.gridLayout_8.addWidget(self.gaussLaplaceCheckBox, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.imageOptionsVerticalGroupBox)
        self.colorGridGroupBox = QtWidgets.QGroupBox(self.selectTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.colorGridGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.colorGridGroupBox.setSizePolicy(sizePolicy)
        self.colorGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.colorGridGroupBox.setTitle("Color Options")
        self.colorGridGroupBox.setObjectName("colorGridGroupBox")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.colorGridGroupBox)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.colorComboBox = QtWidgets.QComboBox(self.colorGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.colorComboBox.sizePolicy().hasHeightForWidth()
        )
        self.colorComboBox.setSizePolicy(sizePolicy)
        self.colorComboBox.setToolTip("")
        self.colorComboBox.setIconSize(QtCore.QSize(100, 10))
        self.colorComboBox.setObjectName("colorComboBox")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/PuOr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.colorComboBox.addItem(icon1, "")
        self.colorComboBox.setItemText(0, "PuOr")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/RdYlBu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.colorComboBox.addItem(icon2, "")
        self.colorComboBox.setItemText(1, "RdYlBu")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/bwr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.colorComboBox.addItem(icon3, "")
        self.colorComboBox.setItemText(2, "bwr")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/viridis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.colorComboBox.addItem(icon4, "")
        self.colorComboBox.setItemText(3, "viridis")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/cividis.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.colorComboBox.addItem(icon5, "")
        self.colorComboBox.setItemText(4, "cividis")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/gray.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.colorComboBox.addItem(icon6, "")
        self.colorComboBox.setItemText(5, "gray")
        self.gridLayout_9.addWidget(self.colorComboBox, 0, 0, 1, 1)
        self.logScaleCheckBox = QtWidgets.QCheckBox(self.colorGridGroupBox)
        self.logScaleCheckBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.logScaleCheckBox.setText("Log Colorscale")
        self.logScaleCheckBox.setObjectName("logScaleCheckBox")
        self.gridLayout_9.addWidget(self.logScaleCheckBox, 0, 1, 1, 1)
        self.quickWidget_3 = QQuickWidget(self.colorGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.quickWidget_3.sizePolicy().hasHeightForWidth()
        )
        self.quickWidget_3.setSizePolicy(sizePolicy)
        self.quickWidget_3.setMinimumSize(QtCore.QSize(0, 30))
        self.quickWidget_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.quickWidget_3.setToolTip("Adjust plot range (Z)")
        self.quickWidget_3.setWhatsThis("Color Range")
        self.quickWidget_3.setAutoFillBackground(True)
        self.quickWidget_3.setProperty("source", QtCore.QUrl("qrc:/rangeslider.qml"))
        self.quickWidget_3.setObjectName("quickWidget_3")
        self.gridLayout_9.addWidget(self.quickWidget_3, 1, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.colorGridGroupBox)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem)
        self.xyzDataGridGroupBox = QtWidgets.QGroupBox(self.selectTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.xyzDataGridGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.xyzDataGridGroupBox.setSizePolicy(sizePolicy)
        self.xyzDataGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.xyzDataGridGroupBox.setObjectName("xyzDataGridGroupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.xyzDataGridGroupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.yComboBox = QtWidgets.QComboBox(self.xyzDataGridGroupBox)
        self.yComboBox.setMinimumSize(QtCore.QSize(250, 0))
        self.yComboBox.setObjectName("yComboBox")
        self.gridLayout_4.addWidget(self.yComboBox, 4, 1, 1, 1)
        self.zComboBox = QtWidgets.QComboBox(self.xyzDataGridGroupBox)
        self.zComboBox.setMinimumSize(QtCore.QSize(250, 0))
        self.zComboBox.setObjectName("zComboBox")
        self.gridLayout_4.addWidget(self.zComboBox, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.xyzDataGridGroupBox)
        self.label_12.setText("Axis-1 Values")
        self.label_12.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 3, 0, 1, 1)
        self.xComboBox = QtWidgets.QComboBox(self.xyzDataGridGroupBox)
        self.xComboBox.setMinimumSize(QtCore.QSize(250, 0))
        self.xComboBox.setObjectName("xComboBox")
        self.gridLayout_4.addWidget(self.xComboBox, 3, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.xyzDataGridGroupBox)
        self.label_13.setText("Z Values")
        self.label_13.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 1, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.xyzDataGridGroupBox)
        self.label_14.setText("Axis-2 Values")
        self.label_14.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 4, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.xyzDataGridGroupBox)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.calibrateXGridGroupBox = QtWidgets.QGroupBox(self.selectTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.calibrateXGridGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.calibrateXGridGroupBox.setSizePolicy(sizePolicy)
        self.calibrateXGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.calibrateXGridGroupBox.setMaximumSize(QtCore.QSize(320, 16777215))
        self.calibrateXGridGroupBox.setTitle("Calibrate X Axis")
        self.calibrateXGridGroupBox.setObjectName("calibrateXGridGroupBox")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.calibrateXGridGroupBox)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.rawX1LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rawX1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawX1LineEdit.setSizePolicy(sizePolicy)
        self.rawX1LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.rawX1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawX1LineEdit.setToolTip("")
        self.rawX1LineEdit.setText("0.0")
        self.rawX1LineEdit.setObjectName("rawX1LineEdit")
        self.gridLayout_10.addWidget(self.rawX1LineEdit, 0, 2, 1, 1)
        self.calibrateX2Button = QtWidgets.QToolButton(self.calibrateXGridGroupBox)
        self.calibrateX2Button.setToolTip(
            "Calibrate x2, allows selection of coordinate inside plot"
        )
        self.calibrateX2Button.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.calibrateX2Button.setIcon(icon7)
        self.calibrateX2Button.setObjectName("calibrateX2Button")
        self.gridLayout_10.addWidget(self.calibrateX2Button, 1, 0, 1, 1)
        self.mapX2LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mapX2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapX2LineEdit.setSizePolicy(sizePolicy)
        self.mapX2LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.mapX2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapX2LineEdit.setToolTip("")
        self.mapX2LineEdit.setText("1.0")
        self.mapX2LineEdit.setObjectName("mapX2LineEdit")
        self.gridLayout_10.addWidget(self.mapX2LineEdit, 1, 4, 1, 1)
        self.rawX2LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rawX2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawX2LineEdit.setSizePolicy(sizePolicy)
        self.rawX2LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.rawX2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawX2LineEdit.setToolTip("")
        self.rawX2LineEdit.setText("1.0")
        self.rawX2LineEdit.setObjectName("rawX2LineEdit")
        self.gridLayout_10.addWidget(self.rawX2LineEdit, 1, 2, 1, 1)
        self.mapX1LineEdit = CalibrationLineEdit(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mapX1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapX1LineEdit.setSizePolicy(sizePolicy)
        self.mapX1LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.mapX1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapX1LineEdit.setToolTip("")
        self.mapX1LineEdit.setInputMask("")
        self.mapX1LineEdit.setText("0.0")
        self.mapX1LineEdit.setObjectName("mapX1LineEdit")
        self.gridLayout_10.addWidget(self.mapX1LineEdit, 0, 4, 1, 1)
        self.calibrateX1Button = QtWidgets.QToolButton(self.calibrateXGridGroupBox)
        self.calibrateX1Button.setToolTip(
            "Calibrate x1, allows selection of coordinate inside plot"
        )
        self.calibrateX1Button.setText("")
        self.calibrateX1Button.setIcon(icon7)
        self.calibrateX1Button.setObjectName("calibrateX1Button")
        self.gridLayout_10.addWidget(self.calibrateX1Button, 0, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setText(
            '<html><head/><body><p align="right">X<span style=" vertical-align:sub;">1</span></p></body></html>'
        )
        self.label_15.setObjectName("label_15")
        self.gridLayout_10.addWidget(self.label_15, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setText(
            '<html><head/><body><p align="right">X<span style=" vertical-align:sub;">2</span></p></body></html>'
        )
        self.label_16.setObjectName("label_16")
        self.gridLayout_10.addWidget(self.label_16, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setText(
            '<html><head/><body><p align="right">→ X<span style=" vertical-align:sub;">1</span>\'</p></body></html>'
        )
        self.label_17.setObjectName("label_17")
        self.gridLayout_10.addWidget(self.label_17, 0, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.calibrateXGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setText(
            '<html><head/><body><p align="right">→ X<span style=" vertical-align:sub;">2</span>\'</p></body></html>'
        )
        self.label_18.setObjectName("label_18")
        self.gridLayout_10.addWidget(self.label_18, 1, 3, 1, 1)
        self.verticalLayout_2.addWidget(self.calibrateXGridGroupBox)
        self.calibrateYGridGroupBox = QtWidgets.QGroupBox(self.selectTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.calibrateYGridGroupBox.sizePolicy().hasHeightForWidth()
        )
        self.calibrateYGridGroupBox.setSizePolicy(sizePolicy)
        self.calibrateYGridGroupBox.setMinimumSize(QtCore.QSize(330, 0))
        self.calibrateYGridGroupBox.setMaximumSize(QtCore.QSize(320, 16777215))
        self.calibrateYGridGroupBox.setToolTip("")
        self.calibrateYGridGroupBox.setTitle("Calibrate Y Axis")
        self.calibrateYGridGroupBox.setObjectName("calibrateYGridGroupBox")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.calibrateYGridGroupBox)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.rawY2LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rawY2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawY2LineEdit.setSizePolicy(sizePolicy)
        self.rawY2LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.rawY2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawY2LineEdit.setToolTip("")
        self.rawY2LineEdit.setText("1.0")
        self.rawY2LineEdit.setObjectName("rawY2LineEdit")
        self.gridLayout_11.addWidget(self.rawY2LineEdit, 1, 2, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setText(
            '<html><head/><body><p align="right">Y<span style=" vertical-align:sub;">1</span></p></body></html>'
        )
        self.label_19.setObjectName("label_19")
        self.gridLayout_11.addWidget(self.label_19, 0, 1, 1, 1)
        self.calibrateY2Button = QtWidgets.QToolButton(self.calibrateYGridGroupBox)
        self.calibrateY2Button.setToolTip(
            "Calibrate y2, allows selection of coordinate inside plot"
        )
        self.calibrateY2Button.setText("")
        self.calibrateY2Button.setIcon(icon7)
        self.calibrateY2Button.setObjectName("calibrateY2Button")
        self.gridLayout_11.addWidget(self.calibrateY2Button, 1, 0, 1, 1)
        self.mapY1LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mapY1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapY1LineEdit.setSizePolicy(sizePolicy)
        self.mapY1LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.mapY1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapY1LineEdit.setToolTip("")
        self.mapY1LineEdit.setText("0.0")
        self.mapY1LineEdit.setObjectName("mapY1LineEdit")
        self.gridLayout_11.addWidget(self.mapY1LineEdit, 0, 4, 1, 1)
        self.calibrateY1Button = QtWidgets.QToolButton(self.calibrateYGridGroupBox)
        self.calibrateY1Button.setToolTip(
            "Calibrate y1, allows selection of coordinate inside plot"
        )
        self.calibrateY1Button.setText("")
        self.calibrateY1Button.setIcon(icon7)
        self.calibrateY1Button.setObjectName("calibrateY1Button")
        self.gridLayout_11.addWidget(self.calibrateY1Button, 0, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setText(
            '<html><head/><body><p align="right">Y<span style=" vertical-align:sub;">2</span></p></body></html>'
        )
        self.label_20.setObjectName("label_20")
        self.gridLayout_11.addWidget(self.label_20, 1, 1, 1, 1)
        self.mapY2LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mapY2LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.mapY2LineEdit.setSizePolicy(sizePolicy)
        self.mapY2LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.mapY2LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.mapY2LineEdit.setToolTip("")
        self.mapY2LineEdit.setText("1.0")
        self.mapY2LineEdit.setObjectName("mapY2LineEdit")
        self.gridLayout_11.addWidget(self.mapY2LineEdit, 1, 4, 1, 1)
        self.rawY1LineEdit = CalibrationLineEdit(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.rawY1LineEdit.sizePolicy().hasHeightForWidth()
        )
        self.rawY1LineEdit.setSizePolicy(sizePolicy)
        self.rawY1LineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.rawY1LineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.rawY1LineEdit.setToolTip("")
        self.rawY1LineEdit.setText("0.0")
        self.rawY1LineEdit.setObjectName("rawY1LineEdit")
        self.gridLayout_11.addWidget(self.rawY1LineEdit, 0, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setText(
            '<html><head/><body><p align="right">→ Y<span style=" vertical-align:sub;">1</span>\'</p></body></html>'
        )
        self.label_21.setObjectName("label_21")
        self.gridLayout_11.addWidget(self.label_21, 0, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.calibrateYGridGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setText(
            '<html><head/><body><p align="right">→ Y<span style=" vertical-align:sub;">2</span>\'</p></body></html>'
        )
        self.label_22.setObjectName("label_22")
        self.gridLayout_11.addWidget(self.label_22, 1, 3, 1, 1)
        self.verticalLayout_2.addWidget(self.calibrateYGridGroupBox)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem2)
        self.calibratedCheckBox = QtWidgets.QCheckBox(self.selectTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.calibratedCheckBox.sizePolicy().hasHeightForWidth()
        )
        self.calibratedCheckBox.setSizePolicy(sizePolicy)
        self.calibratedCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.calibratedCheckBox.setText("Apply calibration")
        self.calibratedCheckBox.setObjectName("calibratedCheckBox")
        self.verticalLayout_2.addWidget(self.calibratedCheckBox)
        self.tabWidget.addTab(self.selectTab, "Select data points")
        self.tagTab = QtWidgets.QWidget()
        self.tagTab.setObjectName("tagTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tagTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tagChoicesFrame = QtWidgets.QFrame(self.tagTab)
        self.tagChoicesFrame.setFrameShape(QtWidgets.QFrame.Panel)
        self.tagChoicesFrame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tagChoicesFrame.setObjectName("tagChoicesFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tagChoicesFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.noTagRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.noTagRadioButton.setToolTip("")
        self.noTagRadioButton.setText("No tag")
        self.noTagRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.noTagRadioButton.setChecked(True)
        self.noTagRadioButton.setObjectName("noTagRadioButton")
        self.verticalLayout_4.addWidget(self.noTagRadioButton)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_4.addItem(spacerItem3)
        self.label_23 = QtWidgets.QLabel(self.tagChoicesFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_23.setFont(font)
        self.label_23.setToolTip("")
        self.label_23.setText("Transition between dispersive states")
        self.label_23.setObjectName("label_23")
        self.verticalLayout_4.addWidget(self.label_23)
        self.tagDispersiveBareRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.tagDispersiveBareRadioButton.setToolTip("")
        self.tagDispersiveBareRadioButton.setText("Tag by bare-states indices")
        self.tagDispersiveBareRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagDispersiveBareRadioButton.setObjectName("tagDispersiveBareRadioButton")
        self.verticalLayout_4.addWidget(self.tagDispersiveBareRadioButton)
        self.tagDispersiveDressedRadioButton = QtWidgets.QRadioButton(
            self.tagChoicesFrame
        )
        self.tagDispersiveDressedRadioButton.setToolTip("")
        self.tagDispersiveDressedRadioButton.setText("Tag by dressed-states indices")
        self.tagDispersiveDressedRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagDispersiveDressedRadioButton.setObjectName(
            "tagDispersiveDressedRadioButton"
        )
        self.verticalLayout_4.addWidget(self.tagDispersiveDressedRadioButton)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_4.addItem(spacerItem4)
        self.label_24 = QtWidgets.QLabel(self.tagChoicesFrame)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_24.setFont(font)
        self.label_24.setToolTip("")
        self.label_24.setText("Avoided crossing")
        self.label_24.setObjectName("label_24")
        self.verticalLayout_4.addWidget(self.label_24)
        self.tagCrossingRadioButton = QtWidgets.QRadioButton(self.tagChoicesFrame)
        self.tagCrossingRadioButton.setToolTip("")
        self.tagCrossingRadioButton.setText(
            "Tag as avoided crossing (infer state indices when fitting)"
        )
        self.tagCrossingRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagCrossingRadioButton.setObjectName("tagCrossingRadioButton")
        self.verticalLayout_4.addWidget(self.tagCrossingRadioButton)
        self.tagCrossingDressedRadioButton = QtWidgets.QRadioButton(
            self.tagChoicesFrame
        )
        self.tagCrossingDressedRadioButton.setToolTip("")
        self.tagCrossingDressedRadioButton.setText(
            "Tag as avoided crossing by dressed-states indices"
        )
        self.tagCrossingDressedRadioButton.setIconSize(QtCore.QSize(16, 16))
        self.tagCrossingDressedRadioButton.setObjectName(
            "tagCrossingDressedRadioButton"
        )
        self.verticalLayout_4.addWidget(self.tagCrossingDressedRadioButton)
        self.verticalLayout_3.addWidget(self.tagChoicesFrame)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_3.addItem(spacerItem5)
        self.tagDressedGroupBox = QtWidgets.QGroupBox(self.tagTab)
        self.tagDressedGroupBox.setEnabled(False)
        self.tagDressedGroupBox.setToolTip("")
        self.tagDressedGroupBox.setTitle("Tag by dressed-states indices")
        self.tagDressedGroupBox.setObjectName("tagDressedGroupBox")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tagDressedGroupBox)
        self.gridLayout_13.setObjectName("gridLayout_13")
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_13.addItem(spacerItem6, 0, 2, 1, 1)
        self.inititalStateSpinBox = QtWidgets.QSpinBox(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.inititalStateSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.inititalStateSpinBox.setSizePolicy(sizePolicy)
        self.inititalStateSpinBox.setObjectName("initialStateSpinBox")
        self.gridLayout_13.addWidget(self.inititalStateSpinBox, 0, 4, 1, 1)
        self.finalStateSpinBox = QtWidgets.QSpinBox(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.finalStateSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.finalStateSpinBox.setSizePolicy(sizePolicy)
        self.finalStateSpinBox.setProperty("value", 1)
        self.finalStateSpinBox.setObjectName("finalStateSpinBox")
        self.gridLayout_13.addWidget(self.finalStateSpinBox, 1, 4, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setToolTip("")
        self.label_29.setText("Photons")
        self.label_29.setObjectName("label_29")
        self.gridLayout_13.addWidget(self.label_29, 0, 0, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setToolTip("")
        self.label_30.setText("Initial state")
        self.label_30.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.label_30.setObjectName("label_30")
        self.gridLayout_13.addWidget(self.label_30, 0, 3, 1, 1)
        self.phNumberDressedSpinBox = QtWidgets.QSpinBox(self.tagDressedGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.phNumberDressedSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.phNumberDressedSpinBox.setSizePolicy(sizePolicy)
        self.phNumberDressedSpinBox.setMinimum(1)
        self.phNumberDressedSpinBox.setObjectName("phNumberDressedSpinBox")
        self.gridLayout_13.addWidget(self.phNumberDressedSpinBox, 0, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.tagDressedGroupBox)
        self.label_31.setToolTip("")
        self.label_31.setText("Final state")
        self.label_31.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_31.setObjectName("label_31")
        self.gridLayout_13.addWidget(self.label_31, 1, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_13.addItem(spacerItem7, 0, 5, 1, 1)
        self.verticalLayout_3.addWidget(self.tagDressedGroupBox)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.verticalLayout_3.addItem(spacerItem8)
        self.tagBareGroupBox = QtWidgets.QGroupBox(self.tagTab)
        self.tagBareGroupBox.setEnabled(False)
        self.tagBareGroupBox.setAutoFillBackground(False)
        self.tagBareGroupBox.setTitle("Tag by bare-states indices")
        self.tagBareGroupBox.setFlat(False)
        self.tagBareGroupBox.setObjectName("tagBareGroupBox")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tagBareGroupBox)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.subsysNamesLineEdit = QtWidgets.QLineEdit(self.tagBareGroupBox)
        self.subsysNamesLineEdit.setText("")
        self.subsysNamesLineEdit.setPlaceholderText(
            "Subsystem names:   <name of subsys 1>, <name of subsys 2>, ..."
        )
        self.subsysNamesLineEdit.setClearButtonEnabled(True)
        self.subsysNamesLineEdit.setObjectName("subsysNamesLineEdit")
        self.gridLayout_12.addWidget(self.subsysNamesLineEdit, 0, 0, 1, 5)
        self.label_25 = QtWidgets.QLabel(self.tagBareGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setText("Photons")
        self.label_25.setObjectName("label_25")
        self.gridLayout_12.addWidget(self.label_25, 1, 0, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_12.addItem(spacerItem9, 1, 2, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.tagBareGroupBox)
        self.label_28.setText("Initial state")
        self.label_28.setObjectName("label_28")
        self.gridLayout_12.addWidget(self.label_28, 1, 3, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.tagBareGroupBox)
        self.label_26.setText("Final state")
        self.label_26.setObjectName("label_26")
        self.gridLayout_12.addWidget(self.label_26, 2, 3, 1, 1)
        self.finalStateLineEdit = QtWidgets.QLineEdit(self.tagBareGroupBox)
        self.finalStateLineEdit.setPlaceholderText("e.g.:  0, 1, ...")
        self.finalStateLineEdit.setObjectName("finalStateLineEdit")
        self.gridLayout_12.addWidget(self.finalStateLineEdit, 2, 4, 1, 1)
        self.phNumberBareSpinBox = QtWidgets.QSpinBox(self.tagBareGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.phNumberBareSpinBox.sizePolicy().hasHeightForWidth()
        )
        self.phNumberBareSpinBox.setSizePolicy(sizePolicy)
        self.phNumberBareSpinBox.setMinimum(1)
        self.phNumberBareSpinBox.setObjectName("phNumberBareSpinBox")
        self.gridLayout_12.addWidget(self.phNumberBareSpinBox, 1, 1, 1, 1)
        self.initialStateLineEdit = QtWidgets.QLineEdit(self.tagBareGroupBox)
        self.initialStateLineEdit.setPlaceholderText(
            "<level subsys 1>, <level subsys2>, ..."
        )
        self.initialStateLineEdit.setObjectName("initialStateLineEdit")
        self.gridLayout_12.addWidget(self.initialStateLineEdit, 1, 4, 1, 1)
        self.verticalLayout_3.addWidget(self.tagBareGroupBox)
        spacerItem10 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_3.addItem(spacerItem10)
        self.tabWidget.addTab(self.tagTab, "Tag datasets")
        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 2)
        self.mplFigureCanvas = FigureCanvas(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mplFigureCanvas.sizePolicy().hasHeightForWidth()
        )
        self.mplFigureCanvas.setSizePolicy(sizePolicy)
        self.mplFigureCanvas.setMinimumSize(QtCore.QSize(0, 60))
        self.mplFigureCanvas.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mplFigureCanvas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mplFigureCanvas.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mplFigureCanvas.setLineWidth(1)
        self.mplFigureCanvas.setObjectName("mplFigureCanvas")
        self.resetViewButton = QtWidgets.QPushButton(self.mplFigureCanvas)
        self.resetViewButton.setGeometry(QtCore.QRect(10, 20, 40, 40))
        self.resetViewButton.setToolTip("Reset plot area")
        self.resetViewButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/reset.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.resetViewButton.setIcon(icon8)
        self.resetViewButton.setObjectName("resetViewButton")
        self.panViewButton = QtWidgets.QPushButton(self.mplFigureCanvas)
        self.panViewButton.setGeometry(QtCore.QRect(60, 20, 40, 40))
        self.panViewButton.setCursor(QtCore.Qt.ArrowCursor)
        self.panViewButton.setToolTip("Pan mode: move plot region by dragging")
        self.panViewButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/move.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.panViewButton.setIcon(icon9)
        self.panViewButton.setCheckable(True)
        self.panViewButton.setAutoExclusive(True)
        self.panViewButton.setObjectName("panViewButton")
        self.zoomViewButton = QtWidgets.QPushButton(self.mplFigureCanvas)
        self.zoomViewButton.setGeometry(QtCore.QRect(110, 20, 40, 40))
        self.zoomViewButton.setCursor(QtCore.Qt.ArrowCursor)
        self.zoomViewButton.setToolTip("Zoom mode: select a plot region to enlarge")
        self.zoomViewButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/zoom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.zoomViewButton.setIcon(icon10)
        self.zoomViewButton.setCheckable(True)
        self.zoomViewButton.setAutoExclusive(True)
        self.zoomViewButton.setObjectName("zoomViewButton")
        self.selectViewButton = QtWidgets.QPushButton(self.mplFigureCanvas)
        self.selectViewButton.setGeometry(QtCore.QRect(160, 20, 41, 41))
        self.selectViewButton.setCursor(QtCore.Qt.CrossCursor)
        self.selectViewButton.setToolTip("")
        self.selectViewButton.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(
            QtGui.QPixmap(":/icons/selectmode.png"), QtGui.QIcon.Normal, QtGui.QIcon.On
        )
        self.selectViewButton.setIcon(icon11)
        self.selectViewButton.setCheckable(True)
        self.selectViewButton.setChecked(True)
        self.selectViewButton.setAutoExclusive(True)
        self.selectViewButton.setObjectName("selectViewButton")
        self.swapXYButton = QtWidgets.QPushButton(self.mplFigureCanvas)
        self.swapXYButton.setGeometry(QtCore.QRect(210, 20, 71, 41))
        self.swapXYButton.setCursor(QtCore.Qt.CrossCursor)
        self.swapXYButton.setToolTip("")
        self.swapXYButton.setText("X↔Y")
        self.swapXYButton.setCheckable(True)
        self.swapXYButton.setChecked(True)
        self.swapXYButton.setAutoExclusive(True)
        self.swapXYButton.setObjectName("swapXYButton")
        self.gridLayout.addWidget(self.mplFigureCanvas, 1, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.dataTableView, self.datasetListView)
        MainWindow.setTabOrder(self.datasetListView, self.newRowButton)
        MainWindow.setTabOrder(self.newRowButton, self.deleteRowButton)
        MainWindow.setTabOrder(self.deleteRowButton, self.clearAllButton)
        MainWindow.setTabOrder(self.clearAllButton, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.bgndSubtractXCheckBox)
        MainWindow.setTabOrder(self.bgndSubtractXCheckBox, self.bgndSubtractYCheckBox)
        MainWindow.setTabOrder(self.bgndSubtractYCheckBox, self.savgolFilterYCheckBox)
        MainWindow.setTabOrder(self.savgolFilterYCheckBox, self.savgolFilterXCheckBox)
        MainWindow.setTabOrder(self.savgolFilterXCheckBox, self.gaussLaplaceCheckBox)
        MainWindow.setTabOrder(self.gaussLaplaceCheckBox, self.colorComboBox)
        MainWindow.setTabOrder(self.colorComboBox, self.logScaleCheckBox)
        MainWindow.setTabOrder(self.logScaleCheckBox, self.yComboBox)
        MainWindow.setTabOrder(self.yComboBox, self.zComboBox)
        MainWindow.setTabOrder(self.zComboBox, self.xComboBox)
        MainWindow.setTabOrder(self.xComboBox, self.rawX1LineEdit)
        MainWindow.setTabOrder(self.rawX1LineEdit, self.calibrateX2Button)
        MainWindow.setTabOrder(self.calibrateX2Button, self.mapX2LineEdit)
        MainWindow.setTabOrder(self.mapX2LineEdit, self.rawX2LineEdit)
        MainWindow.setTabOrder(self.rawX2LineEdit, self.mapX1LineEdit)
        MainWindow.setTabOrder(self.mapX1LineEdit, self.calibrateX1Button)
        MainWindow.setTabOrder(self.calibrateX1Button, self.rawY2LineEdit)
        MainWindow.setTabOrder(self.rawY2LineEdit, self.calibrateY2Button)
        MainWindow.setTabOrder(self.calibrateY2Button, self.mapY1LineEdit)
        MainWindow.setTabOrder(self.mapY1LineEdit, self.calibrateY1Button)
        MainWindow.setTabOrder(self.calibrateY1Button, self.mapY2LineEdit)
        MainWindow.setTabOrder(self.mapY2LineEdit, self.rawY1LineEdit)
        MainWindow.setTabOrder(self.rawY1LineEdit, self.calibratedCheckBox)
        MainWindow.setTabOrder(self.calibratedCheckBox, self.noTagRadioButton)
        MainWindow.setTabOrder(self.noTagRadioButton, self.tagDispersiveBareRadioButton)
        MainWindow.setTabOrder(
            self.tagDispersiveBareRadioButton, self.tagDispersiveDressedRadioButton
        )
        MainWindow.setTabOrder(
            self.tagDispersiveDressedRadioButton, self.tagCrossingRadioButton
        )
        MainWindow.setTabOrder(
            self.tagCrossingRadioButton, self.tagCrossingDressedRadioButton
        )
        MainWindow.setTabOrder(
            self.tagCrossingDressedRadioButton, self.inititalStateSpinBox
        )
        MainWindow.setTabOrder(self.inititalStateSpinBox, self.finalStateSpinBox)
        MainWindow.setTabOrder(self.finalStateSpinBox, self.phNumberDressedSpinBox)
        MainWindow.setTabOrder(self.phNumberDressedSpinBox, self.subsysNamesLineEdit)
        MainWindow.setTabOrder(self.subsysNamesLineEdit, self.phNumberBareSpinBox)
        MainWindow.setTabOrder(self.phNumberBareSpinBox, self.initialStateLineEdit)
        MainWindow.setTabOrder(self.initialStateLineEdit, self.finalStateLineEdit)
        MainWindow.setTabOrder(self.finalStateLineEdit, self.resetViewButton)
        MainWindow.setTabOrder(self.resetViewButton, self.panViewButton)
        MainWindow.setTabOrder(self.panViewButton, self.zoomViewButton)
        MainWindow.setTabOrder(self.zoomViewButton, self.selectViewButton)
        MainWindow.setTabOrder(self.selectViewButton, self.swapXYButton)

    def retranslateUi(self, MainWindow):
        pass


from calibration import CalibrationLineEdit
from datawidgets import ListView, TableView
from PySide6.QtQuickWidgets import QQuickWidget
from mplwidgets import FigureCanvas
import resources_rc