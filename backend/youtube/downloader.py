from multiprocessing import Process
from PyQt5.QtCore import QThread, pyqtSignal
import yt_dlp as youtube_dl

import os

if os.path.isfile(
    "【Lyric MV】Zara 'Drowsiness' (Full Ver.) 【MementoMori】 [zqfMYAWDz20].mp4"
):
    os.remove("【Lyric MV】Zara 'Drowsiness' (Full Ver.) 【MementoMori】 [zqfMYAWDz20].mp4")


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
