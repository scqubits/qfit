from PySide6.QtWidgets import (
    QPushButton,
    QMainWindow,
    QLabel,
    QWidget,
    QDialog,
    QVBoxLayout,
    QToolButton,
)
from PySide6.QtCore import QEvent
from PySide6.QtGui import QMovie, QColor, QPalette
from PySide6.QtCore import Qt


class AnimatedToolTip(QLabel):
    def __init__(self, gif_path):
        super().__init__()
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.movie.start()
        self.setWindowFlags(Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def showEvent(self, event):
        self.movie.start()

    def hideEvent(self, event):
        self.movie.stop()


class ButtonWithAnimatedTooltip(QPushButton):
    def __init__(self, *args, gif_path, **kwargs):
        super().__init__(*args, **kwargs)
        self.tooltip_gif = AnimatedToolTip(gif_path)

    def eventFilter(self, obj, event):
        if obj == self.button:
            if event.type() == QEvent.Enter:
                self.tooltip_gif.move(
                    self.button.mapToGlobal(self.button.rect().bottomLeft())
                )
                self.tooltip_gif.show()
            elif event.type() == QEvent.Leave:
                self.tooltip_gif.hide()

        return super().eventFilter(obj, event)


class DialogWindowWithGif(QDialog):
    def __init__(self, text, gif_path):
        super().__init__()
        self.setStyleSheet(
            "QDialog {\n"
            "	background-color: rgb(18, 18, 18);\n"
            "}\n"
            "\n"
            "QFrame {\n"
            "	background-color: rgb(18, 18, 18);\n"
            "}\n"
            "\n"
            "QWidget {\n"
            '	font-family: "Roboto Medium";\n'
            "	font-size: 11pt;\n"
            "}\n"
            "\n"
            "QLabel {\n"
            "	color: rgb(170, 170, 170);\n"
            "}\n"
        )

        # Setup layout
        layout = QVBoxLayout(self)

        # Setup label for text
        text_label = QLabel(text)
        layout.addWidget(text_label)

        # Setup label for GIF
        gif_label = QLabel()
        layout.addWidget(gif_label)

        # Setup Close button
        close_button = QPushButton("CLOSE")
        close_button.setFocusPolicy(Qt.NoFocus)
        close_button.setDefault(False)
        layout.addWidget(close_button)

        self.setFocus()

        # Connect the Close button to the close slot of the dialog
        close_button.clicked.connect(self.close)

        # Load and start movie (GIF)
        movie = QMovie(gif_path)
        gif_label.setMovie(movie)
        movie.start()
