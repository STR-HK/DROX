import sys
from types import ModuleType


class MockModule(ModuleType):
    def __init__(self, module_name, module_doc=None):
        ModuleType.__init__(self, module_name, module_doc)
        if "." in module_name:
            package, module = module_name.rsplit(".", 1)
            get_mock_module(package).__path__ = []
            setattr(get_mock_module(package), module, self)

    def _initialize_(self, module_code):
        self.__dict__.update(module_code(self.__name__))
        self.__doc__ = module_code.__doc__


def get_mock_module(module_name):
    if module_name not in sys.modules:
        sys.modules[module_name] = MockModule(module_name)
    return sys.modules[module_name]


def modulize(module_name, dependencies=[]):
    for d in dependencies:
        get_mock_module(d)
    return get_mock_module(module_name)._initialize_


##===========================================================================##


@modulize("MyPicker")
def _MyPicker(__name__):
    ##----- Begin MyPicker.py ----------------------------------------------------##
    import scipy, scipy.cluster, scipy.misc
    from PIL import Image
    import numpy as np
    import binascii
    import json
    import os

    cachePath = "cache.json"

    def load_cache() -> dict:
        """
        Loads the dictionary from the cache file.

        :return: A dictionary of the caches.
        """
        return json.loads(open(cachePath, "r").read())

    def make_cachefile_if_not_exist() -> None:
        """
        Make the cache file if it doesn't exist.

        :return: None
        """
        if not os.path.isfile(cachePath):
            open(cachePath, "w").write(json.dumps({}))

    def is_cache_exists(path) -> bool:
        """
        Check if the cache file exists.

        :param path: Path to an image.
        :return: True if the cache file exists.
        """
        try:
            if load_cache()[path]:
                return True
        except:
            return False

    def get_color_from_cache(path) -> str:
        """
        Get the color from the cache.

        :param path: Path to an image.
        :return: A hex color string.
        """
        return load_cache()[path]

    def store_color_to_cache(path, color) -> None:
        """
        Store the color to the cache.

        :param path: Path to an image.
        :param color: A hex color string.
        :return: None
        """
        json_data = load_cache()
        json_data[path] = color
        open(cachePath, "w").write(json.dumps(json_data))

    def pick_color(path, NUM_CLUSTERS=7, USE_CACHE=True) -> str:
        """
        Pick the main color in an image from its path.

        :param path: Path to an image.
        :param NUM_CLUSTERS = 7: Number of clusters to use.
        :param USE_CACHE = True: Whether to use the cache.

        :return: A hex color string.
        """
        make_cachefile_if_not_exist()
        if is_cache_exists(path) and USE_CACHE:
            return get_color_from_cache(path)
        else:
            im = Image.open(path)
            im = im.resize((150, 150))  # optional, to reduce time
            ar = np.asarray(im)
            shape = ar.shape
            ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
            # print("finding clusters")
            codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
            # print("cluster centres:\n", codes)
            vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
            counts, bins = np.histogram(vecs, len(codes))  # count occurrences
            index_max = np.argmax(counts)  # find most frequent
            peak = codes[index_max]
            colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode("ascii")
            # print("most frequent is %s (#%s)" % (peak, colour))
            colour = "#" + colour[0:6]
            store_color_to_cache(path, colour)
            return colour

    def invert_color(HEX_VALUE, BLACK_WHITE=False):
        """
        Invert the color of a hex value.

        :param HEX_VALUE: A hex color string. (e.g. #XXXXXX)
        :param BLACK_WHITE: Whether to return only black and white.
        :return: A hex color string. (e.g. #XXXXXX)

        """
        if HEX_VALUE[0] == "#":
            HEX_VALUE = HEX_VALUE[1:]

        if len(HEX_VALUE) == 3:
            HEX_VALUE = (
                HEX_VALUE[0]
                + HEX_VALUE[0]
                + HEX_VALUE[1]
                + HEX_VALUE[1]
                + HEX_VALUE[2]
                + HEX_VALUE[2]
            )

        r, g, b = (
            int(HEX_VALUE[0:2], 16),
            int(HEX_VALUE[2:4], 16),
            int(HEX_VALUE[4:6], 16),
        )

        if BLACK_WHITE:
            if (r * 0.299 + g * 0.587 + b * 0.114) > 186:
                return "#000000"
            else:
                return "#FFFFFF"

        r = str(format(255 - r, "x")).zfill(2)
        g = str(format(255 - g, "x")).zfill(2)
        b = str(format(255 - b, "x")).zfill(2)
        return "#" + r + g + b

    ##----- End MyPicker.py ------------------------------------------------------##
    return locals()


