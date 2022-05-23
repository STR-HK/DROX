import yt_dlp
import sys


ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "outtmpl": "./downloads/%(title)s.%(ext)s",
    "noplaylist": True,
    "nocheckcertificate": True,
    "continuedl": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "max_downloads": 1,
    "nooverwrites": True,
    "restrictfilenames": True,
    "simulate": False,
    "skip_download": False,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    retcode = ydl.download("https://www.youtube.com/watch?v=E3g3JvCYCvg")
    print(retcode)
