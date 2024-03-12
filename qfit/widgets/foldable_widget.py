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
from PySide6.QtCore import Qt, QSize, QCoreApplication, Slot, Signal

SPACING = 12
MARGIN = -1


class FoldPushButton(QPushButton):
    """
    Push button that has an icon.
    """

    def __init__(self, title="Foldable", parent=None):
        """
        Create a push button with an icon.

        Parameters
        ----------
        title : str
            The title of the push button.
        parent : QWidget
            The parent widget.
        """
        super().__init__(parent)

        # icon
        self.icon = QIcon()
        self.icon.addFile(
            ":/icons/svg/arrow-right-737373.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.icon.addFile(
            ":/icons/svg/arrow-down-737373.svg",
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        # set the style sheet (which controls the font, color, text align, border, etc.)
        self.setStyleSheet(
            "QPushButton {\n"
            '	font: 14px "Roboto Medium";\n'
            "   font-weight: bold;\n"
            "	color: #AAAAAA;\n"
            "	text-align: left;\n"
            "	border: none;\n"
            "}"
        )
        self.setIcon(self.icon)
        # set title
        self.setText(QCoreApplication.translate("MainWindow", title, None))
        # set checkable
        self.setCheckable(True)
        self.setChecked(True)

    def setCheckable(self, value):
        """
        Set the checkable property of the push button, and remove the icon 
        if the value is False.
        """
        super().setCheckable(value)

        # remove the icon if false
        if not value:
            self.setIcon(QIcon())
        else:
            self.setIcon(self.icon)


class FoldableWidget(QGroupBox):
    """
    A widget that contains a title and a content widget. The content widget will be
    hidden when the widget is not checked.

    Parameters
    ----------
    title : str
        The title of the widget.
    content_widget : QWidget
        The content widget, which will be hidden when the widget is not checked.
    parent : QWidget
        The parent widget.
    """

    expandWidgetToggled = Signal(bool)

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
        self.foldPushButton.clicked.connect(self._toggleContent)
        # initialize the content
        self._toggleContent(self.foldPushButton.isChecked())

        # set the size policy for the foldable widget: expand along horizontal, fixed along vertical
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.boxLayout.setContentsMargins(0, MARGIN, 0, MARGIN)  # Remove the margins
        self.boxLayout.setSpacing(SPACING)

    @Slot(bool)
    def _toggleContent(self, checked):
        """
        Toggle the visibility of the content widget.
        """
        self.content_widget.setVisible(checked)
        # send a signal to expand the frame
        self.expandWidgetToggled.emit(checked)

    def toggle(self):
        """
        Toggle the visibility of the content widget.
        """
        self.foldPushButton.toggle()
        self._toggleContent(self.foldPushButton.isChecked())

    def setConentWidget(self, content_widget):
        """
        Set the content widget.
        """
        # remove
        self.boxLayout.removeWidget(self.content_widget)

        # add
        self.content_widget = content_widget
        self.boxLayout.addWidget(self.content_widget)
