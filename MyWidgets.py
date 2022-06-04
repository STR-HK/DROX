from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import *

# from gui import ACCENT_COLOR


class AppBar(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QHBoxLayout, self).__init__(*args, **kwargs)

        self.setContentsMargins(7, 0, 7, 0)


class AppBarTitle(QLabel):
    def __init__(self, *args, **kwargs):
        super(QLabel, self).__init__(*args, **kwargs)
        self.font = QFont("Pretendard", 20)
        self.setFont(self.font)
        self.setStyleSheet(
            "font-size: 28px; font-weight: 500; color: {};".format("black")
        )
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 5)


class NavButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(QPushButton, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(
            """
            background-color: #fafafa;
            border: 1px solid transparent;
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
