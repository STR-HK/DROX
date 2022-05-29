from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from io import BytesIO
from PIL import Image
import requests
import random
import sys
import os

from MyPicker import pick_color
from MyAssets import *
from MyYt import *


class DroxMain(QWidget):
    def __init__(self):
        super().__init__()

        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setWindowFlags(
        #     Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        # )
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.initUI()
        self.initLayout()

    def initUI(self):
        open("terminate.txt", "w").write("0")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_terminate)
        self.timer.start(500)

        x, y = open("pos.txt", "r").read().split(", ")
        w, h = open("size.txt", "r").read().split(", ")
        self.move(int(x), int(y))
        self.resize(int(w), int(h))

        # self.setWindowTitle("ㅤ")
        self.setWindowTitle("Drox")
        self.setWindowIcon(QIcon("library_music.svg"))
        self.resize(480, 780)
        # self.setFixedSize(480, 780)
        # self.center()
        self.show()

        self.masterLayout = QVBoxLayout()
        self.masterLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.masterLayout)

        self.masterBody = QVBoxLayout()
        self.masterBody.setContentsMargins(5, 5, 5, 5)

        self.threads = []
        self.locationStack = []
        self.locationCursor = -1

        self.location_prev = []
        self.location_next = []

        self.start = QPoint(0, 0)
        self.pressing = False
        self.drag = False

    def changeLayout(self, func, layout, button):
        if self.currentLayout:
            self.layoutData[self.currentLayout].hide()

        self.currentLayout = layout

        if not self.layoutData.get(layout):
            frame = QFrame()
            frame.setLayout(layout)
            self.layouts.addWidget(frame)
            self.layoutData[layout] = frame
        else:
            self.layoutData[layout].show()

        if self.prevbutton:
            self.prevbutton.setStyleSheet(
                self.prevbutton.styleSheet()
                + "background-color: #fafafa; color: black;"
            )
            self.prevbutton.invertIcon()

        self.prevbutton = button

        button.setStyleSheet(
            button.styleSheet() + "background-color: black; color: #fafafa;"
        )
        button.invertIcon()

        self.loc_prev.addItem(str(func))
        self.location_prev.append(func)

    def initLayout(self):
        self.widnowTitleWidget = QWidget()
        self.widnowTitleWidget.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
        self.windowTitleLayout = QHBoxLayout()
        self.widnowTitleWidget.setLayout(self.windowTitleLayout)
        self.windowTitleLayout.setContentsMargins(0, 0, 0, 0)
        self.masterLayout.addWidget(self.widnowTitleWidget)

        self.masterLayout.addLayout(self.masterBody)

        self.layouts = QVBoxLayout()
        self.currentLayout = None
        self.currentLayoutFrame = None
        self.masterBody.addLayout(self.layouts)

        self.prevbutton = None

        self.layoutData = {}

        self.footerLayout = QHBoxLayout()
        self.masterBody.addStretch()
        self.masterBody.addLayout(self.footerLayout)

        self.layoutMain = QVBoxLayout()
        self.layoutSingle = QVBoxLayout()
        self.layoutPlaylist = QVBoxLayout()
        self.layoutSearch = QVBoxLayout()
        self.layoutSetting = QVBoxLayout()

    # Part of code for reloading the windows
    def timer_terminate(self):
        if open("terminate.txt", "r").read() == "1":
            print("Terminating... ")
            self.terminate()
        open("pos.txt", "w").write(f"{self.pos().x()}, {self.pos().y()}")
        open("size.txt", "w").write(f"{self.size().width()}, {self.size().height()}")

    def terminate(self):
        open("terminate.txt", "w").write("0")
        os.execl(sys.executable, sys.executable, '"{}"'.format(*sys.argv))

    # Reloader code ends

    # self.mainAppBar.addStretch()

    # self.icon = QLabel()
    # self.mainAppBar.addWidget(self.icon)
    # self.icon.setScaledContents(True)
    # self.icon.setPixmap(QPixmap("Profile.png"))
    # self.icon.setFixedSize(32, 32)

    def render_main_body(self):
        self.body = QVBoxLayout()
        self.body.setContentsMargins(5, 5, 5, 5)
        self.layoutMain.addLayout(self.body)

        self.menu = QHBoxLayout()
        self.body.addLayout(self.menu)

        class MenuWidget(QGroupBox):
            def __init__(
                self,
            ):
                super().__init__()
                self.setFixedHeight(int(self.width() / 2.5))
                self.setStyleSheet("border: none; border-radius: 5px;")

                self.Layout_M = QVBoxLayout()
                self.setLayout(self.Layout_M)

                self.Image = QPushButton()
                self.Image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.Layout_M.addWidget(self.Image)

                self.MainText = QLabel()
                self.Layout_M.addWidget(self.MainText)
                self.MainText.setText("MainText")
                self.MainText.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.MainText.setStyleSheet("font-size: 1rem; font-weight: bold;")

                self.SubText = QLabel("SubText")
                self.Layout_M.addWidget(self.SubText)
                self.SubText.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.SubText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            def setMainText(self, text):
                self.MainText.setText(text)

            def setSubText(self, text):
                self.SubText.setText(text)

            def setTextColor(self, color):
                self.MainText.setStyleSheet(
                    self.MainText.styleSheet() + "color: {}".format(color)
                )
                self.SubText.setStyleSheet(
                    self.SubText.styleSheet() + "color: {}".format(color)
                )

            def setColor(self, color):
                self.setStyleSheet(
                    self.styleSheet() + "background-color: {}".format(color)
                )

            def setIcon(self, icon):
                self.Image.setStyleSheet(
                    self.Image.styleSheet() + "border-image : url({});".format(icon)
                )

            def setIconColor(self, icon):
                self.Image.setStyleSheet(
                    self.Image.styleSheet() + "border-image : url({});".format(icon)
                )
                self.setColor(pick_color(icon))

        self.playlistMenu = MenuWidget()
        self.playlistMenu.setMainText("PlayList")
        self.playlistMenu.setSubText("0 playlist")
        self.playlistMenu.setTextColor("white")
        self.playlistMenu.setIconColor(C_Cover1)
        self.playlistMenu.Image.clicked.connect(self.on_nav_playlist_clicked)
        self.menu.addWidget(self.playlistMenu)

        self.singleMenu = MenuWidget()
        self.singleMenu.setMainText("Single")
        self.singleMenu.setSubText("0 song")
        self.singleMenu.setTextColor("white")
        self.singleMenu.setIconColor(C_Cover2)
        self.singleMenu.Image.clicked.connect(self.on_nav_single_clicked)
        self.menu.addWidget(self.singleMenu)

    def on_nav_main_clicked(self):
        self.changeLayout(self.on_nav_main_clicked, self.layoutMain, self.nav_main)

    def on_nav_search_clicked(self):
        self.changeLayout(
            self.on_nav_search_clicked, self.layoutSearch, self.nav_search
        )

    def on_nav_playlist_clicked(self):
        self.changeLayout(
            self.on_nav_playlist_clicked, self.layoutPlaylist, self.nav_playlist
        )

    def on_nav_single_clicked(self):
        self.changeLayout(
            self.on_nav_single_clicked, self.layoutSingle, self.nav_single
        )

    def on_nav_setting_clicked(self):
        self.changeLayout(
            self.on_nav_setting_clicked, self.layoutSetting, self.nav_setting
        )

    def btn_minimize_clicked(self):
        self.showMinimized()

    def btn_maximize_clicked(self):
        if self.isMaximized():
            self.showNormal()
            if self.windowTitleRenderMethod == "windows":
                self.btn_maximize.setIcon(QIcon(I_Maximize))
            elif self.windowTitleRenderMethod == "macos":
                pass
        else:
            self.showMaximized()
            if self.windowTitleRenderMethod == "windows":
                self.btn_maximize.setIcon(QIcon(I_Restore))
            elif self.windowTitleRenderMethod == "macos":
                pass

    def btn_close_clicked(self):
        self.close()

    def render_title(self):
        self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.windowTItleText = QLabel("Drox Music Player")

        self.windowTitleRenderMethod = "windows"
        if self.windowTitleRenderMethod == "windows":

            self.btn_minimize = QPushButton()
            self.btn_minimize.setIcon(QIcon(I_Minimize))
            self.btn_minimize.clicked.connect(self.btn_minimize_clicked)
            self.btn_maximize = QPushButton()
            self.btn_maximize.setIcon(QIcon(I_Maximize))
            self.btn_maximize.clicked.connect(self.btn_maximize_clicked)
            self.btn_close = QPushButton()
            self.btn_close.setIcon(QIcon(I_Close))
            self.btn_close.clicked.connect(self.btn_close_clicked)

            self.window_btns = [self.btn_minimize, self.btn_maximize, self.btn_close]
            for button in self.window_btns:
                self.windowTitleLayout.addWidget(button)
                button.setFixedSize(43, 28)
                button.setIconSize(QSize(15, 15))
                button.setStyleSheet(
                    """
                    QPushButton { background-color: rgba(0, 0, 0, 0.0); border: 0px; }
                    QPushButton:hover { background-color: rgba(0, 0, 0, 0.1); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.2); }
                    """
                )
        elif self.windowTitleRenderMethod == "macos":
            self.windowTitleLayout.addWidget(self.windowTItleText)
            self.windowTItleText.setStyleSheet(
                """
                QLabel {
                    color: white;
                    font-size: 1.2rem;
                    font-weight: bold;
                    background-color: rgba(0, 0, 0, 0.0);
                    border: 0px;
                }
                """
            )

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

        self.titlePos = self.windowTitleLayout.geometry()
        left, top, right, bottom = (
            0,
            0,
            self.titlePos.right() + self.titlePos.left(),
            self.titlePos.bottom() + self.titlePos.top(),
        )
        posX, posY = event.pos().x(), event.pos().y()

        # print

        if (left < posX < right) and (top < posY < bottom):
            self.drag = True

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
        self.drag = False

    def mouseMoveEvent(self, event):

        if self.drag:
            if self.pressing:
                self.end = self.mapToGlobal(event.pos())
                self.movement = self.end - self.start
                self.setGeometry(
                    self.mapToGlobal(self.movement).x(),
                    self.mapToGlobal(self.movement).y(),
                    self.width(),
                    self.height(),
                )
                self.start = self.end

    def setRndBg(self, widget):
        widget.setStyleSheet(
            widget.styleSheet()
            + "background-color: {}".format(
                "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            )
        )

    def addResult(self, entry):
        url = entry["thumbnails"][0]["url"]
        text = entry["title"]
        subtext = entry["channel"]["name"]

        duration = entry["duration"]

        item = QListWidgetItem()
        item.setIcon(QIcon(I_Hourglass))
        item.setSizeHint(QSize(0, 70))

        vwidget = QWidget()
        vline = QVBoxLayout()
        vwidget.setLayout(vline)
        vline.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        line1cont = QHBoxLayout()
        line1cont.setAlignment(Qt.AlignmentFlag.AlignLeft)

        line2cont = QHBoxLayout()
        line2cont.setAlignment(Qt.AlignmentFlag.AlignLeft)

        line1 = QLabel(text)
        line1cont.addWidget(line1)
        line1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # line1.setAlignment(Qt.AlignmentFlag.AlignTop)

        item.setToolTip(line1.text())
        line1.setWordWrap(True)
        line1.setStyleSheet("font-size: 13px;")

        line2 = QLabel(subtext)
        line2cont.addWidget(line2)
        line2.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        line2.setStyleSheet("font-size: 10px; color: #999;")

        tag = QLabel("LIVE NOW")
        tag.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        tag.setStyleSheet(
            "font-size: 10px; color: #ff4e45; border: 1px solid #ff4e45; border-radius: 1px;"
        )

        if duration == None:
            line2cont.addWidget(tag)

        vline.addLayout(line1cont)
        vline.addLayout(line2cont)

        self.searchResult.addItem(item)
        self.searchResult.setItemWidget(item, vwidget)

    def if_repaint(self):
        if self.searchResult.paintingActive() == False:
            # print(self.searchResult.paintingActive())
            self.searchResult.repaint()

    def setResultListIcon(self, item, icon):
        item.setIcon(icon)

    def call_search_end(self):
        self.on_search_inputted()

    def addResultByList(self, list: list):
        for entry in list:
            self.addResult(entry)

    def on_search_inputted(self):
        input = self.searchInput.text()
        if input.strip() == "":
            return

        for i in range(self.searchResult.count()):
            self.searchResult.takeItem(0)

        self.sr = search_10(input)
        self.addResultByList(self.sr.result()["result"])

    def update_search(self, value):
        if value == self.searchResult.verticalScrollBar().maximum():
            self.sr.next()
            self.addResultByList(self.sr.result()["result"])

    def render_search_body(self):
        self.searchBody = QVBoxLayout()
        self.layoutSearch.addLayout(self.searchBody)
        self.searchBody.setContentsMargins(5, 5, 5, 5)

        self.searchInputLine = QHBoxLayout()
        self.searchInputLine.setContentsMargins(2, 2, 2, 2)

        self.searchBody.addLayout(self.searchInputLine)

        self.searchInput = QLineEdit("lofi")
        self.searchInputLine.addWidget(self.searchInput)
        self.searchInput.setPlaceholderText("Search")
        self.searchInput.setStyleSheet(
            "border: none; border-radius: 5px; background-color: #EEEEEE; padding: 7.5px;"
        )
        self.searchInput.addAction(QIcon(I_Search), QLineEdit.LeadingPosition)
        self.searchInput.returnPressed.connect(self.call_search_end)

        self.searchButton = QPushButton("")
        self.searchInputLine.addWidget(self.searchButton)
        self.searchButton.setIcon(QIcon(I_Search))
        self.searchButton.setStyleSheet(
            "border: none; border-radius: 5px; background-color: #EEEEEE; padding: 10px;"
        )
        self.searchButton.clicked.connect(self.on_search_inputted)

        self.searchResult = QListWidget()
        # self.searchResult.paintingActive()
        self.searchBody.addWidget(self.searchResult)
        self.searchResult.verticalScrollBar().valueChanged.connect(self.update_search)
        self.searchResult.setFixedHeight(self.height())

        # self.searchResult.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.searchResult.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.searchResult.setStyleSheet(
            """
            QListWidget{
                border: none;
                border-radius: 5px;
                background: transparent;

            }
            QListWidget QScrollBar{
                width: 4px;
                background: #e4e4e4;
                border-radius: 5px;
                margin: 0px;
            }
            QListWidget QScrollBar::handle:vertical {
                background-color: #d4d4d4;
                border-radius: 10px;
            }
            QListWidget QScrollBar::add-line:vertical {
                height: 0px;
            }
            QListWidget QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QListView::item{
                border-bottom: 1px solid #ededed;
            }
            QListView::item:selected{
                selection-color: black;
                selection-background-color: black;
            }
        """
        )
        self.searchResult.setIconSize(QSize(55, 55))

        self.searchButton.click()

    def render_loc_viewer(self):
        self.loc = QHBoxLayout()

        self.loc_prev = QListWidget()
        self.loc.addWidget(self.loc_prev)
        self.loc_next = QListWidget()
        self.loc.addWidget(self.loc_next)

        self.layoutSetting.addLayout(self.loc)

    def handle_window_released(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.XButton1:
            try:
                self.loc_next.addItem(str(self.location_prev[-1]))
                self.location_next.append(self.location_prev[-1])
                self.loc_prev.takeItem(self.loc_prev.count() - 1)
                self.location_prev.pop()

                self.location_prev[-1]()
                self.loc_prev.takeItem(self.loc_prev.count() - 1)
                self.location_prev.pop()
            except:
                pass
        elif event.button() == Qt.MouseButton.XButton2:
            try:
                self.location_next[-1]()
                self.loc_next.takeItem(self.loc_next.count() - 1)
                self.location_next.pop()
            except:
                pass
        elif event.button() == Qt.MouseButton.MiddleButton:
            try:
                pass
                self.loc_prev.clear()
                self.loc_next.clear()
                self.location_prev.clear()
                self.location_next.clear()
            except:
                pass
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DroxMain()
    sys.exit(app.exec_())