@modulize("MyAssets")
def _MyAssets(__name__):
    ##----- Begin MyAssets.py ----------------------------------------------------##

    P_ICON = "./icon/"

    P_ICON_MAIN = P_ICON + "/main/"

    P_COVER = P_ICON_MAIN + "/cover/"
    C_Cover1 = P_COVER + "Cover1.png"
    C_Cover2 = P_COVER + "Cover2.png"
    C_Winter = P_COVER + "Winter.jpg"
    C_Winter2 = P_COVER + "Winter2.jpg"
    C_Winter3 = P_COVER + "Winter3.jpg"

    C_LovelyWinter = P_COVER + "lovely.jpg"
    C_BlackWinter = P_COVER + "BlackWinter.jpg"
    C_HighteenWinter = P_COVER + "Highteen.jpg"
    C_SparkleWinter = P_COVER + "Sparkle.webp"

    C_Heoney = P_COVER + "Heoney.jpg"
    C_M60_UCD1 = P_COVER + "M60-UCD1.jpg"
    C_SultangYeeaeyo = P_COVER + "SultangYeeaeyo.jpg"
    C_init = P_COVER + "init.png"
    C_dust = P_COVER + "dust.png"

    P_FOOTER = P_ICON_MAIN + "/footer/"
    I_Home = P_FOOTER + "home.svg"
    II_Home = P_FOOTER + "home_i.svg"
    I_Search = P_FOOTER + "search.svg"
    II_Search = P_FOOTER + "search_i.svg"
    I_Playlist = P_FOOTER + "playlist.svg"
    II_Playlist = P_FOOTER + "playlist_i.svg"
    I_Single = P_FOOTER + "note.svg"
    II_Single = P_FOOTER + "note_i.svg"
    I_Setting = P_FOOTER + "settings.svg"
    II_Setting = P_FOOTER + "settings_i.svg"
    I_Hourglass = P_FOOTER + "hourglass.svg"
    II_Hourglass = P_FOOTER + "hourglass_i.svg"

    P_WINDOW = P_ICON + "/window/"
    I_Close = P_WINDOW + "chrome-close.svg"
    I_Minimize = P_WINDOW + "chrome-minimize.svg"
    I_Maximize = P_WINDOW + "chrome-maximize.svg"
    I_Restore = P_WINDOW + "chrome-restore.svg"

    P_MACOS = P_ICON + "/macos/"
    I_TR_Close = P_MACOS + "Close_Button.svg"
    I_TR_Close_Active = P_MACOS + "Close_Button_Active.svg"
    I_TR_Close_Hover = P_MACOS + "Close_Button_Hover.svg"
    I_TR_Minimize = P_MACOS + "Minimize_Button.svg"
    I_TR_Minimize_Active = P_MACOS + "Minimize_Button_Active.svg"
    I_TR_Minimize_Hover = P_MACOS + "Minimize_Button_Hover.svg"
    I_TR_Maximize = P_MACOS + "Maximize_Button.svg"
    I_TR_Maximize_Active = P_MACOS + "Maximize_Button_Active.svg"
    I_TR_Maximize_Hover = P_MACOS + "Maximize_Button_Hover.svg"

    P_PROFILE = P_ICON_MAIN + "/profile/"
    R_Profile = P_PROFILE + "Profile.png"
    R_Mention = P_PROFILE + "Mention.jpg"

    P_ANI = P_ICON_MAIN + "/ani/"
    A_Loading = P_ANI + "Spinner.svg"

    kaiyu = P_ICON + "kaiyu.jpg"

    # for var in dir():
    #     if not var.startswith("__"):
    #         globals()[var] = path.abspath(var)

    ##----- End MyAssets.py ------------------------------------------------------##
    return locals()


@modulize("MyYoutube")
def _MyYoutube(__name__):
    ##----- Begin MyYoutube.py ---------------------------------------------------##
    from youtubesearchpython import VideosSearch

    def search_10(query):
        result = VideosSearch(query)
        # pyperclip.copy(str(result.result()))

        # print(result.result()[0])
        return result
        # return YoutubeSearch(query, max_results=10).to_dict()

    # result = search_10("lofi")

    # pyperclip.copy(str(result.result()))

    # result.next()
    # print(result.result())

    ##----- End MyYoutube.py -----------------------------------------------------##
    return locals()


@modulize("MyQtWidgets")
def _MyQtWidgets(__name__):
    ##----- Begin MyQtWidgets.py -------------------------------------------------##
    # from PyQt5.QtWidgets import *  # type: ignore
    # from PyQt5.QtGui import *  # type: ignore
    # from PyQt5.QtCore import *  # type: ignore

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

    class DPushButton(QPushButton):
        def __init__(self, *args, **kwargs):
            super(QPushButton, self).__init__(*args, **kwargs)
            self.setCursor(Qt.PointingHandCursor)

            # self.setAutoRepeat(True)
            # self.setAutoRepeatDelay(1000)
            # self.setAutoRepeatInterval(1000)
            # self.clicked.connect(self.handleClicked)
            # self._state = 0

            filter = ButtonHoverWatcher(self)
            self.installEventFilter(filter)

        def handleClicked(self):
            if self.isDown():
                if self._state == 0:
                    self._state = 1
                    self.setAutoRepeatInterval(50)
                    print("press")
                else:
                    print("repeat")
            elif self._state == 1:
                self._state = 0
                self.setAutoRepeatInterval(1000)
                print("release")
            else:
                print("click")

    class QVBoxLayout(QVBoxLayout):
        def __init__(self, *args, **kwargs):
            super(QVBoxLayout, self).__init__(*args, **kwargs)
            self.setAlignment(Qt.AlignmentFlag.AlignTop)

    ##----- End MyQtWidgets.py ---------------------------------------------------##
    return locals()


