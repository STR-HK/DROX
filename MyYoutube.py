import yt_dlp
from youtube_search import YoutubeSearch
from youtubesearchpython import VideosSearch
import pyperclip


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
