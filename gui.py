from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os

from MyPicker import pick_color
from MyAssets import *
from MyYoutube import *

from MyQtWidgets import *
from MyWidgets import *
from MyThreads import *
from MyObjects import *


class DroxWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui_init_window()
        self.ui_init_vars()
        self.ui_init_layouts()

    def ui_init_window(self):
        open("terminate.txt", "w").write("0")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ui_terminate)
        self.timer.start(500)

        x, y = open("pos.txt", "r").read().split(", ")
        self.move(int(x), int(y))

        self.setWindowTitle("Drox")
        self.setWindowIcon(QIcon("library_music.svg"))
        width = 360
        self.window_size = QSize(width, int(width * 18 / 9))
        self.setFixedSize(self.window_size)
        self.show()

        self.ui_make_round()

    def ui_init_vars(self):
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

    def ui_make_round(self):
        radius = 40.0
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(mask)

    def ui_change_layout(self, func, layout, button):
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

        self.Qlocation_prev.addItem(str(func))
        self.location_prev.append(func)

    def ui_init_layouts(self):
        self.widnowTitleWidget = QWidget()
        # self.widnowTitleWidget.setStyleSheet("background-color: rgba(0, 0, 0, 0.1);")
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

        self.footerLayout = QVBoxLayout()
        self.masterBody.addStretch()
        self.masterBody.addLayout(self.footerLayout)

        self.layoutMain = QVBoxLayout()
        self.layoutSingle = QVBoxLayout()
        self.layoutPlaylist = QVBoxLayout()
        self.layoutSearch = QVBoxLayout()
        self.layoutSetting = QVBoxLayout()

        self.render_title()
        self.render_footer()

        self.render_main_header()
        self.render_main_body()

        self.render_single_header()

        self.render_playlist_header()

        self.render_search_header()
        self.render_search_body()

        self.render_location_viewer()

        self.ui_change_layout(
            self.on_nav_search_clicked, self.layoutSearch, self.nav_search
        )

    def ui_terminate(self):
        if open("terminate.txt", "r").read() == "1":
            open("terminate.txt", "w").write("0")
            os.execl(sys.executable, sys.executable, '"{}"'.format(*sys.argv))
        open("pos.txt", "w").write(f"{self.pos().x()}, {self.pos().y()}")
        open("size.txt", "w").write(f"{self.size().width()}, {self.size().height()}")

    def win_minimize(self):
        self.showMinimized()

    def win_maximize(self):
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

    def win_close(self):
        self.close()

    def on_nav_main_clicked(self):
        self.ui_change_layout(self.on_nav_main_clicked, self.layoutMain, self.nav_main)

    def on_nav_search_clicked(self):
        self.ui_change_layout(
            self.on_nav_search_clicked, self.layoutSearch, self.nav_search
        )

    def on_nav_playlist_clicked(self):
        self.ui_change_layout(
            self.on_nav_playlist_clicked, self.layoutPlaylist, self.nav_playlist
        )

    def on_nav_single_clicked(self):
        self.ui_change_layout(
            self.on_nav_single_clicked, self.layoutSingle, self.nav_single
        )

    def on_nav_setting_clicked(self):
        self.ui_change_layout(
            self.on_nav_setting_clicked, self.layoutSetting, self.nav_setting
        )

    def render_main_header(self):
        self.mainAppBar = AppBar()
        self.layoutMain.addLayout(self.mainAppBar)

        self.mainAppBarText = AppBarTitle("Drox Music Player")
        self.mainAppBar.addWidget(self.mainAppBarText)

        # self.mainAppBar.addStretch()

        self.icon = QLabel()
        # self.mainAppBar.addWidget(self.icon)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(QPixmap("Profile.png"))
        self.icon.setFixedSize(32, 32)

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
                self.setFixedHeight(int(self.width() / 3.25))
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
                self.SubText.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

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

    def render_title(self):
        # self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.windowTitleLayout.setContentsMargins(30, 15, 30, 15)

        self.windowTItleText1 = QLabel("09:42")
        self.windowTItleText2 = QLabel("100%")
        self.windowTItleText1.setStyleSheet("background-color: 0")
        self.windowTItleText2.setStyleSheet("background-color: 0")
        self.windowTitleLayout.addWidget(self.windowTItleText1)
        self.windowTitleLayout.addStretch()
        self.windowTitleLayout.addWidget(self.windowTItleText2)

        self.windowTitleRenderMethod = "windows"
        self.render_traffic_light = False
        if self.render_traffic_light:
            if self.windowTitleRenderMethod == "windows":

                self.btn_minimize = QPushButton()
                self.btn_minimize.setIcon(QIcon(I_Minimize))
                self.btn_minimize.clicked.connect(self.win_minimize)
                self.btn_maximize = QPushButton()
                self.btn_maximize.setIcon(QIcon(I_Maximize))
                self.btn_maximize.clicked.connect(self.win_maximize)
                self.btn_close = QPushButton()
                self.btn_close.setIcon(QIcon(I_Close))
                self.btn_close.clicked.connect(self.win_close)

                self.window_btns = [
                    self.btn_minimize,
                    self.btn_maximize,
                    self.btn_close,
                ]
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

    def render_footer(self):
        self.footer = QHBoxLayout()
        self.footerLayout.addLayout(self.footer)
        self.footer.setContentsMargins(5, 5, 5, 0)
        # self.layout.(self.footer)

        self.footer_itemList = []

        self.nav_main = NavButton("Main")
        self.nav_main.setIcon(QIcon(I_Home))
        self.nav_main.setInvertIcon(QIcon(II_Home))
        self.footer_itemList.append(self.nav_main)
        self.footer.addWidget(self.nav_main)
        self.nav_main.clicked.connect(self.on_nav_main_clicked)

        self.nav_search = NavButton("Search")
        self.nav_search.setIcon(QIcon(I_Search))
        self.nav_search.setInvertIcon(QIcon(II_Search))
        self.footer_itemList.append(self.nav_search)
        self.footer.addWidget(self.nav_search)
        self.nav_search.clicked.connect(self.on_nav_search_clicked)

        self.nav_playlist = NavButton("PlayList")
        self.nav_playlist.setIcon(QIcon(I_Playlist))
        self.nav_playlist.setInvertIcon(QIcon(II_Playlist))
        self.footer_itemList.append(self.nav_playlist)
        self.footer.addWidget(self.nav_playlist)
        self.nav_playlist.clicked.connect(self.on_nav_playlist_clicked)

        self.nav_single = NavButton("Single")
        self.nav_single.setIcon(QIcon(I_Single))
        self.nav_single.setInvertIcon(QIcon(II_Single))
        self.footer_itemList.append(self.nav_single)
        self.footer.addWidget(self.nav_single)
        self.nav_single.clicked.connect(self.on_nav_single_clicked)

        self.nav_setting = NavButton("Setting")
        self.nav_setting.setIcon(QIcon(I_Setting))
        self.nav_setting.setInvertIcon(QIcon(II_Setting))
        self.footer_itemList.append(self.nav_setting)
        self.footer.addWidget(self.nav_setting)
        self.nav_setting.clicked.connect(self.on_nav_setting_clicked)

        self.controller = QHBoxLayout()
        self.footerLayout.addLayout(self.controller)

        self.bar = QPushButton()
        self.bar.setFixedSize(int(self.width() / 3), 5)

        self.bar.setStyleSheet("background-color: black; border-radius: 5px;")
        self.bar.clicked.connect(self.win_minimize)
        self.controller.addWidget(self.bar)

    def render_search_header(self):
        self.searchAppBar = AppBar()
        self.layoutSearch.addLayout(self.searchAppBar)

        self.searchAppBarText = AppBarTitle("Search")
        self.searchAppBar.addWidget(self.searchAppBarText)

    def f_search_add_result(self, entry):
        url = entry["thumbnails"][0]["url"]
        text = entry["title"]
        subtext = entry["channel"]["name"]

        duration = entry["duration"]

        item = QListWidgetItem()
        item.setIcon(QIcon(I_Hourglass))
        item.setSizeHint(QSize(0, 70))

        thread = LazyIcon(
            self.searchResult,
            item,
            url,
        )
        thread.repaint.connect(self.f_search_repaint_list)
        thread.setResultListIcon.connect(self.f_search_item_icon)
        self.threads.append(thread)
        self.threads[-1].start()

        vwidget = QWidget()
        # vwidget.setStyleSheet("background-color: red;")
        vline = QVBoxLayout()
        vwidget.setLayout(vline)
        vline.setAlignment(Qt.AlignmentFlag.AlignTop)

        line1cont = QHBoxLayout()
        line1cont.setAlignment(Qt.AlignmentFlag.AlignLeft)

        line2cont = QHBoxLayout()
        line2cont.setAlignment(Qt.AlignmentFlag.AlignLeft)

        line1 = QLabel(text)
        # line1.setStyleSheet("")
        line1cont.addWidget(line1)
        line1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
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

    def f_search_repaint_list(self):
        if self.searchResult.paintingActive() == False:
            self.searchResult.repaint()

    def f_search_item_icon(self, item, icon):
        item.setIcon(icon)

    def f_search_result_by_list(self, list: list):
        for entry in list:
            self.f_search_add_result(entry)

    def f_on_search_input(self):
        input = self.searchInput.text()
        if input.strip() == "":
            return

        for i in range(self.searchResult.count()):
            self.searchResult.takeItem(0)

        self.sr = search_10(input)
        self.f_search_result_by_list(self.sr.result()["result"])

    def f_search_update(self, value):
        if value == self.searchResult.verticalScrollBar().maximum():
            self.sr.next()
            self.f_search_result_by_list(self.sr.result()["result"])

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
            "border: none; border-radius: 2px; background-color: #EEEEEE; padding: 7.5px;"
        )
        self.searchInput.addAction(QIcon(I_Search), QLineEdit.LeadingPosition)
        self.searchInput.returnPressed.connect(self.f_on_search_input)

        # self.searchButton = QPushButton("")
        # self.searchInputLine.addWidget(self.searchButton)
        # self.searchButton.setIcon(QIcon(I_Search))
        # self.searchButton.setStyleSheet(
        # "border: none; border-radius: 5px; background-color: #EEEEEE; padding: 10px;"
        # )
        # self.searchButton.clicked.connect(self.on_search_input)

        self.searchResult = QListWidget()
        # self.searchResult.paintingActive()
        self.searchBody.addWidget(self.searchResult)
        self.searchResult.verticalScrollBar().valueChanged.connect(self.f_search_update)
        self.searchResult.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        # self.searchResult.setFixedHeight(self.height())

        self.searchResult.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.searchResult.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.searchResult.setStyleSheet(
            """
            QListWidget{
                border: none;
                border-radius: 5px;
                background: transparent;

            }
            QListWidget QScrollBar{
                width: 0px;
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

    def render_location_viewer(self):
        self.Qlocations = QHBoxLayout()

        self.Qlocation_prev = QListWidget()
        self.Qlocations.addWidget(self.Qlocation_prev)
        self.Qlocation_next = QListWidget()
        self.Qlocations.addWidget(self.Qlocation_next)

        self.layoutSetting.addLayout(self.Qlocations)

    def render_playlist_header(self):
        self.playlistAppBar = AppBar()
        self.layoutPlaylist.addLayout(self.playlistAppBar)

        self.playlistAppBarText = AppBarTitle("Playlist")
        self.playlistAppBar.addWidget(self.playlistAppBarText)

    def render_single_header(self):
        self.singleAppBar = AppBar()
        self.layoutSingle.addLayout(self.singleAppBar)

        self.singleAppBarText = AppBarTitle("Single")
        self.singleAppBar.addWidget(self.singleAppBarText)

    def e_window_released(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.XButton1:
            try:
                self.Qlocation_next.addItem(str(self.location_prev[-1]))
                self.location_next.append(self.location_prev[-1])
                self.Qlocation_prev.takeItem(self.Qlocation_prev.count() - 1)
                self.location_prev.pop()

                self.location_prev[-1]()
                self.Qlocation_prev.takeItem(self.Qlocation_prev.count() - 1)
                self.location_prev.pop()
            except:
                pass
        elif event.button() == Qt.MouseButton.XButton2:
            try:
                self.location_next[-1]()
                self.Qlocation_next.takeItem(self.Qlocation_next.count() - 1)
                self.location_next.pop()
            except:
                pass
        elif event.button() == Qt.MouseButton.MiddleButton:
            try:
                pass
                self.location_prev.clear()
                self.location_next.clear()
                self.Qlocation_prev.clear()
                self.Qlocation_next.clear()
            except:
                pass
        else:
            pass

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

    def resizeEvent(self, event):
        self.ui_make_round()


if __name__ == "__main__":

    import ctypes

    myappid = "mycompany.myproduct.subproduct.version"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    palatte = QPalette()
    palatte.setColor(QPalette.Background, QColor(255, 255, 255))
    # palatte.setColor(QPalette.Background, QColor(169, 98, 95))
    app.setPalette(palatte)
    # app.setPalette(QPalette.setColor(QPalette.Background, QColor(169, 98, 95)))
    app.setFont(QFont("Pretendard", 10))

    # app.setQuitOnLastWindowClosed(False)

    dw = DroxWidget()

    mouse_observer = MouseObserver(dw.windowHandle())
    mouse_observer.released.connect(dw.e_window_released)

    sys.exit(app.exec_())
