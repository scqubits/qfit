# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_manage_datasets.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from qfit.widgets.data_extracting import ListView
from . import resources_rc


class Ui_ManageDatasetsWidget(object):
    def setupUi(self, ManageDatasetsWidget):
        if not ManageDatasetsWidget.objectName():
            ManageDatasetsWidget.setObjectName(u"ManageDatasetsWidget")
        ManageDatasetsWidget.resize(400, 138)
        self.horizontalLayout = QHBoxLayout(ManageDatasetsWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.allDatasetsButtonsFrame = QFrame(ManageDatasetsWidget)
        self.allDatasetsButtonsFrame.setObjectName(u"allDatasetsButtonsFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.allDatasetsButtonsFrame.sizePolicy().hasHeightForWidth()
        )
        self.allDatasetsButtonsFrame.setSizePolicy(sizePolicy)
        self.allDatasetsButtonsFrame.setStyleSheet(
            u"QPushButton {\n"
            "	border: 0px solid rgb(52, 59, 72);\n"
            "	border-radius: 15px;	\n"
            "	background-color: rgb(93, 93, 93);\n"
            "	color: rgb(200, 200, 200);\n"
            "}\n"
            "QPushButton:hover {\n"
            "	background-color: rgb(196, 150, 250);\n"
            "	border: 0px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {	\n"
            "	background-color: rgb(196, 150, 250);\n"
            "	border: 0px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.verticalLayout_7 = QVBoxLayout(self.allDatasetsButtonsFrame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.newRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.newRowButton.setObjectName(u"newRowButton")
        sizePolicy.setHeightForWidth(self.newRowButton.sizePolicy().hasHeightForWidth())
        self.newRowButton.setSizePolicy(sizePolicy)
        self.newRowButton.setMinimumSize(QSize(100, 30))
        # if QT_CONFIG(tooltip)
        self.newRowButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.newRowButton.setText(u"NEW   ")
        icon = QIcon()
        icon.addFile(u":/icons/16x16/cil-plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.newRowButton.setIcon(icon)

        self.verticalLayout_7.addWidget(self.newRowButton)

        self.deleteRowButton = QPushButton(self.allDatasetsButtonsFrame)
        self.deleteRowButton.setObjectName(u"deleteRowButton")
        sizePolicy.setHeightForWidth(
            self.deleteRowButton.sizePolicy().hasHeightForWidth()
        )
        self.deleteRowButton.setSizePolicy(sizePolicy)
        self.deleteRowButton.setMinimumSize(QSize(100, 30))
        # if QT_CONFIG(tooltip)
        self.deleteRowButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.deleteRowButton.setText(u"DELETE  ")
        icon1 = QIcon()
        icon1.addFile(u":/icons/16x16/cil-minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteRowButton.setIcon(icon1)

        self.verticalLayout_7.addWidget(self.deleteRowButton)

        self.clearAllButton = QPushButton(self.allDatasetsButtonsFrame)
        self.clearAllButton.setObjectName(u"clearAllButton")
        sizePolicy.setHeightForWidth(
            self.clearAllButton.sizePolicy().hasHeightForWidth()
        )
        self.clearAllButton.setSizePolicy(sizePolicy)
        self.clearAllButton.setMinimumSize(QSize(100, 30))
        # if QT_CONFIG(tooltip)
        self.clearAllButton.setToolTip(u"")
        # endif // QT_CONFIG(tooltip)
        self.clearAllButton.setText(u"CLEAR ALL")

        self.verticalLayout_7.addWidget(self.clearAllButton)

        self.horizontalLayout.addWidget(self.allDatasetsButtonsFrame)

        self.datasetListView = ListView(ManageDatasetsWidget)
        self.datasetListView.setObjectName(u"datasetListView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.datasetListView.sizePolicy().hasHeightForWidth()
        )
        self.datasetListView.setSizePolicy(sizePolicy1)
        self.datasetListView.setMinimumSize(QSize(0, 100))
        self.datasetListView.setMaximumSize(QSize(230, 100))
        self.datasetListView.setStyleSheet(u"background-color: rgb(47, 47, 47)")
        self.datasetListView.setFrameShape(QFrame.NoFrame)
        self.datasetListView.setFrameShadow(QFrame.Plain)

        self.horizontalLayout.addWidget(self.datasetListView)

        self.retranslateUi(ManageDatasetsWidget)

        QMetaObject.connectSlotsByName(ManageDatasetsWidget)

    # setupUi

    def retranslateUi(self, ManageDatasetsWidget):
        ManageDatasetsWidget.setWindowTitle(
            QCoreApplication.translate("ManageDatasetsWidget", u"Form", None)
        )

    # retranslateUi
