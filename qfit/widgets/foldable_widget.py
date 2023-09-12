from PySide6.QtWidgets import (
    QGroupBox, 
    QVBoxLayout, 
    QLabel, 
    QSizePolicy,
    QPushButton,
)

from PySide6.QtGui import (
    QIcon,
)
from PySide6.QtCore import Qt, QSize, QCoreApplication, Slot

SPACING = 10
MARGIN = 10

class FoldPushButton(QPushButton):
    """
    Push button that has an icon.
    """
    def __init__(self, title="Foldable", parent=None):
        super().__init__()
        
        # icon
        icon = QIcon()
        icon.addFile(
            ":/icons/svg/cil-caret-right.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon.addFile(
            ":/icons/svg/cil-caret-bottom.svg",
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        # set the style sheet (which controls the font, color, text align, border, etc.)
        self.setStyleSheet(
            "QPushButton {\n"
            '	font: 57 11pt "Roboto Medium";\n'
            "	color: rgb(170, 170, 170);\n"
            "	text-align: left;\n"
            "	border: none;\n"
            "}"
        )
        self.setIcon(icon)
        # set title
        self.setText(
            QCoreApplication.translate("MainWindow", title, None)
        )
        # set checkable
        self.setCheckable(True)
        self.setChecked(True)


class FoldableWidget(QGroupBox):
    """
    A widget that contains a title and a content widget. The content widget will be
    hidden when the widget is not checked.
    """

    def __init__(self, title="Foldable", content_widget=None, parent=None):
        super().__init__(parent)
        # set fold push button
        self.setObjectName("foldPushButton")

        self.foldPushButton = FoldPushButton(title, self)

        # set the box layout
        self.boxLayout = QVBoxLayout(self)
        # add push button to the layout
        self.boxLayout.addWidget(self.foldPushButton)
        # add content widget
        self.content_widget = (
            content_widget if content_widget else QLabel("No Content", self)
        )
        self.boxLayout.addWidget(self.content_widget)

        # connect the push button to the setVisible method
        self.foldPushButton.clicked.connect(
            self._toggleContent
        )
        # initialize the content
        self._toggleContent(self.foldPushButton.isChecked())

        # set the size policy for the foldable widget: expand along horizontal, fixed along vertical
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.boxLayout.setContentsMargins(0, MARGIN, 0, MARGIN)  # Remove the margins
        self.boxLayout.setSpacing(SPACING)

    @Slot(bool)
    def _toggleContent(self, checked):
        self.content_widget.setVisible(checked)

    def toggle(self):
        self.foldPushButton.toggle()
        self._toggleContent(self.foldPushButton.isChecked())

    def setConentWidget(self, content_widget):
        # remove
        self.boxLayout.removeWidget(self.content_widget)

        # add
        self.content_widget = content_widget
        self.boxLayout.addWidget(self.content_widget)