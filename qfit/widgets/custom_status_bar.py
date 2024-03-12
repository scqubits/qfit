from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRect
from PySide6.QtWidgets import QStatusBar


class CustomStatusBar(QStatusBar):
    """
    Status bar for the main window. Currently unused.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Set the color for the leftmost 30px and draw
        leftColor = QColor("#121212")
        painter.fillRect(QRect(0, 0, 190, self.height()), leftColor)

        # Set the color for the rest of the status bar and draw
        restColor = QColor("#212121")
        painter.fillRect(QRect(190, 0, self.width() - 190, self.height()), restColor)
