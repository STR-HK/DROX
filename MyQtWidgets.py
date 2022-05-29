from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class QPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)


class QVBoxLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QVBoxLayout, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
