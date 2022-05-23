from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster


import json
import os

cachePath = "cache.json"


def make_cacheFile_if_not_exist():
    # j = {}

    if not os.path.isfile(cachePath):
        with open(cachePath, "w") as f:
            j = {}
            f.write(json.dumps(j))
    # else:


def cache_exists(path):
    # return False

    r = open(cachePath, "r").read()
    j = json.loads(r)
    try:
        if j[path]:
            return True
    except:
        return False


def get_color_from_cache(path):
    r = open(cachePath, "r").read()
    j = json.loads(r)
    return j[path]


def store_color_to_cache(path, color):
    r = open(cachePath, "r").read()
    j = json.loads(r)
    j[path] = color
    with open(cachePath, "w") as f:
        f.write(json.dumps(j))


NUM_CLUSTERS = 20


def pick_color(path):
    make_cacheFile_if_not_exist()
    if cache_exists(path):
        print("cache exists")
        return get_color_from_cache(path)
    else:
        print("cache not exists")
        print("generating clusters... may take a while")
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
