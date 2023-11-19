from PySide6.QtWidgets import (
    QPushButton,
    QMainWindow,
    QLabel,
    QWidget,
    QDialog,
    QVBoxLayout,
    QToolButton,
    QHBoxLayout,
    QSizePolicy,
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
        layout.setAlignment(Qt.AlignCenter)

        # Setup label for text
        text_label = QLabel(text)
        layout.addWidget(text_label)
        text_label.setAlignment(Qt.AlignLeft)

        media_label_list = []
        # insert media here
        for media in media_list:
            media_label_list.append(QLabel())
            media_label_list[-1].setAlignment(Qt.AlignCenter)
            media_path, width = media
            # if the media is a GIF
            if media_path.endswith(".gif"):
                # Setup label
                # Load and start movie (GIF)
                movie = QMovie(media_path)
                media_label_list[-1].setMovie(movie)
                movie.start()
                # set the width of the GIF, if width is provided, scale the GIF down
                if width is not None:
                    media_label_list[-1].setFixedWidth(width)
                    # scale the GIF down by the same factor as the width
                    scaled_size = movie.currentPixmap().size() * (
                        width / movie.currentPixmap().width()
                    )
                    movie.setScaledSize(
                        movie.currentPixmap().size()
                        * (width / movie.currentPixmap().width())
                    )
                    # get current height
                    height = scaled_size.height()
                    # set the height of the GIF
                    media_label_list[-1].setFixedHeight(height)
                else:
                    media_label_list[-1].setFixedWidth(movie.currentPixmap().width())
                    media_label_list[-1].setFixedHeight(movie.currentPixmap().height())

            # if the media is an image
            elif media_path.endswith(".png") or media_path.endswith(".jpg"):
                # Load image
                pixmap = QPixmap(media_path)
                media_label_list[-1].setPixmap(pixmap)
                # set the width of the image, if width is provided, scale the image
                if width is not None:
                    media_label_list[-1].setFixedWidth(width)
                    # scale the image down by the same factor as the width
                    media_label_list[-1].setPixmap(pixmap.scaledToWidth(width))
                    # get current height
                    height = pixmap.scaledToWidth(width).height()
                    # set the height of the image
                    media_label_list[-1].setFixedHeight(height)
                else:
                    media_label_list[-1].setFixedWidth(pixmap.width())
                    media_label_list[-1].setFixedHeight(pixmap.height())
            layout.addWidget(media_label_list[-1], alignment=Qt.AlignCenter)

        # Setup close button
        close_button = QPushButton("CLOSE")
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        # set close button width
        close_button.setFixedWidth(100)
        # center the button position
        # close_button_widget_layout.setAlignment(Qt.AlignCenter)

        close_button.setStyleSheet("QPushButton { text-align: center; }")
        close_button.setFocusPolicy(Qt.NoFocus)
        close_button.setDefault(False)

        self.setFocus()

        # Connect the Close button to the close slot of the dialog
        close_button.clicked.connect(self.close)
