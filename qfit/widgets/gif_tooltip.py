from PySide6.QtWidgets import (
    QPushButton,
    QMainWindow,
    QLabel,
    QWidget,
    QDialog,
    QVBoxLayout,
    QToolButton,
    QHBoxLayout,
)
from PySide6.QtCore import QEvent
from PySide6.QtGui import QMovie, QColor, QPalette, QPixmap
from PySide6.QtCore import Qt

from typing import List, Tuple, Union


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


class DialogWindowWithMedia(QDialog):
    def __init__(self, text: str, media_list: List[Tuple[str, Union[int, None]]]):
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

        media_label_list = []
        media_widget_list = []
        media_layout_list = []
        # insert media here
        for media in media_list:
            media_widget_list.append(QWidget())
            layout.addWidget(media_widget_list[-1])
            media_layout_list.append(QVBoxLayout(media_widget_list[-1]))
            media_layout_list[-1].setContentsMargins(0, 0, 0, 0)
            media_layout_list[-1].setSpacing(0)
            media_layout_list[-1].setAlignment(Qt.AlignCenter)
            media_path, width = media
            media_label_list.append(QLabel())
            # if the media is a GIF
            if media_path.endswith(".gif"):
                # Setup label
                media_layout_list[-1].addWidget(media_label_list[-1])
                # Load and start movie (GIF)
                movie = QMovie(media_path)
                media_label_list[-1].setMovie(movie)
                movie.start()
                # set the width of the GIF, if width is provided, scale the GIF down
                if width is not None:
                    media_label_list[-1].setFixedWidth(width)
                    # scale the GIF down by the same factor as the width
                    movie.setScaledSize(
                        movie.currentPixmap().size()
                        * (width / movie.currentPixmap().width())
                    )
                else:
                    media_label_list[-1].setFixedWidth(movie.currentPixmap().width())

            # if the media is an image
            elif media_path.endswith(".png") or media_path.endswith(".jpg"):
                # Setup label
                media_label_list.append(QLabel())
                media_layout_list[-1].addWidget(media_label_list[-1])
                # Load image
                pixmap = QPixmap(media_path)
                media_label_list[-1].setPixmap(pixmap)
                # set the width of the image, if width is provided, scale the image
                if width is not None:
                    media_label_list[-1].setFixedWidth(width)
                    # scale the image down by the same factor as the width
                    media_label_list[-1].setPixmap(pixmap.scaledToWidth(width))
                else:
                    media_label_list[-1].setFixedWidth(pixmap.width())

        # Setup a widget for the close button to be centered
        close_button_widget = QWidget()
        layout.addWidget(close_button_widget)
        close_button_widget_layout = QHBoxLayout(close_button_widget)
        close_button_widget_layout.setContentsMargins(0, 0, 0, 0)
        close_button_widget_layout.setSpacing(0)

        # Setup close button
        close_button = QPushButton("CLOSE")
        close_button_widget_layout.addWidget(close_button)
        # set close button width
        close_button.setFixedWidth(100)
        # center the button position
        close_button_widget_layout.setAlignment(Qt.AlignCenter)

        close_button.setStyleSheet("QPushButton { text-align: center; }")
        close_button.setFocusPolicy(Qt.NoFocus)
        close_button.setDefault(False)

        self.setFocus()

        # Connect the Close button to the close slot of the dialog
        close_button.clicked.connect(self.close)
