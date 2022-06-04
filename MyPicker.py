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
