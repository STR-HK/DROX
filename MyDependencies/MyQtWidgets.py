from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ButtonHoverWatcher(QObject):
    hovered = pyqtSignal()

    def __init__(self, widget) -> None:
        super().__init__()
        self.widget = widget

    def eventFilter(self, obj, event) -> bool:
        print("filter")
        if obj == self.widget:
            print("event")
            if event.type() == QEvent.Enter:
                print("enter")
                self.hovered.emit()


# class DPushButton(QPushButton):
#     def __init__(self, *args, **kwargs):
#         super(QPushButton, self).__init__(*args, **kwargs)
#         self.setCursor(Qt.PointingHandCursor)
#
#         # self.setAutoRepeat(True)
#         # self.setAutoRepeatDelay(1000)
#         # self.setAutoRepeatInterval(1000)
#         # self.clicked.connect(self.handleClicked)
#         # self._state = 0
#
#         filter = ButtonHoverWatcher(self)
#         self.installEventFilter(filter)
#
#     def handleClicked(self):
#         if self.isDown():
#             if self._state == 0:
#                 self._state = 1
#                 self.setAutoRepeatInterval(50)
#                 print("press")
#             else:
#                 print("repeat")
#         elif self._state == 1:
#             self._state = 0
#             self.setAutoRepeatInterval(1000)
#             print("release")
#         else:
#             print("click")


class QPushButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        self.setMinimumHeight(40)
        # self.setStyleSheet(f"""
        #     QPushButton {{
        #         background-color: {colorScheme.surface};
        #         color: {colorScheme.primary};
        #         border-radius: 20px;
        #         font-size: 12px;
        #         font-weight: 500;
        #         text-align: center;
        #         padding: 0 24px 0 24px;
        #         border: none;
        #     }}
        #     QPushButton:hover {{
        #         background-color: {colorScheme.background};
        #         color: {colorScheme.surface};
        #     }}
        # """)
        self.setStyleSheet('bakcground-color: red;')
class QVBoxLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(QVBoxLayout, self).__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
