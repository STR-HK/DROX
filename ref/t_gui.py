import io
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

import requests

from MyYt import *

from PIL import Image
from io import BytesIO


class MouseObserver(QObject):
    pressed = pyqtSignal(QEvent)
    released = pyqtSignal(QEvent)
    moved = pyqtSignal(QEvent)

    def __init__(self, window):
        super().__init__(window)
        self._window = window

        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window

    def eventFilter(self, obj, event):
        if self.window is obj:
            if event.type() == QEvent.MouseButtonPress:
                self.pressed.emit(event)
            elif event.type() == QEvent.MouseMove:
                self.moved.emit(event)
            elif event.type() == QEvent.MouseButtonRelease:
                self.released.emit(event)
        return super().eventFilter(obj, event)


class QPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)


class QVBoxLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QVBoxLayout, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)


class AppBarTitle(QLabel):
    def __init__(self, *args, **kwargs):
        super(QLabel, self).__init__(*args, **kwargs)
        self.font = QFont("Pretendard", 20)
        self.setFont(self.font)
        self.setStyleSheet("font-size: 28px; font-weight: 500; color: black;")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


class NavButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(
            """
            background-color: #fafafa;
            border: 1px solid #fafafa;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            font-weight: 500;
            color: black;
            margin: 5px;
            """
        )

        self.inverted = False

    def setIcon(self, icon):
        if not hasattr(self, "icon_"):
            self.icon_ = icon
        super(QPushButton, self).setIcon(icon)

    def setInvertIcon(self, invert):
        self.invert = invert

    def invertIcon(self):
        if hasattr(self, "invert"):
            if self.inverted == False:
                self.setIcon(self.invert)
                self.inverted = True
            else:
                self.setIcon(self.icon_)
                self.inverted = False
        else:
            print("No invert icon")


class LazyIcon(QThread):
    repaint = pyqtSignal()
    setResultListIcon = pyqtSignal(QListWidgetItem, QIcon)

    def __init__(self, list, item, url):
        super().__init__()
        self.list = list
        self.item = item
        self.url = url

    def run(self):
        r = requests.get(self.url)
        self.edit(r.content)

    def edit(self, content):
        try:
            thumbImg = Image.open(BytesIO(content))
            thumbImg = thumbImg.convert("RGBA")
            thumbImg = thumbImg.crop(
                (
                    int((thumbImg.width - thumbImg.height) / 2),
                    0,
                    int((thumbImg.width - thumbImg.height) / 2) + thumbImg.height,
                    thumbImg.height,
                )
            )

            imgByte = io.BytesIO()
            thumbImg.save(imgByte, format="PNG")
            qpix = QPixmap()
            qpix.loadFromData(imgByte.getvalue())
            # self.item.setIcon(QIcon(qpix))
            self.setResultListIcon.emit(self.item, QIcon(qpix))

            self.repaint.emit()
        except Exception as e:
            print(e)

    def apply(self, content):
        pix = QPixmap()
        pix.loadFromData(content)
        self.item.setIcon(QIcon(pix))


class AppBar(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QHBoxLayout, self).__init__(*args, **kwargs)

        self.setContentsMargins(7, 7, 7, 7)


class DroxMain(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.initUI()

    def initUI(self):
        open("terminate.txt", "w").write("0")

        x, y = open("pos.txt", "r").read().split(", ")
        w, h = open("size.txt", "r").read().split(", ")
        self.move(int(x), int(y))
        self.resize(int(w), int(h))

        self.setWindowTitle("ㅤ")
        self.setWindowIcon(QIcon("library_music.svg"))
        self.resize(480, 680)
        # self.center()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DroxMain()
    sys.exit(app.exec_())
