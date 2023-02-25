from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
from PIL import Image
from io import BytesIO


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

            imgByte = BytesIO()
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