@modulize("SvgEditor")
def _SvgEditor(__name__):
    ##----- Begin SvgEditor.py ---------------------------------------------------##
    from lxml import etree

    # from PyQt5.QtWidgets import *  # type: ignore
    # import sys
    # from PyQt5.QtGui import *  # type: ignore

    def change_color(path, color):
        tree = etree.parse(path)
        root = tree.getroot()
        root.set("fill", color)
        # root.set("height", "28")
        # root.set("width", "28")
        # tree.write(path, pretty_print=True)
        xml = etree.tostring(root, pretty_print=True)
        return xml

    ##----- End SvgEditor.py -----------------------------------------------------##
    return locals()


@modulize("MyColors")
def _MyColors(__name__):
    ##----- Begin MyColors.py ----------------------------------------------------##
    ACCENT_COLOR = "#731D2C"
    ACCENT_COLOR_LIGHT = "#902437"  # 25% Lighter

    ##----- End MyColors.py ------------------------------------------------------##
    return locals()


@modulize("MyWidgets")
def _MyWidgets(__name__):
    ##----- Begin MyWidgets.py ---------------------------------------------------##

    # from PyQt5.QtWidgets import *  # type: ignore # type: ignore
    # from PyQt5.QtCore import *  # type: ignore # type: ignore
    #
    # from PyQt5.QtGui import *  # type: ignore
    #
    # from MyPicker import *  # type: ignore
    # import SvgEditor
    #
    # from MyColors import *  # type: ignore

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
                pix.loadFromData(SvgEditor.hange_color(self.icon_, "gray"))

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
            self.setStyleSheet(
                self.styleSheet() + "background-color: {};".format(color)
            )

        def setIcon(self, icon):
            self.Image.setIcon(icon)
            self.setBgColor(pick_color(icon))
            self.setTextColor(
                invert_color(HEX_VALUE=pick_color(icon), BLACK_WHITE=True)
            )

    ##----- End MyWidgets.py -----------------------------------------------------##
    return locals()


@modulize("MyThreads")
def _MyThreads(__name__):
    ##----- Begin MyThreads.py ---------------------------------------------------##
    # from PyQt5.QtWidgets import *  # type: ignore
    # from PyQt5.QtCore import *  # type: ignore
    # from PyQt5.QtGui import *  # type: ignore
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

    ##----- End MyThreads.py -----------------------------------------------------##
    return locals()


@modulize("MyObjects")
def _MyObjects(__name__):
    ##----- Begin MyObjects.py ---------------------------------------------------##
    # from PyQt5.QtCore import *  # type: ignore

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

        def eventFilter(self, obj, event: QEvent):
            if self.window is obj:
                if event.type() == QEvent.MouseButtonPress:
                    self.pressed.emit(event)
                elif event.type() == QEvent.MouseMove:
                    self.moved.emit(event)
                elif event.type() == QEvent.MouseButtonRelease:
                    self.released.emit(event)
            return super().eventFilter(obj, event)

    ##----- End MyObjects.py -----------------------------------------------------##
    return locals()


@modulize("backend.youtube.downloader")
def _downloader(__name__):
    ##----- Begin backend/youtube/downloader.py ----------------------------------##
    from PyQt5.QtCore import QThread, pyqtSignal
    import yt_dlp as youtube_dl

    import os

    if os.path.isfile(
        "【Lyric MV】Zara 'Drowsiness' (Full Ver.) 【MementoMori】 [zqfMYAWDz20].mp4"
    ):
        os.remove(
            "【Lyric MV】Zara 'Drowsiness' (Full Ver.) 【MementoMori】 [zqfMYAWDz20].mp4"
        )

    class loggerOutputs:
        def error(msg):
            print("Captured Error: " + msg)

        def warning(msg):
            print("Captured Warning: " + msg)

        def debug(msg):
            # print("Captured Log: " + msg)
            pass

    class Downloader(QThread):
        finished = pyqtSignal(bool)
        updated = pyqtSignal(float)
        success = pyqtSignal(bool)

        def __init__(self, url="https://www.youtube.com/watch?v=zqfMYAWDz20"):
            super().__init__()
            self.url = url

            # self.run()

        def my_hook(self, dl_info):
            # print(dl_info)
            if dl_info["status"] == "downloading":
                percent = round(
                    float(dl_info["downloaded_bytes"])
                    / float(dl_info["total_bytes"])
                    * 100,
                    1,
                )
                # print(f"emitting {percent}")
                self.updated.emit(percent)
                # self.e.emit(f"{percent}%")
            # if dl_info["status"] == "finished":
            #     filename = dl_info["filename"]
            # print(filename)

        def download(self):
            ydl_opts = {
                # "format": "bestvideo[width<=1080]+bestaudio/best",
                "quiet": True,
                # "no_warnings": True,
                "progress_hooks": [self.my_hook],
                "logger": loggerOutputs,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.url)

            self.finished.emit(True)
            self.success.emit(True)

        def run(self):
            # self.update.emit(f"Downloading {self.url}")

            self.download()
            # self.finished.emit(True)

        def stop(self):
            pass
            print("ETA... Stopping")

    ##----- End backend/youtube/downloader.py ------------------------------------##
    return locals()


