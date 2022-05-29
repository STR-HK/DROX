from PyQt5.QtCore import *


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
