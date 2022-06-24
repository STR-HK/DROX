from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import *


from MyPicker import *
import SvgEditor

from MyColors import *


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
            "font-size: 28px; font-weight: 600; color: {};".format("black")
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


class NeuNavButton(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super(QWidget, self).__init__(*args, **kwargs)
        self.wid = QVBoxLayout()

        self.setContentsMargins(0, 0, 0, 0)
        self.wid.setContentsMargins(0, 0, 0, 0)
        self.wid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.icon = QLabel()
        self.icon.setFixedHeight(26)
        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.icon.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.wid.addWidget(self.icon)

        self.btn = QLabel("Default")
        self.setTextColor("lightgray")
        self.wid.addWidget(self.btn)

        self.setLayout(self.wid)

        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.inverted = False

    def setIcon(self, icon):
        if not hasattr(self, "icon_"):
            self.icon_ = icon
            pix = QPixmap()
            pix.loadFromData(SvgEditor.change_color(self.icon_, "gray"))

            self.icon.setPixmap(pix)

        else:
            self.icon.setPixmap(icon)

    def setText(self, text):
        self.btn.setText(text)

    def setTextColor(self, color):
        self.btn.setStyleSheet("font-size: 10px; color: {}".format(color))

    def setInvertIcon(self, invert):
        self.invert = invert

    def invertIcon(self):
        if hasattr(self, "invert"):
            if self.inverted == False:
                pix = QPixmap()
                pix.loadFromData(SvgEditor.change_color(self.icon_, ACCENT_COLOR))
                self.setIcon(pix)
                self.inverted = True

                self.setTextColor(ACCENT_COLOR)
            else:
                pix = QPixmap()
                pix.loadFromData(SvgEditor.change_color(self.icon_, "gray"))
                self.setIcon(pix)
                self.inverted = False

                self.setTextColor("gray")
        else:
            print("No invert icon")

    def clicked(self, event):
        print(event)


class ScaledTopRoundLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self)
        self.radius = 5
        self._pixmap = QPixmap(self.pixmap())

    def setRadius(self, radius):
        self.radius = radius

    def resizeEvent(self, event):
        # print("ScaledTopRoundLabel::resize")
        self.updateImg()
        self.setFixedHeight(self.width())

    def setIcon(self, icon):
        self._pixmap = QPixmap(icon)
        self.setPixmap(self._pixmap)

    def updateImg(self):
        pixmap = self._pixmap
        sang = self.radius / self.width() * 1.8  # amplify the radius
        # print(sang)
        radius = int((pixmap.size() * sang).width())

        rounded = QPixmap(pixmap.size())
        rounded.fill(QColor("transparent"))

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(pixmap))
        painter.setPen(Qt.NoPen)
        path = QPainterPath()
        path.moveTo(radius, 0)
        path.lineTo(pixmap.width() - radius, 0)
        path.arcTo(pixmap.width() - radius, 0, radius, radius, 90, -90)
        path.lineTo(pixmap.width(), pixmap.height())
        path.lineTo(0, pixmap.height())
        path.lineTo(0, radius)
        path.arcTo(0, 0, radius, radius, 180, -90)
        painter.drawPath(path)
        painter.end()

        self.setPixmap(rounded)


class MainMenuWidget(QGroupBox):
    clicked = pyqtSignal()
    context = pyqtSignal()

    def __init__(
        self,
    ):
        super().__init__()
        self.radius = 5

        self.setStyleSheet(f"border: none; border-radius: {self.radius}px;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setContentsMargins(0, 0, 0, 0)

        self.Layout_M = QVBoxLayout()
        self.setLayout(self.Layout_M)
        self.Layout_M.setContentsMargins(0, 0, 0, 10)

        self.Image = ScaledTopRoundLabel()
        self.Layout_M.addWidget(self.Image)
        self.Image.setRadius(self.radius)
        self.Image.setScaledContents(True)

        self.MainText = QLabel()
        self.Layout_M.addWidget(self.MainText)
        self.MainText.setText("MainText")
        self.MainText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.MainText.setStyleSheet("font-size: 1rem; font-weight: bold;")

        self.SubText = QLabel("SubText")
        self.Layout_M.addWidget(self.SubText)
        self.SubText.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.context.emit()

    def setMainText(self, text):
        self.MainText.setText(text)

    def setSubText(self, text):
        self.SubText.setText(text)

    def setTextColor(self, color):
        self.MainText.setStyleSheet(
            self.MainText.styleSheet() + "color: {};".format(color)
        )
        self.SubText.setStyleSheet(
            self.SubText.styleSheet() + "color: {};".format(color)
        )

    def setBgColor(self, color):
        self.setStyleSheet(self.styleSheet() + "background-color: {};".format(color))

    def setIcon(self, icon):
        self.Image.setIcon(icon)
        self.setBgColor(pick_color(icon))
        self.setTextColor(invert_color(HEX_VALUE=pick_color(icon), BLACK_WHITE=True))