@modulize("gui")
def _gui(__name__):
    ##----- Begin gui.py ---------------------------------------------------------##
    # from PyQt5.QtWidgets import *  # type: ignore
    # from PyQt5.QtCore import *  # type: ignore
    # from PyQt5.QtGui import *  # type: ignore
    #
    # import sys
    # import os
    #
    # from MyPicker import invert_color, pick_color
    # from MyAssets import *  # type: ignore
    # from MyYoutube import *  # type: ignore
    #
    # from MyQtWidgets import *  # type: ignore
    # from MyWidgets import *  # type: ignore
    # from MyThreads import *  # type: ignore
    # from MyObjects import *  # type: ignore
    # from SvgEditor import change_color

    # ACCENT_COLOR = "#731D2C"
    # from MyColors import *  # type: ignore

    class MyPopup(QWidget):
        def __init__(self, parentPos):
            QWidget.__init__(self)

            self.setWindowFlags(Qt.WindowType.Popup)
            self.ui_make_round()

            self.setGeometry(parentPos.x() + 20, parentPos.y() + 30, 250, 600)
            self.setWindowOpacity(0.99)

            palatte = QPalette()
            palatte.setColor(QPalette.Background, QColor(237, 237, 237))
            self.setPalette(palatte)

        def resizeEvent(self, event):
            self.ui_make_round()

        def ui_make_round(self):
            # return
            radius = 15
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), radius, radius)
            mask = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)

    class ContextButton(QPushButton):
        def __init__(self, *args, **kwargs):
            super(QPushButton, self).__init__(*args, **kwargs)
            self.setStyleSheet(
                """
            QPushButton {
                background-color: transparent;
                text-align:left;
                padding-left: 10;
                padding-right: 10;
                padding-top: 2;
                padding-bottom: 2;
            }
            QPushButton:hover {
                background-color: """
                + ACCENT_COLOR_LIGHT
                + """;
                border: 0;
                color: white;
                border-radius: 5;
            }
            """
            )

    class WindowContext(QWidget):
        def __init__(self, mousePos):
            QWidget.__init__(self)

            self.setContentsMargins(0, 0, 0, 0)

            self.setWindowFlags(Qt.WindowType.Popup)
            self.setWindowOpacity(0.99)
            self.ui_make_round()

            palatte = QPalette()
            palatte.setColor(QPalette.Background, QColor(237, 237, 237))
            self.setPalette(palatte)

            self.contextLayout = QVBoxLayout()
            self.contextLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.contextLayout)

            self.move = ContextButton("Move")
            self.contextLayout.addWidget(self.move)
            self.move.clicked.connect(self.suicide)

            self.size = ContextButton("Size")
            self.contextLayout.addWidget(self.size)
            self.size.clicked.connect(self.suicide)

            self.minimize = ContextButton("Minimize")
            self.contextLayout.addWidget(self.minimize)
            self.minimize.clicked.connect(self.suicide)

            self.maximize = ContextButton("Maximize")
            self.contextLayout.addWidget(self.maximize)
            self.maximize.clicked.connect(self.suicide)

            line = QWidget()
            line.setFixedHeight(1)
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            line.setStyleSheet("background-color: lightgray")
            self.contextLayout.addWidget(line)

            self.close = ContextButton("Close")
            self.contextLayout.addWidget(self.close)
            self.close.clicked.connect(self.suicide)

            self.show()

            self.setGeometry(
                mousePos.x(),
                mousePos.y(),
                self.contextLayout.contentsRect().width(),
                self.contextLayout.contentsRect().height(),
            )

        def suicide(self):
            self.hide()

        def resizeEvent(self, event):
            self.ui_make_round()

        def ui_make_round(self):
            # return
            radius = 7
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), radius, radius)
            mask = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)

    class Context(QWidget):
        def __init__(self, mousePos):
            QWidget.__init__(self)

            self.setContentsMargins(0, 0, 0, 0)

            self.setWindowFlags(Qt.WindowType.Popup)
            self.setWindowOpacity(0.99)
            self.ui_make_round()

            palatte = QPalette()
            palatte.setColor(QPalette.Background, QColor(237, 237, 237))
            self.setPalette(palatte)

            self.contextLayout = QVBoxLayout()
            self.contextLayout.setContentsMargins(5, 5, 5, 5)
            self.setLayout(self.contextLayout)

            self.ctxM1 = ContextButton("New Folder")
            self.contextLayout.addWidget(self.ctxM1)
            self.ctxM1.clicked.connect(self.suicide)

            line = QWidget()
            line.setFixedHeight(1)
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            line.setStyleSheet("background-color: lightgray")
            self.contextLayout.addWidget(line)

            self.ctxM2 = ContextButton("Get Info")
            self.contextLayout.addWidget(self.ctxM2)
            self.ctxM2.clicked.connect(self.suicide)

            self.show()

            self.setGeometry(
                mousePos.x(),
                mousePos.y(),
                self.contextLayout.contentsRect().width(),
                self.contextLayout.contentsRect().height(),
            )

        def suicide(self):
            self.hide()

        def resizeEvent(self, event):
            self.ui_make_round()

        def ui_make_round(self):
            # return
            radius = 7
            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), radius, radius)
            mask = QRegion(path.toFillPolygon().toPolygon())
            self.setMask(mask)

    class ExampleContext(WindowContext):
        def __init__(self, pos):
            super(WindowContext, self).__init__(pos)
            self.first = ContextButton("Carbon Dioxide")
            self.contextLayout.addWidget(self.first)

    class DroxWidget(QWidget):
        def __init__(self):
            super().__init__()

            self.setWindowFlags(
                Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
            )
            # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

            effect = QGraphicsDropShadowEffect(self)
            effect.setBlurRadius(12)
            effect.setOffset(0, 0)
            effect.setColor(Qt.gray)
            # self.setGraphicsEffect(effect)

            self.ui_init_window()
            self.ui_init_vars()
            self.ui_init_layouts()

            tp = QShortcut(QKeySequence("Ctrl+Shift+Q"), self)
            tp.activated.connect(self.ui_teleport)

        def ui_teleport(self):
            # self.move(QCursor.pos())
            self.move(0, 0)

        def ui_init_window(self):
            open("terminate.txt", "w").write("0")

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.ui_terminate)
            self.timer.start(500)

            x, y = open("../../PycharmProjects/RodavClient/pos.txt", "r").read().split(", ")
            self.move(int(x), int(y))

            self.setWindowTitle("Drox")
            self.setWindowIcon(QIcon("icon.svg"))
            width = 360
            self.window_size = QSize(width, int(width * 18 / 9))
            self.setFixedSize(self.window_size)
            # self.resize(self.window_size)
            self.show()

            self.ui_make_round()

        def ui_init_vars(self):
            self.masterLayout = QVBoxLayout()
            self.masterLayout.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self.masterLayout)

            self.masterBody = QVBoxLayout()
            self.masterBody.setContentsMargins(5, 5, 5, 5)

            self.threads = []

            self.location_prev = []
            self.location_next = []

            self.start = QPoint(0, 0)
            self.pressing = False
            self.drag = False

        def ui_make_round(self):
            # return
            # radius = 35
            radius = 5
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
                self.prevbutton.invertIcon()

            self.prevbutton = button

            button.invertIcon()

            self.Qlocation_prev.addItem(str(func))
            self.location_prev.append(func)

        def ui_init_layouts(self):
            self.widnowTitleWidget = QWidget()
            self.windowTitleLayout = QHBoxLayout()
            self.widnowTitleWidget.setLayout(self.windowTitleLayout)
            self.windowTitleLayout.setContentsMargins(0, 0, 0, 0)
            self.masterLayout.addWidget(self.widnowTitleWidget)

            line = QWidget()
            line.setFixedHeight(1)
            line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            line.setStyleSheet("background-color: lightgray")
            self.masterLayout.addWidget(line)

            self.masterLayout.addLayout(self.masterBody)

            self.layouts = QVBoxLayout()
            self.layouts.setContentsMargins(0, 0, 0, 0)
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

            self.windowTitleRenderMethod = "macos"
            self.render_title()
            self.render_footer()

            self.render_main_header()
            self.render_main_body()

            self.render_single_header()

            self.render_playlist_header()

            self.render_search_header()
            self.render_search_body()

            self.render_location_viewer()

            # self.ui_change_layout(
            #     self.on_nav_search_clicked, self.layoutSearch, self.nav_search
            # )

            self.ui_change_layout(
                self.on_nav_playlist_clicked, self.layoutPlaylist, self.nav_playlist
            )

            # self.ui_change_layout(self.on_nav_main_clicked, self.layoutMain, self.nav_main)

        def ui_terminate(self):
            if open("terminate.txt", "r").read() == "1":
                open("terminate.txt", "w").write("0")
                os.execl(sys.executable, sys.executable, '"{}"'.format(*sys.argv))
            open("../../PycharmProjects/RodavClient/pos.txt", "w").write(f"{self.pos().x()}, {self.pos().y()}")
            open("size.txt", "w").write(
                f"{self.size().width()}, {self.size().height()}"
            )

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

        def on_nav_main_clicked(self, *args):
            self.ui_change_layout(
                self.on_nav_main_clicked, self.layoutMain, self.nav_main
            )

        def on_nav_search_clicked(self, *args):
            self.ui_change_layout(
                self.on_nav_search_clicked, self.layoutSearch, self.nav_search
            )

        def on_nav_playlist_clicked(self, *args):
            self.ui_change_layout(
                self.on_nav_playlist_clicked, self.layoutPlaylist, self.nav_playlist
            )

        def on_nav_single_clicked(self, *args):
            self.ui_change_layout(
                self.on_nav_single_clicked, self.layoutSingle, self.nav_single
            )

        def on_nav_setting_clicked(self, *args):
            self.ui_change_layout(
                self.on_nav_setting_clicked, self.layoutSetting, self.nav_setting
            )

        def render_main_header(self):
            self.mainAppBar = AppBar()
            self.layoutMain.addLayout(self.mainAppBar)

            self.mainAppBarText = AppBarTitle("Drox Music Player")
            self.mainAppBar.addWidget(self.mainAppBarText)

            self.icon = QLabel()
            self.mainAppBar.addWidget(self.icon)
            self.icon.setScaledContents(True)
            self.icon.setPixmap(QPixmap("Profile.png"))
            self.icon.setFixedSize(32, 32)

        def render_main_body(self):
            self.body = QVBoxLayout()
            self.body.setContentsMargins(8, 8, 8, 8)
            self.layoutMain.addLayout(self.body)

            self.menu = QHBoxLayout()
            self.body.addLayout(self.menu)

            self.playlistMenu = MainMenuWidget()
            self.playlistMenu.setMainText("PlayList")
            self.playlistMenu.setSubText("0 playlist")
            self.playlistMenu.setTextColor("white")
            self.playlistMenu.setIcon(C_SparkleWinter)
            self.playlistMenu.clicked.connect(self.on_nav_playlist_clicked)
            # self.playlistMenu.mouseReleaseEvent = self.on_nav_playlist_clicked
            self.menu.addWidget(self.playlistMenu)

            self.singleMenu = MainMenuWidget()
            self.singleMenu.setMainText("Single")
            self.singleMenu.setSubText("0 song")
            self.singleMenu.setTextColor("white")
            self.singleMenu.setIcon(C_HighteenWinter)
            self.singleMenu.clicked.connect(self.on_nav_single_clicked)
            self.menu.addWidget(self.singleMenu)

            def normalize():
                self.playlistMenu.setIcon(C_init)
                self.singleMenu.setIcon(C_dust)

            normalize()

        def fun_change_title_render_method(self):
            if self.windowTitleRenderMethod == "macos":
                self.windowTitleRenderMethod = "windows"
                self.render_title()
            else:
                self.windowTitleRenderMethod = "macos"
                self.render_title()

        def context_title(self):
            pass

        def render_title(self):
            # self.windowTitleLayout.setContentsMargins(30, 15, 30, 15)
            # self.windowTitleLayout.setContentsMargins(20, 15, 20, 0) //선 없을 떄
            self.windowTitleLayout.setContentsMargins(20, 15, 20, 5)
            self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            # self.windowTitleLayout.

            self.windowTItleText1 = QLabel("09:42")
            self.windowTItleText2 = QLabel("100%")
            self.windowTItleText1.setStyleSheet("background-color: 0")
            self.windowTItleText2.setStyleSheet("background-color: 0")

            self.render_traffic_light = True
            if self.render_traffic_light:
                while self.windowTitleLayout.count():
                    item = self.windowTitleLayout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clearLayout(item.layout())

                if self.windowTitleRenderMethod == "macos":
                    self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

                    def close_hover_enter(event):
                        self.traffic_close.setIcon(QIcon(I_TR_Close_Hover))

                    def close_hover_leave(event):
                        self.traffic_close.setIcon(QIcon(I_TR_Close))

                    def close_active(event):
                        self.traffic_close.setIcon(QIcon(I_TR_Close_Active))

                    def close_reset(event):
                        self.traffic_close.setIcon(QIcon(I_TR_Close))
                        self.win_close()

                    self.traffic_close = QPushButton()
                    self.traffic_close.setIcon(QIcon(I_TR_Close))
                    self.traffic_close.enterEvent = close_hover_enter
                    self.traffic_close.leaveEvent = close_hover_leave
                    self.traffic_close.mousePressEvent = close_active
                    self.traffic_close.mouseReleaseEvent = close_reset

                    def minimize_hover_enter(event):
                        self.traffic_minimize.setIcon(QIcon(I_TR_Minimize_Hover))

                    def minimize_hover_leave(event):
                        self.traffic_minimize.setIcon(QIcon(I_TR_Minimize))

                    def minimize_active(event):
                        self.traffic_minimize.setIcon(QIcon(I_TR_Minimize_Active))

                    def minimize_reset(event):
                        self.traffic_minimize.setIcon(QIcon(I_TR_Minimize))
                        self.win_minimize()

                    self.traffic_minimize = QPushButton()
                    self.traffic_minimize.setIcon(QIcon(I_TR_Minimize))
                    self.traffic_minimize.enterEvent = minimize_hover_enter
                    self.traffic_minimize.leaveEvent = minimize_hover_leave
                    self.traffic_minimize.mousePressEvent = minimize_active
                    self.traffic_minimize.mouseReleaseEvent = minimize_reset

                    def maximize_hover_enter(event):
                        self.traffic_maximize.setIcon(QIcon(I_TR_Maximize_Hover))

                    def maximize_hover_leave(event):
                        self.traffic_maximize.setIcon(QIcon(I_TR_Maximize))

                    def maximize_active(event):
                        self.traffic_maximize.setIcon(QIcon(I_TR_Maximize_Active))

                    def maximize_reset(event):
                        self.traffic_maximize.setIcon(QIcon(I_TR_Maximize))
                        self.win_maximize()

                    self.traffic_maximize = QPushButton()
                    self.traffic_maximize.setIcon(QIcon(I_TR_Maximize))
                    self.traffic_maximize.enterEvent = maximize_hover_enter
                    self.traffic_maximize.leaveEvent = maximize_hover_leave
                    self.traffic_maximize.mousePressEvent = maximize_active
                    self.traffic_maximize.mouseReleaseEvent = maximize_reset

                    self.window_btns = [
                        self.traffic_close,
                        self.traffic_minimize,
                        self.traffic_maximize,
                    ]
                    # self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    for button in self.window_btns:
                        self.windowTitleLayout.addWidget(button)
                        button.setFixedSize(13, 28)
                        button.setIconSize(QSize(13, 13))
                        button.setStyleSheet(
                            """
                            QPushButton { background-color: rgba(0, 0, 0, 0.0); border: 0px; }
                            """
                        )

                    return
                elif self.windowTitleRenderMethod == "windows":
                    self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

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
                    # self.windowTitleLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

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

        def render_footer(self):
            self.footer = QHBoxLayout()
            # self.footer.setSty
            self.footerLayout.addLayout(self.footer)
            self.footer.setContentsMargins(0, 10, 0, 15)

            self.footer_itemList = []

            self.nav_main = NeuNavButton()
            self.nav_main.setText("Main")
            self.nav_main.setIcon(I_Home)
            self.nav_main.setInvertIcon(II_Home)
            self.footer.addWidget(self.nav_main)
            self.nav_main.mouseReleaseEvent = self.on_nav_main_clicked

            self.nav_search = NeuNavButton()
            self.nav_search.setText("Search")
            self.nav_search.setIcon(I_Search)
            self.nav_search.setInvertIcon(II_Search)
            self.footer.addWidget(self.nav_search)
            self.nav_search.mouseReleaseEvent = self.on_nav_search_clicked

            self.nav_playlist = NeuNavButton()
            self.nav_playlist.setText("Playlist")
            self.nav_playlist.setIcon(I_Playlist)
            self.nav_playlist.setInvertIcon(II_Playlist)
            self.footer.addWidget(self.nav_playlist)
            self.nav_playlist.mouseReleaseEvent = self.on_nav_playlist_clicked

            self.nav_single = NeuNavButton()
            self.nav_single.setText("Single")
            self.nav_single.setIcon(I_Single)
            self.nav_single.setInvertIcon(II_Single)
            self.footer.addWidget(self.nav_single)
            self.nav_single.mouseReleaseEvent = self.on_nav_single_clicked

            self.nav_setting = NeuNavButton()
            self.nav_setting.setText("Setting")
            self.nav_setting.setIcon(I_Setting)
            self.nav_setting.setInvertIcon(II_Setting)
            self.footer.addWidget(self.nav_setting)
            self.nav_setting.mouseReleaseEvent = self.on_nav_setting_clicked

            self.controller = QHBoxLayout()
            self.footerLayout.addLayout(self.controller)
            self.controller.setContentsMargins(0, 0, 0, 10)

            self.bar = QPushButton()
            self.bar.setCursor(Qt.PointingHandCursor)
            self.bar.setFixedSize(int(self.width() / 2.5), 15)

            self.bar.setStyleSheet(
                "background-color: black; border: 7px; border-color: transparent; border-style: solid; border-radius: 7px;"
            )
            self.bar.clicked.connect(self.win_minimize)
            # self.controller.addWidget(self.bar)

        def render_search_header(self):
            self.searchAppBar = AppBar()
            self.layoutSearch.addLayout(self.searchAppBar)

            self.searchAppBarText = AppBarTitle("Search")
            self.searchAppBar.addWidget(self.searchAppBarText)

        def fun_search_add_result(self, entry):
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
            thread.repaint.connect(self.fun_search_repaint_list)
            thread.setResultListIcon.connect(self.fun_search_item_icon)
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

        def fun_search_repaint_list(self):
            if self.searchResult.paintingActive() == False:
                self.searchResult.repaint()

        def fun_search_item_icon(self, item, icon):
            item.setIcon(icon)

        def fun_search_result_by_list(self, list: list):
            for entry in list:
                self.fun_search_add_result(entry)

        def fun_on_search_input(self):
            input = self.searchInput.text()
            if input.strip() == "":
                return

            for i in range(self.searchResult.count()):
                self.searchResult.takeItem(0)

            self.sr = search_10(input)
            self.fun_search_result_by_list(self.sr.result()["result"])

        def fun_search_update(self, value):
            if value == self.searchResult.verticalScrollBar().maximum():
                self.sr.next()
                self.fun_search_result_by_list(self.sr.result()["result"])

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
            self.searchInput.returnPressed.connect(self.fun_on_search_input)

            self.searchButton = QPushButton("")
            self.searchInputLine.addWidget(self.searchButton)
            self.searchButton.setIcon(QIcon(I_Search))
            self.searchButton.setCursor(Qt.PointingHandCursor)
            self.searchButton.setStyleSheet(
                "border: none; border-radius: 5px; background-color: #EEEEEE; padding: 10px;"
            )
            self.searchButton.clicked.connect(self.fun_on_search_input)

            self.searchResult = QListWidget()
            self.searchBody.addWidget(self.searchResult)
            self.searchResult.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Expanding
            )
            # self.searchResult.setFixedHeight(int(self.height() / 2.5))
            # self.searchResult.setFixedHeight(int(self.height() / 2.5))

            self.searchResult.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            self.searchResult.verticalScrollBar().valueChanged.connect(
                self.fun_search_update
            )
            self.searchResult.verticalScrollBar().setSingleStep(5)
            self.searchResult.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
            self.searchResult.setStyleSheet("")
            self.searchResult.setIconSize(QSize(55, 55))

            # self.Fixed = QPushButton("Fixed")
            # self.Fixed.clicked.connect(lambda x: self.cc("Fixed"))
            # self.searchBody.addWidget(self.Fixed)

            # self.searchBody.addStretch()

        # def cc(self, name):

        #     self.searchResult.setFixedHeight(int(self.height() / 2.5))

        def render_location_viewer(self):
            self.Qlocations = QHBoxLayout()

            self.Qlocation_prev = QListWidget()
            self.Qlocations.addWidget(self.Qlocation_prev)
            self.Qlocation_next = QListWidget()
            self.Qlocations.addWidget(self.Qlocation_next)

            self.layoutSetting.addLayout(self.Qlocations)

        @pyqtSlot(float)
        def fun_dl_updated(self, value):
            self.dl_pr.setValue(int(value))

        @pyqtSlot(bool)
        def fun_dl_finished(self, value):
            print(value)

        def fun_dl_btn_clicked(self):
            from backend.youtube.downloader import Downloader

            try:
                if self.i_.isRunning() == False:
                    self.i_ = Downloader()
                    self.i_.updated.connect(self.fun_dl_updated)
                    self.i_.finished.connect(self.fun_dl_finished)
                    self.i_.start()

                    self.dl_btn.setText("Cancel")
                else:
                    self.i_.stop()
                    self.dl_btn.setText("Download")
            except:
                self.i_ = Downloader()
                self.i_.updated.connect(self.fun_dl_updated)
                self.i_.finished.connect(self.fun_dl_finished)
                self.i_.start()

        def render_playlist_header(self):
            self.playlistAppBar = AppBar()
            self.layoutPlaylist.addLayout(self.playlistAppBar)

            self.playlistAppBarText = AppBarTitle("Playlist")
            self.playlistAppBar.addWidget(self.playlistAppBarText)

            # self.layoutPlaylist
            self.dl_box = QGroupBox()
            self.layoutPlaylist.addWidget(self.dl_box)
            self.dl_box.setTitle("Download")

            self.dl_box_layout = QVBoxLayout()
            self.dl_box.setLayout(self.dl_box_layout)

            self.dl_pr = QProgressBar()
            self.dl_pr.setValue(0)
            self.dl_pr.setMaximum(100)
            self.dl_pr.setMinimum(0)
            # self.dl_pr.setTextVisible(False)
            self.dl_box_layout.addWidget(self.dl_pr)

            self.dl_btn = QPushButton("Download")
            self.dl_btn.clicked.connect(self.fun_dl_btn_clicked)
            self.dl_box_layout.addWidget(self.dl_btn)

            self.ch_tl_rd_mth = QPushButton("Change Window Title Render Method")
            self.ch_tl_rd_mth.clicked.connect(self.fun_change_title_render_method)
            self.layoutPlaylist.addWidget(self.ch_tl_rd_mth)

        def render_single_header(self):
            self.singleAppBar = AppBar()
            self.layoutSingle.addLayout(self.singleAppBar)

            self.singleAppBarText = AppBarTitle("Single")
            self.singleAppBar.addWidget(self.singleAppBarText)

        def event_window_pressed(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.RightButton:

                self.titlePos = self.windowTitleLayout.geometry()
                left, top, right, bottom = (
                    0,
                    0,
                    self.titlePos.right() + self.titlePos.left(),
                    self.titlePos.bottom() + self.titlePos.top(),
                )
                posX, posY = event.pos().x(), event.pos().y()

                if (left < posX < right) and (top < posY < bottom):
                    self.ctx = WindowContext(event.globalPos())
                    self.ctx.show()

        def event_window_released(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.XButton1:
                print("Left")
                try:
                    print(self.location_prev, self.location_next)
                    self.Qlocation_next.addItem(str(self.location_prev[-1]))
                    self.location_next.append(self.location_prev[-1])
                    self.Qlocation_prev.takeItem(self.Qlocation_prev.count() - 1)
                    self.location_prev.pop()

                    self.location_prev[-1]()
                    self.Qlocation_prev.takeItem(self.Qlocation_prev.count() - 1)
                    self.location_prev.pop()
                    #
                except Exception as e:
                    print(e)
            elif event.button() == Qt.MouseButton.XButton2:
                try:
                    self.location_next[-1]()
                    self.Qlocation_next.takeItem(self.Qlocation_next.count() - 1)
                    self.location_next.pop()
                    # pass
                except:
                    pass
            elif event.button() == Qt.MouseButton.MiddleButton:
                try:
                    self.location_prev.clear()
                    self.location_next.clear()
                    self.Qlocation_prev.clear()
                    self.Qlocation_next.clear()
                except:
                    pass
            elif event.button() == Qt.MouseButton.RightButton:
                # self.doit()
                # print(event.pos())

                # print(event.)
                pass

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton:
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

    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)

    if __name__ == "__main__":
        import platform

        if platform.system() == "Windows":
            import ctypes

            myappid = "mycompany.myproduct.subproduct.version"  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        app = QApplication(sys.argv)
        palatte = QPalette()
        palatte.setColor(QPalette.Background, QColor(255, 255, 255))
        # palatte.setColor(QPalette.Background, QColor(169, 98, 95))
        app.setPalette(palatte)
        app.setFont(QFont("Pretendard", 10))

        # app.setQuitOnLastWindowClosed(False)

        dw = DroxWidget()
        # app.installEventFilter(fo)

        mouse_observer = MouseObserver(dw.windowHandle())
        mouse_observer.pressed.connect(dw.event_window_pressed)
        mouse_observer.released.connect(dw.event_window_released)

        native_style = QCommonStyle()
        dw.setStyle(native_style)

        import sys

        sys.excepthook = except_hook

        sys.exit(app.exec_())

    ##----- End gui.py -----------------------------------------------------------##
    return locals()
