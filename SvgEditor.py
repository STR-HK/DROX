from lxml import etree

import MyAssets

from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *


def change_color(path, color):
    tree = etree.parse(path)
    root = tree.getroot()
    root.set("fill", color)
    # root.set("height", "28")
    # root.set("width", "28")
    # tree.write(path, pretty_print=True)
    xml = etree.tostring(root, pretty_print=True)
    return xml
